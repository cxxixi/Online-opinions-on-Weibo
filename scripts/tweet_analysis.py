# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas import Series
import matplotlib.pyplot as plt
import seaborn as sns
from time import strptime,mktime,strftime
from datetime import datetime
from matplotlib.font_manager import FontProperties
from scipy.misc import imread
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
import thulac
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Configurate the font you gonna use in matplotlib otherwise you cannot print with chinese characters.
font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=14)
font_path = "C:\\WINDOWS\\Fonts\\simsun.ttc"

global tweets_data
## input the comment data we've scracped. 
path = 'D:\my_documents\competition\government\Report\\event2\\comment.csv'
comment_data = pd.read_csv(path,header=0)
comment_data.columns = ['tweetid', 'comment_id', 'created_at', 'text', 'like_counts', 'reply_id', 'reply_text', 'user_id',\
                       'profile_url', 'screen_name', 'verified', 'verified_type']


#把数字映射成文字标签
verified_dic = {
    -1:u'普通用户',
    0:u'名人',
    1:u'政府',
    2:u'企业',
    3:u'媒体',
    4:u'校园',
    5:u'网站',
    6:u'应用',
    7:u'团体（机构）',
    8:u'待审企业',
    10:u'微博女郎',
    200:u'初级达人',
    220:u'中高级达人',
    400:u'已故V用户'
}
tweets_data['verified'] = tweets_data['verified'].map(lambda x:verified_dic[x])

# def description():
#基本的统计信息
#   看status_count,follower_count,rank,follow,count,comment_count……的分位数
description = tweets_data.describe()
description = description.drop(['tweetid','userid','verified_type'],axis=1)
description.to_csv('D:\my_documents\competition\government\Report\event\description.csv')



