from datetime import date
from engine import main_db
from sqlalchemy import exc, text, bindparam
import pandas as pd

def stock_aleart_greeting(engine):
    try:
        stmt = f"""select product.id as product_id
            ,product_name
            ,stock
            ,count(main.product_id) as sale_volume 
            from product 
            left join main on main.product_id = product.id 
            where  product.stock < 10 
            group by product.id 
            order by count(main.product_id) desc"""
        t=text(stmt)
        df=pd.read_sql(t, con = engine)
        df.set_index("product_id",inplace=True)
        print(df)
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def main(user):
    ##while True:
        user = input('What do you like to do today? (type 1, 2, 3, 4, or 5): ')
        if user in ['1','2','3','4','5']:
            if user == '1':
                print(f'\nYou are now in "Insert Data" page')
            elif user == '2':
                print(f'\nYou are now in "Update Data" page')
            elif user == '3':
                print(f'\nYou are now in "Delete Data" page')
            elif user == '4':
                print(f'\nYou are now in "See report" page')
            elif user == '5':
                print(f'\nGoodbye :)')
        else:
            print(f'\nPlease enter the correct menu (1-5)')