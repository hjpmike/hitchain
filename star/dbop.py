#coding:utf-8

from config import config
import MySQLdb

conn = MySQLdb.connect(config["db_host"],config["db_user"], 
							config["db_passwd"],config["db_name"],charset='utf8mb4')
							
#########################################
### 一些可以执行简单sql语句的函数
#########################################
def execute(sql_stat):
	cursor = conn.cursor()
	cursor.execute(sql_stat)
	conn.commit()
	cursor.close()

def select_one(sql_stat):
	cursor = conn.cursor()
	cursor.execute(sql_stat)
	result = cursor.fetchone()
	conn.commit()
	cursor.close()
	return result

def select_all(sql_stat):
	cursor = conn.cursor()
	cursor.execute(sql_stat)
	result = cursor.fetchall()
	conn.commit()
	cursor.close()
	return result

#########################################
#### funcs created for get_json_info.py
#########################################
def createJsonRaw(dat_type):
	pass

def createPrInfo():
	pass

def createIssueInfo():
	pass

#########################################
#### funcs created for get_html_info.py
#########################################
def storeHtmlError(repo_id,error_msg):
	cursor = conn.cursor()
	sql_stat = "insert into html_error(repo_id,error_msg) values(%s,'%s')"%(repo_id,error_msg)
	cursor.execute(sql_stat)
	conn.commit()
	cursor.close()

def storeHtmlNums(repo_id, nums):
	cursor = conn.cursor()
	fields = nums.keys()
	values = [nums[field] for field in fields]
	values.insert(0,"%d"%repo_id)

	sql_stat = "insert into html_info(repo_id,%s) values(%s)"%(",".join(fields), ",".join(values))
	cursor.execute(sql_stat)
	cursor.close()

def createHtmlError():
	html_error_sql = '''
		CREATE TABLE IF NOT EXISTS`html_error` (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`repo_id` int(11) DEFAULT NULL,
		`error_msg` text,
		`error_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=latin1
	'''
	cursor = conn.cursor()
	cursor.execute(html_error_sql)
	cursor.close()

def createHtmlInfo():
	html_info_sql = '''
	CREATE TABLE IF NOT EXISTS `html_info`  (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`repo_id` int(11) DEFAULT NULL,
		`star` int(11) DEFAULT NULL,
		`fork` int(11) DEFAULT NULL,
		`watch` int(11) DEFAULT NULL,
		`commits` int(11) DEFAULT NULL,
		`branches` int(11) DEFAULT NULL,
		`releases` int(11) DEFAULT NULL,
		`contributors` int(11) DEFAULT NULL,
		`fetched_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=latin1
	'''
	cursor = conn.cursor()
	cursor.execute(html_info_sql)
	cursor.close()