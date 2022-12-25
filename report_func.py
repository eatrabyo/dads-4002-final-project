import pandas as pd

import datetime
from sqlalchemy import text,exc


#function check date time format

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return('correct')

##############################################################

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
        tot_sale = df['sale'].values[0]
        return tot_sale

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
        tot_sale = df['sum(ds.sale)'].values[0]
        return tot_sale
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
        df.set_index('date', inplace = True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


#รวม#ยอดขายของ ... วันย้อนหลัง ยุบรวม
def query_tot_sale_timerange_sum(engine,t_interval,startdate,stopdate=None):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        SELECT round((sum(ds.sale)/{t_interval}),2) as avg_sale
from (
	SELECT DATE(purchasing_time) as date, SUM(price_per_unit * unit) as sale
FROM main
where purchasing_time between DATE_SUB('{startdate}', INTERVAL {t_interval} DAY) and '{startdate} 23:59:59'
GROUP BY DATE(purchasing_time)) as ds;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        tot_sale = df['avg_sale'].values[0]
        return tot_sale

    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

#เลือกสินค้าขายดี 10 อันดับแรก
def query_top_sale_product(engine):
    try:
        stmt = f"""SELECT product_name as 'product name',
SUM(price_per_unit * unit) as sale
FROM main
Left join product
ON main.product_id = product.id
group by product_name
order by sale DESC
limit 10;"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('product name', inplace = True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

#ยัง join ไม่สำเร็จ
def query_top_sale_cate(engine,startdate,stopdate):
    try:
        stmt = f"""
        select case 
            when d.product_category = 'pot' then 'กระถางต้นไม้'
            when d.product_category = 'agl' then 'อโกลนีมา'
            when d.product_category = 'phi' then 'ฟืโลเดนดรอน'
            when d.product_category = 'sun' then 'ต้นไม้ทนแดด'
            when d.product_category = 'air' then 'ต้นไม้ฟอกอากาศ'
            when d.product_category = 'bon' then 'บอนไซ'
            when d.product_category = 'han' then 'ต้นไม้แขวน'
            when d.product_category = 'mmk' then 'ต้นไม้มงคล'
            when d.product_category = 'fer' then 'ปุ๋ย'
            when d.product_category = 'plu' then 'พลูด่าง'
            when d.product_category = 'til' then 'ต้นไม้รากอากาศ'
            when d.product_category = 'dec' then 'ของตกแต่ง'
                    else 'A'
            end as 'category name',
            d.sale
            
            from (
                SELECT product_category,
                SUM(price_per_unit * unit) as sale
                    from main
                Left join product
                ON main.product_id = product.id
                where purchasing_time between '{startdate}' and '{stopdate}'
                group by product_category
                order by sale DESC
                limit 3
                ) as d;

"""
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('category name', inplace = True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


def query_percentage_change(engine,startdate,stopdate):
    try:
        stmt = f"""with net_sale as (
	SELECT date(purchasing_time) as date,
	       SUM(price_per_unit * unit) as sale
	       
	from main
	where date(purchasing_time) between '{startdate}' and '{stopdate}'
	GROUP BY DATE(purchasing_time)
	order by Date(purchasing_time) ASC 
    )

    select date,sale,
    sale - LAG(sale,1) OVER (ORDER BY date) AS diff,
    round(((sale / ( LAG(sale,1) OVER (ORDER BY date)) -1) *100),2) AS 'diff(%)'
    from (net_sale);"""


        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)



def query_top_profit(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
            SELECT 
            product_name as 'product name',
            price_per_unit as 'price',
            unit,
            product_cost as cost,
            SUM((price_per_unit-product_cost) * unit) as profit
        FROM main
        Left join product
        ON main.product_id = product.id
        where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
        group by product_name,product_cost,price_per_unit,unit
        order by profit DESC
        limit 10;
    
        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('product name', inplace = True)

        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)



def query_avr_basket(engine,startdate,stopdate=None):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        select round(avg(d1.sale),2) as 'average basket size'
        from(select 
            transaction_id
            ,date(purchasing_time) as "purchasing date"
            ,SUM(price_per_unit * unit) as sale
            ,customer_user
            from main
            Left join customer
            ON main.customer_id = customer.id
            
            where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
            GROUP BY transaction_id,purchasing_time,customer_user) as d1
        ;        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        tot_sale = df['average basket size'].values[0]
        return tot_sale
        
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


def query_crm_top5(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        select 
            customer_user as 'customer name',
            SUM(price_per_unit * unit) as sale   
            from main
            Left join customer
            ON main.customer_id = customer.id

        where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
        GROUP BY transaction_id,purchasing_time,customer_user
        order by sale DESC
        limit 10;
    
        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('customer name', inplace = True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


#แก้ need group by transaction id
def query_crm_old(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        select case when dm.old_customer = 1 
            then 'old customer'
            else 'new customer'
        end as 'customer status',
        count(dm.old_customer) as 'number of customer'
		from ( 
			select 
			    old_customer
			    from main
			Left join customer
			ON main.customer_id = customer.id
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
			)as dm
		group by dm.old_customer;

        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('customer status', inplace = True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)
        


def query_crm_old_list(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        select customer_user 'customer name',
            case when dm.old_customer = 1 
                    then 'old customer'
                    else 'new customer'
            end as 'customer status'
            
            from ( 
                    select 
                    old_customer,
                    customer_user
                    from main
                    Left join customer
                    ON main.customer_id = customer.id
                    
                    where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
                    group by customer_user,old_customer) as dm;
            """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('customer name', inplace = True)

        return df

    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


def export_crm_old_list(engine):
    with engine.connect() as con:
 
        rs = con.execute("""
                select customer_user 'customer name',
                        case when dm.old_customer = 1 
                                then 'old customer'
                                else 'new customer'
                        end as 'customer status'
                        
                        from ( 
                                select 
                                old_customer,
                                customer_user
                                from main
                                Left join customer
                                ON main.customer_id = customer.id
                                
                                where purchasing_time between '2022-10-10' and '2022-10-20 23:59:59'
                                group by customer_user,old_customer) as dm;
                        """)    
        lst = []
        for row in rs:
                w = row[0] + ',' + row[1]
                lst.append(w)
                #print(row[0],row[1])

        with open ("export.txt",mode = 'w',encoding = 'utf-8') as f:
                for i in range (len(lst)):
                        x = lst[i]
                        f.writelines(x)
                        f.writelines('\n')

    


#def print_crm_old_list(engine,startdate,stopdate):
 #       for row in rs:
  #      #writeline
        #print(row[0],row[1])
        
        #with main_db.connect() as con:
 #   rs = con.execute('SELECT * FROM product')
  #  for row in rs:
   #     print(row[0],row[1],row[2],row[3],row[4])
        

    #######
    
