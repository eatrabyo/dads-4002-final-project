import pandas as pd
from sqlalchemy import exc, text, bindparam


def update_email(engine,cus_id,email):
    try:
        if email != '':
            with engine.begin() as conn:
                sql = f"""
                UPDATE customer SET email = '{email}'
                WHERE id = {cus_id}
                """
                
                conn.execute(text(sql))
            print('Finished update new email.')
        else:
            with engine.begin() as conn:
                sql = f"""
                UPDATE customer SET email = NULL
                WHERE id = {cus_id}
                """
                
                conn.execute(text(sql))
            print('Finished update new email.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_phone(engine,cus_id,phone):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE customer SET phone_number = '{phone}'
            WHERE id = {cus_id}
            """
            
            conn.execute(text(sql))
        print('Finished update new phone number.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_stock(engine,product_id,stock):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE product SET stock = {stock}
            WHERE id = '{product_id}'
            """
            
            conn.execute(text(sql))
        print('Finished update new stock.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def update_prod_cost(engine,product_id,cost):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE product SET product_cost = {cost}
            WHERE id = '{product_id}'
            """
            
            conn.execute(text(sql))
        print('Finished update new cost.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)