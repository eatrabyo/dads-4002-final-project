from datetime import date, datetime
import os
from sqlalchemy import exc, text
import pandas as pd

from engine import main_db

def stock_aleart_greeting(engine):
    ##try:
        os.system('cls') 
        stmt = f"""select product_id,
product.product_name,
stock,
count(main.product_id) as sales_vol
from main
left join product on product.id = main.product_id
where stock < 10
group by product_id
order by stock asc;

SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
"""
        t=text(stmt)
        df=pd.read_sql(t, con = engine)
        df.set_index("product_id",inplace=True)
        print(f'\n----- STOCK ALERT ON {date.today()} -----')
        print(df)
    
    #except exc.SQLAlchemyError as e:
     #   print(type(e))
      #  print(e.orig)
     #   print(e.statement)



#check password
def login():
    #try:
        os.system('cls')
        stmt = """SELECT * FROM dads_4002.admin_info"""
        t=text(stmt)
        df = pd.read_sql(t,con=main_db)
        dict_user=dict(zip(df['admin_username'],df['admin_password']))
        while True:
            print('\n--- LOGIN to Inventory Management System ---')
            user_name = input(f'\nPlease enter your username: ' )
            user_password = input(f'Please enter your password: ')
            if (user_name,user_password) in dict_user.items():
                print('-\n----- LOGIN SUCCESSFULLY ------')
                auth = True
                login_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                break              
            else:
                print(f'\nPlease enter the correct username and password!!')
                continue               
        return auth, login_time, user_name    
    #except exc.SQLAlchemyError as e:
        #print(type(e))
        #print(e.orig)
        ##print(e.statement)

stock_aleart_greeting(main_db)