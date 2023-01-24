import chart_definitions
import file_handler

daily_list = file_handler.get_days_from_csv(r'C:\Users\McLoad\Desktop\Python2\strings\Stock_strategy\cleaned.csv')

def trend_turning_list(list,day):
    tt_list = []
    for i in list:
        if i >= 833:
            break
        test_list = day[i:i+6]      # i and i+1 trend, i+1 or i+2 top/bottom, between i+2 i+5 direction is changing
        tt = chart_definitions.trend_turning(test_list)
        if tt == 'tu' or tt == 'td':
            tt_list.append(i)
    return tt_list

def fourty_ten_morning_strategy(day,tt_list): # Cheking all morning tt index < 120 with 40 point target and 10 point fix stop loss 
    results = []
    for test in tt_list:
        if test > 120:
            break
        else:
            info = chart_definitions.open_searcher(day,test)
            open = info[1]
            result = chart_definitions.exit_searcher(day,open,info[0],40,10)
            results.append([test,result])
    return results

def strategy(daily_list):
    day_number = 1
    sum = 0
    result_list = []
    for day in daily_list:
        one_direction = chart_definitions.trend_searcher_double(day)
        tt_list = trend_turning_list(one_direction, day)
        results = fourty_ten_morning_strategy(day , tt_list)
        result = 0
        for [i,res] in results:
            result += res
        result_list.append([day_number,result])
        day_number += 1
        sum += result
    return [result_list, sum]

print(strategy(daily_list))

