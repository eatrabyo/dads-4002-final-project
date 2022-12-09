import os
import datetime

from query import query_customer_by_id, query_customer_list,query_product_list,query_product_by_id,query_trans_id_list,query_trans_by_id
from engine import main_db
from update_func import update_email,update_phone,update_stock,update_prod_cost,update_product_main,update_customer_main,update_purchasing_time_main,update_product_price_main,\
    update_product_unit_main

# update customer table menu
def update_customer_tbl():
    while True:
        os.system('clear') # 'clear' on mac, for windows 'cls'
        try:
            # asking user for which customer_id to update
            customer_id = int(input("Please enter customer_id: "))
            cus_list = query_customer_list(main_db)

            # check if user input have match with in our db
            if customer_id in cus_list:
                #query customer info base on id
                customer_df = query_customer_by_id(main_db,customer_id)
                print("\n",customer_df,"\n")
                # ask user which column to update
                print("\n Which column would you like to update?\n    1. Phone number\n    2. Email\n    3. Exit")
                
                # check if user enter valid menu number
                while True:
                    cus_update_menu_num = input('Please enter menu number: ')
                    if cus_update_menu_num in ['1','2','3']:
                        break
                    else:
                        print('Wrong menu number.')
                        continue

                if cus_update_menu_num == '1':

                    # check if phone number have length of 11 and start with 66
                    while True:
                        new_phone = input('Enter new phone number: ')
                        if len(new_phone) == 11 and new_phone.startswith('66',0,2) == True:
                            break
                        else:
                            print('Please input valid phone number.')
                            continue

                    # update phone no. to our db
                    update_phone(engine=main_db,cus_id=customer_id,phone=new_phone)

                    # print new data
                    new_cus_info = query_customer_by_id(main_db,customer_id)
                    print("\n",new_cus_info,"\n")

                elif cus_update_menu_num == '2':
                    # check for space
                    while True:
                        new_email = input('Enter new email: ')
                        if new_email != ' ':
                            break
                        else:
                            continue
                    # update email to our db
                    update_email(engine=main_db,cus_id=customer_id,email=new_email)

                    # print new data
                    new_cus_info = query_customer_by_id(main_db,customer_id)
                    print("\n",new_cus_info,"\n")
                elif cus_update_menu_num == '3':
                    break
            else:
                raise
        except:
            print("Please enter valid customer_id")
            continue

        # loop for asking update more or no
        while True:
            loop_to_main = input("Would you like to update more? (Y/N): ").lower()
            if loop_to_main in ['y','n']:
                break
            else:
                continue
        if loop_to_main == 'y':
            continue
        elif loop_to_main == 'n':
            break

# update product table menu
def update_product_tbl():
    while True:
        os.system('clear') # 'clear' on mac, for windows 'cls'
        try:
            # asking customer which product_id to update
            prod_id = input("Please enter product id: ")
            product_list = query_product_list(main_db)
            
            # check if product is match with our db
            if prod_id in product_list:
                # query product info base on product id
                product_info = query_product_by_id(main_db,product_id=prod_id)
                print("\n",product_info,"\n")
                # ask user which column to update
                print("\n Which column would you like to update?\n    1. Stock\n    2. Product cost\n    3. Exit")

                # check if menu number is valid
                while True:
                    product_update_menu_num = input('Please enter menu number: ')
                    if product_update_menu_num in ['1','2','3']:
                        break
                    else:
                        print('Wrong menu number.')
                        continue
                
                if product_update_menu_num == '1':

                    # check for user input number only
                    while True:
                        try:
                            new_stock = int(input('Enter new stock value: '))
                            break
                        except:
                            print("Please enter only integer number")
                            continue

                    # update new data to our db
                    update_stock(engine=main_db,product_id=prod_id,stock=new_stock)
                    # print new data
                    product_info = query_product_by_id(main_db,product_id=prod_id)
                    print("\n",product_info,"\n")

                elif product_update_menu_num == '2':
                    while True:
                        try:
                            new_cost = int(input('Enter new cost value: '))
                            if new_cost != 0:
                                break
                            else:
                                print('Please enter only number')
                                continue
                        except:
                            print("Please enter only number")
                            continue

                    # update new data to our db
                    update_prod_cost(engine=main_db,product_id=prod_id,cost=new_cost)
                    # print new data
                    product_info = query_product_by_id(main_db,product_id=prod_id)
                    print("\n",product_info,"\n")
                elif product_update_menu_num == '3':
                    break
            else:
                raise
        except:
            print('Please enter valid product id.')
            continue

        # loop for asking update more or no
        while True:
            loop_to_main = input("Would you like to update more? (Y/N): ").lower()
            if loop_to_main in ['y','n']:
                break
            else:
                continue
        if loop_to_main == 'y':
            continue
        elif loop_to_main == 'n':
            break

