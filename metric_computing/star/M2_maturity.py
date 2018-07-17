# coding:utf-8
# 计算项目的项目成熟度

from config import config
import time
import dbop
import logging
from logging.handlers import TimedRotatingFileHandler
log_fmt = '%(asctime)s %(levelname)s(%(lineno)s): %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(filename="log/maturity", when="D", interval=1, backupCount=7)
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



def _continuous_dev_month(data):
	month_rec = set()
	for item in data:
		dev_date = item[0]
		dev_date = dev_date.split("T")[0]
		dev_date = "-".join(dev_date.split("-")[0:-1])
		month_rec.add(dev_date)
	return len(month_rec)

def _nor_data(dataSet):
	min_edge = min(dataSet)
	max_edge = max(dataSet)
	dur_edge = max_edge - min_edge
	
	# 如果数组内的元素都相同，直接返回一组0
	if dur_edge == 0:
		return[0]*len(dataSet)

	return [(item*1.0 - min_edge)/dur_edge for item in dataSet]


def computeMaturity():
	# maturity: repo_id, issue_done, commit_total, age_dev, fans_dev
	
	issue_done, commit_total, age_dev, stars,watchs,forks = [],[],[],[],[],[]
	metrics = [issue_done, commit_total, age_dev, stars,watchs,forks]

	# 获取每个指标
	for repo in REPOS:

		# issue_done
		result = dbop.select_one("select count(*) from issues_info where repo_id=%s and is_pr=0 and closed_at is not NULL",(REPO_ID[repo],))
		issue_done.append(result[0])

		# commit_total
		result = dbop.select_one("select count(*) from commits_info where repo_id=%s",(REPO_ID[repo],))
		commit_total.append(result[0])

		# age_dev
		result = dbop.select_all("select author_date from commits_info where repo_id =%s",(REPO_ID[repo],))
		age_dev.append(_continuous_dev_month(result))

		# fans_dev
		result = dbop.select_all("select watch,star,fork from html_info where repo_id=%s order by id desc limit 1",(REPO_ID[repo],))
		for row in result:
			stars.append(row[0])
			watchs.append(row[1])
			forks.append(row[2])

	# 归一化
	nor_data = []
	for metric in metrics:
		nor_data.append(_nor_data(metric))

	for i in range(0,len(REPOS)):
		tmp_row = [nor_metric[i] for nor_metric in nor_data]
		dbop.execute("insert into maturity(repo_id, issue_done, commit_total, age_dev, fans_dev) values(%s,%s,%s,%s,%s)",
						(REPO_ID[REPOS[i]],tmp_row[0],tmp_row[1],tmp_row[2],sum(tmp_row[3:])))
		

def main():
	logger.info(">>>>>maturity begins to work")
	while True:

		logger.info("\tstart another round of work")
		start_time = time.time()

		computeMaturity()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

def init():
	logger.info("init ...")
	readPrjLists()

	dbop.createMaturity()


if __name__ == '__main__':
	init()
	main()