import os
from engine import main_db
from report_func import *


def report():
    #จะแสดง executive summary มาเลย 
    startdate = '2022-10-10'
    #from datetime import date
    #startdate = date.today()
    #ตั้งใจให้แสดง dashboard ของ วันปัจจุบัน

    os.system('clear') # 'clear' on mac, for windows 'cls'
    print('Welcome')
    print(f"Let's see summary of: {startdate}")
    print()


    df = query_tot_sale_day_sum(main_db,startdate)
    print(f'Total sale = {df} baht')
    print()

    df=query_avr_basket(main_db,startdate,stopdate=None)
    print(f'Average basket size = {df} baht')
    print()

    print(f'Sale of previous 7 days:')
    t_interval = 7
    df = query_tot_sale_timerange(main_db,t_interval,startdate)
    print(df)
    print()

    df = query_tot_sale_timerange_sum(main_db,t_interval,startdate)
    print(f'7 days rolling average of sale: {df} baht')

    t_interval = 30
    df = query_tot_sale_timerange_sum(main_db,t_interval,startdate)
    print(f'30 days rolling average of sale: {df} baht')
    print()

    # สินค้าขายดี 10 อันดับแรกของวันที่เลือก
    print(f'Top 10 product sale:')
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
        while True:
            print('Report menu: \n 1. Sale report \n 2. Product top sale and top profit \n 3. Customer data \n 4. Showing data \n 5. exit')
            report_menu = input('Please enter menu number: ')
            if report_menu in ['1','2','3','4','5']:
                break 
            else:
                print('Wrong menu number.')
                print('Please select again from menu 1-5 as follow:')
                continue
        print()


        if report_menu == '1':
            os.system('clear') # 'clear' on mac, for windows 'cls'
            print(f'Menu 1: Sale report')
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

            if startdate > stopdate:
                startdate , stopdate = stopdate , startdate
                print(f'Since startdate greater than stopdate, we interchange its value.')
                print(f'> new start date: {startdate}')
                print(f'> new stop date: {stopdate}')
                print()

            df = existdf(main_db,startdate,stopdate=None)
            if len(df) == 0:
                print('No data in given date selection')
            else:
                # รายการยอดรวม สินค้า ตามวันที่เลือก
                print(f'Sale summary between: {startdate} to {stopdate}')

                df = query_tot_sale_day_sum(main_db,startdate,stopdate)
                print(f'Total sale = {df} baht')
                print()

                df = query_tot_sale_timerange(main_db,startdate,stopdate)
                print(f'Sale of each day:')
                print(df)
                print()

                df=query_avr_basket(main_db,startdate,stopdate=None)
                print(f'Average basket size = {df} baht')
                print()

                print(f'percentage change in sale: ')
                print(f'day on day different')
                df = query_percentage_change(main_db,startdate,stopdate)
                print(df)

                while True:
                    user_input = input (f'Would you to export data? (Y/N): ').lower()
                    if user_input in ['y','n']:
                        break
                    else:
                        continue

                if user_input == 'y':
                    export_sale_report(main_db,startdate,stopdate)
                    # export_sale_report2(main_db,startdate,stopdate)
                    #export_sale_report3(main_db,startdate,stopdate)



 ##################           

        elif report_menu == '2':
            os.system('clear') # 'clear' on mac, for windows 'cls'
            print(f'Menu 2: Product top sale and top profit')
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
            print()

            if startdate > stopdate:
                startdate , stopdate = stopdate , startdate
                print(f'Since startdate greater than stopdate, we interchange its value.')
                print(f'> new start date: {startdate}')
                print(f'> new stop date: {stopdate}')
                print()

            df = existdf(main_db,startdate,stopdate=None)
            if len(df) == 0:
                print('No data in given date selection')
            else:
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
                

                #สินค้าที่ทำกำไรสูงสุด 3 อันดับแรกของวันที่เลือก
                print(f'Top 10 profitable product:')
                df = query_top_profit(main_db,startdate,stopdate)
                print(df)
                print()
                
                while True:
                    user_input = input (f'Would you to export data? (Y/N): ').lower()
                    if user_input in ['y','n']:
                        break
                    else:
                        continue

                if user_input == 'y':
                    export_top_sale_product(main_db,startdate,stopdate)
                    export_top_sale_cate(main_db,startdate,stopdate)
                    export_top_profit(main_db,startdate,stopdate)



        #CRM
        elif report_menu == '3':
            os.system('clear') # 'clear' on mac, for windows 'cls'
            print(f'Menu 3: Customer data')
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

            print()

            if startdate > stopdate:
                startdate , stopdate = stopdate , startdate
                print(f'Since startdate greater than stopdate, we interchange its value.')
                print(f'> new start date: {startdate}')
                print(f'> new stop date: {stopdate}')
                print()

            df = existdf(main_db,startdate,stopdate=None)
            if len(df) == 0:
                print('No data in given date selection')

            else:

                print(f'top 10 buyer with highest sale volume: ')
                df = query_crm_top10(main_db,startdate,stopdate)
                print(df)
                print()

                print(f'top 10 province with highest sale volume: ')
                df = query_crm_top_province(main_db,startdate,stopdate)
                print(df)
                print()

                print(f'number of new and old buyer: ')
                df = query_crm_old(main_db,startdate,stopdate)
                print(df)
                print()

                while True:
                    user_input = input (f'Would you to export data? (Y/N): ').lower()
                    if user_input in ['y','n']:
                        break
                    else:
                        continue

                if user_input == 'y':
                    export_crm_top10(main_db,startdate,stopdate)
                    export_crm_top_province(main_db,startdate,stopdate)
                    export_crm_old(main_db,startdate,stopdate)


    ###############

    #query
        elif report_menu == '4':
             #query
    
            os.system('clear') # 'clear' on mac, for windows 'cls'
            print(f'Menu 4: Raw data')

    ###
            print('Which table you would like to see')
            while True:
                while True:
                    print('Report menu: \n 1. Transaction table \n 2. Customer information \n 3. product and stock \n 4. exit')
                    export_menu = input('Please enter menu number: ')
                    if export_menu in ['1','2','3','4']:
                        break 
                    else:
                        print('Wrong menu number.')
                        print('Please select again from menu 1-4 as follow:')
                        continue
                print()
                
                if export_menu == '1':
                    os.system('clear') # 'clear' on mac, for windows 'cls'
                    print(f'Menu 1: Main table')

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

                    if startdate > stopdate:
                        startdate , stopdate = stopdate , startdate
                        print(f'Since startdate greater than stopdate, we interchange its value.')
                        print(f'> new start date: {startdate}')
                        print(f'> new stop date: {stopdate}')
                        print()
            
                    df = existdf(main_db,startdate,stopdate=None)
                    if len(df) == 0:
                        print('No data in given date selection')
                    else:               
                        print(f'list of transaction: ')
                        df = query_rawdata_main(main_db,startdate,stopdate)
                        print(df)
                        print()

                        while True:
                            user_input = input (f'Would you to export data? (Y/N): ').lower()
                            if user_input in ['y','n']:
                                break
                            else:
                                continue

                        if user_input == 'y':
                            export_rawdata_main(main_db,startdate,stopdate)

