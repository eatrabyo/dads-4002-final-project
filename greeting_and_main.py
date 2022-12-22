from datetime import date
from engine import main_db
from sqlalchemy import exc, text, bindparam
import pandas as pd
from greeting_and_main_func import stock_aleart_greeting, main, login

#Greeting
print('\033[\n\n+1m'+'**** Welcome to Stock management DADs4002 ****'+'\033[0m')
#login and check password
login()

# STOCK ALERT
print(f'\n----- STOCK ALERT ON {date.today()} -----')
stock_aleart_greeting(engine = main_db)

#USER CHOOSING MANU >> add more text to tell user which manu they are in
print('\n\nPlease select any of the following manu \n 1.Insert data \n 2.Update data \n 3.Delete data \n 4.See report \n 5.Exit')
user_respond = input('What do you like to do today? (type 1, 2, 3, 4, or 5): ')
main(user=user_respond)