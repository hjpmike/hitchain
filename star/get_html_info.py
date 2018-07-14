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

logger = logging.getLogger()
hdlr = logging.FileHandler("log/get_html_info.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


INTERVAL_TIME = config["html_fetch_interval"]
REPO_ID = {}
def readPrjLists():
	prjs = []
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = prj_line.split("\t")
			prjs.append(prjls[1])
			REPO_ID[prjls[1]] = int(prjls[0])
	return prjs


def extract_html(prj,ini_html):
	nums = {}
	# watch,star,fork
	lis = etree.HTML(ini_html).xpath('//*/ul[@class="pagehead-actions"]/li')
	# !!! 应该要判断该规则是否还有效
	for li in lis:
		try:
			tmp_text = li.xpath("./a[1]/text()")[-1].strip()
			tmp_num = li.xpath("./a[2]/text()")[0].strip()
			nums[tmp_text] = tmp_num.replace(",", "")
		except Exception,e:
			logger.error(e)
			dbop.storeHtmlError(REPO_ID[prj],e)
	
	#contributor,release,commit,branch
	# # !!! 应该要判断该规则是否还有效
	lis = etree.HTML(ini_html).xpath('//*/ul[@class="numbers-summary"]/li/a')
	for lia in lis:
		try:
			tmp_txt = lia.xpath("./text()")[-1].strip()
			tmp_num = lia.xpath("./span")[0].text.strip()
			nums[tmp_txt] = tmp_num.replace(",","")
		except Exception,e:
			if(tmp_txt != "mit"):
				logger.error(e)
				dbop.storeHtmlError(REPO_ID[prj],e)
	
	dbop.storeHtmlNums(REPO_ID[prj],nums)

def fetchHtmlInfo(prj):
	url = "https://github.com/%s"%prj
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
		# !!!!!应该持久化 错误信息
		logger.error("error_msg:\t%s,%s"%(error_msg,url))
		dbop.storeHtmlError(REPO_ID[prj],error_msg)
		return

	extract_html(prj,ini_html)

def main():
	while True:

		logger.info("start another round of work")
		# 爬完历史信息后，每个一天更新一次
		start_time = time.time()

		prjs = readPrjLists()
		for prj in prjs:
			fetchHtmlInfo(prj)
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("not enough interval, sleep a while")
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