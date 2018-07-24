#coding=utf-8
import pymysql
import xlrd
import xlwt

dbname='lyz'
user='root'
passwd='111111'
host = '10.107.10.110'

conn =  pymysql.connect(host=host, port=3306, user=user, passwd=passwd, db=dbname,charset='utf8')
conn.autocommit(1)
cur=conn.cursor()

def read_coinProjectList():

    excelData = xlrd.open_workbook(u'bitinfo.xlsx')
    sheet0 = excelData.sheet_by_index(0)
    print(sheet0)
    coinUrlList = sheet0.col_values(9)
    del coinUrlList[0]
    coinIdList = sheet0.col_values(0)
    del coinIdList[0]
    coinNameList = sheet0.col_values(1)
    del coinNameList[0]

    insert_sql = "insert into user_email(id,login,email) values(%d,\'%s\',\'%s\')"

    return coinUrlList


if __name__ == '__main__':
    coinUrlList = read_coinProjectList()

