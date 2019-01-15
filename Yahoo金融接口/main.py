import tushare as ts
#博时黄金 159937
#中证500 510500
#沪深300 510300

df = ts.get_k_data('510500',start='2018-01-01',end='2018-03-15')
print(df)

# #沪深300成份及权重
# # code :股票代码
# # name :股票名称
# # date :日期
# # weight:权重

# df = ts.get_hs300s()
# print(df)

# #上证50成份股
# # code：股票代码
# # name：股票名称

# df = ts.get_sz50s()
# print(df)

# #中证500成份股
# # code：股票代码
# # name：股票名称
# df = ts.get_zz500s()
# print(df)

# df = ts.get_deposit_rate()
# print(df)

# df = ts.get_gdp_year()
# print(df)