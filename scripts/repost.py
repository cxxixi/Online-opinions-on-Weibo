
# -*- coding: utf-8 -*-

##scrape all comments to each tweets

from time import sleep
import csv
import json
from urllib2 import urlopen,Request,ProxyHandler,build_opener,install_opener
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
proxy = '106.120.78.129:80'
proxy_handler = ProxyHandler({'http': proxy})
opener = build_opener(proxy_handler)
install_opener(opener)
print proxy,'ok'

def scrape_repost_page_url(tweetid):
    pagenum = 1
    repost_page_url = []
    try:
        baseurl = 'https://m.weibo.cn/api/statuses/repostTimeline?id='+tweetid+'&page='
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
                repost_page_url.append(baseurl+str(i))
            return repost_page_url
    except urllib2.HTTPError as e:
        print e
        sleep(1)
        scrape_repost_page_url(tweetid)

def scrape_repost(url):
    try:
        print url
        req = Request(url, headers=headers)
        response = urlopen(req)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf-8')
        jsonObject = json.loads(jsonString)
        for repost in jsonObject['data']:
            time = repost['created_at']
            repost_id = repost['id']
            text = repost['raw_text']
            like_counts = repost['like_counts']
            user_id = repost['user']['id']
            profile_url = repost['user']['profile_url']
            screen_name = repost['user']['screen_name']
            verified = repost['user']['verified']
            verified_type = repost['user']['verified_type']
            feature = [tweetid, repost_id, time, text, like_counts, user_id, \
                       profile_url, screen_name, verified, verified_type]
            writer.writerow(feature)
    except urllib2.HTTPError as e:
        print e
        sleep(1)
        scrape_repost(url)
    except:
        pass


if __name__ = "__main__":
    
    tweet_ids = []
    file = open('D:\my_documents\competition\government\Report\event1\\tweetids_event1.txt')
    for line in file:
        tweet_ids.append(line.strip())

    tweet_ids = tweet_ids[:1000]
    global writer
    file = open('D:\my_documents\competition\government\Report\event1\\repost.csv','wb')
    writer = csv.writer(file)

    count = 0
    for tweetid in tweet_ids:
        count += 1
        print count
        repost_url_list = scrape_repost_page_url(tweetid)
        if repost_url_list!= None:
            for url in repost_url_list:
                scrape_repost(url)
        else:
            print count,'none'

