from datetime import date
from engine import main_db
from sqlalchemy import exc, text, bindparam
import pandas as pd
from greeting_and_main_func import stock_aleart_greeting, main

#Greeting
print('\033[\n\n+1m'+'**** Welcome to Stock management DADs4002 ****'+'\033[0m')

## LOG IN >> add check if user is correct matching from table
user_name_input = ''
password_input=''
while True:
  if user_name_input != 'eatjung' and password_input != '9999':
    print('\nPlease enter the correct username and password:')
    user_name_input=str(input(f'▪ Please enter your username: ')).lower()
    password_input=str(input(f'▪ Please enter your password: '))
  else:
    break
print('------ LOG IN SUCCESSFULLY ------')


# STOCK ALERT
print(f'\n----- STOCK ALERT ON {date.today()} -----')
stock_aleart_greeting(engine = main_db)

#USER CHOOSING MANU >> add more text to tell user which manu they are in
print('\n\nPlease select any of the following manu \n 1.Insert data \n 2.Update data \n 3.Delete data \n 4.See report \n 5.Exit')
user_respond = input('What do you like to do today? (type 1, 2, 3, 4, or 5): ')
main(user=user_respond)