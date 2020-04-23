import datetime
import logging

import pandas as pd
import redis as redis
import tushare as ts
from pandas.io import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(filename)s:%(lineno)d][%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

# 每日涨停，redis hash，date->{stock:value}
STOCK_LIMIT_UP = "Stock:Limit:Up:{}"
# 每日跌停，redis hash，date->{stock:value}
STOCK_LIMIT_DOWN = "Stock:Limit:Down:{}"
# 个股概念，redis list，stock->list
STOCK_CONCEPT_DETAIL = "Stock:Concept:Detail:{}"

ts.set_token('724d638ffc9ca97a8b631f10e607d5d37c7f6d1699158ffa4e75579c')
pro = ts.pro_api()

pool = redis.ConnectionPool(host='49.232.82.238', port=26379, password='Abc1234%', decode_responses=True)
r = redis.Redis(connection_pool=pool)


class Stock:
    def __init__(self):
        self.trade_date = None
        self.ts_code = None
        self.name = None
        self.close = None
        self.pct_chg = None
        self.amp = None
        self.fc_ratio = None
        self.fl_ratio = None
        self.fd_amount = None
        self.first_time = None
        self.last_time = None
        self.open_times = None
        self.strth = None
        self.limit = None
        self.limit_num = None
        self.concept = None
        self.symbol = None
        self.area = None
        self.industry = None
        self.list_date = None


def collect_limit(start_date, end_date):
    log.info("collect start, start date: {}, end date: {}".format(start_date, end_date))
    # 获取股票基础数据
    stock_basic = pro.query('stock_basic', exchange='', list_status='L',
                            fields='ts_code, symbol, area, industry, list_date')
    calendar_list = pro.query('trade_cal', exchange="SSE", start_date=start_date, end_date=end_date, is_open="1",
                              fields='exchange, cal_date, is_open, pretrade_date')
    count = 0
    for index, cal_row in calendar_list.iterrows():
        # 获取某日涨停股票
        limit_list = pro.limit_list(trade_date=cal_row['cal_date'], limit_type='U')
        limit_list_mg = pd.merge(limit_list, stock_basic, how='left', on='ts_code')
        limit_list_mg['limit_num'] = 1
        for index, row in limit_list_mg.iterrows():
            # 30天前日期
            day30 = (datetime.date.today() - datetime.timedelta(30)).strftime("%Y%m%d")
            if 'ST' in row['name'] or row['list_date'] > day30:
                continue
            limit_stock = r.hget(STOCK_LIMIT_UP.format(cal_row['pretrade_date']), row['ts_code'])
            if limit_stock is not None:
                stock = Stock()
                stock.__dict__ = json.loads(limit_stock)
                row['limit_num'] = stock.limit_num + 1
            r.hset(STOCK_LIMIT_UP.format(row['trade_date']), row['ts_code'],
                   row.to_json(orient='index', force_ascii=False))

        # 获取某日跌停股票
        limit_list = pro.limit_list(trade_date=cal_row['cal_date'], limit_type='D')
        limit_list_mg = pd.merge(limit_list, stock_basic, how='left', on='ts_code')
        for index, row in limit_list_mg.iterrows():
            if 'ST' in row['name']:
                continue
            r.hset(STOCK_LIMIT_DOWN.format(row['trade_date']), row['ts_code'],
                   row.to_json(orient='index', force_ascii=False))
    log.info("collect end")


if __name__ == '__main__':
    end_day = (datetime.date.today() - datetime.timedelta(0)).strftime("%Y%m%d")
    start_day = (datetime.date.today() - datetime.timedelta(3)).strftime("%Y%m%d")
    collect_limit(start_day, end_day)
