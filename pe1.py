import tushare as ts  
  
# 初始化Tushare，设置token  
token = 'd689cb3c1d8c8a618e49ca0bb64f4d6de2f70e28ab5f76a867b31ac7'  # 请替换为您的Tushare token  
ts.set_token(token)  
pro = ts.pro_api()  
  
years = ['2021', '2022', '2023', '2024']  
quarter = '2024Q1'  
  

def check_stock(ts_code, years, quarter):  

    df_net_profit0 = pro.income(ts_code=ts_code, period=f'{years[0]}1231', fields='ts_code,end_date,n_income_attr_p')
    df_net_profit1 = pro.income(ts_code=ts_code, period=f'{years[1]}1231', fields='ts_code,end_date,n_income_attr_p')
    df_net_profit2 = pro.income(ts_code=ts_code, period=f'{years[2]}1231', fields='ts_code,end_date,n_income_attr_p')

    print(df_net_profit0)
    print(df_net_profit1)
    print(df_net_profit2)
      
    if len(df_net_profit0) > 0 and len(df_net_profit1) > 0 and len(df_net_profit2) > 0:
        r0 = (df_net_profit1.loc[0,'n_income_attr_p'] - df_net_profit0.loc[0,'n_income_attr_p']) / df_net_profit0.loc[0,'n_income_attr_p']
        r1 = (df_net_profit2.loc[0,'n_income_attr_p'] - df_net_profit1.loc[0,'n_income_attr_p']) / df_net_profit1.loc[0,'n_income_attr_p']
        if r0 > 0.1 and r1 > 0.1:
            
            df_net_profit3 = pro.income(ts_code=ts_code, period=f'{years[3]}0331', fields='ts_code,end_date,n_income_attr_p')
            df_net_profit4 = pro.income(ts_code=ts_code, period=f'{years[2]}0331', fields='ts_code,end_date,n_income_attr_p')
            print(df_net_profit4)
            print(df_net_profit3)
            r2 = (df_net_profit3.loc[0,'n_income_attr_p'] - df_net_profit4.loc[0,'n_income_attr_p']) / df_net_profit4.loc[0,'n_income_attr_p']
            if r2 > 0.1:  
                df_valuation = pro.daily_basic(ts_code=ts_code, trade_date='20240510', fields='ts_code,pe')
                if df_valuation.loc[0, 'pe'] != None and df_valuation.loc[0, 'pe'] < 20:
                    print("OK", r0, r1, r2, df_valuation.loc[0, 'pe'])
                    return True  
    return False  

stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')

selected_stocks = []  
for index, stock in stock_list.iterrows():
    ts_code = stock['ts_code']
    print (stock['ts_code'], stock['name'], stock['industry'])
    if check_stock(ts_code, years, quarter):  
        selected_stocks.append(ts_code)

print("Finish")
print(selected_stocks)