# Data Crawling
For training models , we crawled Dcard posts and our FB chatroom's messages.  

## FB Chatroom's Messages
Due to [Facebook Graph API](https://developers.facebook.com/tools/explorer/)'s limited API calling rate , directly downloading a FB personal backup and parsing it may be a good choice.  
After downloading backup file, I change it to Python's Dict-type.

### Download Personal Backup
*   **1st step:**
 
![FB1](FB_images/FB1.png)   

* **2nd step:**

![FB1](FB_images/FB2.png)  

* **3rd step:**  

![FB1](FB_images/FB3.png)    

* **4th step:**          
             
![FB1](FB_images/FB4.png)  

### File We Need   
After downloading, we need `messages.htm` in:  
`/Facebook-[a_sequence_of_number]/html/messages.htm`

### Usage
`pip3 install requirement.txt`  
`python3 FBhtml2dict.py <input_file> <output_file> <FB_name> -s`  

`-s` : is optional, if yot want to segment setences.

ex:   
`FBhtml2dict.py yao_messages.htm yao_FBmsgDict_.txt 朱瑤章`  
`<FB_name>` is main speaker of these chatrooms. Get dict without segmenting sentences.
### Result Data Types
* set `-s` : segment every sentence.  

```
{
	'names_of_both_speaker':{
		'msgs’:[['timestamp','speaker',['term','term']]],
		’segm’:{'term': count_num_of_main_speaker}
	}
}  

```
 <mark>Beware</mark>: Messgages contents in `['term','term']`  may be blank, and it will be `[]`.    
 <mark>Beware</mark>: `count_num_of_main_speaker` not count on whom you speak.   

ex:         

```
{
    '朱瑤章, 鄭宇軒':{
         'msgs': [ ['2014年3月9日 1:31:59', '朱瑤章', ['好', ' ', '我', '再', '催', '一下']],  
                   [‘2014年3月9日 1:30:59', '鄭宇軒',  ['因為', '我', '還要', '拿', '去']]  ],  
         'segm': {' ': 5,',': 18,'OK': 1,'ㄟ': 1}
        },  
    '朱瑤章, 許靜':{  
         'msgs': [ ['2014年8月1日 12:46:59', '許靜', [] ],  
                   [‘2014年7月27日 14:07:59', '朱瑤章', ['找','不到']] ],  
         'segm': {'\n': 2,' ': 3,',': 5,'xd': 1}  
        }  
}  
```   
  
* not set `-s` : output whole sentence.  

```
{
	'names_of_both_speaker':{
		'msgs’:[['timestamp','speaker','contents_of_a_sentence']]
	}
}  
```  
 <mark>Beware</mark>: Messgages contents in `contents_of_a_sentence`  may be blank, and it will be `None` type.    
 <mark>Beware</mark>: `count_num_of_main_speaker` not count on whom you speak.  
 
ex:
  
```
{
	'朱瑤章, 蔡伯禮': {
		'msgs': [ ['2016年3月20日 1:07:59', '朱瑤章', '以後再說啦XD'],
				  ['2016年3月20日 1:01:59', '蔡伯禮', '一定要喔ww'],
				  ]
		}
}
```


### Reading Dict in Python
```python
f1 = open('YAO_msgDict.txt','r')
s1 = f1.read()
dictYao = eval(s1)  #turn str -> default dict object
```

## Dcard Posts
Calling Dcard's API to get posts and replies contents.  
`https://www.dcard.tw/api/post/all/[number]`  
In the past, we can get posts linearly from `[number]` being `10001` to `1000000`,  
 but recently, Dcard has change their saving rules and there will be many "holes" in `[number]`(it means consecutive posts' `[number]`  will not be `n` and `n+1`) , so linear search will not fit very well in recent posts.  

### Usage
`pip3 install requirement.txt`  
`python3 tdcardCrowl.py <from_postid> <to_postid> <output_file>`  
ex:  
`python3 dcardCrowl.py 10001 1000000 dcardData.txt`

### Result Data Types
pure `str` with posts and replies seperating by `\n` (not count on `\n` in original contents).  
ex:  

```
By 中央德萊尼  
推B2  
希望畢業以後  
也可以一直感受這種午夜樂趣XDD  
聯大，Bonheur  
```

