#coding:utf-8

from config import config
import MySQLdb

conn = MySQLdb.connect(config["db_host"],config["db_user"], 
							config["db_passwd"],config["db_name"],charset='utf8mb4')



