import pandas as pd

csv1 = pd.read_csv('D:\my_documents\competition\government\Report\event\\1.csv',header=None)
csv2 = pd.read_csv('D:\my_documents\competition\government\Report\event\\2.csv',header=None)
csv3 = pd.read_csv('D:\my_documents\competition\government\Report\event\\3.csv',header=None)
csv4 = pd.read_csv('D:\my_documents\competition\government\Report\event\\4.csv',header=None)
csv5 = pd.read_csv('D:\my_documents\competition\government\Report\event\\5.csv',header=None)
csv6 = pd.read_csv('D:\my_documents\competition\government\Report\event\\6.csv',header=None)

comment_data = pd.concat([csv1,csv2,csv3,csv4,csv5,csv6],axis=0)
comment_data.to_csv('D:\my_documents\competition\government\Report\event\\comment_data.csv',header=None)

