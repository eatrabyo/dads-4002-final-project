import os
import datetime
import pandas as pd

from engine import main_db

while True:
    os.system('clear') # 'clear' on mac, for windows 'cls'
    try:
        # check email and user name input is valid
        while True:
            cus_user_name = input("Enter customer user name: ")
            cus_email = input("Enter user email:")
            
            if cus_user_name not in ['',' '] and cus_email != ' ':
                break
            else:
                print('Invalid input')
                continue
        # check if phone number is correct format
        while True:
            cus_phone = input("Enter phone number in format (66XXXXXXXXX): ")
            if len(cus_phone) == 11 and cus_phone.startswith('66',0,2) == True:
                break
            else:
                print('Please input valid phone number.')
                continue
        # status for old_customer column
        status = 0
        # blank dataframe
        cus_for_insert_df = pd.DataFrame(columns=['customer_user','old_customer','phone_number','email'])
        # adding user inout to dataframe
        cus_for_insert_df.loc[len(cus_for_insert_df)] = [cus_user_name,status,cus_phone,cus_email]
        print(cus_for_insert_df)
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