#coding=utf-8
import requests
import pymysql
from bs4 import BeautifulSoup
import xlrd
import logging
import datetime
import time
from email_monitor import email

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='twitter_get.log',
                filemode='w')

logging.getLogger("requests").setLevel(logging.WARNING)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

dbname='lyz'
user='root'
passwd='111111'
host = '10.107.10.110'

conn =  pymysql.connect(host=host, port=3306, user=user, passwd=passwd, db=dbname,charset='utf8')
conn.autocommit(1)
cur=conn.cursor()
insertSql = "insert into twitters_data(coin_id, name, tweets_num, following_num, followers_num, created_time) values ('%d', '%s', '%d', '%d', '%d', '%s')"
insertSql_null = "insert into twitters_data(coin_id, name, created_time) values ('%d', '%s', '%s')"

# url爬取，并且解析
def get_twitterdata(coin_url):
    if coin_url == "":
        return 0, 0, 0

    logging.info(coin_url)
    try:
        response = requests.get(coin_url).text
    except:
        logging.info("getUrlResponseFailed!: ", coin_url)
        return "EOF","EOF","EOF"
    soup_xml = BeautifulSoup(response, "lxml")
    # 加上此行，可以优化代码运行速度
    try:
        soup_tmp = soup_xml.find_all('ul', "ProfileNav-list")
        soup = soup_tmp[0]
    except:
        logging.info("不可用的链接")
        return "wr_url", "wr_url", "wr_url"

    try:
        tweets_li = soup.find_all('li', "ProfileNav-item ProfileNav-item--tweets is-active")
        if tweets_li.__len__() > 0:
            tweets_span = tweets_li[0].find_all(name='span', attrs={"ProfileNav-value"})
            tweets_num = int(tweets_span[0].attrs['data-count'])
        else:
            tweets_num = 0

        following_li = soup.find_all('li', "ProfileNav-item ProfileNav-item--following")
        if following_li.__len__() > 0:
            following_span = following_li[0].find_all(name='span', attrs={"ProfileNav-value"})
            following_num = int(following_span[0].attrs['data-count'])
        else:
            following_num = 0

        followers_li = soup.find_all('li', "ProfileNav-item ProfileNav-item--followers")
        if followers_li.__len__() > 0:
            followers_span = followers_li[0].find_all(name='span', attrs={"ProfileNav-value"})
            followers_num = int(followers_span[0].attrs['data-count'])
        else:
            followers_num = 0
    except:
        logging.info("网络异常，连接不上")
        email.email("爬取twitter网络异常")

    return tweets_num, following_num, followers_num

# 读取项目列表
def read_coinProjectList():
    excelData = xlrd.open_workbook(u'bitinfo.xlsx')
    sheet0 = excelData.sheet_by_index(0)
    coinUrlList = sheet0.col_values(9)
    del coinUrlList[0]
    coinIdList = sheet0.col_values(0)
    del coinIdList[0]
    coinNameList = sheet0.col_values(1)
    del coinNameList[0]
    return coinIdList, coinNameList, coinUrlList

# 开始爬取
def start():
    coinIdList, coinNameList, coinUrlList = read_coinProjectList()
    coin_list_len = coinIdList.__len__()
    re_extract_url_list = []
    re_extract_id_list = []
    re_extract_name_list = []
    for i in range(coin_list_len):
        tweets_num, following_num, followers_num = get_twitterdata(coinUrlList[i])
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if tweets_num == "EOF":
            re_extract_id_list.append(coinIdList[i])
            re_extract_url_list.append(coinUrlList[i])
            re_extract_name_list.append(coinNameList[i])
            continue
        if tweets_num == "wr_url":
            cur.execute(
                insertSql % (int(coinIdList[i]), str(coinNameList[i]), 0, 0, 0, dt))
            continue
        logging.info(str(int(coinIdList[i])) + "  " + str(coinNameList[i]) + "  " + str(tweets_num) + "  "  + str(following_num) + "  "  + str(followers_num))
        cur.execute(
            insertSql % (int(coinIdList[i]), str(coinNameList[i]), tweets_num, following_num, followers_num, dt))
    # 重新爬取一次
    if re_extract_url_list.__len__() > 0:
        time.sleep(10)
        if(re_extract(re_extract_id_list, re_extract_name_list, re_extract_url_list)):
            logging.info("爬取结束")
        else:
            logging.info("爬取网络有问题")
    cur.close()

#重新爬取函数
def re_extract(coinIdList, coinNameList, coinUrlList):
    re_extract_flag = True
    coin_list_len = coinIdList.__len__()
    for i in range(coin_list_len):
        tweets_num, following_num, followers_num = get_twitterdata(coinUrlList[i])
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if tweets_num == "EOF":
            logging.info("重新爬取失败" + str(int(coinIdList[i])) + "  " + str(coinNameList[i]) + "  " + str(tweets_num) + "  " + str(
                following_num) + "  " + str(followers_num))
            re_extract_flag = False
            continue
        logging.info(str(int(coinIdList[i])) + "  " + str(coinNameList[i]) + "  " + str(tweets_num) + "  " + str(
            following_num) + "  " + str(followers_num))
        cur.execute(
            insertSql % (int(coinIdList[i]), str(coinNameList[i]), tweets_num, following_num, followers_num, dt))
    return re_extract_flag

if __name__ == '__main__':
    logging.info("hello")
    start()


