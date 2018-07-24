#coding=utf-8
import requests
import pymysql
from bs4 import BeautifulSoup

import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse,json,re,datetime,sys,http.cookiejar
from pyquery import PyQuery


def getJsonReponse(refresh_cursor, cookieJar, proxy):
    url_pri = "https://twitter.com/i/profiles/show/Bitcoin/timeline/tweets?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false"
    # refresh_cursor = "1014079045066080256"
    url = "https://twitter.com/Bitcoin"
    print(url)

    headers = [
        ('Host', "twitter.com"),
        ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
        ('Accept', "application/json, text/javascript, */*; q=0.01"),
        ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
        ('X-Requested-With', "XMLHttpRequest"),
        ('Referer', url),
        ('Connection', "keep-alive")
    ]

    if proxy:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}),
                                             urllib.request.HTTPCookieProcessor(cookieJar))
    else:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))
    opener.addheaders = headers

    try:
        response = opener.open(url)
        jsonResponse = response.read()
    except:
        # print("Twitter weird response. Try to see on browser: ", url)
        print(
            "Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd")
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit()
        return



    print(jsonResponse.decode())
    jR = jsonResponse.decode().replace("true","\"\"").replace("\n", "")
    # print(type(eval(jR)))
    # print(eval(jR))
    return eval(jR)

def get_tweet_data(coin_name, max_position):
    cookieJar = http.cookiejar.CookieJar()
    active = True
    proxy = None
    receiveBuffer = None

    refresh_cursor = max_position

    while active:
        json = getJsonReponse(refresh_cursor, cookieJar, proxy)
        if len(json['items_html'].strip()) == 0:
            break

        # 下一页的id游标，每一页有20个
        refresh_cursor = json['min_position']
        print(refresh_cursor)
        scrapedTweets = PyQuery(json['items_html'])
        # Remove incomplete tweets withheld by Twitter Guidelines
        scrapedTweets.remove('div.withheld-tweet')
        tweets = scrapedTweets('div.js-stream-tweet')('div.content')('div.stream-item-footer')(
            'div.ProfileTweet-actionCountList')
        # print("tweets", tweets)

        if len(tweets) == 0:
            break
        for tweetHTML in tweets:
            print(tweetHTML)

            tweetPQ = PyQuery(tweetHTML)

            tweet_id = tweetPQ(
                "span.ProfileTweet-action--reply span.ProfileTweet-actionCount span.ProfileTweet-actionCountForAria").attr(
                "id").split("-")[6]
            print("tweet_id: ", tweet_id)

            reply_num = tweetPQ("span.ProfileTweet-action--reply span.ProfileTweet-actionCount").attr(
                "data-tweet-stat-count")
            print("reply_num: ", reply_num)

            retweet_num = tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr(
                "data-tweet-stat-count")
            print("retweet_num: ", retweet_num)

            favorite_num = tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr(
                "data-tweet-stat-count")
            print("favorite_num: ", favorite_num)


if __name__ == '__main__':


    get_tweet_data("ethereum", "1")