###########################################
        
                elif export_menu == '2':
                    os.system('clear') # 'clear' on mac, for windows 'cls'
                    print(f'Menu 2: Customer information')

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

                    if startdate > stopdate:
                        startdate , stopdate = stopdate , startdate
                        print(f'Since startdate greater than stopdate, we interchange its value.')
                        print(f'> new start date: {startdate}')
                        print(f'> new stop date: {stopdate}')
                        print()
                    df = existdf(main_db,startdate,stopdate=None)
                    if len(df) == 0:
                        print('No data in given date selection')
                    else:
                        print(f'list of customer: ')
                        df = query_rawdata_cus(main_db,startdate,stopdate)
                        print(df)
                        print()

                        print(f'list of old customer: ')
                        df = query_rawdata_oldcus(main_db,startdate,stopdate)
                        print(df)
                        print()

                        print(f'list of new customer: ')
                        df = query_rawdata_newcus(main_db,startdate,stopdate)
                        print(df)
                        print()
                        
                        while True:
                            user_input = input (f'Would you to export data? (Y/N): ').lower()
                            if user_input in ['y','n']:
                                break
                            else:
                                continue

                        if user_input == 'y':             
                            export_rawdata_cus(main_db,startdate,stopdate)
                            export_rawdata_oldcus(main_db,startdate,stopdate)
                            export_rawdata_newcus(main_db,startdate,stopdate)
                    
                
###########################################
                elif export_menu == '3':
                    os.system('clear') # 'clear' on mac, for windows 'cls'
                    print(f'Menu 3: Product and inventory')

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

                    if startdate > stopdate:
                        startdate , stopdate = stopdate , startdate
                        print(f'Since startdate greater than stopdate, we interchange its value.')
                        print(f'> new start date: {startdate}')
                        print(f'> new stop date: {stopdate}')
                        print()
                    
                    df = existdf(main_db,startdate,stopdate=None)
                    if len(df) == 0:
                        print('No data in given date selection')
                    else:                    
                        print(f'list of Product and Inventory: ')
                        df = query_rawdata_product(main_db,startdate,stopdate)
                        print(df)
                        print()

                        while True:
                            user_input = input (f'Would you to export data? (Y/N): ').lower()
                            if user_input in ['y','n']:
                                break
                            else:
                                continue

                        if user_input == 'y':             
                            export_rawdata_product(main_db,startdate,stopdate)
                
                if export_menu == '4':
                    print(f'Back to main menu')
                    break
                else:
                    while True:
                        loop_to_main = input("Would you like to see another table? (Y/N): ").lower()
                        if loop_to_main in ['y','n']:
                            break
                        else:
                            continue
                    if loop_to_main == 'y':
                        continue
                    elif loop_to_main == 'n':
                        print(f'Back to report menu')
                        break

    ###############
        if report_menu == '5':
            print(f'Back to main menu')
            break
        else:
            while True:
                loop_to_main = input("Would you like to see another report? (Y/N): ").lower()
                if loop_to_main in ['y','n']:
                    break
                else:
                    continue
            if loop_to_main == 'y':
                continue
            elif loop_to_main == 'n':
                print(f'Back to main menu')
                break

report()



