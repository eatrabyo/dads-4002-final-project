import pandas as pd

from query import query_customer_by_id, query_customer_list
from engine import main_db
from update_func import update_email,update_phone

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
                print("\n which column would you like to update?\n    1. phone number\n    2. email\n    3. Exit")
                cus_update_menu_num = input('Please enter menu number: ')

                if cus_update_menu_num == '1':

                    # check if phone number have length of 11 and start with 66
                    while True:
                        new_phone = input('enter new phone number: ')
                        if len(new_phone) == 11 and new_phone.startswith('66',0,2) == True:
                            break
                        else:
                            print('Please input valid phone number')
                            continue

                    # update phone no. to our db
                    update_phone(engine=main_db,cus_id=customer_id,phone=new_phone)

                    # print new data
                    new_cus_info = query_customer_by_id(main_db,customer_id)
                    print("\n",new_cus_info,"\n")
                elif cus_update_menu_num == '2':
                    new_email = input('enter new email: ')
                    # update email to our db
                    update_email(engine=main_db,cus_id=customer_id,email=new_email)

                    # print new data
                    new_cus_info = query_customer_by_id(main_db,customer_id)
                    print("\n",new_cus_info,"\n")
                elif cus_update_menu_num == '3':
                    break
                else:
                    raise
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
update_customer_tbl()