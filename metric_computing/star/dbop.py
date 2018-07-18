#coding:utf-8

from config import config
import MySQLdb
import Queue

#########################################
### 一些可以执行简单sql语句的函数
#########################################
THREAD_POOL = Queue.Queue()
for i in range(0,config["db_conn_pool_size"]):
	conn =  MySQLdb.connect(config["db_host"],config["db_user"], 
							config["db_passwd"],config["db_name"],charset='utf8mb4')
	THREAD_POOL.put(conn)
def get_conn():
	conn = THREAD_POOL.get()
	try:
		conn.ping()
	except Exception,e:
		conn = MySQLdb.connect(config["db_host"],config["db_user"], 
							config["db_passwd"],config["db_name"],charset='utf8mb4')
		THREAD_POOL.put(conn)
	return conn
def put_conn(conn):
	THREAD_POOL.put(conn)	

def execute(sql_stat,params=None):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(sql_stat,params)
	conn.commit()
	cursor.close()
	put_conn(conn)

def select_one(sql_stat, params,none_return_value=None):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(sql_stat,params)
	result = cursor.fetchone()
	conn.commit()
	cursor.close()
	put_conn(conn)
	if result is None:
		return none_return_value
	else:
		return result

def select_all(sql_stat,params=None):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(sql_stat,params)
	result = cursor.fetchall()
	conn.commit()
	cursor.close()
	put_conn(conn)
	return result

#########################################
#### funcs created for inf_dev.py
#########################################

def createINF_DEV():
	html_info_sql = '''
	CREATE TABLE IF NOT EXISTS `inf_dev`  (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`repo_id` int(11) DEFAULT NULL,
		`star` int(11) DEFAULT NULL,
		`fork` int(11) DEFAULT NULL,
		`watch` int(11) DEFAULT NULL,
		`inf_dev` double DEFAULT NULL,
		`computed_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=latin1
	'''
	execute(html_info_sql)

def createMaturity():
	html_info_sql = '''
	CREATE TABLE IF NOT EXISTS `maturity`  (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`repo_id` int(11) DEFAULT NULL,
		`issue_done` double(4,3) DEFAULT NULL,
		`commit_total` double(4,3) DEFAULT NULL,
		`age_dev` double(4,3) DEFAULT NULL,
		`fans_dev` double(4,3) DEFAULT NULL,
		`computed_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=latin1
	'''
	execute(html_info_sql)