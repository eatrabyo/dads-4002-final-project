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
print(startdate)
print(stopdate)