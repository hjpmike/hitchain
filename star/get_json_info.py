#coding:utf-8
'''
created by starlee @ 2018-07-14 10:45
for fetching json infos
'''
import time
import urllib2
import json
import logging
import sys
import dbop
from config import config
import gh_token_pool
import threading
lock = threading.RLock()

logger = logging.getLogger()
hdlr = logging.FileHandler("log/get_json_info.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

INTERVAL_TIME = config["json_fetch_interval"]
REPO_ID = {}
PRJS = []
PRJS_DONE = [] #多线程干完活后放到这个里面
DEFAULT_THD_NUM = 3 # 默认线程个数
URL_TEMPLATE = "https://api.github.com/repos/%s/%s?page=%d&per_page=100&state=all&direction=asc"

def _get_url(url,retry_times=3):
	# token池
	send_headers = {"Content-Type":"application/json","Authorization":"*"}
	token = gh_token_pool.get_token()
	if token is None:
		return None,None
	send_headers['Authorization'] = 'token %s'%(token,)
	gh_token_pool.push_token(token)

	req = urllib2.Request(url,headers = send_headers)
	try:
		error_msg = None
		result = urllib2.urlopen(req,timeout=20)
		raw_data = result.read().decode('utf-8')
		logger.info("%s: download:\t%s:%s"%(threading.current_thread().name,url,token[1:8]))
	except urllib2.HTTPError, e:
		error_msg = e.code
	except urllib2.URLError, e:
		error_msg = e.reason
	except Exception,e:
		error_msg = e.message
		
	if error_msg != None:
		dbop.execute("insert into json_error(url,error) values(%s,%s)", (url, error_msg))
		logger.info("%s: error_msg:\t%s,%s:%s"%(threading.current_thread().name,error_msg,url,token[1:8]))
		if retry_times == 0:
			return None,None
		else:
			logger.info("%s: retry:\t%s:%s"%(threading.current_thread().name,url,token[1:8]))
			return _get_url(url,retry_times-1)
	
	return result, raw_data

def _get_last_fetch(prj,dataType):
	# 获取上次记录，以及上次获得数据集合
	last_page = dbop.select_one("select page from " + "%s_json_raw"%dataType + " where repo_id=%s order by id desc limit 1",
								(REPO_ID[prj],), (1,))[0]
	last_data_set = set([ item[0] for item in 
						dbop.select_all("select number from " +"%s_info"%dataType + " where repo_id=%s and page =%s", (
							REPO_ID[prj],last_page))
						])
	
	return last_page, last_data_set


def _fetchIssueJson4Prj(prj, dataType):

	last_page, last_data_set = _get_last_fetch(prj,dataType)

	while last_page is not None:
		url =  URL_TEMPLATE%(prj,dataType,last_page)
		result, raw_json = _get_url(url)
		if result is None:
			break

		dbop.execute("insert into " + "%s_json_raw"%dataType +"(repo_id, page, raw) values(%s,%s,%s)", (
							REPO_ID[prj], last_page, raw_json))
		new_data_set = json.loads(raw_json)

		for n_data in new_data_set:

			if n_data["number"] not in last_data_set:
				dbop.execute("insert into " + "%s_info"%dataType + "(repo_id,number,page,created_at,closed_at,user_id,user_name) values (%s,%s,%s,%s,%s,%s,%s)", 
					( REPO_ID[prj],n_data["number"],last_page,n_data["created_at"],
									n_data["closed_at"],n_data["user"]["id"],n_data["user"]["login"]
					))
			
		
		# 以后的last_data_set 应该为空
		last_data_set = []

		# 获取下一个列表页url
		if 'link' not in result.headers.keys():
			logger.info("%s: maybe %s has less 100 prs"%(threading.current_thread().name, prj))
			break
		links = result.headers["link"]
		if "next" in links:
			last_page += 1
		else:
			last_page = None
			logger.info("%s: %s %s"%(threading.current_thread().name,prj, "no next link any more",))
		


def fetchThread():
	logger.info("%s start to work"%( threading.current_thread().name))
	while True:
		lock.acquire()
		try:
			prj = PRJS.pop(0)
			logger.info("%s fetch %s"%( threading.current_thread().name,prj))
		except Exception,e:
			logger.info("%s no more prjs"%( threading.current_thread().name))
			break 
		finally:
			lock.release()

		# _fetchJson(prj, "issues")
		_fetchIssueJson4Prj(prj, "pulls")

		lock.acquire()
		try:
			PRJS_DONE.append(prj)
		finally:
			lock.release()


def fetchJsonInfo():
	global PRJS_DONE, PRJS
	# 用多线程进行并行操作
	if len(sys.argv) < 2:
		threading_num = DEFAULT_THD_NUM
	else:
		threading_num = int(sys.argv[1])

	thread_list = [] 
	if threading_num > len(PRJS):
		threading_num = len(PRJS)

	for i in range(0,threading_num):
		t = threading.Thread(target=fetchThread,name="Thread-%d"%i)
		thread_list.append(t)

	for thread in thread_list:
		thread.start()
	for thread in thread_list:
		thread.join()

	logger.info("all threads done work")
	PRJS = PRJS_DONE
	PRJS_DONE = []

	
def readPrjLists():
	prjs = []
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = [item.strip() for item in prj_line.split("\t")]
			prjs.append(prjls[1])
			REPO_ID[prjls[1]] = int(prjls[0])
	return prjs

def main():
	global PRJS
	while True:

		logger.info("start another round of work")
		# 爬完历史信息后，每个一天更新一次
		start_time = time.time()

		PRJS = readPrjLists()
		fetchJsonInfo()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("not enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

def launchTokenPool():
	pass
def createTable():
	dbop.createJsonRaw("pulls")
	dbop.createJsonRaw("issues")
	dbop.createPrInfo()
	dbop.createIssueInfo()

def init():
	# 启动token池 
	launchTokenPool()
	# 创建表
	createTable()
if __name__ == '__main__':
	init()
	main()