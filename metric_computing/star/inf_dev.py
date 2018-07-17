# coding:utf-8
# 计算项目的开发社区影响力

from config import config
import time
import dbop
import logging
from logging.handlers import TimedRotatingFileHandler
log_fmt = '%(asctime)s %(levelname)s(%(lineno)s): %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(filename="log/inf_dev", when="D", interval=1, backupCount=7)
log_file_handler.setFormatter(formatter)    
logger = logging.getLogger()
logger.addHandler(log_file_handler)
logger.setLevel(logging.INFO)

REPOS, REPO_ID = [], {}
INTERVAL_TIME = config['metric_compute_interval']
	
def readPrjLists():
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = [item.strip() for item in prj_line.split("\t")]
			REPOS.append(prjls[1])
			REPO_ID[prjls[1]] = int(prjls[0])


def update_separate_metric():
	# 首先遍历更新每个项目 每个指标的最新数值
	for repo in REPOS:
		result = dbop.select_one("select watch,star,fork from html_info where repo_id=%s order by id desc limit 1",(REPO_ID[repo],))
		if result is None:
			logger.info("no lastest html info for repo:%s"%REPO_ID[repo])
			continue
		dbop.execute("update inf_dev set watch=%s,star=%s,fork=%s where repo_id=%s", 
						(result[0],result[1],result[2],REPO_ID[repo]))
		logger.info("\t\t   update html info for repo:%s"%REPO_ID[repo])

def compute_nor_metric():
	print "update_separate_metric"
	

def computeINF_DEV():
	# 先更新各个指标的最新数值
	logger.info("\t\t update separate metrics")
	update_separate_metric()


	# 再计算归一化的数值
	logger.info("\t\t update nor metrics")
	compute_nor_metric()

def main():
	logger.info(">>>>>inf_dev begins to work")
	while True:

		logger.info("\tstart another round of work")
		start_time = time.time()

		computeINF_DEV()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

def init():
	logger.info("init ...")
	readPrjLists()
	dbop.createINF_DEV()
	for repo in REPOS:
		if dbop.select_one("select * from inf_dev where repo_id=%s",(REPO_ID[repo],)) is None:
			logger.info("  init row for repo:%s"%(REPO_ID[repo]))
			dbop.execute("insert into inf_dev(repo_id) values(%s)", 
						(REPO_ID[repo],))

if __name__ == '__main__':
	init()
	main()