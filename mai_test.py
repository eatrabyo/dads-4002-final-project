import os

from engine import main_db
from report_func import *

os.system('clear') # 'clear' on mac, for windows 'cls'

#จะแสดง executive summary มาเลย 
startdate = '2022-10-10'

#อยากใส่ชื่ออ่ะ Welcome = "name" ของคนที่ login
print('Welcome')
print(f"Let's see summary of: {startdate}")
print()


df = query_tot_sale_day(main_db,startdate)
print(f'Total sale = {df}')
print()

print(f'sale of previous 7 days:')
t_interval = 7
df = query_tot_sale_timerange(main_db,t_interval,startdate)
print(df)
print()

df = query_tot_sale_timerange_sum(main_db,t_interval,startdate)
print(f'7 days rolling average of sale: {df}')

t_interval = 30
df = query_tot_sale_timerange_sum(main_db,t_interval,startdate)
print(f'30 days rolling average of sale: {df}')
print()

# สินค้าขายดี 10 อันดับแรกของวันที่เลือก
print(f'Top product sale:')
df = query_top_sale_product(main_db)
print(df)
print()

# หมวดหมู่สินค้าขายดี 3 อันดับแรกของวันที่เลือก
print(f'Top 3 category sale:')
df = query_top_sale_cate(main_db,startdate,stopdate=None)    
print(df)
print()


##############################################################
#เลือก menu
print('To explore further?')
while True:
    print('report menu: \n 1. sale report \n 2. percentage change in sale  \n 3. product top sale and top profit \n 4. showing data \n 5. exit')
    report_menu = input('Please enter menu number: ')
    if report_menu in ['1','2','3','4','5']:
        break 
    else:
        print('Wrong menu number.')
        print('Please select again from menu 1-5 as follow:')
        continue

if report_menu == '1':
    while True:
        try:
            startdate = input('Start date (yyyy-mm-dd): ')
            validate(startdate)
            break
        except:
            print("Invalid date and time format")
            continue

    while True:
        try:
            stopdate = input('Stop date (yyyy-mm-dd): ')
            validate(stopdate)
            break
        except:
            print("Invalid date and time format")
            continue
        #print('end of date stop format prove')

    # รายการยอดรวม สินค้า ตามวันที่เลือก
    print(f'Sale summary between: {startdate} to {stopdate}')

    df = query_tot_sale_day_sum(main_db,startdate,stopdate)
    print(f'Total sale = {df}')
    print()

    df = query_tot_sale_timerange(main_db,startdate,stopdate)
    print(f'Sale of each day:')
    print(df)
    print()

    df=query_avr_basket(main_db,startdate,stopdate=None)

elif report_menu == '2':
    while True:
        try:
            startdate = input('Start date (yyyy-mm-dd): ')
            validate(startdate)
            break
        except:
            print("Invalid date and time format")
            continue

    while True:
        try:
            stopdate = input('Stop date (yyyy-mm-dd): ')
            validate(stopdate)
            break
        except:
            print("Invalid date and time format")
            continue
        #print('end of date stop format prove')

    # สินค้าขายดี 10 อันดับแรกของวันที่เลือก
    print(f'Top product sale:')
    df = query_top_sale_product(main_db)
    print(df)
    print()

    #หมวดหมู่สินค้าขายดี 3 อันดับแรกของวันที่เลือก
    print(f'Top 3 category sale:')
    df = query_top_sale_cate(main_db,startdate,stopdate)
    print(df)
    print()
    
    #เป็นปัญหา!!!!
    #สินค้าที่ทำกำไรสูงสุด 3 อันดับแรกของวันที่เลือก
    print(f'Top 10 profitable product:')
    df = query_top_profit(main_db,startdate,stopdate)
    print(df)
    print()


elif report_menu == '3':
    while True:
        try:
            startdate = input('Start date (yyyy-mm-dd): ')
            validate(startdate)
            break
        except:
            print("Invalid date and time format")
            continue

    while True:
        try:
            stopdate = input('Stop date (yyyy-mm-dd): ')
            validate(stopdate)
            break
        except:
            print("Invalid date and time format")
            continue
        #print('end of date stop format prove')

    print(f'percentage change in sale: ')
    df = query_percentage_change(main_db,startdate,stopdate)
    print(df)





