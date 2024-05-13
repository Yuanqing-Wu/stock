import tushare as ts
import numpy as np
import pandas as pd
ts.set_token('d689cb3c1d8c8a618e49ca0bb64f4d6de2f70e28ab5f76a867b31ac7')
pro = ts.pro_api()

df = pro.query('daily_basic', ts_code='', trade_date='20240425',fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,total_mv')
df = df[df['pe'] != None]
df = df[df['pe'] < 20]
df = df[df['close'] > 8]
df = df[df['total_mv'] > 2000000]
df = df[~df['ts_code'].str.contains('BJ')]
df = df[~df['ts_code'].str.startswith('3')]
df = df[~df['ts_code'].str.startswith('688')]
df = df[~df['ts_code'].str.startswith('689')]
# df = df[~df['name'].str.contains('ST')]

df.to_csv("./data/pe.csv")

