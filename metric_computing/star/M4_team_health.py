# coding:utf-8
# 计算项目的团队健康度

from config import config
import time
import dbop
import logging
from logging.handlers import TimedRotatingFileHandler
log_fmt = '%(asctime)s %(levelname)s(%(lineno)s): %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(filename="log/team_healty", when="D", interval=1, backupCount=7)
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

def _common_num(dataset1, dataset2):
	data_common = 0
	for item in dataset1:
		if item in dataset2:
			data_common += 1
	return data_common
def computeTeamHealth():

	# 几个重要时间点
	time_now = time.time()
	time_now_str = _strtime_before_days(time_now,0)
	time_before_1_window = _strtime_before_days(time_now, EXAMINE_WINDOW)
	time_before_2_window = _strtime_before_days(time_now, 2*EXAMINE_WINDOW)
	time_before_3_window = _strtime_before_days(time_now, 3*EXAMINE_WINDOW)

	ccrs, ngrs = [], []
	metrics = [ccrs]
	for repo in REPOS:
		# 几个重要集合
		data_before_1_window = [item[0] for item in 
									dbop.select_all("select author_id from commits_info where repo_id=%s and (author_date>%s and author_date<%s)",
												(repo,time_before_1_window,time_now_str)) ] 
		data_before_2_window = [item[0] for item in  
									dbop.select_all("select author_id from commits_info where repo_id=%s and (author_date>%s and author_date<%s)",
												(repo,time_before_2_window,time_before_1_window))]
		data_before_3_window = [item[0] for item in  
									dbop.select_all("select author_id from commits_info where repo_id=%s and (author_date>%s and author_date<%s)",
												(repo,time_before_3_window,time_before_2_window))]

		# ccr
		data_common = _common_num(data_before_1_window, data_before_2_window)
		ccrs.append(data_common*1.0 / (len(data_before_2_window)+1)) #避免分母为0

		# ngr
		new_users_1 = len(data_before_1_window) - data_common  + 1 #避免分母为0
		data_common_2 =  _common_num(data_before_3_window, data_before_2_window)
		new_users_2 = len(data_before_2_window) - data_common_2 + 1 #避免分母为0
		ngrs.append((new_users_1-new_users_2)*1.0/new_users_2)

		# tbr 
	metrics.append(_nor_data(ngrs))
	for i in range(0,len(REPOS)):
		tmp_row = [REPOS[i]]
		for j in range(0,len(metrics)):
			tmp_row.append(metrics[j][i])
		dbop.execute("insert into team_health(repo_id, ccr,ngr) values(%s,%s,%s)",
						tmp_row)



def main():
	logger.info(">>>>>TeamHealth begins to work")
	while True:

		logger.info("\tstart another round of work")
		start_time = time.time()

		computeTeamHealth()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

def init():
	logger.info("init ...")
	readPrjLists()
	dbop.createTeamHealth()


if __name__ == '__main__':
	init()
	main()