# -*- coding: utf-8 -*-

##scrape all comments of each status

from time import sleep
import csv
import json
import pandas
from urllib2 import urlopen,Request
import urllib2
import sys

# It's rather trickey to deal with Chinese Character in python2, if you're using Python2 you need to set the default encoding to utf-8 
#otherwise you might run into trouble in this program.
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

# STEP1: scrape url of every comment page and return them 
def scrape_comment_page_url(tweetid):
    pagenum = 1
    comment_page_url = []
    try:
        baseurl = 'https://m.weibo.cn/api/comments/show?id='+tweetid+'&page='
        url = baseurl+str(pagenum)
        print url
        sleep(1)
        req = Request(url, headers=headers)
        response = urlopen(req)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf-8')
        jsonObject = json.loads(jsonString)

#check if the page num exceed the maximum
        if len(jsonObject)<=2:
            return None
        else:
            for i in xrange(1,jsonObject['max']+1):
                comment_page_url.append(baseurl+str(i))
            return comment_page_url
    except urllib2.HTTPError as e:
        print e
        sleep(1)
        scrape_comment_page_url(tweetid)

# STEP2 : get comments from each url we scraped in STEP1
def scrape_comment(url):
    try:
        print url
        sleep(1)
        req = Request(url, headers=headers)
        response = urlopen(req)
        jsonBytes = response.read()
        jsonString = jsonBytes.decode('utf-8')
        jsonObject = json.loads(jsonString)
        
        #the contents we want show as follows:
        for comment in jsonObject['data']:
            time = comment['created_at']
            comment_id = comment['id']
            text = comment['text']
            like_counts = comment['like_counts']
        # the json object might not have these two features
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

if __name__ == '__main__':

    # open files and set writer to control the output process
    tweet_ids = []
    file = open("PUT YOUR PATH HERE")
    for line in file:
        tweet_ids.append(line.strip())

    global writer
    file = open('PUT YOUR PATH HERE','wb')
    writer = csv.writer(file)

    count = 0
    for tweetid in tweet_ids:
        count += 1
        print count
        comment_url_list = scrape_comment_page_url(tweetid)
        if comment_url_list!= None:
            for url in comment_url_list:
                scrape_comment(url)
        else:
            print count,'none'
