# coding:utf-8
# 计算项目的主观质量

from config import config
import time
import dbop
import logging
from logging.handlers import TimedRotatingFileHandler
log_fmt = '%(asctime)s %(levelname)s(%(lineno)s): %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(filename="log/quality_sub", when="D", interval=1, backupCount=7)
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


def _time_str4int(time_str):
	return time.mktime(time.strptime(time_str,"%Y-%m-%dT%H:%M:%SZ"))

def computeQualitySub():

	# 缺陷修复比例，平均修复时间
	repair_ratio, repair_time = [],[]
	metrics = [repair_ratio, repair_time]
	for repo in REPOS:


		# issue_total,done
		result = dbop.select_all("select closed_at,created_at from issues_info where repo_id=%s and is_pr=0",(repo,))
		total_num = len(result)
		if total_num == 0:
			tmp_repair_ratio = 0
			tmp_repair_time = 0
		else:
			issue_done = [item for item in result if item[0] is not None]
			tmp_repair_ratio = len(issue_done)*1.0 / total_num
			tmp_repair_time = sum( [_time_str4int(item[0]) - _time_str4int(item[1]) 
										for item in issue_done])*1.0 / len(issue_done)

		repair_ratio.append(tmp_repair_ratio)
		repair_time.append(tmp_repair_time)

	repair_time = _nor_data(repair_time)
	for i in range(0,len(REPOS)):
		dbop.execute("insert into quality_sub(repo_id,repair_ratio,repair_time) values(%s,%s,%s)",
					(REPOS[i],repair_ratio[i],repair_time[i]))


def main():
	logger.info(">>>>>QualitySub begins to work")
	while True:

		logger.info("\tstart another round of work")
		start_time = time.time()

		computeQualitySub()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

def init():
	logger.info("init ...")
	readPrjLists()
	dbop.createQualitySub()


if __name__ == '__main__':
	init()
	main()