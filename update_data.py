

from query import query_customer_by_id, query_customer_list,query_product_list,query_product_by_id
from engine import main_db
from update_func import update_email,update_phone,update_stock,update_prod_cost

def update_customer_tbl():
    while True:
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
                    new_email = input('Enter new email: ')
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

def update_product_tbl():
    while True:
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
                            print("Please enter only number")
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
                            break
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
