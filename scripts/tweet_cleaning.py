# -*- coding: utf-8 -*-

# wrangle and clean the data scraped

import re
import pandas as pd
from chardet import detect
import numpy
import matplotlib.pyplot as plt
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

path = 'D:\my_documents\competition\government\\Report\\event2\\tweets_event2.csv' ##put your path here
tweets_data = pd.read_csv(path,header=None)
columns = ['tweetid','status','created_at','userid', 'nickname', 'status_count','verified','verified_type'\
    ,'follower_count','gender','rank','reposts_count','like_count','follower_count','follow_count','comments_count']
tweets_data.columns = columns

# eliminate some characters from the status.
def clean(text):
    patt1 = re.compile(r'<.*?>')
    pattern_list = [patt1]
    for pattern in pattern_list:
        text = re.sub(pattern,"",text)
    return text

_status = tweets_data['status']
for i in range(len(_status)):
    _status[i] = clean(_status[i])

tweets_data['status'] = _status
#
# repost_count = tweets_data['reposts_count'].copy()
# repost_count = repost_count.ix[:,0]
#
# follower_count = tweets_data['follower_count'].copy()
# follower_count = follower_count.ix[:,0]
#
# follow_count = tweets_data['follow_count'].copy()
# follow_count = follow_count.ix[:,0]
#
# comment_count = tweets_data['comments_count'].copy()
# comment_count = comment_count.ix[:,0]
#
# like_count = tweets_data['like_count'].copy()
# like_count = like_count.ix[:,0]
#
# tweets_data = tweets_data.drop(['reposts_count','follower_count','follow_count','like_count','comments_count'],axis=1)
# tweets_data['repost_count'] = repost_count
# tweets_data['follower_count'] = follower_count
# tweets_data['follow_count'] = follow_count
# tweets_data['like_count'] = like_count
# tweets_data['comment_count'] = comment_count

tweets_data.to_csv('D:\my_documents\competition\government\\clean_tweets_event2.csv',index=False)

print tweets_data.head(20)
print tweets_data.columns

# tweets_data['status'] = _status
# print tweets_data['status']

# def clean_emoji(text):
    # for word in set(text):
    #     try:
    #         print word,detect(word)
    #         tran_word = word.decode(detect(word)).encode('gbk')
    #     except:
    #         new_text = re.sub(word,"",new_text)
    # print len(set(text))
    # print text.decode('')
    # print type(text)
    # for i in range(len(text)):

        # print text[i].decode(detect(text[i])['encoding'])#.encode('gb2312')
    # return new_text

# _status = tweets_data['status']
# for i in range(len(_status)):
    # print _status[i]
    # _status[i] = clean(_status[i])
    # _status[i] = clean_emoji(_status[i])
    # print _status[i]
