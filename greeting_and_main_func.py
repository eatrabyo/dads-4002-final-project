from datetime import date, datetime
import os
from sqlalchemy import exc, text
import pandas as pd
from tabulate import tabulate

from engine import main_db, mysql_engine

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


        while True:
            ack = input('\nPlease READ stock alert and acknowledge (type a to acknowledge): ').lower()
            if ack == 'a':
                break
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

def backup_all_data():
    with main_db.connect() as con:
        pr = con.execute('SELECT * FROM product')
        with open('ProductBackUp.txt', 'w', encoding='utf-8') as product_backup:   
            product_backup.writelines(f'\n---- Backup Product Data on {datetime.now()} ----')
            product_backup.writelines(f'\n\nid,product_category,product_name,product_cost,stock') 
            for row in pr:
                product_backup.writelines(f'\n{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}')

        ma = con.execute('SELECT * FROM main')
        with open('MainBackUp.txt', 'w', encoding='utf-8') as main_backup:   
            main_backup.writelines(f'\n---- Backup Main Data on {datetime.now()} ----')
            main_backup.writelines(f'\n\ntransaction_id,purchasing_time,customer_id,product_id,price_per_uni,uni,destination_district,destination_province,postal_code') 
            for row in ma:
                main_backup.writelines(f'\n{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]}')
        
        cu = con.execute('SELECT * FROM customer')
        with open('CustomerBackUp.txt', 'w', encoding='utf-8') as customer_backup:   
            customer_backup.writelines(f'\n---- Backup Customer Data on {datetime.now()} ----')
            customer_backup.writelines(f'\n\ncustomer_user,old_customer,phone_number,email') 
            for row in cu:
                customer_backup.writelines(f'\n{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}')
        
        pc = con.execute('SELECT * FROM customer')
        with open('ProductCategoryBackUp.txt', 'w', encoding='utf-8') as product_cat_backup:   
            product_cat_backup.writelines(f'\n---- Backup ProductCategory Data on {datetime.now()} ----')
            product_cat_backup.writelines(f'\n\nproduct_category,name') 
            for row in pc:
                product_cat_backup.writelines(f'\n{row[0]},{row[1]}')