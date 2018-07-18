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


def computeINF_DEV():

	deltas = [[],[],[]]
	for repo in REPOS:

		# 先提取出范围指标，!! 为方便起见，就对某个repo的记录按照采集的时间取最后30个
		result = dbop.select_all("select watch,star,fork from html_info where repo_id=%s order by id desc limit %s",
					(repo,EXAMINE_WINDOW))

		metric_now = result[0]
		# 如果历史数据不足以一个窗口期，那就默认为0。虽然一开始部署时，前一个窗口期内计算得到的数值都会偏大，但是归一化后就可以了
		if len(result) < EXAMINE_WINDOW:
			metric_before = [0,0,0] 
		else:
			metric_before = result[-1]

		# 计算指标变化量, !!还真有变少的，
		for i in range(0,3):
			deltas[i].append(metric_now[i] - metric_before[i])

	print deltas

	nor_deltas = []
	for delta in deltas:
		nor_deltas.append(_nor_data(delta))

	for i in range(0,len(REPOS)):
		row_delta = []
		for j in range(0,len(nor_deltas)):
			row_delta.append(nor_deltas[j][i])
		row_delta.insert(0,REPOS[i])
		row_delta.append(sum(row_delta))
		dbop.execute("insert into inf_dev(repo_id,watch,star,fork,inf_dev) values(%s,%s,%s,%s,%s)", row_delta)

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


if __name__ == '__main__':
	init()
	main()