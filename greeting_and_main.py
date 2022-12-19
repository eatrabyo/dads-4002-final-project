from datetime import date
from engine import main_db
from sqlalchemy import exc, text, bindparam
import pandas as pd

#Greeting
print('\033[\n\n+1m'+'**** Welcome to Stock management DADs4002 ****'+'\033[0m')

## LOG IN
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
print(f'\n----- STOCK ALERT ON {date.today()} -----',)
try:
  stmt = f'''select product.id as product_id
                ,product_name
                ,stock
                ,count(main.product_id) as sale_volume
          from product
          left join main on main.product_id = product.id
          where  product.stock < 10
          group by product.id
          order by count(main.product_id) desc'''
  t=text(stmt)
  df=pd.read_sql(t, con = main_db)
  print(df)
except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

#USER CHOOSING MANU
print('\n\nPlease select any of the following manu \n 1.Insert data \n 2.Update data \n 3.Delete data \n 4.See report')
user = input('What do you like to do today? (type 1, 2, 3, or 4): ')