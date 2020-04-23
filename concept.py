import time

import redis as redis
import tushare as ts

ts.set_token('724d638ffc9ca97a8b631f10e607d5d37c7f6d1699158ffa4e75579c')
pro = ts.pro_api()
pool = redis.ConnectionPool(host='49.232.82.238', port=26379, password='Abc1234%', decode_responses=True)
r = redis.Redis(connection_pool=pool)
# 个股概念，redis set，stock->set
STOCK_CONCEPT_DETAIL = "Stock:Concept:Detail:{}"
# 个股详情，redis hash，stock->hash
STOCK_BASIC_SYMBOL = "Stock:Basic:Symble"

# 获取股票基础数据
stock_basic = pro.query('stock_basic', exchange='', list_status='L',
                        fields='ts_code,symbol,name,area,industry,list_date')
i = 0
count = 1
for index, row in stock_basic.iterrows():
    ts_code = row["ts_code"]
    r.hset(STOCK_BASIC_SYMBOL, ts_code.split('.')[0], ts_code)
    i = i + 1
    if i > 199:
        print(i * count)
        i = 0
        count = count + 1
        time.sleep(60)
    concept = pro.concept_detail(ts_code=row["ts_code"])
    concept_list = concept['concept_name'].values
    with r.pipeline(transaction=False) as p:
        for cept in concept_list:
            p.sadd(STOCK_CONCEPT_DETAIL.format(row['ts_code']), cept)
        p.execute()
