#coding:utf-8
'''
created by starlee @ 2018-07-13 15:00
for fetching raw infos from html
'''
import time
import logging
 
logger = logging.getLogger()
hdlr = logging.FileHandler("log/get_html_info.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)


INTERVAL_TIME = 6 #in seconds

def readPrjLists():
	prjs = []
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = prj_line.split("\t")
			prjs.append(prjls[0])
	return prjs


def fetchHtmlInfo(prj):
	pass

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


if __name__ == '__main__':
	main()