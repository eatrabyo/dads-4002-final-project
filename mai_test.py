import pandas as pd
from sqlalchemy import text,exc

from engine import main_db
from query import query_stock_alert

#รวมยอดขายของวันนั้นๆ แต่ยัง ยุบวันแบบไม่มีเวลาไม่ได้ T-T
def query_tot_sale_day(engine):
    try:
        stmt = f"""select 
purchasing_time,
SUM(price_per_unit * unit) as sale
from main
where purchasing_time between '2022-10-10' and '2022-10-10 23:59:59'
GROUP BY purchasing_time"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

#เลือกสินค้าขายดี 10 อันดับแรก
def query_top_sale(engine):
    try:
        stmt = f"""SELECT transaction_id, 
SUM(price_per_unit * unit) as sale
FROM main
GROUP BY transaction_id
ORDER BY sale DESC
limit 10;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

#function check date time format
import datetime
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return('correct')

##############################################################
#เลือก menu
while True:
    report_menu = input('Please enter menu number: ')
    print('report menu: \n 1. summary report \n 2. sale report')
    if report_menu in ['1','2','3']:
        break 
    else:
        print('Wrong menu number.')
        continue
#print('end')

##############################################################
#summary report
if report_menu == '1' :
    
    #select date
    while True:
        try:
            date_pick = input('Date: (yyyy-mm-dd)')
            validate(date_pick)
            break
        except:
            print("Invalid date and time format")
            continue

    #print('end of date start format prove')

#จะแสดง executive summary มาเลย ไม่ต้องเลือกอะไรนอกจากวัน
    #function > sale summary ของ วันที่เลือก
    #ยอดขายรวมของวันที่เลือก
    print(f'Sale summary of: {date_pick}')
    df = query_tot_sale_day(main_db)
    print(df)
    #ยอดขายรวม 7 วันย้อนหลัง นับจากวันที่เลือก
    df = query_tot_sale_week(main_db)
    print(df)
    #ยอดขายรวม 30 วันย้อนหลัง นับจากวันที่เลือก
    df = query_tot_sale_month(main_db)
    print(df)
    #สินค้าขายดี 10 อันดับแรกของวันที่เลือก
    df = query_top_sale_product(main_db)
    print(df)
    #หมวดหมู่สินค้าขายดี 3 อันดับแรกของวันที่เลือก
    df = query_top_sale_cate(main_db)
        print(df)


####################
#menu อื่นๆ เลือก ช่วงเวลาได้
    #select date
    while True:
        try:
            date_start = input('Start date: (yyyy-mm-dd)')
            validate(date_start)
            break
        except:
            print("Invalid date and time format")
            continue

    #print('end of date start format prove')

    while True:
        try:
            date_stop = input('St date: (yyyy-mm-dd)')
            validate(date_stop)
            break
        except:
            print("Invalid date and time format")
            continue
    #print('end of date stop format prove')