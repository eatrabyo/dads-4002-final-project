import pandas as pd
from sqlalchemy import exc, text, bindparam


def query_stock_alert(engine):
    try:
        stmt = f"""SELECT p.id as product_id ,p.product_name, p.stock from product p
            where p.stock < 10"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_customer_by_id(engine,cus_id):
    try:
        stmt = f"""SELECT c.id as customer_id, c.customer_user,c.phone_number,c.email  from customer c
            where c.id = {cus_id} """
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        df.set_index('customer_id',inplace=True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_customer_list(engine):
    try:
        stmt = f"""SELECT c.id as customer_id from customer c"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        cus_list = df['customer_id'].to_list()
        return cus_list
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)
