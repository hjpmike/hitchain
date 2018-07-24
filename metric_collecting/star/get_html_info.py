#coding:utf-8
'''
created by starlee @ 2018-07-13 15:00
for fetching raw infos from html
'''
import time
import logging
import urllib2
from config import config
from lxml import etree
import dbop

from logging.handlers import TimedRotatingFileHandler
log_fmt = '%(asctime)s %(levelname)s(%(lineno)s): %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(filename="log/get_html_info", when="D", interval=1, backupCount=7)
log_file_handler.setFormatter(formatter)    
logger = logging.getLogger()
logger.addHandler(log_file_handler)
logger.setLevel(logging.INFO)


INTERVAL_TIME = config["html_fetch_interval"]
REPO_ID = {}
def readPrjLists():
	result = dbop.select_all("select prj_id,github_url from prj_list")
	for prj in result:
		if prj[1] is not None:
			repo_name =  prj[1][19:]
			prjs.append(repo_name)
			REPO_ID[repo_name] = int(prj[0])
	return prjs

def _uni_field(field):
	# contributor,release,commit,branch 存在单复数区别
	if not field.endswith("s"):
		if field.endswith("h"):
			return field + "es"
		else:
			return field + "s"
	else:
		return field

def _extract_html(ini_html):
	nums = {}
	errors = []
	# watch,star,fork
	lis = etree.HTML(ini_html).xpath('//*/ul[@class="pagehead-actions"]/li')
	# !!! 应该要判断该规则是否还有效
	for li in lis:
		try:
			tmp_text = li.xpath("./a[1]/text()")[-1].strip()
			tmp_num = li.xpath("./a[2]/text()")[0].strip()
			nums[tmp_text] = tmp_num.replace(",", "")
		except Exception,e:
			logger.error("\t\t\tstar-fork-watch:%s"%e)
			errors.append("star-fork-watch:%s"%e)
	
	#contributor,release,commit,branch
	# # !!! 应该要判断该规则是否还有效
	lis = etree.HTML(ini_html).xpath('//*/ul[@class="numbers-summary"]/li/a')
	for lia in lis:
		try:
			tmp_txt = _uni_field(lia.xpath("./text()")[-1].strip())
			if tmp_txt not in ["commit","commits","branch","branches","release","releases",
									"contributor","contributors"]:
				print tmp_txt
				continue
			tmp_num = lia.xpath("./span")[0].text.strip()
			nums[tmp_txt] = tmp_num.replace(",","")
		except Exception,e:
			logger.error("\t\t\tommitj-branch:%s"%e)
			errors.append("commitj-branch:%s"%e)
	
	return nums,errors

def _get_url(url,retry_times=3):
	req = urllib2.Request(url)
	try:
		error_msg = None
		# !!!要判断返回的是否是正常页面，比如url本身就是错的
		ini_html = urllib2.urlopen(req,timeout=20).read().lower().decode('utf-8')
	except urllib2.HTTPError, e:
		error_msg = e.code
	except urllib2.URLError, e:
		error_msg = e.reason
	except Exception,e:
		error_msg = e.message

	if error_msg != None:
		logger.error("\t\t\t error:\t%s,%s"%(error_msg,url))
		if retry_times > 0:
			return _get_url(url,retry_times-1)
		else:
			return (None, error_msg)
	return (ini_html,)

def fetchHtmlInfo(prj):

	logger.info("\t\tfetchHtmlInfo:%s"%(prj))
	# 下载
	logger.info("\t\t download")
	url = "https://github.com/%s"%prj
	url_result = _get_url(url)
	if url_result[0] is None:
		dbop.execute("insert into html_error(repo_id,error_msg) values(%s,%s)",(REPO_ID[prj],url_result[1]))
		return 

	logger.info("\t\t extract")
	# 抽取
	ini_html = url_result[0]
	nums, errors = _extract_html(ini_html)

	logger.info("\t\t store")
	# 持久化
	fields = nums.keys()
	if len(fields) > 0:
		values = [nums[field] for field in fields]
		values.insert(0,"%d"%REPO_ID[prj])
		dbop.execute("insert into html_info(repo_id," + ",".join(fields) + ") values(%s" + ",%s"*len(fields) +")",(values))
	for error in errors:
		dbop.execute("insert into html_error(repo_id,error_msg) values(%s,%s)",(REPO_ID[prj],error))


def main():
	logger.info(">>>>>get_html_info begins to work")
	while True:
		logger.info("\tstart another round of work")
		# 爬完历史信息后，每个一天更新一次
		start_time = time.time()

		prjs = readPrjLists()
		for prj in prjs:
			fetchHtmlInfo(prj)
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)


def createTables():
	# !!!创建一个表html_info_error(repo_id,repo_name,error_msg,error_at)
	logger.info("\t create tables")
	dbop.createHtmlInfo()
	dbop.createHtmlError()


def init():
	#应该查看数据库表等是否存在
	logger.info("init...")
	createTables()

if __name__ == '__main__':
	init()
	main()