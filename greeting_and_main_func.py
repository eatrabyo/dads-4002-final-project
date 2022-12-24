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
            cs = con.execute('SELECT * FROM customer')
            with open('CustomerBackUp.txt', 'w', encoding='utf-8') as customer_backup:   
                customer_backup.writelines(f'\n---- Backup Customer Data on {datetime.now()} ----\n\nid   customer_user    old_customer    phone_number     email  ')
            for row in cs:
                cs_detail = row[0],row[1],row[2],row[3],row[4]  
                with open('CustomerBackUp.txt', 'a', encoding='utf-8') as customer_backup:   
                    customer_backup.writelines(f'\n\n {cs_detail}')

            ms = con.execute('SELECT * FROM main')
            with open('MainBackUp.txt', 'w', encoding='utf-8') as main_backup:   
                main_backup.writelines(f'\n---- Backup Main Data on {datetime.now()} ----\n\ntransaction_id	    purchasing_time	    customer_id	    product_id	   price_per_unit	  unit	  destination_district	   destination_province	     postal_code')
            for row in ms:
                main_detail = row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]
                with open('MainBackUp.txt', 'a', encoding='utf-8') as main_backup:   
                    main_backup.writelines(f'\n\n {main_detail}')

            ps = con.execute('SELECT * FROM product')
            with open('ProductBackUp.txt', 'w', encoding='utf-8') as product_backup:
                product_backup.writelines(f'---- Backup Product Data on {datetime.now()} ----\n\nid	    product_category	product_name	product_cost	stock')
            for row in ps:
                product_detail = row[0],row[1],row[2],row[3],row[4]
                with open('ProductBackUp.txt', 'a', encoding='utf-8') as product_backup:   
                    product_backup.writelines(f'\n\n{product_detail}')

            pc = con.execute('SELECT * FROM product_category')
            with open('ProductCategoryBackUp.txt', 'w', encoding='utf-8') as productcat_backup:
                productcat_backup.writelines(f'---- Backup Product Category Data on {datetime.now()} ---- \n\nproduct_category   name')
            for row in pc:
                productcat_detail = [row[0],row[1]]
                with open('ProductCategoryBackUp.txt', 'a', encoding='utf-8') as productcat_backup:   
                    productcat_backup.writelines(f'\n\n {productcat_detail}')