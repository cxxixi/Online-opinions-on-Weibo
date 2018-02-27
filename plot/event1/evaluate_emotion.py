# -*- coding: utf-8 -*-
import jieba
import numpy as np
import codecs
import pandas as pd
import sys
import re
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random

reload(sys)
sys.setdefaultencoding('utf8')
words = []

font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=14)
file1 = codecs.open(
    "D:\my_documents\competition\government\emotion\dicword.csv", 'r', 'utf-8'
)
for line in file1:
    words.append(line.strip())

# content=file1.readlines()
file1.close()

emotions = []

file2 = codecs.open(
    "D:\my_documents\competition\government\emotion\dicemotion.csv", 'r', 'utf-8'
)
for line in file2:
    emotions.append(line.strip())

# content=file1.readlines()
file2.close()

# dicfile2 = pandas.read_csv('/Users/renwendi/Documents/dicemotion.csv','utf-8')
#
# dic_Emotion = dicfile2["emotion"]
#
# dic={}
# i=0
# l=len(dicfile)
# while i<l:
#    dic[content[i]]=dic_Emotion[i]
#    print(content[i])
#    i=i+1
def clean_text(text):
    patt1 = re.compile(r'<.*?>')
    pattern_list = [patt1, r"回复", "@.*?:", "@.*? "]
    for pattern in pattern_list:
        text = re.sub(pattern, "", text)
    # try:
    #     text = text.split(r'\\@')[0]
    #     text = text.split(r'//@')[0]
    #
    #     re.sub('转发微博',"",text)
    #     strip_punctuation = lambda X: re.sub("[\s*【】“”\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode('utf-8'),
    #     #                                      "".decode('utf-8'), X.decode('utf-8'))
    # except:
    #     pass
    print text
    return text

dictionary = dict(zip(words, emotions))

NegationList = ['不',
                '不可',
                '切勿',
                '勿',
                '反',
                '少',
                '毋须',
                '未',
                '未必',
                '未有',
                '未曾',
                '别',
                '否',
                '否定',
                '否认',
                '决不',
                '没',
                '没有',
                '并非',
                '尚未',
                '非',
                '从不',
                '从未',
                '毫不',
                '毫无',
                '莫',
                '无',
                '绝不',
                '绝非',
                '绝无',
                '难以']


# comment_data = pd.read_csv('D:\my_documents\competition\government\Report\event\\comment_data.csv',header=None)

# comment_data = pd.read_csv('D:\my_documents\competition\government\Report\event2\\comment_data_event2.csv',header=None)

comment_data = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment_data.csv')

# comment_data1 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment1123.csv',header=None)
# comment_data2 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment855.csv',header=None)
# comment_data = pd.concat([comment_data1,comment_data2],axis=0)
# comment_data.index = [i for i in range(len(comment_data))]
# comment_data = comment_data.dropna()

comment_data.columns = ['a','text','tweet', 'like_counts', 'reply_id', 'reply_text','created_at','user_id',\
                       'profile_url', 'screen_name', 'verified']

comment_data.columns = ['a','tweetid', 'comment_id', 'created_at', 'text', 'like_counts', 'reply_id', 'reply_text', 'user_id',\
                       'profile_url', 'screen_name', 'verified', 'verified_type']
# comment_data = comment_data[comment_data['tweetid']!==]

comment_content = comment_data['text']
num_list = [i for i in range(len(comment_data))]

random_list = random.sample(num_list,40009)
comment_content = [comment_content[i] for i in random_list]

for i in range(len(comment_content)):
    # print repost_content[i]
    print comment_content[i]
    comment_content[i] = clean_text(comment_content[i])

emotions = ['PH', 'NN', 'ND', 'NB', 'PA', 'NE', 'PB', 'PD', 'NC', 'PE',
               'PG', 'NJ', 'NA', 'NI', 'PF', 'PC', 'PK', 'NL', 'NH', 'NG', 'NK']
new_columns = ['created_at','comment', 'PH', 'NN', 'ND', 'NB', 'PA', 'NE', 'PB', 'PD', 'NC', 'PE',
               'PG', 'NJ', 'NA', 'NI', 'PF', 'PC', 'PK', 'NL', 'NH', 'NG', 'NK']
