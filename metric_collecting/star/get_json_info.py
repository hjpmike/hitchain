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
import Queue
import threading

logger = logging.getLogger()
hdlr = logging.FileHandler("log/get_json_info.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

INTERVAL_TIME = config["json_fetch_interval"]
REPO_ID = {}
PRJS = Queue.Queue()
PRJS_DONE = Queue.Queue() #多线程干完活后放到这个里面
DEFAULT_THD_NUM = 3 # 默认线程个数
URL_TEMPLATE = "https://api.github.com/repos/%s/%s?page=%d&per_page=100&state=all&direction=asc"

def _get_url(url,retry_times=3):
	# token池
	send_headers = {"Content-Type":"application/json","Authorization":"*"}
	token = gh_token_pool.get_token()
	if token is None:
		logger.info("\t\t%s: token is none"%(threading.current_thread().name,))
		return None,None

	send_headers['Authorization'] = 'token %s'%(token,)
	gh_token_pool.push_token(token)

	req = urllib2.Request(url,headers = send_headers)
	try:
		error_msg = None
		result = urllib2.urlopen(req,timeout=20)
		raw_data = result.read().decode('utf-8')
		logger.info("\t\t%s: downloaded:\t%s:%s"%(threading.current_thread().name,url[28:-37],token[1:8]))
	except urllib2.HTTPError, e:
		error_msg = e.code
	except urllib2.URLError, e:
		error_msg = e.reason
	except Exception,e:
		error_msg = e.message
		
	if error_msg != None:
		dbop.execute("insert into json_error(url,error) values(%s,%s)", (url, error_msg))
		logger.info("\t\t%s: error_msg:\t%s,%s:%s"%(threading.current_thread().name,error_msg,url[28:-37],token[1:8]))
		if retry_times == 0:
			return None,None
		else:
			logger.info("\t\t%s: retry:\t%s:%s"%(threading.current_thread().name,url[28:-37],token[1:8]))
			return _get_url(url,retry_times-1)
	
	return result, raw_data

def _get_last_issue_fetch(prj,dataType):
	# 获取上次记录，以及上次获得数据集合
	last_page = dbop.select_one("select page from " + "%s_json_raw"%dataType + " where repo_id=%s order by id desc limit 1",
								(REPO_ID[prj],), (1,))[0]
	last_data_set = set([ item[0] for item in 
						dbop.select_all("select number from " +"%s_info"%dataType + " where repo_id=%s and page =%s", (
							REPO_ID[prj],last_page))
						])
	
	return last_page, last_data_set


def _fetchIssueJson4Prj(prj, dataType):

	last_page, last_data_set = _get_last_issue_fetch(prj,dataType)
	logger.info("\t\t%s: %s last %s page:%s/%s"%( threading.current_thread().name,prj,dataType,last_page,len(last_data_set)))
	while last_page is not None:
		
		# 下载原始并存储原始数据
		url =  URL_TEMPLATE%(prj,dataType,last_page)
		result, raw_json = _get_url(url)
		if result is None:
			break

		dbop.execute("insert into " + "%s_json_raw"%dataType +"(repo_id, page, raw) values(%s,%s,%s)", (
							REPO_ID[prj], last_page, raw_json))
		new_data_set = json.loads(raw_json)

		# 抽取
		logger.info("\t\t%s: %s new %s page:%s/%s"%( threading.current_thread().name,prj,dataType,last_page,len(new_data_set)))
		for n_data in new_data_set:
			if n_data["number"] not in last_data_set:
				dbop.execute("insert into " + "%s_info"%dataType + 
						"(repo_id,number,page,created_at,closed_at,user_id,user_name) values (%s,%s,%s,%s,%s,%s,%s)", 
					( REPO_ID[prj],n_data["number"],last_page,n_data["created_at"],
									n_data["closed_at"],n_data["user"]["id"],n_data["user"]["login"]
					))
			
		
		# 以后的last_data_set 应该为空
		last_data_set = []

		# 获取下一个列表页url
		if 'link' not in result.headers.keys():
			logger.info("\t\t%s: %s maybe has less 100 %s"%(threading.current_thread().name, prj,dataType))
			break
		links = result.headers["link"]
		if "next" in links:
			last_page += 1
		else:
			last_page = None
			logger.info("\t\t%s: %s no longer have next link for %s"%(threading.current_thread().name,prj,dataType))
		
def _get_last_release_fetch(prj):
	last_page = dbop.select_one("select page from releases_json_raw where repo_id=%s order by id desc limit 1",
								(REPO_ID[prj],), (1,))[0]
	last_data_set = set([ item[0] for item in 
						dbop.select_all("select r_id from releases_info where repo_id=%s and page =%s", (
							REPO_ID[prj],last_page))])
	
	return last_page, last_data_set

def _fetchReleaseJson4Prj(prj):
	last_page, last_data_set = _get_last_release_fetch(prj)
	logger.info("\t\t%s:%s last release page: %s/%s"%( threading.current_thread().name,prj,last_page,len(last_data_set)))

	while last_page is not None:
		
		# 下载原始并存储原始数据
		url =  URL_TEMPLATE%(prj,"releases",last_page)
		result, raw_json = _get_url(url)
		if result is None:
			break

		dbop.execute("insert into releases_json_raw(repo_id, page, raw) values(%s,%s,%s)", (
							REPO_ID[prj], last_page, raw_json))
		new_data_set = json.loads(raw_json)

		# 抽取
		logger.info("\t\t%s:%s new release page: %s/%s"%( threading.current_thread().name,prj,last_page,len(new_data_set)))
		for n_data in new_data_set:
			if n_data["id"] not in last_data_set:
				dbop.execute("insert into releases_info(" + 
								"repo_id,r_id,page,tag_name,name,created_at,published_at,author_id,author_name)" + 
								" values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
								( REPO_ID[prj],n_data["id"],last_page,n_data["tag_name"],n_data["name"],n_data["created_at"],
								n_data["published_at"],n_data["author"]["id"],n_data["author"]["login"]))
			
		# 以后的last_data_set 应该为空
		last_data_set = []

		# 获取下一个列表页url
		if 'link' not in result.headers.keys():
			logger.info("\t\t%s: %s maybe has less 100 releases"%(threading.current_thread().name, prj))
			break
		links = result.headers["link"]
		if "next" in links:
			last_page += 1
		else:
			last_page = None
			logger.info("\t\t%s: %s no longer have next link for releases"%(threading.current_thread().name,prj))


def _get_last_commit_fetch(prj):
	last_page = dbop.select_one("select page from commits_json_raw where repo_id=%s order by id desc limit 1",
								(REPO_ID[prj],), (1,))[0]
	last_data_set = set([ item[0] for item in 
						dbop.select_all("select sha from commits_info where repo_id=%s and page =%s", (
							REPO_ID[prj],last_page))])
	
	return last_page, last_data_set

def _fetchCommitJson4prj(prj):
	last_page, last_data_set = _get_last_commit_fetch(prj)
	logger.info("\t\t%s:%s last commit page: %s/%s"%( threading.current_thread().name,prj,last_page,len(last_data_set)))

	# commit(id,repo_id,sha,author_id,author_name,author_date,committer_id,committer_name,committer_date,parent)
	while last_page is not None:
		
		# 下载原始并存储原始数据
		url =  URL_TEMPLATE%(prj,"commits",last_page)
		result, raw_json = _get_url(url)
		if result is None:
			break

		dbop.execute("insert into commits_json_raw(repo_id, page, raw) values(%s,%s,%s)", (
							REPO_ID[prj], last_page, raw_json))
		new_data_set = json.loads(raw_json)

		# 抽取
		logger.info("\t\t%s:%s new commit page: %s/%s"%( threading.current_thread().name,prj,last_page,len(new_data_set)))
		for n_data in new_data_set:
			if n_data["sha"] not in last_data_set:
				parents_sha = ";".join([parent["sha"] for parent in n_data["parents"]])
				author = n_data["author"] # author在github的用户名有时为空
				if author is None:
					author_id,author_name = None,None
				else:
					author_id,author_name = author["id"],author["login"]
				committer = n_data["committer"]
				if committer is None:
					commit_id,commiter_name = None,None
				else:
					commit_id,commiter_name = committer["id"],committer["login"]
				dbop.execute("insert into commits_info(" + 
								"repo_id,page,sha,author_id,author_name,author_date,committer_id,committer_name,committer_date,parents)" + 
								" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
								( REPO_ID[prj],last_page,n_data["sha"],
								author_id,author_name,n_data["commit"]["author"]["date"],
								commit_id,commiter_name,n_data["commit"]["committer"]["date"],parents_sha))
			
		# 以后的last_data_set 应该为空
		last_data_set = []

		# 获取下一个列表页url
		if 'link' not in result.headers.keys():
			logger.info("\t\t%s: %s maybe has less 100 commits"%(threading.current_thread().name, prj))
			break
		links = result.headers["link"]
		if "next" in links:
			last_page += 1
		else:
			last_page = None
			logger.info("\t\t%s: %s no longer have next link for commits"%(threading.current_thread().name,prj))


def fetchThread():
	logger.info("\t\t%s starts to work"%( threading.current_thread().name))
	while True:
		try:
			prj = PRJS.get()
			logger.info("\t\t%s fetch %s"%( threading.current_thread().name,prj))
		except Exception,e:
			logger.info("\t\t%s no more prjs"%( threading.current_thread().name))
			break 

		# _fetchIssueJson4Prj(prj, "issues")
		# _fetchIssueJson4Prj(prj, "pulls")
		# _fetchReleaseJson4Prj(prj)
		_fetchCommitJson4prj(prj)

		PRJS_DONE.put(prj)
	

def fetchJsonInfo():
	global PRJS_DONE, PRJS
	# 用多线程进行并行操作
	if len(sys.argv) < 2:
		threading_num = DEFAULT_THD_NUM
	else:
		threading_num = int(sys.argv[1])

	thread_list = [] 
	if threading_num > PRJS.qsize():
		threading_num = PRJS.qsize()
	logger.info("\tthreads number:%d"%(threading_num,))
	for i in range(0,threading_num):
		t = threading.Thread(target=fetchThread,name="Thread-%d"%i)
		thread_list.append(t)

	for thread in thread_list:
		thread.start()
	for thread in thread_list:
		thread.join()

	logger.info("\tall threads done work")
	PRJS = PRJS_DONE
	PRJS_DONE = Queue.Queue()

	
def readPrjLists():
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = [item.strip() for item in prj_line.split("\t")]
			PRJS.put(prjls[1])
			REPO_ID[prjls[1]] = int(prjls[0])

def main():
	global PRJS
	logger.info(">>>>>get_json_info begins to work")
	while True:

		logger.info("\tstart another round of work")
		# 爬完历史信息后，每个一天更新一次e3edx 
		start_time = time.time()

		readPrjLists()
		fetchJsonInfo()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)


def createTable():
	logger.info("\tcreate tables")
	dbop.createJsonError()

	dbop.createIssueJsonRaw("pulls")
	dbop.createIssueJsonRaw("issues")
	dbop.createPrInfo()
	dbop.createIssueInfo()

	dbop.createReleaseJsonRaw()
	dbop.createReleaseInfo()

	dbop.createCommitInfo()
	dbop.createCommitJsonRaw()




def init():
	# 创建表
	logger.info("init...")
	createTable()
if __name__ == '__main__':
	init()
	main()