import datetime as dt
import os
import pandas as pd


from engine import main_db
import greeting_and_main_func as gtfc
from insert_data import insert_customer_tbl

def main():
#Greeting
    os.system('cls')
    print('\033[\n\n+1m'+'**** Welcome to Stock management DADs4002 ****'+'\033[0m')
    auth, login_time, user_name = gtfc.login()
    
    if auth == True:
        ##print(f'your login time is {login_time,user_name}')
        gtfc.stock_aleart_greeting(main_db)
        while True:
            while True:
                print('\n\nPlease select any of the following manu \n 1.Insert data \n 2.Update data \n 3.Delete data \n 4.See report \n 5.Exit')
                user = input('\nWhat do you like to do today? (type 1, 2, 3, 4, or 5): ')
                if user in ['1','2','3','4','5']:
                    break
                else:
                    print('Please enter the menu!!')
                    continue

            if user == '1':
                print(f'\nYou are now in "Insert Data" page')
                print('Which data do you want to insert? \n 1. Customer \n2. Transaction \n 3.Exit ')
                while True:
                    user_insert = input('Please select option above: ')
                    if user_insert in ['1','2','3']:
                        break
                    else:
                        print('Please enter the menu!!')
                    continue
    
                if user_insert == '1':
                    insert_customer_tbl()
                elif user_insert == '2':
                    print('Which data do you want to insert? \n 1. New Transaction \n2. New Product for Old Transaction \3.Exit')
                    while True:
                        user_insert_option_2 = input('Please select option above: ')
                        if user_insert_option_2 in ['1','2','3']:
                            break
                        else:
                            print('Please enter the menu!!')
                            continue
                    if user_insert_option_2 == '1':
                        print('insert main table')
                    if user_insert_option_2 == '2':
                        print('insert main table for more products')
                    if user_insert_option_2 == '3':
                        break
                elif user_insert == '3':
                    pass
            ##break

            elif user == '2':
                print(f'\nYou are now in "Update Data" page')
                print('Which data do you want to update? \n 1. Customer \n2. Product \n 3.Transaction \n4.Exit')
                while True:
                    user_update = input('Please select option above: ')                    
                    if user_update in ['1','2','3','4']:
                        break
                    else:
                        print('Please enter the menu!!')
                        continue

                if user_update == '1':
                    print('update customer table')
                elif user_update == '2':
                    print('update product table')
                elif user_update == '3':
                    print('update Transaction table')
                elif user_update == '4':
                    pass            
                ##break
            elif user == '3':
                print(f'\nYou are now in "Delete Data" page')
                print('delete transaction table')
                ##break
            elif user == '4':
                print(f'\nYou are now in "See report" page')
                print('โค้ดใหม่')
                ##break
            elif user == '5':
                print(f'\nGoodbye :)')
                break

            #ask if user want to do something else
            while True:
                user_continue = input('\nContinue or Exit (type c=Continue, e=Exit):').lower()
                if user_continue in ['c','e']:
                    break
                else:
                    continue
            
            if user_continue == 'c':
                continue
            else:
                print('\nGoodbye :)')
                break
        
        logout_time = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        header = pd.DataFrame([[user_name,login_time,logout_time]], columns=['USER','IN','OUT'])
        t1 = dt.datetime.strptime(login_time, "%d/%m/%Y %H:%M:%S")
        t2 = dt.datetime.strptime(logout_time, "%d/%m/%Y %H:%M:%S")
        ##logbook=
        
    with open('RecordData.txt', 'a', encoding='utf-8') as myfile:    
        myfile.writelines(f'\n\nUSER: {user_name}\nIN: {login_time}\nOUT: {logout_time}\nTotal time spent: {t2-t1}')

        #table = dfrecord.set_index("id",inplace=True)

main()  