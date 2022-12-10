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
        stmt = """SELECT c.id as customer_id from customer c"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        cus_list = df['customer_id'].to_list()
        return cus_list
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_product_list(engine):
    try:
        stmt = """SELECT p.id as product_id from product p"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        product_list = df['product_id'].to_list()
        return product_list
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_product_by_id(engine,product_id):
    try:
        stmt = f"""SELECT p.id as product_id, p.product_category, p.product_name,p.product_cost,p.stock from product p
            where p.id = '{product_id}' """
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        df.set_index('product_id',inplace=True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_trans_id_list(engine):
    try:
        stmt = """SELECT DISTINCT(m.transaction_id) as trans_id from main m"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        trans_list = df['trans_id'].to_list()
        return trans_list
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_trans_by_id(engine,trans_id,row_id = None):
    try:
        if row_id == None:
            stmt = f"""SELECT * from main m
                where m.transaction_id = '{trans_id}' """
            t = text(stmt)
            df = pd.read_sql(t, con=engine)
            df.set_index('id',inplace=True)
            return df
        else:
            stmt = f"""SELECT * from main m
                where m.transaction_id = '{trans_id}' and m.id = {row_id} """
            t = text(stmt)
            df = pd.read_sql(t, con=engine)
            df.set_index('id',inplace=True)
            return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_stock_by_product_id(engine,product_id):
    try:
        stmt = f"""SELECT p.stock from product p
            WHERE p.id = '{product_id}'"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        old_stock = df['stock'][0]
        return old_stock
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_product_name(engine,product_id):
    try:
        stmt = f"""SELECT p.product_name from product p
            WHERE p.id = '{product_id}'"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        name = df['product_name'][0]
        return name
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_new_customer(engine):
    try:
        stmt = """SELECT c.id as customer_id, c.customer_user,c.old_customer,c.phone_number,c.email from customer c
                where c.id = (SELECT max(c2.id) from customer c2)"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        df.set_index('customer_id',inplace=True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_lastest_transaction(engine):
    try:
        stmt = """    SELECT m.transaction_id from main m
            WHERE m.id = (SELECT max(m2.id) from main m2)"""
        t = text(stmt)
        df = pd.read_sql(t, con=engine)
        lastest_trans = df['transaction_id'][0]
        pre_fix, running_trans_id = lastest_trans.split('_')
        return pre_fix, running_trans_id
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)