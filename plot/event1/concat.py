import pandas as pd

csv1 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment855.csv',header=None)
csv2 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment1123.csv',header=None)

comment_data = pd.concat([csv1,csv2],axis=0)
comment_data.head()
comment_data.shape
comment_data.columns = ['tweetid', 'comment_id', 'created_at', 'text', 'like_counts', 'reply_id', 'reply_text', 'user_id',\
                       'profile_url', 'screen_name', 'verified', 'verified_type']

comment_data = comment_data.drop_duplicates()
comment_data.groupby(by=['tweetid']).size().sort_values(ascending=False)


comment_data.to_csv('D:\my_documents\competition\government\Report\event1\\comment_plot.csv')







