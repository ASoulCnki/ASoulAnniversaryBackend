目前数据库中还没有最终各个查询表的名称和字段，所以我提前写了，以后再根据具体的表名和字段修改

```
{
	"code":0,
	"message":"",
	"data":{
		"total":{
			"dynamicCount":null,
			"replyCount":null,
			"total_charCount":null,
			"danmuCount":null
		},
		"first":{
			"first_replytime":null,
			"first_content":null,
			"first_dynamicid":null
		},
		"comment_rank":{
			"total_reply_num":null,
			"total_dynamic_num":null,
			"rank":null
		},
		"comment_member_rank":{
			"uid":null,
			"member":null,
			"total":null,
			"rank":null
		}
	}
}
```



## first表

统计每个用户第一次评论的时间，内容和动态id

```
"first_replytime": first_reply_time
"first_content": content,
"first_dynamicid": dynamic_id
```

## comment_rank表

统计每个用户发表的评论数，以及评论所在的动态/投稿数，并按评论总数从大到小排名

```
"total_reply_num": total_reply_num,
"total_dynamic_num": total_dynamic_num,
"rank": rank
```

## comment_member_rank表

统计每个用户发送评论次数最多的成员和评论数，并根据成员的评论数从大到小排名

```
"uid":uid,
"member":member,
"total":total,
"rank":rank}
```