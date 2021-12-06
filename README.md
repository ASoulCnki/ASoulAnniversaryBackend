目前数据库中还没有最终各个查询表的名称和字段，所以我提前写了，以后再根据具体的表名和字段修改

```
{
	"code":0,
	"message":"",
	"data":{
		"total": {
			"dynamicNumber": 1,  对应 comment_rank -> total_dynamic_num
			"sendNumber": 1,  对应 comment_rank -> total_reply_num
			"rank": 1,  对应 comment_rank -> rank
			"maxDynamicOwner": "嘉然今天吃什么",  对应 comment_member_rank -> member
			"maxSendNumber": 1,  对应 comment_member_rank -> total
			"maxOwnerRank": 1   对应 comment_member_rank -> rank
		},
		"first_send": {
			"time": 1637205720285,  对应 first -> first_reply_time
			"dynamicOwner": "嘉然今天吃什么",  字段缺失
			"rank": 5.5,  这个字段不要了👿
			"content": "文本",  对应 first -> content
		},
		"max_like": {
			"time": 1637205720285,  字段缺失
			"dynamicOwner": "嘉然今天吃什么",  字段缺失
			"rank": 5.5,  对应 max_like -> rank
			"content": "文本",  对应 max_like -> content
			"likeNum": 123,  对应 max_like -> max_likes
		},
		"max_used": {
			"time": 1637205720285,  字段缺失
			"dynamicOwner": "嘉然今天吃什么",  字段缺失
			"rank": 5.5,  字段缺失
			"content": "文本",  对应 max_used -> content
			"usedNum": 123,  对应 max_used -> reference_count
		},
		"stolen": { 整个"stolen"疑似摆了😤
			"time": 1637205720285,
			"dynamicOwner": "嘉然今天吃什么",
			"rank": 5.5,
			"content": "文本",
			"stolenNum": 123,
		},
		"max_send_one_day": {
			"time": 1637205720285,  对应 comment_date -> date
			"content": "文本",  对应 comment_date -> content
			"maxSendTime": 100,  对应 comment_date -> max_reply_num
			"timeRange": "早晨", 对应 comment_hour -> reply_hour,但是这里传的是时间，交给前端转为字符串😤
			"sendNum": 123,  对应 comment_hour -> reply_num
		},
		"text": {
			"length": 114514,
			"book": "莎士比亚全集"
		},
	}
}
```



## first表

统计每个用户第一次评论的时间，内容和动态id

```
"first_replytime": first_reply_time	评论时间
"first_content": content,		评论内容
"first_dynamicid": dynamic_id		动态id
```

## comment_rank表

统计每个用户发表的评论数，以及评论所在的动态/投稿数，并按评论总数从大到小排名

```
"total_reply_num": total_reply_num,		评论总数
"total_dynamic_num": total_dynamic_num,		涉及动态/投稿总数
"rank": rank					排名
```

## comment_member_rank表

统计每个用户发送评论次数最多的成员和评论数，并根据成员的评论数从大到小排名

```
"uid":uid,		成员id
"member":member,	成员姓名
"total":total,		评论数
"rank":rank		排名
```

## comment_date表

统计每个用户发送评论数最多的日期和评论数，投稿id 和评论内容

```
"oid":oid, 			动态/投稿id
"date":date, 			动态/投稿日期
"content":content, 		评论内容
"max_reply_num":max_reply_num	评论数
```

## max_like表

统计每个用户点赞数最多的评论，并根据最大点赞数从大到小排名

## reference表

统计每个用户引用数最多的评论

## comment_hour表

统计每个用户发送评论所在的小时