# emotion = ['happiness', 'like', 'anger', 'sadness', 'fear', 'disgust', 'suprise']
emotion_df = pd.DataFrame(np.zeros((len(comment_content), len(new_columns))), columns=new_columns)
emotion_df['comment'] = comment_content
emotion_df['created_at'] = comment_data['created_at']
# num = 0
for i in range(len(comment_content)):
    # num = num + 1
    segments = []
    segs = jieba.cut(comment_content[i])
    for seg in segs:
        if len(seg) > 1:
            segments.append(seg)

    segmentDF = pd.DataFrame({'segment': segments})

    # 移除停用词
    stopwords = pd.read_csv(
        "D:\my_documents\competition\government\\stopwords.txt",
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
    emos = []
    c = 0
    for word in segments:
        flag = 0
        for deny in NegationList:
            if word == deny:
                flag = 1
                break
        if flag == 1:
            c = c + 1
        else:
            if word in dictionary:
                if c % 2 == 0:
                    #            print(word)
                    #            print(dictionary[word])
                    emos.append(dictionary[word])
        # try:
        #     if dictionary[word]=='PH':
        #         print word
        # except:
        #     pass
    for k in emos:
        emotion_df.ix[i,k] = 1
        # print(k)
        # if k == 'PA' or 'PE':
        #     n[0] = n[0] + 1
        # # break
        # elif k == 'PD' or 'PH' or 'PG' or 'PB' or 'PK':
        #     n[1] = n[1] + 1
        # # break
        # elif k == 'NA':
        #     n[2] = n[2] + 1
        # # break
        # elif k == 'NB' or 'NG' or 'NH' or 'PF':
        #     n[3] = n[3] + 1
        # # break
        # elif k == 'NI' or 'NC' or 'NG':
        #     n[4] = n[4] + 1
        # # break
        # elif k == 'NE' or 'ND' or 'NN' or 'NK' or 'NL':
        #     n[5] = n[5] + 1
        # # break
        # elif k == 'PC':
        #     n[6] = n[6] + 1
        #     #            break

    # N = sorted(n)
    # #    print(N[6])
    # for i in range(0, 7):
    #     if n[i] == N[6]:
    #         print(emotion[i])
            #    segStat = segmentDF.groupby(
            #                by=["segment"]
            #            )["segment"].agg({
            #                "计数":numpy.size
            #            }).reset_index().sort(
            #                columns=["计数"],
            #                ascending=False
            #            )


# get_time = lambda X: X.split(':')[0] if len(X.split()[0].split('-'))==3 else '2017-'+X.split(':')[0]
# get_date = lambda X: X.split()[0] if len(X.split()[0].split('-'))==3 else '2017-'+X.split()[0]
emotion_df.loc[:,emotions].sum().sort_values(ascending=False).head(10)
# emotion_df['time'] = emotion_df['created_at'].apply(get_time)
# emotion_df.index = pd.DatetimeIndex(emotion_df['time'])
#
# NN
# ph
# nd
# p

emotion_df.reindex([i for i in range(len(emotion_df))])
def plot(plot_data,fea1,fea2,fea3,fea4):

    get_time = lambda X: X.split(':')[0] if len(X.split()[0].split('-')) == 3 else '2017-' + X.split(':')[0]
    fig,axes = plt.subplots(2,2,sharex=True,sharey=True)
    # for i in range(2):
    #     for j in range(2):
    #
    # fig = plt.figure(figsize=(18,14))

    ax1 = fig.add_subplot(2,2,1)
    # ax1.set_yticks([0,1],minor=False)
    # ax1.set_xlim(emit=False,auto=False)
    # ax1.tick_params(top = 'off', bottom = 'off', left = 'off', right = 'off')
    # ax1.tick_params(labelbottom ='off', labeltop='off', labelleft='off', labelright='off')
    data = plot_data[plot_data[fea1]==1][[fea1,'created_at']]
    data['time'] = data['created_at'].apply(get_time)
    times = pd.DatetimeIndex(data['time'])
    dup_ts1 = plot_data[plot_data[fea1]==1][fea1].copy()
    dup_ts1.index = times

    grouped = dup_ts1.groupby(level=0)
    grouped = grouped.count()
    grouped.ix['2017':].plot(color='b',label = fea1) #ix['2017':'2017-4-15']

    ax2 = fig.add_subplot(2,2,2)
    # ax2.set_xlim(emit=False, auto=False)
    # ax2.tick_params(top='off', bottom='off', left='off', right='off')
    # ax2.tick_params(labelbottom='off', labeltop='off', labelleft='off', labelright='off')
    data = plot_data[plot_data[fea2]==1][[fea2,'created_at']]
    data['time'] = data['created_at'].apply(get_time)
    times = pd.DatetimeIndex(data['time'])
    dup_ts1 = plot_data[plot_data[fea2]==1][fea2].copy()
    dup_ts1.index = times
    grouped = dup_ts1.groupby(level=0)
    grouped = grouped.count()
    grouped.ix['2017':].plot(color='g',label =fea2)

    ax3 = fig.add_subplot(2,2,3)
    # ax3.set_xlim(emit=False, auto=False)
    # ax3.tick_params(top='off', bottom='off', left='off', right='off')
    # ax3.tick_params(labelbottom='off', labeltop='off', labelleft='off', labelright='off')
    data = plot_data[plot_data[fea3]==1][[fea3,'created_at']]
    data['time'] = data['created_at'].apply(get_time)
    times = pd.DatetimeIndex(data['time'])
    dup_ts1 = plot_data[plot_data[fea3]==1][fea3].copy()
    dup_ts1.index = times
    grouped = dup_ts1.groupby(level=0)
    grouped = grouped.count()
    grouped.ix['2017':].plot(color='r',label = fea3)


    ax4 = fig.add_subplot(2,2,4)
    # ax4.set_xlim(emit=False, auto=False)
    # ax4.tick_params(top='off', bottom='off', left='off', right='off')
    # ax4.tick_params(labelbottom='off', labeltop='off', labelleft='off', labelright='off')
    data = plot_data[plot_data[fea4]==1][[fea4,'created_at']]
    data['time'] = data['created_at'].apply(get_time)
    times = pd.DatetimeIndex(data['time'])
    dup_ts1 = plot_data[plot_data[fea4]==1][fea4].copy()
    dup_ts1.index = times
    grouped = dup_ts1.groupby(level=0)
    grouped = grouped.count()
    grouped.ix['2017':].plot(color='y',label =fea4)

    # plt.xlabel(u'时间', fontproperties=font)
    # plt.ylabel(u'强度', fontproperties=font)
    # plt.title(u'主要的四种情感随时间变化曲线', fontproperties=font)
    # plt.legend(loc='best')
    plt.subplots_adjust(wspace=0,hspace=0)
    plt.show()

def plot2(plot_data,fea1,fea2,fea3,fea4):

    check_time = lambda X: X.split(':')[0] if len(X.split()[0].split('-')) == 3 else '2017-' + X.split(':')[0]
    get_time = lambda X: X.split(':')[0] if len(X.split()[0].split('-')) == 3 else '2017-' + X.split(':')[0]
    #
    # fig,axes = plt.subplots(2,2)#,sharex=True,sharey=True)
    # # for i in range(2):
    # #     for j in range(2):
    # #
    fig = plt.figure(figsize=(30,24))

    # ax1 = fig.add_subplot(2,2,1)
    data = plot_data[plot_data[fea1]==1][[fea1,'created_at']]

    data['time'] = data['created_at'].apply(get_time)
    print data.ix[2340:2350, 'time']
    times = pd.DatetimeIndex(data['time'])

    # print times[2344:2350]
    dup_ts1 = plot_data[plot_data[fea1]==1][fea1].copy()
    dup_ts1.index = times
    grouped = dup_ts1.groupby(level=0)
    grouped = grouped.count()
    grouped.ix['2017':].plot(color='b',label=fea1,linewidth=2)#,marker='o'
#.ix['2017-1-23':'2017-02-28']

    # ax2 = fig.add_subplot(2,2,2)
    data = plot_data[plot_data[fea2]==1][[fea2,'created_at']]
    data['time'] = data['created_at'].apply(get_time)
    times = pd.DatetimeIndex(data['time'])
    dup_ts1 = plot_data[plot_data[fea2]==1][fea2].copy()
    dup_ts1.index = times
    grouped = dup_ts1.groupby(level=0)
    grouped = grouped.count()
    grouped.ix['2017':].plot(color='k',label=fea2)#,marker="+"
#
    # ax3 = fig.add_subplot(2,2,3)
    data = plot_data[plot_data[fea3]==1][[fea3,'created_at']]
    data['time'] = data['created_at'].apply(get_time)
    times = pd.DatetimeIndex(data['time'])
    dup_ts1 = plot_data[plot_data[fea3]==1][fea3].copy()
    dup_ts1.index = times
    grouped = dup_ts1.groupby(level=0)
    grouped = grouped.count()
    grouped.ix['2017':].plot(color='r',label=fea3)#,marker="*"

    # ax4 = fig.add_subplot(2,2,4)
    data = plot_data[plot_data[fea4]==1][[fea4,'created_at']]
    data['time'] = data['created_at'].apply(get_time)
    times = pd.DatetimeIndex(data['time'])
    dup_ts1 = plot_data[plot_data[fea4]==1][fea4].copy()
    dup_ts1.index = times
    grouped = dup_ts1.groupby(level=0)
    grouped = grouped.count()
    grouped.ix['2017':].plot(color='y',label=fea4)#,marker="+"

    plt.xlabel(u'时间', fontproperties=font)
    plt.ylabel(u'强度', fontproperties=font)
    plt.title(u'主要的四种情感随时间变化曲线', fontproperties=font)
    plt.legend(loc='best')
    plt.show()

plot(emotion_df,'NN','PH','ND','PG') #辱母
plot2(emotion_df,'NN','PH','ND','PG')

plot(emotion_df,'NN','PH','ND','PG')#丽江
plot2(emotion_df,'NN','PH','ND','PG')

plot(emotion_df,'PE','PH','PK','NN')
plot2(emotion_df,'PE','PH','PK','NN')
#
# PH_data = emotion_df[['PH','time']].copy()
# PH_data['time'] = PH_data['time'].apply(get_time)
# PH_data = PH_data.groupby(['time']).size()
# PH_data.index = pd.DatetimeIndex(PH_data.index)
# # NN = pd.Series(NN_data,index=NN_index)
# PH_data.ix['2017':].plot()
# plt.show()
#
# NI_data = emotion_df[['NI', 'time']].copy()
# NI_data['time'] = NI_data['time'].apply(get_time)
# NI_data = NI_data.groupby(['time']).size()
# NI_data.index = pd.DatetimeIndex(NI_data.index)
# # NN = pd.Series(NN_data,indes
# NI_data.ix['2017':].plot()
# plt.show()
#
#
#
#
#
#
#
#
#









file.close()
# print(num)