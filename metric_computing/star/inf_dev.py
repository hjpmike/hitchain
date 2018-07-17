# coding:utf-8
# 计算项目的开发社区影响力

from config import config
import time
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
	print "update_separate_metric"

def compute_nor_metric():
	print "compute_nor_metric"

def computeINF_DEV():
	# 先更新各个指标的最新数值
	update_separate_metric()

	# 再计算归一化的数值
	compute_nor_metric()

def main():
	logger.info(">>>>>inf_dev begins to work")
	while True:

		logger.info("\tstart another round of work")
		start_time = time.time()

		readPrjLists()
		computeINF_DEV()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

if __name__ == '__main__':
	main()