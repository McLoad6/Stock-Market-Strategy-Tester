import csv
import sys
from datetime import datetime, timedelta

def get_dict_from_csv(file_name):      #file reader for uncleaned data
    dict = {}
    try: 
        file = open(file_name, encoding="UTF-8")
        try:
            file_content = csv.reader(file, delimiter=';')
            next(file_content, None)
            for row in file_content:        #Format changed for YYYYMMDDHHMM , Open, High, Low, Close, Volume
                date = datetime.strptime(row[0],'%Y.%m.%d')
                time = datetime.strptime(row[1],'%H:%M').time()
                key = datetime.combine(date,time)
                key = format(key, '%Y%m%d%H%M')
                key1 = int(key)
                modified_row = [row[3].replace(',','.'), row[4].replace(',','.'), row[5].replace(',','.'), row[6].replace(',','.'), row[7]]
                dict[key1] = modified_row
        finally:
            file.close()
    except OSError:
        sys.exit('File not found!')
    else:
        return dict

def border_keys(dict):
    key_list = list(dict.keys())
    low_key = key_list[0]
    high_key = key_list[0]
    for key in key_list:
        if key < low_key:
            low_key = key
        if key > high_key:
            high_key = key
    return (low_key,high_key)

def time_occurrence(dict):
    key_list = list(dict.keys())
    time_dict = {}
    for key in key_list:
        key1 = str(key)
        hour = key1[-4:]
        if hour in time_dict:
            time_dict[hour] +=1
        else:
            time_dict[hour] = 1 
    return time_dict

def day_occurrence(dict):
    key_list = list(dict.keys())
    time_dict = {}
    for key in key_list:
        key1 = str(key)
        day = key1[:8]
        if day in time_dict:
            time_dict[day] +=1
        else:
            time_dict[day] = 1 
    return time_dict

def filling_missing_rows(dict):
    # Working with the days which has more than 800 rows
    # Filling the empty road with simulated data's Open = previous Close and Close = next Open 
    date_dict = day_occurrence(dict)
    start = datetime.strptime('08:00:00', '%H:%M:%S')
    end = datetime.strptime('21:59:00', '%H:%M:%S')
    minutes = []        #minutes between 8:00 - 22:00
    while start <= end:
        minute = str(start)
        minutes.append(minute[-8:-6] + minute[-5:-3])
        start = start + timedelta(minutes=1)
    minute_list = []        # list for all YYYYMMDDHHMM which will be used for the new dictionary
    filled_dict = {}
    for date in date_dict:
        if date_dict[date] > 800:
            for time in minutes:
                ymdhm = str(date) + str(time)
                number = int(ymdhm)
                minute_list.append(number)
    missing_minutes = []
    for minute in minute_list:
        if minute in dict:
            filled_dict[minute] = dict[minute]
            open = dict[minute][3]
        else:
            missing_minutes.append(minute) 
            filled_dict[minute] = [open, 0, 0, 0, 0] #Open, High, Low, Close, Volume
    for minute in minute_list[::-1]:
        if minute in missing_minutes:
            filled_dict[minute] = [filled_dict[minute][0],filled_dict[minute][1],filled_dict[minute][2],close,0]
        close = filled_dict[minute][0]
    for minute in minute_list:
        if minute in missing_minutes:
            open = filled_dict[minute][3]
            close = filled_dict[minute][0]
            if open >= close:
                min = close
                max = open
            else:
                min = open
                max = close
            filled_dict[minute] = [filled_dict[minute][0], max, min, filled_dict[minute][3], 0]
    return filled_dict


def write_dict_to_csv(file_name, dict_name):   #file writer
    file = open(file_name, 'w', newline='')
    writer = csv.writer(file)
    for key,value in dict_name.items():
        row = str(key) + ';' + str(value[0]) + ';' + str(value[1]) + ';' + str(value[2]) + ';' + str(value[3]) + ';' + str(value[4])
        writer.writerow([row])
    file.close()   
    return

def get_days_from_csv(file_name):      #file reader for cleaned file
    daily_list = []
    file = open(file_name, encoding="UTF-8")
    file_content = csv.reader(file, delimiter=';')
    day = []
    date1 = 0
    for row in file_content:        #Format changed for YYYYMMDDHHMM , Open, High, Low, Close, Volume
        content = list(map(float, row[1:5]))
        test = str(row[0])
        test1 = test[0:8]
        if date1 == test1:
            day.append(content)
        else:
            date = str(row[0])
            date1 = date[0:8]
            daily_list.append(day)
            day = []
            day.append(content)
    file.close()
    del daily_list[0]
    return daily_list    
