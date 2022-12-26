from datetime import date, datetime
import os
from sqlalchemy import exc, text
import pandas as pd
from tabulate import tabulate

from engine import main_db

def stock_aleart_greeting(engine):
    try:
        ## os.system('cls') 
        stmt = """
select
	product.id, product_name, stock, count(main.product_id) as sale_vol 
    from product
    left join main on product.id = main.product_id 
    where  stock < 10
    group by product.id
    order by stock asc;
"""
        t=text(stmt)
        df=pd.read_sql(t,con=main_db)
        table = df.set_index("id",inplace=True)
        print(f'\n----- STOCK ALERT ON {date.today()} -----')
        print(tabulate(df, headers='keys', tablefmt='psql'))
        safety_stock = 10


    
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)



#check password
def login():
    try:
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
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)
