# -*- coding: utf-8 -*-

##scrape all comments to each tweets

from time import sleep
import csv
import json
import pandas
from urllib2 import urlopen,Request,ProxyHandler,build_opener,install_opener
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
proxy = '210.38.1.135:8080'
proxy_handler = ProxyHandler({'http': proxy})
opener = build_opener(proxy_handler)
install_opener(opener)
print proxy,'ok'

def scrape_comment_page_url(tweetid):
    pagenum = 1
    comment_page_url = []
    try:
        baseurl = 'https://m.weibo.cn/api/comments/show?id='+tweetid+'&page='
        url = baseurl+str(pagenum)
        print url
        req = Request(url, headers=headers)
        response = urlopen(req)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf-8')
        jsonObject = json.loads(jsonString)
        if len(jsonObject)==2:
            return None
        else:
            for i in xrange(1,jsonObject['max']+1):
                comment_page_url.append(baseurl+str(i))
            return comment_page_url
    except urllib2.HTTPError as e:
        print e
        sleep(1)
        scrape_comment_page_url(tweetid)

def scrape_comment(url):
    try:
        print url
        req = Request(url, headers=headers)
        response = urlopen(req)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf-8')
        jsonObject = json.loads(jsonString)
        for comment in jsonObject['data']:
            time = comment['created_at']
            comment_id = comment['id']
            text = comment['text']
            like_counts = comment['like_counts']
            try:
                reply_id = comment['reply_id']
                reply_text = comment['reply_text']
            except:
                reply_id = None
                reply_text = None
            user_id = comment['user']['id']
            profile_url = comment['user']['profile_url']
            screen_name = comment['user']['screen_name']
            verified = comment['user']['verified']
            verified_type = comment['user']['verified_type']
            feature = [tweetid, comment_id, time, text, like_counts, reply_id, reply_text, user_id, \
                       profile_url, screen_name, verified, verified_type]
            writer.writerow(feature)
    except urllib2.HTTPError as e:
        print e
        sleep(1)
        scrape_comment(url)
    except:
        pass


tweet_ids = []
file = open('D:\my_documents\competition\government\Report\event2\\tweetids_event2.txt')
for line in file:
    tweet_ids.append(line.strip())

tweet_ids = tweet_ids[1000:]
global writer
file = open('D:\my_documents\competition\government\Report\event2\\comment1000.csv','wb')
writer = csv.writer(file)

count = 1000
for tweetid in tweet_ids:
    count += 1
    print count
    comment_url_list = scrape_comment_page_url(tweetid)
    if comment_url_list!= None:
        for url in comment_url_list:
            scrape_comment(url)
    else:
        print count,'none'

#execute('D:\my_documents\competition\government\\comment.py')



        # if pagenum==1 and len(jsonObject)==2:
        #     return None
        # else:
        #     if pagenum<jsonObject['max']:
        #         for comment in jsonObject['data']:
        #             comment_list.append(comment)
        #         pagenum +=1
        #     else:
        #         for comment in jsonObject['data']:
        #             comment_list.append(comment)
        #         print len(comment_list)
        #         return comment_list