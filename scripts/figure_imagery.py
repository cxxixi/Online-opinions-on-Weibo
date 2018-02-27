# -*- coding: utf-8 -*-

## scrape basic infos about users
import time
import csv
import json
import pandas as pd
from urllib2 import urlopen,Request
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def basic_info(userid):
    time.sleep(1)
    url = 'http://m.weibo.cn/api/container/getIndex?containerid=230283'+userid+'_-_INFO&title=%25E5%259F%25BA%25E6%259C%25AC%25E4%25BF%25A1%25E6%2581%25AF&luicode=10000011&lfid='+userid+'&featurecode=20000180'
    print url
    try:
        req = Request(url, headers=headers)
        response = urlopen(req,timeout=10)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf-8')
        jsonObject = json.loads(jsonString)

        card_group = []
        verified_type = None
        verified_reason = None
        for card in jsonObject['cards']:
            if card['card_group']!=[] and card['show_type']==2:
                card_group+=card['card_group']
            for card in card_group:
                if 'item_type' in card.keys():
                    verified_type = card['item_type']
                    verified_reason = card['item_content']
                    break
        card_group = [card for card in card_group if 'item_name' in card.keys()]


        feature_name = [item['item_name'] for item in card_group]

        feature_item = [item['item_content'] for item in card_group]

        try:
            nickname = feature_item[feature_name.index(u'昵称')]
        except:
            nickname = None
        try:
            gender = feature_item[feature_name.index(u'性别')]
        except:
            gender = None

        try:
            place = feature_item[feature_name.index(u'所在地')]
        except:
            place = None

        try:
            rank = feature_item[feature_name.index(u'等级')]
        except:
            rank = None
        try:
            credit = feature_item[feature_name.index(u'阳光信用')]
        except:
            credit = None
        try:
            sign_up_time = feature_item[feature_name.index(u'注册时间')]
        except:
            sign_up_time = None

        feature = [userid,nickname,gender,place,rank,credit,sign_up_time,verified_type,verified_reason]
        writer.writerow(feature)
    except urllib2.HTTPError as e:
        print e
        basic_info(userid)
    except:
        print 'error'
        return



if __name__ == "__main__":

    #those user who commented on the tweet.
    userid_list = pd.read_csv('D:\my_documents\competition\government\\Report\\event1\\comment_userid.csv',header=None)
    userid_list.columns = ['userid']
    userid_list = userid_list.dropna()
    userid_list = set(userid_list['userid'])
    sub_list = pd.read_csv('D:\my_documents\competition\government\\Report\\event1\\figure_imagery.csv',header=None)
    sub_list.columns = list('abcdefghi')
    sub_list = set(sub_list['a'])
    sub_list = set([str(i) for i in sub_list])
    id_left = userid_list-sub_list

    global writer
    file = open('D:\my_documents\competition\government\Report\event1\\figure_imagery1.csv','wb')
    writer = csv.writer(file)

    count = 1
    userid_list = id_left
    for userid in userid_list:
        print count
        basic_info(userid)
        count+=1

