# -*- coding: utf-8 -*-
import jieba
import numpy
import codecs
import pandas as pd
import wordcloud
import re

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def clean(text):
    patt1 = re.compile(r'<.*?>')
    pattern_list = [patt1,r"回复","@.*?:","@.*? "]
    for pattern in pattern_list:
        text = re.sub(pattern,"",text)
    return text

comment = pd.read_csv('D:\my_documents\competition\government\Report\event2\\comment_data.csv')
comment.columns = ['a','tweetid', 'comment_id', 'created_at', 'text', 'like_counts', 'reply_id', 'reply_text', 'user_id',\
                       'profile_url', 'screen_name', 'verified', 'verified_type']
# comment.groupby(by=['tweetid']).size().sort_values()
# get_time = lambda X: X if len(X.split()[0].split('-'))==3 else '2017-'+X
# get_time = lambda X: X[:-3] if len(X.split()[0].split('-'))==3 else '2017-'+X[:-3]
# get_date = lambda X: X.split()[0] if len(X.split()[0].split('-'))==3 else '2017-'+X.split()[0]

# dates = pd.DatetimeIndex(repost_data['date'])
# times = pd.DatetimeIndex(repost_data['time'])
# # dup_ts = Series(np.ones(len(repost_data['date'])),index=dates)
# dup_ts = Series(np.ones(len(repost_data['date'])),index=times)

comment[comment['tweetid']==4089975262195562]
# comment['date'] = comment['created_at'].apply(get_date)

comment = comment[comment['tweetid']==4089176619718807]
comment
# comment = comment[comment['date']=='2017-01-26']#['text']
comment_data = comment['text'].copy()
comment_data.index = [i for i in range(len(comment_data))]
# comment.index = pd.DatetimeIndex(times)
for i in range(len(comment_data)):
    # print comment[i]
    comment_data[i] = clean(comment_data[i])
    print comment_data[i]

comment_data.to_csv('D:\my_documents\competition\government\Report\event2\\trial.csv')
file = codecs.open(
    "D:\my_documents\competition\government\Report\event2\\trial.csv", 'r', 'utf-8'
)


content = file.read()
file.close()

segments = []
segs = jieba.cut(content)
for seg in segs:
    if len(seg)>1:
        segments.append(seg)

segmentDF = pd.DataFrame({'segment':segments})

#移除停用词
stopwords = pd.read_csv(
    "D:\my_documents\competition\government\\stopwords_addition.txt",
    encoding='utf8',
    index_col=False,
    quoting=3,
    sep="\t"
)

segmentDF = segmentDF[
    ~segmentDF.segment.isin(
        stopwords
    )
]

segStat = segmentDF.groupby(
            by=["segment"]
        )["segment"].agg({
            "计数":numpy.size
        }).reset_index().sort_values(
            ["计数"],
            ascending=False
        )

segStat.head(100)

#绘画词云
#http://www.lfd.uci.edu/~gohlke/pythonlibs/
wordcloud = WordCloud(
    font_path='simhei.ttf',
    background_color="white"
)

words = segStat.set_index('segment').to_dict()

wordcloud = wordcloud.fit_words(words['计数'])

plt.figure(
    num=None, figsize=(100, 80),
    dpi=100, facecolor='w', edgecolor='k'
)

plt.axis("off")
plt.imshow(wordcloud)
plt.show()


plt.close()
