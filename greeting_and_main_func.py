import mysql.connector
import pandas as pd
import sqlalchemy as db

#connect to data base
engine = db.create_engine()

my_db, my_cusor = None, None

try:
    my_db = mysql.connector.connect(host='localhost',
                                    user = root,
                                    password=mjkiakk2,
                                    database='dads_4002')
    print('Successfully connected to the database.')

    my_cusor = my_db.cursor() #prepare SQL insertion command and a row of data to be inserted
    
    # create a string of MySQL insertion command
    print('----- Execute command -----')
    sql_command = """select
	id, product_name, stock from product
    where  stock < 10
    order by stock asc;"""
    my_cusor.execute(sql_command)
    
df = pd.read_sql(sql_command,my_db)
print('\n === df.info () ===')
_ = display(df.info())
print('\n === df ===')
_ = display(df)