##status
# clean data : eliminate the following punctuation  
strip_punctuation = lambda X: re.sub("[\s*【】“”\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode('utf-8'), "".decode('utf-8'),X.decode('utf-8'))
status_list = tweets_data['status'].apply(strip_punctuation)
stop_word_list = []

## use stopwords to break the sentences into works.
with open('D:\my_documents\competition\government\\stopwords_addition.txt') as f:
    for line in f:
        stop_word_list.append(line.strip().decode('utf-8'))

#use jieba libaray to do the job
sentence_list = [jieba.cut(status) for status in status_list]
word_list = []
for sentence in sentence_list:
    for word in sentence:
        word_list.append(word)

seg_word = [word for word in word_list if word not in stop_word_list]
seg_word = [word for word in seg_word if word != '​']
len(seg_word),len(set(seg_word))
print Series(seg_word).value_counts()

word_count = pd.DataFrame(Series(word_list),columns=['segment']).groupby(by=['segment'])
print word_count.sort_values(ascending=False).head(100)


word_count = pd.DataFrame(Series(word_list).value_counts(),columns=['count'])

##plot the word cloud
word_count.head()
wordcloud = WordCloud(font_path = font_path,
               max_words = 200)
plt.figure(num=None, figsize=(1000, 600), dpi=800, facecolor='w', edgecolor='k')
wordcloud = wordcloud.fit_words(word_count.head(200).itertuples(index=False))
plt.imshow(wordcloud)



##likewise, you can use thunlp to do the same job
thul = thulac.thulac()
all_text = []
for i in range(len(status_list)):
    print thul.cut(status_list[i])
    all_text.append(thul.cut(status_list[i]))
print all_text


    # for item in thul.cut(status_list[i]):
    #     all_text += ' '+item[0]
word_dic = pd.DataFrame(all_text,columns=['word','property'])
print word_dic.shape()

property_count = word_list.groupby(['property']).value_counts().sort_values(ascending=False)
word_count = word_list.groupby(['word']).value_counts().sort_values(ascending=False)
print property_count

print len(all_text.split())
word_dic = set(all_text.split())
print len(word_dic)

img_path = 'D:\my_documents\competition\government\\trial.jpg'
bg_img = imread(img_path)

wc = WordCloud(font_path = font_path,
               max_words = 200)
               # background = "white")
wc.generate(r' '.join(seg_word))

# mask = bg_img
# stopwords = STOPWORDS
# image_colors = ImageColorGenerator(bg_img)
# wc.recolor(color_func = image_colors)
plt.imshow(wc)
plt.axis("off")
plt.show()



# get_time = lambda X: X if len(X.split()[0].split('-'))==3 else '2017-'+X
get_time = lambda X: X[:-3] if len(X.split()[0].split('-'))==3 else '2017-'+X[:-3]
# get_date = lambda X: X.split()[0] if len(X.split()[0].split('-'))==3 else '2017-'+X.split()[0]
comment_data['date'] = comment_data['created_at'].apply(get_time)
# comment_data['time'] = comment_data['created_at'].apply(get_time)
# dates = pd.DatetimeIndex(repost_data['date'])
times = pd.DatetimeIndex(comment_data['date'])
# dup_ts = Series(np.ones(len(repost_data['date'])),index=dates)
dup_ts = Series(np.ones(len(comment_data['date'])),index=times)
grouped = dup_ts.groupby(level=0)
grouped = grouped.count()
# given a specific time range, plot the number of repost changes along with time. 
grouped.ix['2017-03-24':'2017-3-27'].plot()
plt.xlabel(u'时间',fontproperties=font)
plt.ylabel(u'转发数量',fontproperties=font)
plt.title(u'相关微博评论数随时间变化',fontproperties=font)
plt.show()




selected_tweets_data = pd.concat([tweets_data[tweets_data['verified']==u'名人'],\
    tweets_data[tweets_data['verified']==u'政府'],tweets_data[tweets_data['verified']==u'媒体']])
celebrity_data = tweets_data[tweets_data['verified']==u'名人']
govornment_data = tweets_data[tweets_data['verified']==u'政府']
media_data = tweets_data[tweets_data['verified']==u'媒体']

#created_at
get_time = lambda X: X.split()[1]+' '+X.split()[2]+' '+X.split()[-1]+' '+X.split()[3].split(':')[0]
get_date = lambda X: X.split()[1]+' '+X.split()[2]+' '+X.split()[-1]
tweets_data['date'] = tweets_data['created_at'].apply(get_date)
tweets_data['time'] = tweets_data['created_at'].apply(get_time)
# dates = pd.DatetimeIndex(tweets_data['date'])
times = pd.DatetimeIndex(tweets_data['time'])
# dup_ts = Series(np.ones(len(tweets_data['date'])),index=dates)
dup_ts1 = Series(np.ones(len(tweets_data['time'])),index=times)
# grouped = dup_ts.groupby(level=0)
# grouped = grouped.count()
# grouped.ix['2017':'2017-01-31'].plot(kind='bar')
grouped1 = dup_ts1.groupby(level=0)
grouped1 = grouped1.count()
grouped1.ix[:'2017-04-10'].plot() #
plt.xlabel(u'时间',fontproperties=font)
plt.ylabel(u'微博数量',fontproperties=font)
plt.title(u'微博发帖数随时间变化',fontproperties=font)
plt.show()

#尺度缩小到事情发生点的后两周
# fig = plt.figure(figsize=(12,6))
# ax = fig.add_subplot(1,1,1)
# end_point = strptime("Aug 26 00 2015","%b %d %H %Y")
# get_time = lambda X: strptime(X.split(':')[0]+' '+X.split()[-1],"%a %b %d %H %Y")
# to_str = lambda X: strftime("%a %b %d %H %Y",X).split()[1]+' '+strftime("%a %b %d %H %Y",X).split()[2]
# is_in = lambda X: mktime(X)<mktime(end_point)
# focus = tweets_data['created_at'].apply(get_time)
# focus = focus[focus.apply(is_in)].value_counts().sort_index()
# ticklabel = Series(focus.index).apply(to_str).unique()
# focus.plot()
# plt.xlim()
# ax.set_xlim([0,200])
# ax.set_xticks([i for i in xrange(14)])
#
# ax.set_xticklabels(ticklabel)
# plt.show()

# get_time =lambda X: strptime(' '.join(X.split()[1:4])+' '+X.split()[-1],"%b %d %H:%M:%S %Y")
# time_series = tweets_data['created_at'].apply(get_time)


# userid 没有人发多条微博
print tweets_data.groupby(['userid']).size().sort_values(ascending=False)

#pairplot
col = ['status_count','follower_count','rank','follow_count','verified']
selected_user = [u'政府',u'媒体']#u'普通用户',,'comment_count','like_count','repost_count']
pair_df = tweets_data[tweets_data['verified'] ==u'名人'][col]
for user in selected_user:
    pair_df = pd.concat([pair_df,tweets_data[tweets_data['verified']==user][col]])
# ax = sns.pairplot(pair_df,hue='verified',kind='reg',diag_kind='kde')
ax = sns.pairplot(pair_df,hue='verified',diag_kind='kde')
plt.show()

##verified
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)
verified_series = tweets_data['verified'].value_counts()
ax = verified_series.plot(kind='bar')## (range(len(verified_series.index)),verified_series.values)
ax.set_xticks([i for i in range(len(verified_series))])
ax.set_xticklabels(verified_series.index,fontproperties=font,fontsize=12,rotation=30)
plt.xlabel(u'认证类别',fontproperties=font)
plt.ylabel(u'数量',fontproperties=font)
plt.title(u'微博发布者认证类别统计',fontproperties=font)
plt.show()

#rank_distribution
_xrange = len(set(tweets_data['rank']))

