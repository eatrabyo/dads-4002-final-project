import pandas as pd
from sqlalchemy import exc, text, bindparam
import pandas as pd


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
