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

def query_percentage_change(engine):
    try:
        stmt = f"""with net_sale as (
	SELECT date(purchasing_time) as d,
	       SUM(price_per_unit * unit) as p
	       
	from main
	where date(purchasing_time) between DATE_SUB('2022-10-20', INTERVAL 7 DAY) and '2022-10-20 23:59:59'
	GROUP BY DATE(purchasing_time)
	order by Date(purchasing_time) ASC 
)


select d,p,
LAG(p,1) OVER (ORDER BY d) AS previous_sale,
p - LAG(p,1) OVER (ORDER BY d) AS DOD_Difference,
(p / ( LAG(p,1) OVER (ORDER BY d)) -1) *100 AS 'DOD_Diff(%)'
from (net_sale);"""
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
##############################################################

#จะแสดง executive summary มาเลย 
startdate = '2022-10-10'

#อยากใส่ชื่ออ่ะ Welcome = "name" ของคนที่ login
print('Welcome')
print(f"Let's see summary of: {startdate}")
print()

print(f'Total sale of: {startdate}')
df = query_tot_sale_day(main_db,startdate)
print(df)
print()

print('sale of previous 7 days')
t_interval = 7
df = query_tot_sale_timerange(main_db,t_interval,startdate)
print(df)
print()

print('sale 7 days rolling average')
df = query_tot_sale_timerange_sum(main_db,t_interval,startdate)
print(df)

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


##############################################################
#เลือก menu
print('To explore further?')
while True:
    print('report menu: \n 1. sale report (pick your own time range)  \n 2.  \n 3. exit')
    report_menu = input('Please enter menu number: ')
    if report_menu in ['1','2','3']:
        break 
    else:
        print('Wrong menu number.')
        continue
#print('end')

if report_menu == '1':
    while True:
        try:
            startdate = input('Start date: (yyyy-mm-dd)')
            validate(startdate)
            break
        except:
            print("Invalid date and time format")
            continue
1
    #print('end of date start format prove')
#?? อันนี้อยากให้มัน tab ไปทางขวา 1 ดึ๊บ ตอนนี้มันอยู่นอก if
while True:
    try:
        stopdate = input('Stop date: (yyyy-mm-dd)')
        validate(stopdate)
        break
    except:
        print("Invalid date and time format")
        continue
    #print('end of date stop format prove')

# รายการยอดรวม สินค้า ตามวันที่เลือก
print(f'Sale summary between: {startdate} to {stopdate}')
df = query_tot_sale_day(main_db,startdate,stopdate)
print(df)

df = query_tot_sale_day_sum(main_db,startdate,stopdate)
print(df)

df = query_percentage_change(main_db)
print(df)