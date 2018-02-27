import pandas as pd

csv1 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\500-593.csv',header=None)
csv2 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment594.csv',header=None)
csv3 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment855.csv',header=None)
csv4 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment993.csv',header=None)
csv5 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment1123.csv',header=None)
csv6 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment1137.csv',header=None)
csv7 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment1.csv',header=None)
csv8 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\comment350.csv',header=None)
csv9 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\addition.csv',header=None)
csv10 = pd.read_csv('D:\my_documents\competition\government\Report\event1\\addition_1.csv',header=None)



comment_data = pd.concat([csv1,csv2,csv3,csv4,csv5,csv6,csv7,csv8,csv9,csv10],axis=0)
comment_data.head()
comment_data.shape
comment_data.columns = ['tweetid', 'comment_id', 'created_at', 'text', 'like_counts', 'reply_id', 'reply_text', 'user_id',\
                       'profile_url', 'screen_name', 'verified', 'verified_type']

comment_data = comment_data.drop_duplicates()
comment_data.groupby(by=['tweetid']).size().sort_values(ascending=False)


comment_data.to_csv('D:\my_documents\competition\government\Report\event1\\comment_data.csv')







