from datetime import date, datetime
import os
from sqlalchemy import exc, text
import pandas as pd
from tabulate import tabulate

from engine import main_db, mysql_engine

def stock_aleart_greeting(engine):
    try:
        ## os.system('cls')
        safety_stock = 10          
        stmt = f"""
select
	product.id, product_name, stock, count(main.product_id) as sale_vol 
    from product
    left join main on product.id = main.product_id 
    where  stock < {safety_stock}
    group by product.id, product_name, stock
    order by stock asc;
"""
        #stock slert
        t=text(stmt)
        df=pd.read_sql(t,con=main_db)
        table = df.set_index("id",inplace=True)
        print(f'\n----- STOCK ALERT ON {date.today()} -----')
        print(tabulate(df, headers='keys', tablefmt='psql'))
        
        #to do list
        print('\n\nTo-do list')
        subtract = pd.DataFrame(safety_stock - df['stock'])
        subtract.rename(columns = {'stock':'จำนวนที่ต้องซื้อเข้า'}, inplace = True)
        df2=subtract.merge(df['product_name'],left_index=True, right_index=True)
        print(tabulate(df2, headers='keys', tablefmt='psql'))

        while True:
            ack = input('\nPlease READ stock alert and acknowledge "To-do list" (type a to acknowledge): ').lower()
            if ack == 'a':
                break
    except exc.SQLAlchemyError as e:
        print(type(e)) #type ของ error คืออะไร
        print(e.orig) #error มาจากไหน
        print(e.statement) #statement sql ที่เกิด error

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
        print(type(e)) #type ของ error คืออะไร
        print(e.orig) #error มาจากไหน
        print(e.statement) #statement sql ที่เกิด error

def backup_all_data():
    with main_db.connect() as con:
        now1 = datetime.now()
        pr = con.execute('SELECT * FROM product')
        with open(f'ProductBackUp {now1.strftime("%d%m%Y_%H%M%S")}.txt', 'w', encoding='utf-8') as product_backup:   
            product_backup.writelines(f'\n\nid,product_category,product_name,product_cost,stock') 
            for row in pr:
                product_backup.writelines(f'\n{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}')

        ma = con.execute('SELECT * FROM main')
        with open(f'MainBackUp {now1.strftime("%d%m%Y_%H%M%S")}.txt', 'w', encoding='utf-8') as main_backup:   
            main_backup.writelines(f'\n\nid,transaction_id,product_id,customer_id,purchasing_time,price_per_uni,unit,destination_district,destination_province,postal_code') 
            for row in ma:
                main_backup.writelines(f'\n{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]},{row[9]}')
        
        cu = con.execute('SELECT * FROM customer')
        with open(f'CustomerBackUp {now1.strftime("%d%m%Y_%H%M%S")}.txt', 'w', encoding='utf-8') as customer_backup:   
            customer_backup.writelines(f'\n\nid,customer_user,old_customer,phone_number,email') 
            for row in cu:
                customer_backup.writelines(f'\n{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}')
        
        pc = con.execute('SELECT * FROM product_category')
        with open(f'ProductCategoryBackUp {now1.strftime("%d%m%Y_%H%M%S")}.txt', 'w', encoding='utf-8') as product_cat_backup:   
            product_cat_backup.writelines(f'\n\nproduct_category,name') 
            for row in pc:
                product_cat_backup.writelines(f'\n{row[0]},{row[1]}')