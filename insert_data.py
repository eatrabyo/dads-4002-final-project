import os
import datetime
import pandas as pd
from sqlalchemy import exc, text

from engine import main_db
from insert_func import insert_new_customer,insert_new_transaction
from query import query_new_customer,query_latest_transaction,query_product_list,query_customer_list,query_product_name,query_stock_by_product_id,query_trans_by_id,query_total_trans_by_customer,query_trans_id_list
from update_func import update_cus_status_by_id

def insert_customer_tbl():
    while True:
        os.system('clear') # 'clear' on mac, for windows 'cls'
        try:
            # check email and user name input is valid
            while True:
                cus_user_name = input("Enter new customer's username: ")
                cus_email = input("Enter new customer's email:")
                
                if cus_user_name not in ['',' '] and cus_email != ' ':
                    if cus_email == '':
                        cus_email = None
                        break
                    else:
                        break
                else:
                    print("Invalid, please re-enter customer's username and email.")
                    continue
            # check if phone number is correct format
            while True:
                cus_phone = input("Enter new customer's phone number in format (replace 0 with 66): ")
                if len(cus_phone) == 11 and cus_phone.startswith('66',0,2) == True:
                    break
                else:
                    print('Please input valid phone number.')
                    continue
            # status for old_customer column
            status = 0
            # blank dataframe
            cus_for_insert_df = pd.DataFrame(columns=['customer_user','old_customer','phone_number','email'])

            # adding user input to dataframe
            cus_for_insert_df.loc[len(cus_for_insert_df)] = [cus_user_name,status,cus_phone,cus_email]
            
            # insert dataframe to db
            insert_new_customer(df=cus_for_insert_df,engine=main_db)
            # show new data
            new_cus = query_new_customer(main_db)
            print("\n",new_cus,"\n")
        except Exception as e:
                print(e)
        # loop for asking update more or no
        while True:
            loop_to_main = input("Would you like to add more customer? (Y/N): ").lower()
            if loop_to_main in ['y','n']:
                break
            else:
                continue
        if loop_to_main == 'y':
            continue
        elif loop_to_main == 'n':
            break

def insert_main_tbl():
    while True:
        os.system('clear') # 'clear' on mac, for windows 'cls'

        # empty dataframe
        new_trans_df = pd.DataFrame(columns=['transaction_id','product_id','customer_id','purchasing_time','price_per_unit','unit','destination_district',
                                        'destination_province','postal_code'])
        # empty dict for new stock
        dict_for_update_stock = {}

        # get latest transaction_id from our db
        pre_fix, latest_trans_num = query_latest_transaction(main_db)
        # new trans num
        new_trans_id = "trans_" + str(int(latest_trans_num) + 1)

        # ask user customer_id
        customer_list = query_customer_list(main_db)
        # check if customer id is in our db
        while True:
            try:
                customer_for_this_trans = int(input('Enter customer id: '))
                if customer_for_this_trans in customer_list:
                    break
                else:
                    print(f'Customer id: {customer_for_this_trans} is not in database.')
                    continue
            except:
                print('Enter valid customer id.')

        # ask user for purchasing time
        while True:
            try:
                date_for_this_trans = input("Enter date and time in format (YYYY-MM-DD hh:mm): ")
                format_datetime = datetime.datetime.strptime(date_for_this_trans,"%Y-%m-%d %H:%M")
                break
            except:
                print('Invalid date and time format.')
        
        
        # get postal code
        address_ref = pd.read_csv('district_province_ref.csv')
        postal_list = address_ref['postal_code'].to_list()

        # asking for postal code
        while True:
            try:
                postal_code = int(input("Enter postal code: "))
                if postal_code in postal_list:
                    # get new district and province from csv file
                    district = address_ref.loc[address_ref['postal_code'] == postal_code,'district'].values[0]
                    province = address_ref.loc[address_ref['postal_code'] == postal_code,'province'].values[0]
                    break
                else:
                    print('Please enter valid postal code.')
                    continue
            except:
                print("Invalid postal code")

        # ask user how many product in this trans
        while True:
            os.system('clear') # 'clear' on mac, for windows 'cls'
            try:
                counter_limit = int(input("How many product in this new transaction?: "))
                if counter_limit > 0:
                    break
                else:
                    print('Enter positive intger only')
                    continue
            except:
                print('Enter integer only.')
        # counter
        c = 0
        product_list = query_product_list(main_db)
        while c != counter_limit:
            os.system('clear') # 'clear' on mac, for windows 'cls'

            # product for this trans
            # check if product id is valid
            while True:
                product_for_this_trans = input(f"Please enter product id number {c + 1}: ")
                # check if product is match with our db
                if product_for_this_trans in product_list:
                    product_name = query_product_name(main_db,product_for_this_trans)
                    break
                else:
                    print("Invalid product_id, please re-enter.")
                    continue
                
            # Price Per Unit
            while True:
                try:
                    price_per_unit = float(input(f"Enter selling price for {product_name}: "))
                    break
                except:
                    print('Please enter number only.')

            # selling unit
            # query old stock
            stock = query_stock_by_product_id(engine=main_db,product_id=product_for_this_trans)
            while True:
                try:
                    selling_unit = int(input(f"Enter selling unit for {product_name}: "))
                    # input unit must be more than zero
                    if selling_unit > 0:
                        break
                    else:
                        print('Invalid unit, please re-enter.')
                        continue
                except:
                    print('Please enter integer only.')

            new_stock = stock - selling_unit
            # check if stock is enough
            if new_stock >= 0:
                dict_for_update_stock[product_for_this_trans] = new_stock
            else:
                print(f'Not enough stock for {product_name}.')
                break

        # add to dataframe template
            new_trans_df.loc[len(new_trans_df)] = [new_trans_id,product_for_this_trans,customer_for_this_trans,date_for_this_trans,price_per_unit,selling_unit,
                                district,province,postal_code]
            c += 1

        # insert new trans to our db
        if len(new_trans_df) > 0:
            insert_new_transaction(new_trans_df,main_db)

            # update stock
            for k,v in dict_for_update_stock.items():
                try:
                    with main_db.begin() as conn:
                        sql = f"""
                        UPDATE product SET stock = {v}
                        WHERE id = '{k}'
                        """
                        
                        conn.execute(text(sql))
                    print(f'Finished update new stock for {k}')
                except exc.SQLAlchemyError as e:
                    print(type(e))
                    print(e.orig)
                    print(e.statement)

            # update customer status
            total_trans = query_total_trans_by_customer(main_db,customer_for_this_trans)

            if total_trans > 1:
                update_cus_status_by_id(main_db,customer_for_this_trans)
            # show new data
            result_df = query_trans_by_id(main_db,new_trans_id)
            print("\n",result_df,"\n")
            
        # loop for asking update more or no
        while True:
            loop_to_main = input("Would you like to add more transaction? (Y/N): ").lower()
            if loop_to_main in ['y','n']:
                break
            else:
                continue
        if loop_to_main == 'y':
            continue
        elif loop_to_main == 'n':
            break

