import tushare as ts
import numpy as np

ts.set_token('d689cb3c1d8c8a618e49ca0bb64f4d6de2f70e28ab5f76a867b31ac7')
pro = ts.pro_api()
df = pro.daily_basic(ts_code='', trade_date='20240403', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
df.to_csv("./data/pe_20240403.csv")