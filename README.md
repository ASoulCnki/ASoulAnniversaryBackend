字段说明:
```python
{
  "code": 0,
  "message": "",
  "data": {
    # all存放所有au共有数据 -> 无需建表
    "all": {
      "replyCount": 3001234,    # au发过的评论总数
      "danmuCount": 30012345,   # au发过的弹幕总数
      "dynamicCount": 233       # as发过的动态总数
    },
    # reply_first存放个人第一次评论相关 -> reply_first表
    "reply_first":{
      "time": 1638862558,       # 个人第一次评论时间戳
      "content": "以后国v第一",  # 个人第一次评论内容
      "uid": 672328094          # 个人第一次评论成员uid
    },
    # reply_total存放个人评论总览 -> reply_total表
    "reply_total": {
      "dynamicNumber": 12,      # 个人评论过的动态总数
      "replyNumber": 101,       # 个人评论总数
      "rank": 0.2346667         # 个人评论总数正向排名(%)
    },
    # danmu_total存放个人弹幕总览 -> danmu_total表
    "danmu_total": {
      "danmuNumber": 102,       # 个人发送弹幕总数
      "memberUid": 672328094,   # 个人发送最多的直播间成员uid
      "memberDanmuNumber": 56,  # 个人发送最多的直播间发送弹幕总数
      "impDanmuNumber": 10,     # 个人发送醒目留言总数
      "cost": 555,              # 个人花费人民币总数
    },
    # reply_total_like存放个人总点赞数相关 -> reply_total_like表
    "reply_total_like": {
      "likeNumber": 304,        # 个人所有评论获赞总数
      "rank": 0.2346667         # 个人所有评论获赞总数正向排名(%)
    },
    # reply_max_like存放个人点赞数最高评论相关 -> reply_max_like表
    "reply_max_like": {
      "time": 1638862558,       # 个人点赞数最高评论时间戳
      "content": "以后国v第一",  # 个人点赞数最高评论内容
      "uid": 672328094,         # 个人点赞数最高评论成员uid
      "likeNumber": 304,        # 个人点赞数最高评论获赞数
      "rank": 0.2346667         # 个人点赞数最高评论获赞数正向排名(%)
    },
    # reply_max_used存放个人被引用数最高评论相关 -> reply_max_used表
    "reply_max_used": {
      "time": 1638862558,       # 个人被引用数最高评论时间戳
      "content": "以后国v第一",  # 个人被引用数最高评论内容
      "uid": 672328094,         # 个人被引用数最高评论成员uid
      "usedNumber": 304,        # 个人被引用数最高评论引用数
      "rank": 0.2346667         # 个人被引用数最高评论引用数正向排名(%)
    },
    # reply_max_send_one_day存放个人发送评论最多日期相关 -> reply_max_send_one_day表
    "reply_max_send_one_day": {
      "date": "2021-12-01",     # 个人发送评论最多日期
      "content": "以后国v第一",  # 个人发送评论最多日期其中一条内容
      "maxSendNumber": 304,     # 个人发送评论最多日期评论数
    },
    # reply_prefer_time存放个人偏爱评论时间相关 -> reply_prefer_time表
    "reply_prefer_time": {
      "time": "上午",           # 个人偏爱评论时间段
      "maxHour": 12,            # 下午、晚上则为最晚，早晨、上午则为最早
    },
  }
}
```