# insert new product by old transaction
def insert_main_tbl_for_more_prod():
    while True:
        os.system('clear') # 'clear' on mac, for windows 'cls'
        try:
            # asking user for old transaction
            edited_trans = input('Enter transaction you want to add more product: ')
            trans_list = query_trans_id_list(main_db)

            # empty dataframe
            empty_edited_trans = pd.DataFrame(columns=['transaction_id','product_id','customer_id','purchasing_time','price_per_unit','unit','destination_district',
                                        'destination_province','postal_code'])

            # empty dict for new stock
            dict_for_update_stock = {}
            if edited_trans in trans_list:
                # get old data from edited trans
                ref_trans = query_trans_by_id(main_db,edited_trans)
                
                # reference data from transaction database
                ref_customer = ref_trans['customer_id'].values[0]
                ref_times = ref_trans['purchasing_time'].values[0]
                ref_district = ref_trans['destination_district'].values[0]
                ref_province = ref_trans['destination_province'].values[0]
                ref_postal_code = ref_trans['postal_code'].values[0]
                list_product = list(ref_trans['product_id'])


                # ask user how many product in this trans
                while True:
                    os.system('clear') # 'clear' on mac, for windows 'cls'
                    try:
                        counter_limit = int(input("How many product in this new transaction?: "))
                        if counter_limit > 0:
                            break
                        else:
                            print('Enter positive integer only.')
                            continue
                    except:
                        print('Please enter integer only.')
                # counter
                c = 0
                product_list = query_product_list(main_db)
                while c != counter_limit:
                    os.system('clear') # 'clear' on mac, for windows 'cls'

                    # product for this trans
                    # check if product id is valid
                    while True:
                        product_for_this_trans = input(f"Please enter product id number {c + 1}: ")
                        # check if product is match with our db
                        if product_for_this_trans in product_list:
                            if product_for_this_trans not in list_product:
                                product_name = query_product_name(main_db,product_for_this_trans)
                                break
                            else:
                                print(f'{edited_trans} already has {product_for_this_trans}.')
                                continue
                        else:
                            print("Invalid product_id, please re-enter.")
                            continue

                    # Price Per Unit
                    while True:
                        try:
                            price_per_unit = float(input(f"Enter selling price for {product_name}: "))
                            break
                        except:
                            print('Please enter number only.')

                    # selling unit
                    # query old stock
                    stock = query_stock_by_product_id(engine=main_db,product_id=product_for_this_trans)
                    while True:
                        try:
                            selling_unit = int(input(f"Enter selling unit for {product_name}: "))
                            # input unit must be more than zero
                            if selling_unit > 0:
                                break
                            else:
                                print('Invalid unit, please re-enter.')
                                continue
                        except:
                            print('Please enter integer only.')

                    new_stock = stock - selling_unit
                    # check if stock is enough
                    if new_stock >= 0:
                        dict_for_update_stock[product_for_this_trans] = new_stock
                    else:
                        print(f'Not enough stock for {product_name}.')
                        break
                    
                    # add to dataframe template
                    empty_edited_trans.loc[len(empty_edited_trans)] = [edited_trans,product_for_this_trans,ref_customer,ref_times,price_per_unit,selling_unit,
                                        ref_district,ref_province,ref_postal_code]
                    c += 1

                # insert new trans to our db
                if len(empty_edited_trans) > 0:
                    insert_new_transaction(empty_edited_trans,main_db)

                    # update stock
                    for k,v in dict_for_update_stock.items():
                        try:
                            with main_db.begin() as conn:
                                sql = f"""
                                UPDATE product SET stock = {v}
                                WHERE id = '{k}'
                                """
                                
                                conn.execute(text(sql))
                            print(f'Finished update new stock for {k}')
                        except exc.SQLAlchemyError as e:
                            print(type(e))
                            print(e.orig)
                            print(e.statement)
                # show new data
                result_df = query_trans_by_id(main_db,edited_trans)
                print("\n",result_df,"\n")
            else:
                continue
        except:
            print('invalid')
        # loop for asking update more or no
        while True:
            loop_to_main = input("Would you like to add more transaction? (Y/N): ").lower()
            if loop_to_main in ['y','n']:
                break
            else:
                continue
        if loop_to_main == 'y':
            continue
        elif loop_to_main == 'n':
            break