# update main table
while True:
    os.system('clear') # 'clear' on mac, for windows 'cls'
    try:
        # asking user which transaction to update
        trans_id = input('Please enter transaction id: ')
        trans_list = query_trans_id_list(main_db)

        # check if transaction id match from our db
        if trans_id in trans_list:

            #query customer info base on id
            trans_df = query_trans_by_id(main_db,trans_id)

            # list for store primary key
            main_tbl_id = trans_df.reset_index()['id'].to_list()

            print("\n",trans_df,"\n")
            # ask user which column to update
            print("\n Which column would you like to update?\n    1. Product id\n    2. Customer id\n    3. Purchasing time\
                \n    4. Price per unit\n    5. Unit\n    6. Destination District\
                    \n    7. Destination province\n    8. Postal code\n    9. Exit")
            
            # check if menu number is valid
            while True:
                product_update_menu_num = input('Please enter menu number: ')
                if product_update_menu_num in ['1','2','3','4','5','6','7','8','9']:
                    break
                else:
                    print('Wrong menu number.')
                    continue
            
            # Product id menu
            if product_update_menu_num == '1':
                os.system('clear') # 'clear' on mac, for windows 'cls'
                print(trans_df)

                # check if user input row_id match with list of primary key
                while True:
                    try:
                        row_id = int(input('\nWhich row would you like to revised product id: '))
                        if row_id in main_tbl_id:
                            break
                        else:
                            os.system('clear') # 'clear' on mac, for windows 'cls'
                            print(f'Please enter valid row id for {trans_id}\n')
                            print(trans_df)
                            continue
                    except:
                        os.system('clear') # 'clear' on mac, for windows 'cls'
                        print(f'Please enter valid row id for {trans_id}\n')
                        print(trans_df)
                        continue
                
                product_list = query_product_list(main_db)
                

                # check if edited product id is in our db
                while True:
                    edited_product_id = input('Enter revised product id: ')
                    if edited_product_id in product_list:
                        break
                    else:
                        print(f'Product id: {edited_product_id} is not in database.')
                        continue
                
                # update new data
                update_product_main(engine=main_db,row_id=row_id,product_id=edited_product_id)
                # show new data
                new_trans_df = query_trans_by_id(main_db,trans_id,row_id=row_id)
                print('\n',new_trans_df)
                
            # customer id menu
            elif product_update_menu_num == '2':
                os.system('clear') # 'clear' on mac, for windows 'cls'
                print(trans_df)

                customer_list = query_customer_list(main_db)
                # check if edited customer id is in our db
                while True:
                    try:
                        edited_customer_id = int(input('Enter revised customer id: '))
                        if edited_customer_id in customer_list:
                            break
                        else:
                            print(f'Customer id: {edited_customer_id} is not in database.')
                            continue
                    except:
                        print('Enter valid customer id.')
                
                # update new data
                update_customer_main(engine=main_db,trans_id=trans_id,cus_id=edited_customer_id)
                # show new data
                new_trans_df = query_trans_by_id(main_db,trans_id)
                print('\n',new_trans_df)
            
            # purchasing time menu
            elif product_update_menu_num == '3':
                os.system('clear') # 'clear' on mac, for windows 'cls'
                print(trans_df)

                # check user input is correct datetime format
                while True:
                    try:
                        edited_datetime = input("Enter revised date and time in format (YYYY-MM-DD hh:mm): ")
                        format_datetime = datetime.datetime.strptime(edited_datetime,"%Y-%m-%d %H:%M")
                        break
                    except:
                        print("Invalid date and time format")
                        continue
                # update new data
                update_purchasing_time_main(engine=main_db,trans_id=trans_id,purchasing_time=format_datetime)
                # show new data
                new_trans_df = query_trans_by_id(main_db,trans_id)
                print('\n',new_trans_df)

            # Price per unit menu
            elif product_update_menu_num == '4':
                os.system('clear') # 'clear' on mac, for windows 'cls'
                print(trans_df)

                # check if user input row_id match with list of primary key
                while True:
                    try:
                        row_id = int(input("\nWhich row would you like to revised product's price: "))
                        if row_id in main_tbl_id:
                            break
                        else:
                            os.system('clear') # 'clear' on mac, for windows 'cls'
                            print(f'Please enter valid row id for {trans_id}\n')
                            print(trans_df)
                            continue
                    except:
                        os.system('clear') # 'clear' on mac, for windows 'cls'
                        print(f'Please enter valid row id for {trans_id}\n')
                        print(trans_df)
                        continue
                
                # temp df for using in format string
                df_temp = trans_df.copy()
                df_temp.reset_index(inplace=True)
                
                # check if price is valid
                while True:
                    try:
                        edited_price = float(input(f"Enter revised price for {df_temp.loc[df_temp['id'] == row_id,'product_id'].values[0]}: "))
                        break
                    except:
                        print('Please enter valid price.')
                # update new data
                update_product_price_main(engine=main_db,row_id=row_id,product_price=edited_price)
                # show new data
                new_trans_df = query_trans_by_id(main_db,trans_id,row_id=row_id)
                print('\n',new_trans_df)
                
            # Unit menu
            elif product_update_menu_num == '5':
                os.system('clear') # 'clear' on mac, for windows 'cls'
                print(trans_df)

                # check if user input row_id match with list of primary key
                while True:
                    try:
                        row_id = int(input("\nWhich row would you like to revised product's selling unit: "))
                        if row_id in main_tbl_id:
                            break
                        else:
                            os.system('clear') # 'clear' on mac, for windows 'cls'
                            print(f'Please enter valid row id for {trans_id}\n')
                            print(trans_df)
                            continue
                    except:
                        os.system('clear') # 'clear' on mac, for windows 'cls'
                        print(f'Please enter valid row id for {trans_id}\n')
                        print(trans_df)
                        continue
                
                # temp df for using in format string
                df_temp = trans_df.copy()
                df_temp.reset_index(inplace=True)
                
                # check if price is valid
                while True:
                    try:
                        edited_unit = int(input(f"Enter revised selling unit for {df_temp.loc[df_temp['id'] == row_id,'product_id'].values[0]}: "))
                        break
                    except:
                        print('Please enter integer only.')
                # update new data
                update_product_unit_main(engine=main_db,row_id=row_id,product_unit=edited_unit)
                # show new data
                new_trans_df = query_trans_by_id(main_db,trans_id,row_id=row_id)
                print('\n',new_trans_df)

            # Destination district menu
            elif product_update_menu_num == '6':
                pass

            # Destination province menu
            elif product_update_menu_num == '7':
                pass

            # Postal code menu
            elif product_update_menu_num == '8':
                pass

            # Exit menu
            elif product_update_menu_num == '9':
                break
        else:
            raise
    except:
        print('Please enter valid transaction id.')
        continue
    # loop for asking update more or no
    while True:
        loop_to_main = input("Would you like to update more? (Y/N): ").lower()
        if loop_to_main in ['y','n']:
            break
        else:
            continue
    if loop_to_main == 'y':
        continue
    elif loop_to_main == 'n':
        break


