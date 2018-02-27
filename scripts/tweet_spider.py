# -*- coding: utf-8 -*-

##scrape all status concerning specific topics

import json
import pandas
from urllib2 import urlopen,Request
import urllib2
from bs4 import BeautifulSoup
import re
from urllib import quote
import csv
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
# insert_sql = '''INSERT INTO tweets(`status`,`created_at`,`textlength`,`userid`,`nickname`,`status_count`,`follower_count`,`follow_count`,`reposts`_`count`,`comments_count`,`like_count`,`follower_count`,`follow_count`,`reposts_count`,`comments_count`,`like_count`)
#                     VALUES(status,created_at,textlength,userid,nickname,status_count,follower_count,follow_count,reposts_count,comments_count,like_count,follower_count,follow_count,reposts_count,comments_count,like_count)'''
#
#
# def insert_data(cursor,status,created_at,textlength,userid,nickname,status_count,follower_count,follow_count,reposts_count,comments_count,like_count,follower_count,follow_count,reposts_count,comments_count,like_count):
#     cursor.execute(insert_sql)


def getJSONObject(keyword, page):
    do = True
    sleepSecond = 1
    jsonObject = ""

    while do:
        # time.sleep(sleepSecond)
        keyword = quote(keyword)
        print keyword
        # dataURL = 'https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%s&featurecode=20000320&oid=4074811614843068&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%94%BE%s&title=%s&containerid=100103type%3D1%26q%3D%s&page=%d' % (keyword, keyword, keyword, keyword, page)
        dataURL = 'https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%E5%85%A8%E9%9D%A2%E4%BA%8C%E8%83%8E&featurecode=20000320&oid=4074811614843068&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%94%BE%E5%BC%80%E4%BA%8C%E5%AD%A9%E6%94%BF%E7%AD%96&title=%E5%85%A8%E9%9D%A2%E4%BA%8C%E8%83%8E&containerid=100103type%3D1%26q%3D%E5%85%A8%E9%9D%A2%E4%BA%8C%E8%83%8E&page='+str(page)
        #dataURL = 'https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%s&featurecode=20000320&oid=4074811614843068&luicode=10000011&lfid=106003&title=%s&containerid=100103&page=%d' % (keyword, keyword,page)
        # dataURL = 'http://m.weibo.cn/container/getIndex?type=all&queryVal=%s&luicode=10000011&lfid=100103type%%3D1%%26q%%3D%s&title=%s&containerid=100103type%%3D1%%26q%%3D%s&page=%d' % (
        #keyword, keyword, keyword, keyword, page)
        print("处理 URL: %s" % (dataURL))

        req = Request(dataURL, headers=headers)
        response = urlopen(req)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf-8')
        jsonObject = json.loads(jsonString)

        if 'cards' not in jsonObject:
            sleepSecond = sleepSecond + 5
            print("遭受限制~~~，%s 秒后重试" % (sleepSecond))
            continue
        else:
            do = False

    return jsonObject

# extract info from returned jsonobject
def scrape_tweet(tweetid):
    try:
        url = 'https://m.weibo.cn/status/'+tweetid
        print url
        req = Request(url,headers=headers)
        response = urlopen(req)
        soup = BeautifulSoup(response)

        status = re.findall(r'"text":.*',str(soup))[0].split(r'": "')[1][:-2]
        created_at = re.findall(r'"created_at":.*',str(soup))[0].split(r'": "')[1][:-2]
        userid = re.findall(r'"id":.*',str(soup))[0].split(r'": "')[1][:-2]
        nickname = re.findall(r'"screen_name":.*',str(soup))[0].split(r'": "')[1][:-2]
        status_count = re.findall(r'"statuses_count":.*',str(soup))[0].split(r'":')[1][:-1]
        verified = re.findall(r'"verified":.*',str(soup))[0].split(r'":')[1][:-1]
        verified_type = re.findall(r'"verified_type":.*', str(soup))[0].split(r'":')[1][:-1]
        gender = re.findall(r'"gender":.*', str(soup))[0].split(r'": "')[1][:-2]
        rank = re.findall(r'"urank":.*', str(soup))[0].split(r'":')[1][:-1]
        follower_count = re.findall(r'"followers_count":.*', str(soup))[0].split(r'":')[1][:-1]
        follow_count = re.findall(r'"follow_count":.*', str(soup))[0].split(r'":')[1][:-1]
        reposts_count = re.findall(r'"reposts_count":.*', str(soup))[0].split(r'":')[1][:-1]
        comments_count = re.findall(r'"comments_count":.*', str(soup))[0].split(r'":')[1][:-1]
        like_count = re.findall(r'"attitudes_count":.*', str(soup))[0].split(r'":')[1][:-1]
        feature = [tweetid, status, created_at, userid, nickname, status_count, verified,verified_type,follower_count, follow_count,\
                   gender, rank,  reposts_count, like_count, comments_count]
        writer.writerow(feature)

    except urllib2.HTTPError as e1:
        print 'urllib2.HTTPError'
        scrape_tweet(tweetid)
    except IndexError as e2:
        print e2
        return
    # insert_data(cursor,tweetid,status,created_at,textlength,userid,nickname,status_count,follower_count,follow_count,reposts_count,comments_count,like_count,follower_count,follow_count,reposts_count,comments_count,like_count)



# These are four events discussed here.
# used the keywords listed below for searching for concerning status
# keyword_list = ['天津塘沽大爆炸','#天津塘沽大爆炸#','塘沽大爆炸','#塘沽大爆炸#','塘沽爆炸','#塘沽爆炸#','8.12爆炸','8.12大爆炸','#8.12大爆炸#']
# keyword_list = ['丽江打人','丽江毁容','丽江恶性','丽江抢劫']#,'丽江旅游黑幕','#塘沽爆炸#','8.12爆炸','8.12大爆炸','#8.12大爆炸#']
# keyword_list =  ['辱母杀人','刺死辱母者','辱母案']
keyword_list = ['全面二孩']#,'放开二孩政策','全面二胎']
Tweet_Ids = []
weiboTexts = []

 for keyword in keyword_list:
     page = 1
     while True:
         print("page:" + str(page)+keyword)
         resultObject = getJSONObject(keyword, page)
         cards = resultObject['cards']
         if len(cards) == 0:
             break
         for card in cards:
             try:
                 cardGroups = card['card_group']
                 for group in cardGroups:
                     if 'mblog' in group:
                         tweet_id = group['mblog']['id']
                         print 'weiboID:',tweet_id
                         Tweet_Ids.append(tweet_id)
             except KeyError as e:
                 print e

         page = page + 1

 store tweetid in csv.
 file = open('D:\my_documents\competition\government\\Report\\event4\\tweetids3.txt','wb')
 for tweet_id in set(Tweet_Ids):
     file.write(tweet_id)
     file.write('\n')

Tweet_Ids = []
file = open('D:\my_documents\competition\government\\Report\\event4\\tweetids.txt','r')
for line in file:
    Tweet_Ids.append(line.strip())

Tweet_Ids = set(Tweet_Ids)

global writer
file = open('D:\my_documents\competition\government\\Report\\event4\\tweets.csv','wb')
writer = csv.writer(file)

count = 1
for tweetid in Tweet_Ids:
    # time.sleep(1)
    scrape_tweet(tweetid)
    count+=1
    print count

