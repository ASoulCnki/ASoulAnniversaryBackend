from clickhouse_driver import Client, dbapi
from config import CLICKHOUSE_USER, CLICKHOUSE_PWD, CLICKHOUSE_HOST, CLICKHOUSE_PORT
from config import DATABASE
from dbutils.pooled_db import PooledDB

# ch_client = Client(
#     host=CLICKHOUSE_HOST,
#     port=CLICKHOUSE_PORT,
#     user=CLICKHOUSE_USER,
#     password=CLICKHOUSE_PWD
# )

# 使用clickhouse连接池，blocking=True设置为阻塞模式
ch_client_pool = PooledDB(
    creator=dbapi,
    blocking=True,
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT,
    user=CLICKHOUSE_USER,
    password=CLICKHOUSE_PWD
)

sql_total_dynamicCount = f"""select count(*) as total from {DATABASE}.user_dynamic;"""
sql_total_replyCount = f"""select count(rpid) as total from {DATABASE}.reply;"""
sql_total_charCount = f"""select sum(lengthUTF8(replaceRegexpAll(content, '\[\\S*]', '*'))) as total from { DATABASE }.reply;"""
sql_total_danmuCount = f""""""


# def query_one(sql, num):
#     try:
#         ch_client = ch_client_pool.connection()
#         cur = ch_client.cursor()
#         cur.execute(sql)
#         res = cur.fetchone()
#         cur.close()
#         ch_client.close()
#         if res is not None:
#             return res
#         else:
#             return [None] * num
#     except Exception as e:
#         return [None] * num


# 没有使用try catch块，编写代码时会跳过一些程序中的错误，不利于排查bug
def query_one(sql, num):
    ch_client = ch_client_pool.connection()
    cur = ch_client.cursor()
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    ch_client.close()
    if res is not None:
        return res
    else:
        return [None] * num


total_dynamicCount = query_one(sql_total_dynamicCount, 1)[0]
total_replyCount = query_one(sql_total_replyCount, 1)[0]
total_charCount = query_one(sql_total_charCount, 1)[0]
# total_danmuCount = query_one(sql_total_danmuCount, 1)[0]

total = {
    "dynamicCount": total_dynamicCount,
    "replyCount": total_replyCount,
    "total_charCount": total_charCount,
    # "danmuCount": total_danmuCount  # 待实现
}


def get_personal_data(mid):
    data = {
        "total": total,
        "first": get_first(mid),
        "comment_rank": get_comment_rank(mid),
        "comment_member_rank": get_comment_member_rank(mid),
        "comment_date": get_comment_date(mid)
    }
    return data


def get_first(mid):
    table = "first"
    elements = "first_reply_time, content, dynamic_id"
    ele_num = 3

    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans = query_one(sql, ele_num)
    return {
        "first_replytime": ans[0],
        "first_content": ans[1],
        "first_dynamicid": ans[2]
    }


def get_comment_rank(mid):
    table = "comment_rank"
    elements = "total_reply_num, total_dynamic_num, rank"
    ele_num = 3

    sql = f"""select { elements } from { DATABASE }.{ table } where mid ={ mid }"""
    ans = query_one(sql, ele_num)
    return {
        "total_reply_num": ans[0],
        "total_dynamic_num": ans[1],
        "rank": ans[2]
    }


def get_comment_member_rank(mid):
    table = "comment_member_rank"
    elements = "uid, member, total, rank"
    ele_num = 4

    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans = query_one(sql, ele_num)
    return {
        "uid": ans[0],
        "member": ans[1],
        "total": ans[2],
        "rank": ans[3]
    }


def get_comment_date(mid):
    table = "comment_date"
    elements = "oid, date, content, max_reply_num"
    ele_num = 4

    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans = query_one(sql, ele_num)
    return {
        "oid": ans[0],
        "date": ans[1],
        "content": ans[2],
        "max_reply_num": ans[3]
    }