from functools import wraps

import MySQLdb
from config import DATABASE_USER, DATABASE_PWD, DATABASE_HOST, DATABASE_PORT
from config import DATABASE
from dbutils.pooled_db import PooledDB


# 使用连接池，blocking=True用处存疑
connection_pool = PooledDB(
    creator=MySQLdb,
    # blocking=True,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    user=DATABASE_USER,
    password=DATABASE_PWD
)

# 没有使用try catch块，编写代码时会跳过一些程序中的错误，不利于排查bug
def query_one(sql, num):
    ch_client = connection_pool.connection()
    cur = ch_client.cursor()
    cur.execute(sql)
    res = cur.fetchone()
    cur.close()
    ch_client.close()
    if res is not None:
        return res
    else:
        return [None] * num

def query_many(sql, num):
    ch_client = connection_pool.connection()
    cur = ch_client.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    ch_client.close()
    if res is not None:
        return res
    else:
        return [None] * num

def Fail2None(func):
    @wraps(func)
    def Fail2None(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return Fail2None

def query_data_by_mid(table, elements, ele_num, mid):
    sql = f"""select {elements} from {DATABASE}.{table} where mid ={mid};"""
    # print(sql)
    ans = query_one(sql, ele_num)
    return ans

# 获取字段all数据
sql_total_replyCount = f"""select count(rpid) as total from asoulcnki.reply;"""
sql_total_danmuCount = f"""select count(mid) as total from {DATABASE}.danmaku_total;"""
sql_total_dynamicCount = f"""select count(*) as total from asoulcnki.user_dynamic;"""
all_data = {
    "replyCount": query_one(sql_total_replyCount, 1)[0], 
    "danmuCount": query_one(sql_total_danmuCount, 1)[0], 
    "dynamicCount": query_one(sql_total_dynamicCount, 1)[0]
}

@Fail2None
def get_all():
    global all_data
    return all_data

@Fail2None
def get_reply_first(mid):
    # 获取字段reply_first数据
    table = "first"
    elements = "`first_reply_time`, `content`, `uid`"
    ele_num = 3
    ans = query_data_by_mid(table, elements, ele_num, mid)
    return {
        "time": ans[0],
        "content": ans[1],
        "uid": ans[2]
    }

@Fail2None
def get_reply_total(mid):
    # 获取字段reply_total数据
    global au_number
    table = "total"
    elements = "`total_dynamic_num`, `total_reply_num`, `rank`"
    ele_num = 3
    ans = query_data_by_mid(table, elements, ele_num, mid)
    return {
        "dynamicNumber": ans[0],
        "replyNumber": ans[1],
        "rank": ans[2]/au_number
    }

@Fail2None
def get_danmu_total(mid):
    # 获取字段danmu_total数据
    table = "danmaku_total"
    elements = "`simple_danmaku_num`, `uid`, `most_danmaku_sent`, `gift_num`, `gift_spent`, `sc_num`, `sc_spent`, `rank`"
    ele_num = 8
    ans = query_data_by_mid(table, elements, ele_num, mid)
    return {
      "danmuNumber": ans[0],
      "memberUid": ans[1],
      "memberDanmuNumber": ans[2],
      "giftNumber": ans[3],
      "giftCost": ans[4],
      "scNumber": ans[5],
      "scCost": ans[6],
      "rank": ans[7]/au_number
    }

@Fail2None
def get_reply_total_like(mid):
    # 获取字段reply_total_like数据
    global au_number
    table = "total_like"
    elements = "`total_likes`, `rank`"
    ele_num = 2
    ans = query_data_by_mid(table, elements, ele_num, mid)
    return {
        "likeNumber": ans[0],
        "rank": ans[1]/au_number
    }

@Fail2None
def get_reply_max_like(mid):
    # 获取字段reply_max_like数据
    global au_number
    table = "max_like"
    elements = "`ctime`, `content`, `uid`, `max_likes`, `rank`"
    ele_num = 5
    ans = query_data_by_mid(table, elements, ele_num, mid)
    return {
        "time": ans[0],
        "content": ans[1],
        "uid": ans[2],
        "likeNumber": ans[3],
        "rank": ans[4]/au_number
    }

@Fail2None
def get_reply_max_used(mid):
    # 获取字段reply_max_used数据
    global au_number
    table = "max_used"
    elements = "`ctime`, `content`, `uid`, `reference_count`, `rank`"
    ele_num = 5
    ans = query_data_by_mid(table, elements, ele_num, mid)
    return {
        "time": ans[0],
        "content": ans[1],
        "uid": ans[2],
        "usedNumber": ans[3],
        "rank": ans[4]/au_number
    }

@Fail2None
def get_reply_max_send_one_day(mid):
    # 获取字段reply_max_send_one_day数据
    table = "max_send_one_day"
    elements = "`max_sent_date`, `content`, `max_reply_num`"
    ele_num = 3
    ans = query_data_by_mid(table, elements, ele_num, mid)
    return {
        "date": ans[0].strftime("%Y-%m-%d"),
        "content": ans[1],
        "maxSendNumber": ans[2]
    }

@Fail2None
def get_reply_prefer_time(mid):
    # 获取字段reply_prefer_time数据
    table = "prefer_time"
    elements = "`reply_hour`, `reply_num`"
    ele_num = 2
    sql = f"""select {elements} from {DATABASE}.{table} where mid={mid};"""
    reply_time = query_many(sql, ele_num)
    time_table = ["凌晨", "上午", "下午", "晚上"]
    count = [0]*4
    for i in reply_time:
        count[i[0]//6]+=1
    index = count.index(max(count))
    return {
        "time": time_table[index],
        "maxHour": reply_time[0][0] if index<2 else reply_time[-1][0]
    }

fansMap = {
    672328094:"嘉心糖",
    672346917:"顶碗人",
    703007996:"一个魂",
    672353429:"贝极星",
    672342685:"奶淇琳",
    351609538:"皇珈骑士"
}

def get_badge_with_level(value, name, base_level, ranges):
    '''
    生成徽章，并根据阈值计算徽章等级
    value      实际值
    name       徽章名称
    base_level 基础等级
    ranges     徽章等级阈值
    '''
    if not value:
        return {
            "name": name,
            "level": base_level,
        }

    range_length = len(ranges)

    for index, range in enumerate(ranges):
        if value > range:
            base_level += 1
            if range_length > index + 1:
                continue
        return {
            "name": name,
            "level": base_level
        }

@Fail2None
def get_medal_fans(danmu_total):
    global fansMap
    memberUid = danmu_total.get("memberUid")
    return {"name":"铁血"+fansMap.get(memberUid), "level":6}

@Fail2None
def get_medal_reply_count(reply_total):
    reply_count = reply_total.get("replyNumber")
    return get_badge_with_level(reply_count, "滔滔不绝", 2, [10, 100, 150, 300])

@Fail2None
def get_medal_reply_like(reply_max_like):
    like_num = reply_max_like.get("likeNumber")
    return get_badge_with_level(like_num, "才高八斗", 1, [30, 300, 1000, 3000])

@Fail2None
def get_medal_reply_copy(reply_max_used):
    used_num = reply_max_used.get("usedNumber")
    return get_badge_with_level(used_num, "枝江学阀", 2, [1, 6, 10, 30])

@Fail2None
def get_medal_perfer_time(reply_prefer_time):
    prefer_time = reply_prefer_time.get("time")
    ret = {"name":"", "level":6}
    if prefer_time=="凌晨" or prefer_time=="上午":
        ret["name"]="爱在黎明破晓前"
    elif prefer_time=="下午":
        ret["name"]="爱在黄昏日落时"
    else:
        ret["name"]="爱在午夜降临前"
    return ret

@Fail2None
def get_medal_danmu_count(danmu_total):
    danmu_num = danmu_total.get("danmuNumber")
    return get_badge_with_level(danmu_num, '爱意绵绵', 2, [100, 400, 800, 1500])

def get_medal(data):
    medal = []
    medal.append(get_medal_fans(data.get("danmu_total")))
    medal.append(get_medal_reply_count(data.get("reply_total")))
    medal.append(get_medal_reply_like(data.get("reply_max_like")))
    medal.append(get_medal_reply_copy(data.get("reply_max_used")))
    medal.append(get_medal_perfer_time(data.get("reply_prefer_time")))
    medal.append(get_medal_danmu_count(data.get("danmu_total")))
    medal.append(None)
    medal = [i for i in medal if i is not None]
    medal = sorted(medal, key=lambda x:x['level'], reverse=True)
    return medal

def get_personal_data(mid):
    import time
    start = time.time()
    data = {
        "all": get_all(),
        "reply_first": get_reply_first(mid),
        "reply_total": get_reply_total(mid),
        "danmu_total": get_danmu_total(mid),
        "reply_total_like": get_reply_total_like(mid),
        "reply_max_like": get_reply_max_like(mid),
        "reply_max_used": get_reply_max_used(mid),
        "reply_max_send_one_day": get_reply_max_send_one_day(mid),
        "reply_prefer_time": get_reply_prefer_time(mid)
    }
    medal = get_medal(data)
    data.update({"medal":medal})
    print(time.time()-start)
    return data

au_number = query_one(f"select count(mid) from {DATABASE}.first;", 1)[0]
