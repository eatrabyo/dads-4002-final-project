from datetime import datetime
import os

from engine import main_db
from greeting_and_main_func import stock_aleart_greeting, login
from 

def main():
#Greeting
    os.system('cls')
    print('\033[\n\n+1m'+'**** Welcome to Stock management DADs4002 ****'+'\033[0m')
    auth, login_time, user_name = login()
    
    if auth == True: 
        stock_aleart_greeting(main_db)
        while True:
            while True:
                user = input('\nWhat do you like to do today? (type 1, 2, 3, 4, or 5): ')
                if user in ['1','2','3','4','5']:
                    break
                else:
                    print('Please enter the menu!!')
                    continue

            if user == '1':
                print(f'\nYou are now in "Insert Data" page')
                print('Which data do you want to insert? \n 1. Customer \n2. Transaction \n 3.Exit ')
                user_insert = input('')
                ## if ==1:
                    insert
                ##break
            elif user == '2':
                print(f'\nYou are now in "Update Data" page')
                ##break
            elif user == '3':
                print(f'\nYou are now in "Delete Data" page')
                ##break
            elif user == '4':
                print(f'\nYou are now in "See report" page')
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
        
        logout_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        ##logbook=




              
main()

