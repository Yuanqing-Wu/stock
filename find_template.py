import tushare as ts
import numpy as np
import pandas as pd
import time

ts.set_token('d689cb3c1d8c8a618e49ca0bb64f4d6de2f70e28ab5f76a867b31ac7')
pro = ts.pro_api()

stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')
# print(stock_list['industry'].value_counts())
stock_list = stock_list[stock_list['industry'] == '电气设备']
# print(stock_list)
stock_list = stock_list[~stock_list['ts_code'].str.contains('BJ')]
stock_list = stock_list[~stock_list['ts_code'].str.startswith('3')]
stock_list = stock_list[~stock_list['ts_code'].str.startswith('688')]
stock_list = stock_list[~stock_list['ts_code'].str.startswith('689')]
stock_list = stock_list[~stock_list['name'].str.contains('ST')]
# print(stock_list)

num = 0
pe_avg = 0
for index, stock in stock_list.iterrows():
    ts_code = stock['ts_code']
    name = stock['name']
    daily_basic = pro.daily_basic(ts_code=ts_code, trade_date='20240409', fields='trade_date,close,turnover_rate,volume_ratio,pe,pb')
    if daily_basic['pe'][0] != None:
        if daily_basic['pe'][0] < 20:
            # print(name)
            # print(daily_basic)
            pe_avg = pe_avg + daily_basic['pe'][0]
            num = num + 1
            k_line = pro.daily(ts_code=ts_code, start_date='20200409', end_date='20240409')
            max_p = k_line['close'].max()
            min_p = k_line['close'].min()
            cur_week_p = k_line.head(7)
            cur_p = cur_week_p.loc[0, 'close']
            
            if (cur_p - min_p)/(max_p - cur_p) < 0.2:
                #print(cur_week_p.loc[6, 'close'])
                last_week_p = cur_week_p.loc[6, 'close']
                if (cur_p - last_week_p) / last_week_p > 0.05 and (cur_p - last_week_p) / last_week_p < 0.1:
                    var = cur_week_p['close'].var() / cur_p / cur_p
                    print(name, cur_p, last_week_p, var)
            
    

# pe_avg = pe_avg / num
# print(num, pe_avg)
# df = pro.daily(ts_code='000001.SZ', start_date='20200409', end_date='20240409')


# print(df)