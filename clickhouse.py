from clickhouse_driver import Client
from config import CLICKHOUSE_USER, CLICKHOUSE_PWD, CLICKHOUSE_HOST, CLICKHOUSE_PORT
from config import DATABASE

ch_client = Client(
    host=CLICKHOUSE_HOST, 
    port=CLICKHOUSE_PORT, 
    user=CLICKHOUSE_USER, 
    password=CLICKHOUSE_PWD)

sql_total_dynamicCount = f"""select count(*) as total from {DATABASE}.user_dynamic;"""
sql_total_replyCount = f"""select count(rpid) as total from {DATABASE}.reply;"""
sql_total_danmuCount = f""""""

def query_one(sql):
    try:
        res = ch_client.execute(sql)
        return res[0]
    except Exception as e:
        return (None, )

total_dynamicCount = query_one(sql_total_dynamicCount)[0]
total_replyCount = query_one(sql_total_replyCount)[0]
total_danmuCount = query_one(sql_total_danmuCount)[0]

total = {
    "dynamicCount":total_dynamicCount,
    "replyCount":total_replyCount,
    "danmuCount":total_danmuCount
}

def get_personal_data(mid):
    data = {
        "total":total,
    }
    return data