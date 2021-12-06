from clickhouse_driver import dbapi
from config import CLICKHOUSE_USER, CLICKHOUSE_PWD, CLICKHOUSE_HOST, CLICKHOUSE_PORT
from config import DATABASE
from dbutils.pooled_db import PooledDB


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

total = { # 这个total计算的是所有au的整体数据，与字段约定不一样
    "dynamicCount": total_dynamicCount,
    "replyCount": total_replyCount,
    "total_charCount": total_charCount,
    # "danmuCount": total_danmuCount  # 待实现
}


def get_personal_data(mid):
    data = {
        "total": get_total(mid),
        "first_send": get_first(mid),  # 待更新
        "max_like": get_max_like(mid),
        "max_used": get_max_used(mid),
        "max_send_one_day": get_send_one_day(mid),  # 已更新
    }
    return data


def get_total(mid):
    # 先读取comment_rank表的内容
    table = "comment_rank"
    elements = "total_reply_num, total_dynamic_num, rank"
    ele_num = 3
    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans1 = query_one(sql, ele_num)

    # 再读取comment_member_rank表的内容
    table = "comment_member_rank"
    elements = "member, total, rank"
    ele_num = 3
    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans2 = query_one(sql, ele_num)
    return {
        "dynamicNumber": ans1[1],
        "sendNumber": ans1[0],
        "rank": ans1[2],
        "maxDynamicOwner": ans2[0],
        "maxSendNumber": ans2[1],
        "maxOwnerRank": ans2[2]
    }


def get_first(mid):
    table = "first"
    elements = "first_reply_time, content, dynamic_id"
    ele_num = 3

    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans = query_one(sql, ele_num)
    return {
        "time": ans[0],
        "content": ans[1],
        "dynamicOwner": ans[2]  # 这里的dynamic_id与dynamicOwner并无对应关系
    }


def get_send_one_day(mid):
    # 先读取comment_date表的内容
    table = "comment_date"
    elements = "date, content, max_reply_num"
    ele_num = 3
    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans1 = query_one(sql, ele_num)

    # 再读取comment_hour表的内容
    table = "comment_hour"
    elements = "reply_hour, reply_num"
    ele_num = 2
    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans2 = query_one(sql, ele_num)
    return {
        "time": ans1[0],
        "content": ans1[1],
        "maxSendTime": ans1[2],
        "timeRange": ans2[0],
        "sendNum": ans2[1]
    }


def get_max_like(mid):
    table = "max_like"
    elements = "content, max_likes, rank"  # 疑似缺少统计了评论时间和所属成员姓名
    ele_num = 3

    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans = query_one(sql, ele_num)
    return {
        # "time": ans[],  # 缺少评论时间的字段
        # "dynamicOwner": ans[],  # 缺少所属成员姓名的字段
        "rank": ans[2],
        "content": ans[0],
        "likeNum": ans[1]
    }


def get_max_used(mid):
    table = "reference"
    elements = "content, reference_count"  # 疑似缺少字段
    ele_num = 2

    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid}"""
    ans = query_one(sql, ele_num)
    return {
        # "time": ans[],  # 缺少评论时间的字段
        # "dynamicOwner": ans[],  # 缺少所属成员姓名的字段
        # "rank": ans[2],
        "content": ans[0],
        "usedNum": ans[1]
    }