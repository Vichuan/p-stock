# -*- coding: UTF-8 -*-

import tushare as ts

pro = ts.pro_api('724d638ffc9ca97a8b631f10e607d5d37c7f6d1699158ffa4e75579c')

# 获取某日涨停股票，并指定字段输出
df = pro.limit_list(trade_date='20200416', limit_type='U')

print(df)
