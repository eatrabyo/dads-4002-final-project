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
            diff_insert = 0
            diff_update = 0
            diff_delete = 0
            diff_stat = 0

            if user == '1':
                manu_one_time_in = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
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
                    manu_one_time_out = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    insert1 = dt.datetime.strptime(manu_one_time_in, "%d/%m/%Y %H:%M:%S")
                    insert2 = dt.datetime.strptime(manu_one_time_out, "%d/%m/%Y %H:%M:%S")
                    diff_insert = insert2-insert1
                    pass
            ##break

            elif user == '2':
                manu_2_time_in = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
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
                    manu_2_time_out = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    update1 = dt.datetime.strptime(manu_2_time_in, "%d/%m/%Y %H:%M:%S")
                    update2 = dt.datetime.strptime(manu_2_time_out, "%d/%m/%Y %H:%M:%S")
                    diff_update = update2-update1
                    pass            
                ##break
            elif user == '3':
                manu_3_time_in = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                print(f'\nYou are now in "Delete Data" page')
                print('delete transaction table')



                manu_3_time_out = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                delete1 = dt.datetime.strptime(manu_3_time_in, "%d/%m/%Y %H:%M:%S")
                delete2 = dt.datetime.strptime(manu_3_time_out, "%d/%m/%Y %H:%M:%S")
                diff_delete = delete2-delete1
                ##break
            elif user == '4':
                print(f'\nYou are now in "See report" page')
                manu_4_time_in = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                print('โค้ดใหม่')


                manu_4_time_out = dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                stat1 = dt.datetime.strptime(manu_4_time_in, "%d/%m/%Y %H:%M:%S")
                stat2 = dt.datetime.strptime(manu_4_time_out, "%d/%m/%Y %H:%M:%S")
                diff_stat = stat2-stat1
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
        t1 = dt.datetime.strptime(login_time, "%d/%m/%Y %H:%M:%S")
        t2 = dt.datetime.strptime(logout_time, "%d/%m/%Y %H:%M:%S")    
       
        ##logbook=
        
    with open(('RecordData.txt'),'a', encoding='utf-8') as myfile:    
        myfile.writelines(f'\n\nUSER: {user_name}\nIN: {login_time}\nOUT: {logout_time}\nTotal time spent: {t2-t1}')
        myfile.writelines(f'\n     Insert Data: {diff_insert}')
        myfile.writelines(f'\n     Update Data: {diff_update}')
        myfile.writelines(f'\n     Delete Data: {diff_delete}')
        myfile.writelines(f'\n     See Report: {diff_stat}')

    gtfc.backup_all_data()

main()  