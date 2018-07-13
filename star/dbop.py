#coding:utf-8

from config import config
import MySQLdb

conn = MySQLdb.connect(config["db_host"],config["db_user"], 
							config["db_passwd"],config["db_name"],charset='utf8mb4')


def storeHtmlNums(nums):
	print "store html nums"

def createHtmlInfo():
	html_info_sql = '''
	CREATE TABLE IF NOT EXISTS `html_info`  (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`repo_id` int(11) DEFAULT NULL,
		`star` int(11) DEFAULT NULL,
		`fork` int(11) DEFAULT NULL,
		`watch` int(11) DEFAULT NULL,
		`commit` int(11) DEFAULT NULL,
		`branch` int(11) DEFAULT NULL,
		`release` int(11) DEFAULT NULL,
		`contributor` int(11) DEFAULT NULL,
		`fetched_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=latin1
	'''
	cursor = conn.cursor()
	cursor.execute(html_info_sql)