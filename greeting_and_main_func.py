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