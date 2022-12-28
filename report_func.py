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

def existdf(engine,startdate,stopdate=None):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        select transaction_id
        from main
        where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
        ;
        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        return df

    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

##############################################################

def query_tot_sale_day(engine,startdate,stopdate=None):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        SELECT DATE(purchasing_time) as date, 
            SUM(price_per_unit * unit) as sale 
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
            SELECT DATE(purchasing_time), 
            SUM(price_per_unit * unit) as sale
            FROM main
            where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
            GROUP BY DATE(purchasing_time)) as ds;
    """
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
        SELECT DATE(purchasing_time) as date, 
        SUM(price_per_unit * unit) as sale
        FROM main
        where date(purchasing_time) between DATE_SUB('{startdate}', INTERVAL {t_interval} DAY) and '{startdate} 23:59:59'
        GROUP BY DATE(purchasing_time)
        order by Date(purchasing_time) ASC;
        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('date', inplace = True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


###########################################################

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
        GROUP BY DATE(purchasing_time)) as ds;
        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        tot_sale = df['avg_sale'].values[0]
        return tot_sale

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
            ;        
        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        tot_sale = df['average basket size'].values[0]
        return tot_sale
        
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


def export_avr_basket(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
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
            ;       
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0])
            lst.append(w)


        with open (f"avr_basket_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('average basket size: ')  
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')

###############
###############
#menu 3
###########################################################
###########################################################
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



def export_top_sale_product(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
        stmt = f"""
        SELECT 
            product_name as 'product name',
            SUM(price_per_unit * unit) as sale
        FROM main
        Left join product
        ON main.product_id = product.id
        group by product_name
        order by sale DESC
        limit 10;
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1])
            lst.append(w)


        with open (f"top_sale_product_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('product name,sale\n')
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')


###########################################################

def query_top_sale_cate(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
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
                where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
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


def export_top_sale_cate(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
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
                    where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
                    group by product_category
                    order by sale DESC
                    limit 3
                    ) as d;
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1])
            lst.append(w)


        with open (f"top_sale_cate_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('category name,sale\n')
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')


###########################################################

def query_percentage_change(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        with net_sale as (
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
            from (net_sale);
        """


        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('date', inplace = True)
        return df

    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

###########################################################

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


def export_top_profit(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
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
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4])
            lst.append(w)


        with open (f"top_profit_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('product name,price,unit,cost,tot profit\n')
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')


###########################################################



###############
###############
#menu 3
def query_crm_top10(engine,startdate,stopdate):
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

def export_crm_top10(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
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

        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1])
            lst.append(w)


        with open (f"crm_top10_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('customer name,sale\n') 
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')

###############
def query_crm_top_province(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        select
            destination_province as province,
            SUM(price_per_unit * unit) as sale
        from main
        where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
        group by destination_province
        order by sale DESC 
        limit 5;
    
        """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('province', inplace = True)
        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


def export_crm_top_province(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
        stmt = f"""
        select
            destination_province as province,
            SUM(price_per_unit * unit) as sale
        from main
        where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
        group by destination_province
        order by sale DESC 
        limit 5;
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1])
            lst.append(w)


        with open (f"crm_top_province_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('province,sale\n')    
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')


###############
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
			    old_customer,
			    customer_user
			    from main
			Left join customer
			ON main.customer_id = customer.id
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
            group by old_customer , customer_user
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


def export_crm_old(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
        stmt = f"""
            select case when dm.old_customer = 1 
            then 'old customer'
            else 'new customer'
        end as 'customer status',
        count(dm.old_customer) as 'number of customer'
		from ( 
			select 
			    old_customer,
			    customer_user
			    from main
			Left join customer
			ON main.customer_id = customer.id
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
            group by old_customer , customer_user
			)as dm
		group by dm.old_customer;
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1])
            lst.append(w)


        with open (f"crm_old_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('customer status,number of customer\n')    
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')

        






##############################
##############################
#menu 4: raw data
def query_rawdata_cus(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        with cus as ( 
			select 
			old_customer,
			customer_user,
			destination_province,
   			transaction_id,
   			SUM(price_per_unit * unit) as sale
   			
			from main
			Left join customer
			ON main.customer_id = customer.id
			
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
			group by customer_user,old_customer,destination_province,transaction_id
		)
        select customer_user as 'customer name',
    
        case when old_customer = 1 
                then 'old customer'
                else 'new customer'
        end as 'customer status',
        destination_province as 'province',
        transaction_id as 'transaction id'
        from cus
            """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('customer name', inplace = True)

        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


def export_rawdata_cus(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
        stmt = f"""
        with cus as ( 
			select 
			old_customer,
			customer_user,
			destination_province,
   			transaction_id,
   			SUM(price_per_unit * unit) as sale
   			
			from main
			Left join customer
			ON main.customer_id = customer.id
			
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
			group by customer_user,old_customer,destination_province,transaction_id
		)
        select customer_user as 'customer name',
    
        case when old_customer = 1 
                then 'old customer'
                else 'new customer'
        end as 'customer status',
        destination_province as 'province',
        transaction_id as 'transaction id'
        from cus
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3])
            lst.append(w)


        with open (f"rawdata_cus_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('customer name,customer status,province,transaction id\n')
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')

####################################
def query_rawdata_oldcus(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        with cus as ( 
			select 
			old_customer,
			customer_user,
			destination_province,
   			transaction_id,
   			SUM(price_per_unit * unit) as sale
   			
			from main
			Left join customer
			ON main.customer_id = customer.id
			
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59' and old_customer = 1 
			group by customer_user,old_customer,destination_province,transaction_id
		)
        select customer_user as 'customer name',
    
        case when old_customer = 1 
                then 'old customer'
                else 'new customer'
        end as 'customer status',
        destination_province as 'province',
        transaction_id as 'transaction id'
        from cus
            """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('customer name', inplace = True)

        return df

    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


def export_rawdata_oldcus(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
        stmt = f"""
        with cus as ( 
			select 
			old_customer,
			customer_user,
			destination_province,
   			transaction_id,
   			SUM(price_per_unit * unit) as sale
   			
			from main
			Left join customer
			ON main.customer_id = customer.id
			
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59' and old_customer = 1 
			group by customer_user,old_customer,destination_province,transaction_id
		)
        select customer_user as 'customer name',
    
        case when old_customer = 1 
                then 'old customer'
                else 'new customer'
        end as 'customer status',
        destination_province as 'province',
        transaction_id as 'transaction id'
        from cus
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3])
            lst.append(w)


        with open (f"rawdata_oldcus_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('customer name,customer status,province,transaction id\n')
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')

####################################
def query_rawdata_newcus(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
        with cus as ( 
			select 
			old_customer,
			customer_user,
			destination_province,
   			transaction_id
   			
			from main
			Left join customer
			ON main.customer_id = customer.id
			
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59' and old_customer = 0 
			group by customer_user,old_customer,destination_province,transaction_id
		)
        select customer_user as 'customer name',
    
        case when old_customer = 1 
                then 'old customer'
                else 'new customer'
        end as 'customer status',
        destination_province as 'province',
        transaction_id as 'transaction id'
        from cus
            """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('customer name', inplace = True)

        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)
    
def export_rawdata_newcus(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
        stmt = f"""
        with cus as ( 
			select 
			old_customer,
			customer_user,
			destination_province,
   			transaction_id
   			
			from main
			Left join customer
			ON main.customer_id = customer.id
			
			where purchasing_time between '{startdate}' and '{stopdate} 23:59:59' and old_customer = 0 
			group by customer_user,old_customer,destination_province,transaction_id
		)
        select customer_user as 'customer name',
    
        case when old_customer = 1 
                then 'old customer'
                else 'new customer'
        end as 'customer status',
        destination_province as 'province',
        transaction_id as 'transaction id'
        from cus
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3])
            lst.append(w)


        with open (f"rawdata_newcus_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('customer name,customer status,province,transaction id\n')
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')


####################################
def query_rawdata_product(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
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
   		d.product_name as 'product name',
		d.id as 'product id',
		d.product_cost as 'cost',
		d.stock
   	
   	from(	
			SELECT 
				product_category,
				product_name,
				product.id,
				product_cost,
				stock
				
				FROM main
				Left join product
				ON main.product_id = product.id
				where purchasing_time between '2022-10-01' and '2022-10-20 23:59:59' 
				group by product_category,product_name,
				product.id,
				product_cost,
				stock
				order by product.id) as d
	;
            """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('product name', inplace = True)

        return df

    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)


def export_rawdata_product(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
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
                d.product_name as 'product name',
                d.id as 'product id',
                d.product_cost as 'cost',
                d.stock
   	
        from(	
                SELECT 
                    product_category,
                    product_name,
                    product.id,
                    product_cost,
                    stock
                    
                    FROM main
                    Left join product
                    ON main.product_id = product.id
                    where purchasing_time between '2022-10-01' and '2022-10-20 23:59:59' 
                    group by product_category,product_name,
                    product.id,
                    product_cost,
                    stock
                    order by product.id) as d

                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3])+ ',' + str(row[4])
            lst.append(w)


        with open (f"rawdata_product_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('category name,product name,product id,cost,stock\n')
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')

    
####################################
def query_rawdata_main(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate
    try:
        stmt = f"""
                select * 
                    from main
                    where purchasing_time between '2022-10-01' and '2022-10-20 23:59:59'
                """
        t = text(stmt)
        df = pd.read_sql(t,con=engine)
        df.set_index('id', inplace = True)

        return df
    except exc.SQLAlchemyError as e:
        print(type(e))
        print(e.orig)
        print(e.statement)

def export_rawdata_main(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
        stmt = f"""
                    select * 
                    from main
                    where purchasing_time between '2022-10-01' and '2022-10-20 23:59:59'
                        """
        rs = con.execute(stmt)
        lst = []
        for row in rs:
            w = str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7]) + ',' + str(row[8]) + ',' + str(row[9])
            lst.append(w)


        with open (f"rawdata_main_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('id,transaction id,product id,customer id,purchasing time,price,unit,district,province,postal code\n')
            for i in range (len(lst)):
                    x = lst[i]
                    f.writelines(x)
                    f.writelines('\n')

##############################
##############################

                       

def export_sale_report(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
    #total sale
        stmt1 = f"""
        SELECT sum(ds.sale)
            from (
                SELECT DATE(purchasing_time), 
                SUM(price_per_unit * unit) as sale
                FROM main
                where purchasing_time between '{startdate}' and '{stopdate} 23:59:59'
                GROUP BY DATE(purchasing_time)) as ds;   
                
                        """
        rs = con.execute(stmt1)
        lst1 = []
        for row in rs:
            w = str(row[0])
            lst1.append(w)

                    
    #average basket size
        stmt2 = f"""
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
            ;       
                        """
        rs = con.execute(stmt2)
        lst2 = []
        for row in rs:
            x = str(row[0])
            lst2.append(x)

        with open (f"sale_report_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
            f.writelines('total sale: ')  
            for i in range (len(lst1)):
                    x = lst1[i]
                    f.writelines(w)
                    f.writelines('\n')

            f.writelines('average basket size: ')  
            for i in range (len(lst2)):
                    x = lst2[i]
                    f.writelines(x)
                    f.writelines('\n')

    

def export_sale_report2(engine,startdate,stopdate):
    if stopdate == None:
        stopdate = startdate

    with engine.connect() as con:
        stmt3 = f"""
        SELECT DATE(purchasing_time) as date, 
        SUM(price_per_unit * unit) as sale
        FROM main
        where date(purchasing_time) between '{startdate}' and '{stopdate}'
        GROUP BY DATE(purchasing_time)
        order by Date(purchasing_time) ASC;
                        """
        rs = con.execute(stmt3)
        lst3 = []
        for row in rs:
            y = str(row[0]) + ',' + str(row[1])
            lst3.append(y)


        with open (f"sale_report_2_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
        #sale of each day     
            f.writelines('date,sale\n')  
            for i in range (len(lst3)):
                    y = lst3[i]
                    f.writelines(y)
                    f.writelines('\n')


# ขึ้น value error -> 

# def export_sale_report3(engine,startdate,stopdate):
#     if stopdate == None:
#         stopdate = startdate

#     with engine.connect() as con:
#         stmt4 = f"""
#         with net_sale as 
#             (SELECT date(purchasing_time) as date,
#                 SUM(price_per_unit * unit) as sale
                
#             from main
#             where date(purchasing_time) between '{startdate}' and '{stopdate}'
#             GROUP BY DATE(purchasing_time)
#             order by Date(purchasing_time) ASC 
#             )

#             select date,sale,
#             sale - LAG(sale,1) OVER (ORDER BY date) AS diff,
#             round(((sale / ( LAG(sale,1) OVER (ORDER BY date)) -1) *100),2) AS 'diff(%)'
#             from net_sale;
#                         """
#         rs = con.execute(stmt4)
#         lst4 = []
#         for row in rs:
#             z = str(row[0])
#             lst4.append(z)

#         with open (f"sale_report_3_{startdate}_{stopdate}.txt",mode = 'w',encoding = 'utf-8') as f:
#             f.writelines('percentage change in sale: ')  
#             for i in range (len(lst4)):
#                     x = lst4[i]
#                     f.writelines(z)
#                     f.writelines('\n')

                

    
        

       



            






        
