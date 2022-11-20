from engine import mysql_engine
import pandas as pd
from sqlalchemy import exc
from omegaconf import OmegaConf

# load config
conf = OmegaConf.load('config.yaml')
mydb_engine = mysql_engine(conf.user, conf.passw, conf.host,
                           conf.port, conf.database_main)

df = pd.read_excel(
    '/Users/itthisak/Desktop/Nida/DADS_4002/DADS_4002_HW/food_tracking.xlsx', sheet_name='main')


try:
    df.to_sql(name="test", con=mydb_engine, if_exists='replace', index=False)
except exc.SQLAlchemyError as e:
    print(type(e))
    print(e.orig)
    print(e.statement)
