import pandas as pd
from sqlalchemy import exc, text, bindparam


def update_email(engine,cus_id,email):
    try:
        with engine.begin() as conn:
            sql = f"""
            UPDATE customer SET email = '{email}'
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
        print('Finished update new email.')
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)