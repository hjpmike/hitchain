#coding:utf-8
'''
created by starlee @ 2018-07-14 10:45
for fetching json infos
'''
import time
import logging
import sys
import dbop
from config import config
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

def _get_url(url):
	# token池
	req = urllib2.Request(url,timeout=20)
	try:
		error_msg = None
		result = urllib2.urlopen(req,timeout=20)
		raw_data = result.read().decode('utf-8')
		logger.info("\t: %s"%(url,))
	except urllib2.HTTPError, e:
		error_msg = e.code
	except urllib2.URLError, e:
		error_msg = e.reason
	except Exception,e:
		error_msg = e.message
		
	if error_msg != None:
		cursor = conn.cursor()
		cursor.execute("insert into json_error(url,error,error_at) values(%s,%s,%s)",
						(lst_url, error_msg, time.strftime('%Y-%m-%d %H:%M:%S')))
		cursor.close()
		conn.commit()
		logger.info("%s: error_msg:\t%s,%s"%(threading.current_thread().name,error_msg,lst_url,))
		return None,None
	
	return result, raw_data

def _get_last_fetch(prj,dataType):
	# 获取上次记录，以及上次获得数据集合
	json_raw_id, last_page = dbop.select_one("select id,page from %s_json_raw where repo_id =%s order by id desc limit 1"%(data_Type, REPO_ID[prj]), 1)
	last_data_set = set([ item[0] for item in 
				dbop.select_all("select pr_num from %s_info where json_raw_id =%s"%(dataType,json_raw_id))])
	
	return last_page, last_data_set


def _fetchJson(prj, dataType):

	last_page, last_data_set = _get_last_fetch(prj,dataType)

	while last_page is not None:
		url =  URL_TEMPLATE%(prj,dataType,last_page)
		result, raw_json = _get_url(url)
		if result is None:
			break

		dbop.execute("insert into %s_json_raw(repo_id, page, raw) vlaues(%s,%s,%s)"%(
							dataType, REPO_ID[prj], last_page, raw_json))
		new_data_set = json.loads(raw_json)
		for n_data in new_date_set:
			if n_date["number"] not in last_data_set:
				pass # 存储数据
		
		# 获取下一个列表页url
		if 'link' not in result.headers.keys():
			logger.info("%s: maybe %s has less 100 prs"%(threading.current_thread().name, prj))
			break

		links = result.headers["link"]
		if "next" in links:
			last_page = links[1:links.index(">")]
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

		_fetchJson(prj, "issues")
		_fetchJson(prj, "pulls")

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
			prjls = prj_line.split("\t")
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