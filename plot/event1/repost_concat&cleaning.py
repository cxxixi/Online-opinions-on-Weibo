import pandas as pd

csv1 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\repost.csv',header=None)
csv2 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\repost1000.csv',header=None)

repost_data = pd.concat([csv1,csv2],axis=0)

repost_data.shape
repost_data.head()

repost_data.columns = ['tweetid', 'repost_id', 'created_at', 'text', 'like_counts', 'user_id',\
                       'profile_url', 'screen_name', 'verified', 'verified_type']

repost_data = repost_data.drop_duplicates()
group = repost_data.groupby(by=['tweetid']).size().sort_values(ascending=False)
pd.merge(tweets_data,repost_data,on='tweetid').groupby(by=['tweetid']).size().sort_values(ascending=False)


tweets_data.sort_values(['reposts_count'],ascending=False)
repost_data = repost_data[repost_data['tweetid']!=4072609702951009 ]##与事件无关

repost_data[repost_data['tweetid']==4067784932183507] #云南丽江警方

repost_data.to_csv('D:\my_documents\competition\government\Report\event1\\repost_data.csv',index=False)



