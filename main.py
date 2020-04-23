import datetime

import numpy as np
import pandas as pd
import redis as redis
import tushare as ts

ts.set_token('724d638ffc9ca97a8b631f10e607d5d37c7f6d1699158ffa4e75579c')
pro = ts.pro_api()

pool = redis.ConnectionPool(host='49.232.82.238', port=26379, password='Abc1234%', decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 获取股票基础数据
stock_basic = pro.query('stock_basic', exchange='', list_status='L',
                        fields='ts_code,symbol,name,area,industry,list_date')

# 获前30天内的交易日
today = (datetime.date.today() - datetime.timedelta(0)).strftime("%Y%m%d")
startday = (datetime.date.today() - datetime.timedelta(30)).strftime("%Y%m%d")
trade_date = pro.trade_cal(exchange='', start_date=startday, end_date=today, is_open='1').sort_values('cal_date',
                                                                                                      ascending=False)
print(today, startday)
# print(trade_date.iloc[0])

num, _ = trade_date.shape

# 每日涨停，redis hash，date->{stock:value}
STOCK_LIMIT_UP = "Stock:Limit:Up:{}"
r.hset("hash1", "k2", "v2")

# 获取某日涨停股票，并指定字段输出
limit_list = pro.limit_list(start_date=startday, end_date=today, limit_type='U')

cur_date = trade_date.iloc[0]['cal_date']
cur_limit = limit_list[limit_list['trade_date'] == cur_date]

cur_merged = pd.merge(cur_limit, stock_basic)

# 计算连板数
cur_merged['limit_num'] = 1
cur_codes = cur_limit['ts_code'].values
print(cur_codes)
for i in range(1, num):
    pre_date = trade_date.iloc[i]['cal_date']
    pre_limit = limit_list[limit_list['trade_date'] == pre_date]
    pre_codes = pre_limit['ts_code'].values

    cur_codes = np.intersect1d(cur_codes, pre_codes)
    if cur_codes.size == 0:
        break

    for code in cur_codes:
        cur_merged.loc[cur_merged['ts_code'] == code, 'limit_num'] += 1

final_data = cur_merged[['ts_code', 'name', 'trade_date', 'area', 'industry', 'limit_num']].sort_values('limit_num',
                                                                                                        ascending=False)

# 追加概念
final_data['concept'] = ''
for code in final_data['ts_code'].values:
    concept = pro.concept_detail(ts_code=code)
    # print(code)
    # print(concept['concept_name'].values)
    concept_str = '/'.join(cept for cept in concept['concept_name'].values)
    # print(concept_str)
    if len(concept_str) == 0:
        concept_str = '暂无概念数据'
    final_data.loc[final_data['ts_code'] == code, 'concept'] += concept_str

final_data.to_csv('replay_' + today + '.csv', encoding='gbk', index=False)


