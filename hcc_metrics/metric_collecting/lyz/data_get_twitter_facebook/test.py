#coding=utf-8
import requests
import pymysql
from bs4 import BeautifulSoup
import xlrd
import datetime

dbname='lyz'
user='root'
passwd='111111'
host = '10.107.10.110'

conn =  pymysql.connect(host=host, port=3306, user=user, passwd=passwd, db=dbname,charset='utf8')
conn.autocommit(1)
cur=conn.cursor()
insertSql = "insert into twitters_data(coin_id, name, tweets_num, following_num, followers_num, created_time) values ('%d', '%s', '%d', '%d', '%d', '%s')"
insertSql_null = "insert into twitters_data(coin_id, name, created_time) values ('%d', '%s', '%s')"


def get_twitterdata(coin_url):
    if coin_url == "":
        return 0, 0, 0

    print(coin_url)
    try:
        response = requests.get(coin_url).text
    except:
        print("getUrlResponseFailed!: ", coin_url)
        return "EOF","EOF","EOF"
    soup = BeautifulSoup(response, "lxml")
    soup = soup.ul


    # json_res = soup.find(attrs = {'class': 'ProfileNav-item ProfileNav-item--favorites','span':'ProfileNav-value'})



    json_response = soup.find_all(onclick='ProfileNav-list')
    flag = 0
    # 判断有些类似Aeternity项目的类型格式
    try:
        tweets_num = int(json_response[0].attrs['data-count'])
        following_num = int(json_response[1].attrs['data-count'])
        followers_num = int(json_response[2].attrs['data-count'])
    except :
        flag = 1

    if flag == 1:
        try:
            tweets_num = int(json_response[0].attrs['data-count'])
            following_num = 0
            followers_num = int(json_response[1].attrs['data-count'])
        except:
            tweets_num, following_num, followers_num = 0, 0, 0

    return tweets_num, following_num, followers_num

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


def start():
    coinIdList, coinNameList, coinUrlList = read_coinProjectList()
    coin_list_len = coinIdList.__len__()
    for i in range(coin_list_len):
        tweets_num, following_num, followers_num = get_twitterdata(coinUrlList[i])
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if tweets_num == "EOF":
            cur.execute(insertSql_null % (int(coinIdList[i]), str(coinNameList[i]), dt))
            continue
        print(str(int(coinIdList[i])) + "  " + str(coinNameList[i]) + "  " + str(tweets_num) + "  "  + str(following_num) + "  "  + str(followers_num))
        cur.execute(
            insertSql % (int(coinIdList[i]), str(coinNameList[i]), tweets_num, following_num, followers_num, dt))
    cur.close()

if __name__ == '__main__':
    start()


