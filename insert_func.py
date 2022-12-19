import pandas as pd
from sqlalchemy import exc

def insert_new_customer(df,engine):
    try:
        df.to_sql(name="customer",con=engine, if_exists='append', index=False)
        print("Finished adding new customer info.")

    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def insert_new_transaction(df,engine):
    try:
        df.to_sql(name="main",con=engine, if_exists='append', index=False)
        print("Finished adding new transaction.")

    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)