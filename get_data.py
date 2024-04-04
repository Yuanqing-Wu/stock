import tushare as ts
import numpy as np
import pandas as pd

ts.set_token('d689cb3c1d8c8a618e49ca0bb64f4d6de2f70e28ab5f76a867b31ac7')
pro = ts.pro_api()

stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')
trade_cal = pro.trade_cal(exchange='', start_date='20230401', end_date='20240403')
#print(trade_cal)
stock_list.to_csv("./data/stock_list.csv")

stock_list = stock_list[~stock_list['ts_code'].str.contains('BJ')]
stock_list = stock_list[~stock_list['name'].str.contains('ST')]

#stock_list.to_csv("./data/pe_20240403.csv")

for index, stock in stock_list.iterrows():
    ts_code = stock['ts_code']
    name  = stock['name']

    stock_data = pd.DataFrame(columns=['trade_date', 'close', 'turnover_rate', 'volume_ratio', 'pe', 'pb'])
    for _, cal in trade_cal.iloc[::-1].iterrows():
        if cal['is_open'] == 1:
            daily_basic = pro.daily_basic(ts_code=ts_code, trade_date=cal['cal_date'], fields='trade_date,close,turnover_rate,volume_ratio,pe,pb')
            stock_data = pd.concat([stock_data, daily_basic])
            print(cal['cal_date'])
    stock_data.to_csv("./data/" + name + '.csv')
    #break