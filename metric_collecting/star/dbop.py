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
#### funcs created for get_json_info.py
#########################################

def createCommitJsonRaw():
	sql_stat = '''
		CREATE TABLE IF NOT EXISTS `commits_json_raw` (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`repo_id` int(11) DEFAULT NULL,
		`page` int(11) DEFAULT NULL,
		`raw` longtext,
		`fetched_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4
		'''
	execute(sql_stat)
def createCommitInfo():
	sql_stat = '''
		CREATE TABLE IF NOT EXISTS `commits_info` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`repo_id` int(11) DEFAULT NULL,
			`page` int(11) DEFAULT NULL,
			`sha` varchar(40) DEFAULT NULL,
			`author_id` int(11) DEFAULT NULL,
			`author_name` varchar(500) DEFAULT NULL,
			`author_date` varchar(20) DEFAULT NULL,
			`committer_id` int(11) DEFAULT NULL,
			`committer_name` varchar(500) DEFAULT NULL,
			`committer_date` varchar(20) DEFAULT NULL,
			`parents` varchar(210) DEFAULT NULL,
			PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=latin1
		'''
	execute(sql_stat)


def createReleaseJsonRaw():
	sql_stat = '''
		CREATE TABLE IF NOT EXISTS `releases_json_raw` (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`repo_id` int(11) DEFAULT NULL,
		`page` int(11) DEFAULT NULL,
		`raw` longtext,
		`fetched_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4
		'''
	execute(sql_stat)
def createReleaseInfo():
	sql_stat = '''
		CREATE TABLE IF NOT EXISTS `releases_info` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`repo_id` int(11) DEFAULT NULL,
			`page` int(11) DEFAULT NULL,
			`r_id` int(11) DEFAULT NULL,
			`name` varchar(500) DEFAULT NULL,
			`tag_name` varchar(500) DEFAULT NULL,
			`created_at` varchar(20) DEFAULT NULL,
			`published_at` varchar(20) DEFAULT NULL,
			`author_id` int(11) DEFAULT NULL,
			`author_name` varchar(500) DEFAULT NULL,
			PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=latin1
		'''
	execute(sql_stat)

def createIssueJsonRaw():
	sql_stat = '''
		CREATE TABLE IF NOT EXISTS `issues_json_raw` (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`repo_id` int(11) DEFAULT NULL,
		`page` int(11) DEFAULT NULL,
		`raw` longtext,
		`fetched_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4
		'''
	execute(sql_stat)
def createIssueInfo():
	sql_stat = '''
		CREATE TABLE IF NOT EXISTS `issues_info` (
			`id` int(11) NOT NULL AUTO_INCREMENT,
			`repo_id` int(11) DEFAULT NULL,
			`page` int(11) DEFAULT NULL,
			`number` int(11) DEFAULT NULL,
			`is_pr` tinyint(1) DEFAULT NULL,
			`created_at` varchar(20) DEFAULT NULL,
			`closed_at` varchar(20) DEFAULT NULL,
			`user_id` int(11) DEFAULT NULL,
			`user_name` varchar(500) DEFAULT NULL,
			PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=latin1
		'''
	execute(sql_stat)


def createJsonError():
	sql_stat = '''
		CREATE TABLE IF NOT EXISTS `json_error` (
		`id` int(11) NOT NULL AUTO_INCREMENT,
		`url` varchar(250) DEFAULT NULL,
		`error` varchar(500) DEFAULT NULL,
		`error_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (`id`)
		) ENGINE=MyISAM DEFAULT CHARSET=latin1
		'''
	execute(sql_stat)


#########################################
#### funcs created for get_html_info.py
#########################################
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
	execute(html_error_sql)

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
	execute(html_info_sql)