celebrity_data_rank = celebrity_data['rank'].value_counts().sort_index()
celebrity_data_rank = [celebrity_data_rank[i] if i in celebrity_data_rank.index else 0 for i in xrange(1,_xrange+1) ]
celebrity_data_rank = pd.DataFrame(celebrity_data_rank,index=xrange(1,_xrange+1),columns=['count'])

govornment_data_rank = govornment_data['rank'].value_counts().sort_index()
govornment_data_rank = [govornment_data_rank[i] if i in govornment_data_rank.index else 0 for i in xrange(1,_xrange+1) ]
govornment_data_rank = pd.DataFrame(govornment_data_rank,index=xrange(1,_xrange+1),columns=['count'])

media_data_rank = media_data['rank'].value_counts().sort_index()
media_data_rank = [media_data_rank[i] if i in media_data_rank.index else 0 for i in xrange(1,_xrange+1) ]
media_data_rank = pd.DataFrame(media_data_rank,index=xrange(1,_xrange+1),columns=['count'])

plt.bar(np.arange(_xrange),celebrity_data_rank['count'],color='r',align='center',width=0.2,alpha=0.5,label=u'celebrity')
plt.bar(np.arange(_xrange)+0.25*np.ones(_xrange),govornment_data_rank['count'],color='g',align='center',width=0.2,alpha=0.5,label=u'govornment')
plt.bar(np.arange(_xrange)+0.5*np.ones(_xrange),media_data_rank['count'],color='b',align='center',width=0.2,alpha=0.5,label=u'media')
plt.xlim([4,47])
plt.title(u'微博发布者等级分布',fontproperties=font)
plt.legend(loc='best')
plt.xlabel(u'等级',fontproperties=font)
plt.ylabel(u'数量',fontproperties=font)
plt.show()


#gender_distribution
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1)
gender_series = tweets_data['gender'].value_counts()
gender_series.plot(kind='bar',width=0.4)
ax.set_xticks([0,1])
ax.set_xticklabels([u'女性',u'男性'],fontproperties=font,rotation=0)
plt.xlabel(u'性别',fontproperties=font)
plt.ylabel(u'数量',fontproperties=font)
plt.title(u'微博发布者性别',fontproperties=font)
plt.show()


def plot_hist(plot_data,xlabel,ylabel,title):
    fig = plt.figure(figsize=(18,10))
    ax = fig.add_subplot(1,1,1)
    plot_data.plot(kind='bar',alpha=0.7)
    ax.set_xticklabels(plot_data.index,fontproperties=font,fontsize=10,rotation=15)
    plt.xlabel(xlabel, fontproperties=font)
    plt.ylabel(ylabel, fontproperties=font)
    plt.title(title, fontproperties=font)
    plt.show()
    #输出到

#看名人，政府媒体中评论数转发数等排名靠前的几个 三个直方图
celebrity_data.index = celebrity_data['nickname']
govornment_data.index = govornment_data['nickname']
media_data.index = media_data['nickname']

verified_celebrity_repost = celebrity_data.sort_values(['repost_count'],ascending=False)['repost_count'].head(10)
plot_hist(verified_celebrity_repost,u'微博发布者',u'数量',u'名人所发微博中转发数前十')
verified_celebrity_like = celebrity_data.sort_values(['like_count'],ascending=False)['like_count'].head(10)
plot_hist(verified_celebrity_like,u'微博发布者',u'数量',u'名人所发微博中点赞数前十')
verified_celebrity_comment = celebrity_data.sort_values(['comment_count'],ascending=False)['comment_count'].head(10)
plot_hist(verified_celebrity_comment,u'微博发布者',u'数量',u'名人所发微博中评论数前十')

verified_govornment_repost = govornment_data.sort_values(['repost_count'],ascending=False)['repost_count'].head(10)
plot_hist(verified_govornment_repost,u'微博发布者',u'数量',u'政府所发微博中转发数前十')
verified_govornment_like = govornment_data.sort_values(['like_count'],ascending=False)['like_count'].head(10)
plot_hist(verified_govornment_like,u'微博发布者',u'数量',u'政府所发微博中点赞数前十')
verified_govornment_comment = govornment_data.sort_values(['comment_count'],ascending=False)['comment_count'].head(10)
plot_hist(verified_govornment_comment,u'微博发布者',u'数量',u'政府所发微博中评论数前十')

verified_media_repost = media_data.sort_values(['repost_count'],ascending=False)['repost_count'].head(10)
plot_hist(verified_media_repost,u'微博发布者',u'数量',u'媒体所发微博中转发数前十')
verified_media_like = media_data.sort_values(['like_count'],ascending=False)['like_count'].head(10)
plot_hist(verified_media_like,u'微博发布者',u'数量',u'媒体所发微博中点赞数前十')
verified_media_comment = media_data.sort_values(['comment_count'],ascending=False)['comment_count'].head(10)
plot_hist(verified_media_comment,u'微博发布者',u'数量',u'媒体所发微博中评论数前十')





