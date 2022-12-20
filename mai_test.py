import pandas as pd
from sqlalchemy import text,exc

from engine import main_db
from query import query_stock_alert

#ยอดขายของช่วงวัน
def query_tot_sale_day(engine,startdate,stopdate=None):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        SELECT DATE(purchasing_time) as date, SUM(price_per_unit * unit) as sale
FROM main 
where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
GROUP BY DATE(purchasing_time)
ORDER BY DATE(purchasing_time) ASC ;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

#รวมยอดขายของช่วงวัน
def query_tot_sale_day_sum(engine,startdate,stopdate=None):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        SELECT sum(ds.sale)
from (
	SELECT DATE(purchasing_time), SUM(price_per_unit * unit) as sale
	FROM main
	where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
	GROUP BY DATE(purchasing_time)) as ds;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

######################################################
##ยอดขายของ ... วันย้อนหลัง แยกตามวัน
def query_tot_sale_timerange(engine,t_interval,startdate,stopdate=None):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        SELECT DATE(purchasing_time) as date, SUM(price_per_unit * unit) as sale
FROM main
where date(purchasing_time) between DATE_SUB('{startdate}', INTERVAL {t_interval} DAY) and '{startdate} 23:59:59'
GROUP BY DATE(purchasing_time)
order by Date(purchasing_time) ASC;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


#รวม#ยอดขายของ ... วันย้อนหลัง แยกตามวัน
def query_tot_sale_timerange_sum(engine,t_interval,startdate,stopdate=None):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        SELECT sum(ds.sale)
from (
	SELECT DATE(purchasing_time) as date, SUM(price_per_unit * unit) as sale
FROM main
where date(purchasing_time) between DATE_SUB('{startdate}', INTERVAL {t_interval} DAY) and '{startdate} 23:59:59'
GROUP BY DATE(purchasing_time) as ds;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)




#เลือกสินค้าขายดี 10 อันดับแรก
def query_top_sale_product(engine):
    try:
        stmt = f"""SELECT product_name,
SUM(price_per_unit * unit) as sale
FROM main
Left join product
ON main.product_id = product.id
group by product_name
order by sale DESC
limit 10;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def query_top_sale_cate(engine):
    try:
        stmt = f"""SELECT product_category,
SUM(price_per_unit * unit) as sale
FROM main
Left join product
ON main.product_id = product.id
group by product_category
order by sale DESC
limit 3;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

##############################################################
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
    print('report menu: \n 1. summary report \n 2. sale report \n 3. exit')
    if report_menu in ['1','2','3']:
        break 
    else:
        print('Wrong menu number.')
        continue
#print('end')

##############################################################
#summary report
if report_menu == '1':
    
    #select date
    while True:
        try:
            # startdate = input('Date: (yyyy-mm-dd)')
            startdate = '2022-10-10'
            validate(startdate)
            break
        except:
            print("Invalid date and time format")
            continue
    #print('end of date start format prove')



#จะแสดง executive summary มาเลย ไม่ต้องเลือกอะไรนอกจากวัน
    #function > sale summary ของ วันที่เลือก
    #ยอดขายรวมของวันที่เลือก
    print(f'Sale summary of: {startdate}')
    print()
    
    print(f'Total sale of: {startdate}')
    df = query_tot_sale_day(main_db,startdate)
    print(df)
    print()


    # #ยอดขายรวม 7 วันย้อนหลัง นับจากวันที่เลือก
    #df = query_tot_sale_week(main_db,t_interval,startdate)
    # print(df)

    print('sale of previous 7 days')
    t_interval = 7
    df = query_tot_sale_timerange(main_db,t_interval,startdate)
    print(df)
    print()
   
    print('sale 7 days rolling average')
    df = query_tot_sale_timerange_sum(main_db,t_interval,startdate)
    print(df)

     #ยอดขายรวม 30 วันย้อนหลัง นับจากวันที่เลือก << เวิ่นเว้อไปหน่อย ตัดทิ้ง
    # print('sale of previous 30 days')
    # t_interval = 30
    # df = query_tot_sale_timerange(main_db,t_interval,startdate)
    # print(df)
    # print()
   
    print('sale 30 days rolling average')
    df = query_tot_sale_timerange_sum(main_db,t_interval,startdate)
    print(df)

    # #สินค้าขายดี 10 อันดับแรกของวันที่เลือก
    print(f'Top product sale of: {startdate}')
    df = query_top_sale_product(main_db)
    print(df)
    print()

    # #หมวดหมู่สินค้าขายดี 3 อันดับแรกของวันที่เลือก
    print(f'Top 3 category sale of: {startdate}')
    df = query_top_sale_cate(main_db)
    print(df)
    print()


####################
#menu อื่นๆ เลือก ช่วงเวลาได้
    #select date
# if report_menu == '2':
#     while True:
#         try:
#             date_start = input('Start date: (yyyy-mm-dd)')
#             validate(date_start)
#             break
#         except:
#             print("Invalid date and time format")
#             continue
# 1
#     #print('end of date start format prove')
#     # 
#     while True:
#         try:
#             stopdate = input('Stop date: (yyyy-mm-dd)')
#             validate(stopdate)
#             break
#         except:
#             print("Invalid date and time format")
#             continue
#     #print('end of date stop format prove')

#     # รายการยอดรวม สินค้า ตามวันที่เลือก
#     print(f'Sale summary of: {startdate} to {stopdate}')
#     df = query_tot_sale_day(main_db,startdate,stopdate)
#     print(df)
#     df = query_tot_sale_day_sum(main_db,startdate,stopdate)
#     print(df)