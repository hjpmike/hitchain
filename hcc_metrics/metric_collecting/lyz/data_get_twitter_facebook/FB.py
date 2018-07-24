#coding=utf-8
import xlrd
import requests
import pymysql
import datetime
from bs4 import BeautifulSoup


dbname='exper'
user='root'
passwd=''
conn =  pymysql.connect(host='127.0.0.1', port=3306, user=user, passwd=passwd, db=dbname,charset='utf8')
conn.autocommit(1)
cur=conn.cursor()

def insert_value(id, name,likenum,watchnum ):
    insert_sql="insert into fb_data(coin_id,fb_name,likes_num,watches_num,update_time) VALUES(%d,\'%s\',%d,%d,\'%s\')"
    dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(insert_sql%(id, name,likenum,watchnum,dt ))

# def update_value(id,likenum,watchnum ):
#     update_sql="update fb_data set likes_num=%d,watches_num=%d where id=%d"
#     cur.execute(update_sql % (likenum, watchnum,id))
def convert_value(numstring):
    tmpnum=numstring.split(",")
    if len(tmpnum)==2:
        return int(tmpnum[0])*1000+int(tmpnum[1])
    else:
        return int(tmpnum[0])
if __name__=='__main__':
    path='bitinfo.xlsx'
    data=xlrd.open_workbook(path)
    sheets=data.sheets()
    sheet_1_by_name=data.sheet_by_name(u'Sheet1')
    n_of_rows=sheet_1_by_name.nrows
    cnt=0
    for i in range(1,n_of_rows):
        link=sheet_1_by_name.row_values(i)[8]
        id=sheet_1_by_name.row_values(i)[0]
        name=sheet_1_by_name.row_values(i)[1]
        if len(link)!=0:
            cnt+=1
            response = requests.get(link)
            soup = BeautifulSoup(response.text)
            res = soup.find_all(name='div', attrs={"class": "_4bl9"})
            try:
                if len(res)>=3:

                    likenum=convert_value(res[1].text.split(" ")[0])
                    watchnum=convert_value(res[2].text.split(" ")[0])
                    insert_value(id,name,likenum,watchnum )
                    print("yes")

            except:
                pass
        else:
            insert_value(id, name, 0, 0)
            print("value 0")
    print(cnt)