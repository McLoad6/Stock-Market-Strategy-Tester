

def candle_type(open, high, low, close):
    if high < open or high < close or low > open or low > close:
        return 'Wrong data!' 
    if open >= close:
        shup = high - open #shadow up part
        shdo = close - low #shadow down part
        body = open - close
        candle = high - low
        if body >= shup + shdo:
            return 'b'  #black candle
        else:
            if shup/candle <= 0.2:
                return 'bs' #black shadow or hanging man
            elif shdo/candle <= 0.2:
                return 'bh' #black hammer
            else:
                return 'bt' #black spinning tops or doji        
    else:
        shup = high - close 
        shdo = open - low 
        body = close - open
        if body >= shup + shdo:
            return 'w'  #white candle
        else:
            if shup/candle <= 0.2:
                return 'wh' #white hammer
            elif shdo/candle <= 0.2:
                return 'ws' #white shadow or hanging man
            else:
                return 'bt' #white spinning tops or doji    

def two_candle_relations(c1,c2): #candle1 = list(open,high,low,close)
    if c2[3] > c2[0]:
        if c1[3] >= c1[0]:
            if c2[3] >= c1[1]:
                return 'us' #up 'trend' strong
            else:
                return 'uw' #up weak
        else:
            if c2[3] >= c1[1]:
                return 'ul' #up light
            else:
                return 'un' #up neutral
    elif c1[3] == c1[0]:
        return 'un'
    else:
        if c1[3] <= c1[0]:
            if c2[3] <= c1[2]:
                return 'ds' #down strong
            else:
                return 'dw'
        else:
            if c2[3] <= c1[2]:
                return 'dl'
            else:
                return 'dn'

def trend_turning(list):
    c1 = list[0]
    c2 = list[1]
    c3 = list[2]
    c4 = list[3]
    c5 = list[4]
    c6 = list[5]
    trend1 = two_candle_relations(c1,c2)
    trend2 = two_candle_relations(c2,c3)
    if trend1[0] == trend2[0]:
        return 'nt'
    if trend1 == 'us' or trend1 == 'uw':
        if c2[1] >= c3[1]:
            if c3[3] < c2[2] or c4[3] < c2[2] or c5[3] < c2[2] or c6[3] < c2[2]:
                return 'td' #turning down
        else:
            if c4[3] < c3[2] or c5[3] < c3[2] or c6[3] < c3[2]:
                return 'td'
    elif trend1 == 'ds' or trend1 == 'dw':
        if c2[2] <= c3[2]:
            if c3[3] > c2[1] or c4[3] > c2[1] or c5[3] > c2[1] or c6[3] > c2[1]:
                return 'tu' #turning up
        else:
            if c4[3] > c3[1] or c5[3] > c3[1] or c6[3] > c3[1]:
                return 'tu' #turning up
    return 'nt' #no trend or no turning

def trend_searcher(list):
    i = 0
    trend_indexes = []
    for minute in list[1:]:
        trend = two_candle_relations(list[i],minute)
        if trend == 'us' or trend == 'uw' or trend == 'ds' or trend == 'dw':
            trend_indexes.append(i)
        i += 1
    return trend_indexes

def trend_searcher_double(list):
    i = 1
    trend_indexes = []
    for minute in list[2:]:
        trend1 = two_candle_relations(list[i-1],list[i])
        trend2  = two_candle_relations(list[i],minute)
        if trend1 == 'us' or trend1 == 'uw':
            if trend2 == 'us' or trend2 == 'uw':
                trend_indexes.append(i)
        elif  trend1 == 'ds' or trend1 == 'dw':
            if trend2 == 'ds' or trend2 == 'dw':
                trend_indexes.append(i)
        i += 1
    return trend_indexes

def exit_searcher(day, open, direction, target, stop): #day_list, minute list, 'u'/'d' target number, stop number 
    i = day[open][0]
    if direction == 'u':
        t = i + target
        s = i - stop
        for minute in day[open:]:
            if minute[1] >= t:
                return target -5 # GAP 5 point
            elif minute[2] <= s:
                return -stop -5
        return day[-1][3] - i
    elif direction == 'd':
        t = i -target
        s = i + stop
        for minute in day[open:]:
            if minute[2] <= t:
                return target -5 
            elif minute[1] >= s:
                return -stop -5
        return i - day[-1][3]
    
def open_searcher(day, tt_index): #from turning point index calculates the open minute index and direction
    six_min_list = day[tt_index : tt_index+6]
    direction = trend_turning(six_min_list)
    if direction[1] == 'u': #turning up = previous trend was down (bear)
        if six_min_list[1][2] <= six_min_list[2][2]:
            target_close = six_min_list[1][1]
            i = 2
            for minute in six_min_list[2:]:
                if minute[3] > target_close:
                    return ['u', i+tt_index]
                else:
                    i += 1
        else:
            target_close = six_min_list[2][1]
            i = 3
            for minute in six_min_list[3:]:
                if minute[3] > target_close:
                    return ['u', i+tt_index]
                else:
                    i += 1
    elif direction[1] == 'd':
        if six_min_list[1][1] >= six_min_list[2][1]:
            target_close = six_min_list[1][2]
            i = 2
            for minute in six_min_list[2:]:
                if minute[3] < target_close:
                    return ['d', i + tt_index]
                else:
                    i += 1
        else:
            target_close = six_min_list[2][2]
            i = 3
            for minute in six_min_list[3:]:
                if minute[3] < target_close:
                    return ['d', i + tt_index]
                else:
                    i += 1


