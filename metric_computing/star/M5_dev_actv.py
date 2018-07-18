# coding:utf-8
# 计算项目的开发活跃度

from config import config
import time
import dbop
import logging
from logging.handlers import TimedRotatingFileHandler
log_fmt = '%(asctime)s %(levelname)s(%(lineno)s): %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(filename="log/dev_activation", when="D", interval=1, backupCount=7)
log_file_handler.setFormatter(formatter)    
logger = logging.getLogger()
logger.addHandler(log_file_handler)
logger.setLevel(logging.INFO)

REPOS = []
INTERVAL_TIME = config['metric_compute_interval']
EXAMINE_WINDOW = config["examine_window"]
def readPrjLists():
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = [item.strip() for item in prj_line.split("\t")]
			REPOS.append(int(prjls[0]))

def _nor_data(dataSet):
	min_edge = min(dataSet)
	max_edge = max(dataSet)
	dur_edge = max_edge - min_edge
	
	# 如果数组内的元素都相同，直接返回一组0
	if dur_edge == 0:
		return[0]*len(dataSet)

	return [(item*1.0 - min_edge)/dur_edge for item in dataSet]

def _strtime_before_days(base_time, before_days):
	# 返回befor_dayas天前的那一天的24点
	before_time = base_time - before_days * 24*60*60
	before_time = time.strftime('%Y-%m-%d 23:59:59',time.localtime(before_time))
	return before_time

def computeDevActv():
	# 几个重要时间点
	time_now = time.time()
	time_now_str = _strtime_before_days(time_now,0)
	time_before_1_window = _strtime_before_days(time_now, EXAMINE_WINDOW)

	# commits_before_1_window,issues_before_1_window,rel_before_1_window
	cbw, ibw, rbw = [],[],[]
	metrics = [cbw, ibw, rbw]
	for repo in REPOS:
		# 几个重要集合
		cbw.append(dbop.select_one("select count(*) from commits_info where repo_id=%s and (author_date>%s and author_date<%s)",
												(repo,time_before_1_window,time_now_str))[0])
		ibw.append(dbop.select_one("select count(*) from issues_info where repo_id=%s and (created_at>%s and created_at<%s)",
												(repo,time_before_1_window,time_now_str))[0]) 
		rbw.append(dbop.select_one("select count(*) from releases_info where repo_id=%s and (created_at>%s and created_at<%s)",
												(repo,time_before_1_window,time_now_str)) [0])
	nor_metrics = [ _nor_data(item) for item in metrics]
	for i in range(0,len(REPOS)):
		dbop.execute("insert into dev_actv(repo_id,dev,rel) values(%s,%s,%s)",
						(REPOS[i], nor_metrics[0][i]+nor_metrics[1][i],nor_metrics[2][i]))


def main():
	logger.info(">>>>>QualitySub begins to work")
	while True:

		logger.info("\tstart another round of work")
		start_time = time.time()

		computeDevActv()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

def init():
	logger.info("init ...")
	readPrjLists()
	dbop.createDevActv()


if __name__ == '__main__':
	init()
	main()