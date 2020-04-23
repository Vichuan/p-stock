import redis as redis

pool = redis.ConnectionPool(host='49.232.82.238', port=26379, password='Abc1234%', decode_responses=True)
r = redis.Redis(connection_pool=pool)
begin_pos = 0
while True:
    result = r.scan(cursor=begin_pos)
    return_pos, datalist = result
    if len(datalist) > 0:
        for key in datalist:
            if key.startswith("Stock:Limit:"):
                print(key)
                r.delete(key)
    if return_pos == 0:
        break
    begin_pos = return_pos
