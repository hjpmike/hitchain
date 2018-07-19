# coding:utf-8
# 计算排名指标

from config import config
import time
import dbop
import logging
from logging.handlers import TimedRotatingFileHandler
log_fmt = '%(asctime)s %(levelname)s(%(lineno)s): %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(filename="log/metrics", when="D", interval=1, backupCount=7)
log_file_handler.setFormatter(formatter)    
logger = logging.getLogger()
logger.addHandler(log_file_handler)
logger.setLevel(logging.INFO) 

####################
# 必要参数
####################
REPOS = []
INTERVAL_TIME = config['metric_compute_interval']
EXAMINE_WINDOW = config["examine_window"]

####################
# 工具函数
####################
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

def _continuous_dev_month(data):
	month_rec = set()
	for item in data:
		dev_date = item[0]
		dev_date = "%d-%d"%(dev_date.year,dev_date.month)
		month_rec.add(dev_date)
	return len(month_rec)

def _datetime2int(date_time):
	return time.mktime(date_time.timetuple())

def _strtime_before_days(base_time, before_days):
	# 返回befor_dayas天前的那一天的凌晨
	before_time = base_time - before_days* 24*60*60
	before_time = time.strftime('%Y-%m-%d 00:00:00',time.localtime(before_time))
	return before_time

def _common_num(dataset1, dataset2):
	data_common = 0
	for item in dataset1:
		if item in dataset2:
			data_common += 1
	return data_common

# 转为 computeTrent函数服务
def _socialfans_till_time(repo, dateTime):
	fans_fb_before_1_window = dbop.select_one("select watches_num from fb_data where coin_id=%s and update_time<=%s order by update_time desc limit 1",
												(repo,dateTime),(0,))
	fans_tw_before_1_window = dbop.select_one("select followers_num from twitters_data where coin_id=%s and created_time<=%s order by created_time desc limit 1",
												(repo,dateTime),(0,))
	return fans_fb_before_1_window[0] + fans_tw_before_1_window[0]

####################
# 功能函数
####################
def computeINF():
	# 几个时间点
	time_now = time.time()
	time_now_str = _strtime_before_days(time_now,0)
	time_before_1_window = _strtime_before_days(time_now, EXAMINE_WINDOW)

	fans = [[],[],[]]
	fans_fb,fans_tw = [],[]
	for repo in REPOS:

		# 开发社区的值
		fans_now = dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
												(repo,time_now_str),(0,0,0))
		fans_before = dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
												(repo,time_before_1_window),(0,0,0))
		# 计算指标变化量, !!还真有变少的，
		for i in range(0,3):
			fans[i].append(fans_now[i] - fans_before[i])

		# 社交社区
		fb_now = dbop.select_one("select watches_num from fb_data where coin_id=%s and update_time<=%s order by update_time desc limit 1",
							(repo,time_now_str),(0,))
		fb_before = dbop.select_one("select watches_num from fb_data where coin_id=%s and update_time<=%s order by update_time desc limit 1",
							(repo,time_before_1_window),(0,))
		tw_now = dbop.select_one("select followers_num from twitters_data where coin_id=%s and created_time<=%s order by created_time desc limit 1",
							(repo,time_now_str),(0,))
		tw_before = dbop.select_one("select followers_num from twitters_data where coin_id=%s and created_time<=%s order by created_time desc limit 1",
							(repo,time_before_1_window),(0,))
		
		fans_fb.append(fb_now[0]-fb_before[0])
		fans_tw.append(tw_now[0]-tw_before[0])
		


	# 归一化
	fans.extend([fans_fb,fans_tw])
	fans = [_nor_data(item) for item in fans]
	for i in range(0,len(REPOS)):
		tmp_row = []
		for j in range(0,len(fans)):
			tmp_row.append(fans[j][i])
		dbop.execute("insert into inf(repo_id,inf_dev,inf_social) values(%s,%s,%s)", 
						(REPOS[i], sum(tmp_row[0:3]), sum(tmp_row[3:])))

def computeMaturity():
	# maturity: repo_id, issue_done, commit_total, age_dev, fans_dev
	
	issue_done, commit_total, age_dev = [],[],[]
	stars,watchs,forks = [],[],[]
	fans_fb, fans_tw = [],[]
	metrics = [issue_done, commit_total, age_dev, stars,watchs,forks, fans_fb,fans_tw]

	# 获取每个指标
	for repo_id in REPOS:

		# issue_done
		result = dbop.select_one("select count(*) from issues_info where repo_id=%s and is_pr=0 and closed_at is not NULL",(repo_id,))
		issue_done.append(result[0])

		# commit_total
		result = dbop.select_one("select count(*) from commits_info where repo_id=%s",(repo_id,))
		commit_total.append(result[0])

		# age_dev
		result = dbop.select_all("select author_date from commits_info where repo_id =%s",(repo_id,))
		age_dev.append(_continuous_dev_month(result))

		# fans_dev
		result = dbop.select_one("select watch,star,fork from html_info where repo_id=%s order by id desc limit 1",(repo_id,),(0,0,0))
		stars.append(result[0])
		watchs.append(result[1])
		forks.append(result[2])

		# fans_social
		result = dbop.select_one("select watches_num from fb_data where coin_id=%s order by id desc limit 1",
									(repo_id,),(0,))
		fans_fb.append(result[0])
		result = dbop.select_one("select followers_num from twitters_data where coin_id=%s order by id desc limit 1",
									(repo_id,),(0,))
		fans_tw.append(result[0])

	# 归一化
	nor_data = []
	for metric in metrics:
		nor_data.append(_nor_data(metric))

	for i in range(0,len(REPOS)):
		tmp_row = [nor_metric[i] for nor_metric in nor_data]
		dbop.execute("insert into maturity(repo_id, issue_done, commit_total, age_dev, fans_dev, fans_social) values(%s,%s,%s,%s,%s,%s)",
						(REPOS[i],tmp_row[0],tmp_row[1],tmp_row[2],sum(tmp_row[3:-2]),sum(tmp_row[-2:])))

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
			tmp_repair_time = sum( [_datetime2int(item[0]) - _datetime2int(item[1]) 
										for item in issue_done])*1.0 / len(issue_done)

		repair_ratio.append(tmp_repair_ratio)
		repair_time.append(tmp_repair_time)

	repair_time = _nor_data(repair_time)
	for i in range(0,len(REPOS)):
		dbop.execute("insert into quality_sub(repo_id,repair_ratio,repair_time) values(%s,%s,%s)",
					(REPOS[i],repair_ratio[i],repair_time[i]))

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

def computeTrend():
	# 几个重要时间点
	time_now = time.time()
	time_now_str = _strtime_before_days(time_now,0)
	time_before_1_window = _strtime_before_days(time_now, EXAMINE_WINDOW)
	time_before_2_window = _strtime_before_days(time_now, 2*EXAMINE_WINDOW)
	time_before_3_window = _strtime_before_days(time_now, 3*EXAMINE_WINDOW)
	
	dits,tits,dcpts,ucpts = [],[],[],[]
	for repo in REPOS:

		# dit
		commits_before_1_window = dbop.select_one("select count(*) from commits_info where repo_id=%s and (author_date>%s and author_date<=%s)",
												(repo,time_before_1_window,time_now_str))[0] 
		commits_before_2_window = dbop.select_one("select count(*) from commits_info where repo_id=%s and (author_date>%s and author_date<=%s)",
												(repo,time_before_2_window,time_before_1_window))[0]
		commits_before_3_window = dbop.select_one("select count(*) from commits_info where repo_id=%s and (author_date>%s and author_date<=%s)",
												(repo,time_before_3_window,time_before_2_window))[0]
		dits.append( ((commits_before_1_window - 2*commits_before_2_window + commits_before_3_window) + 1.0) /
						((commits_before_2_window - commits_before_3_window) + 1.0))

		# tit
		issues_before_1_window = dbop.select_one("select count(*) from issues_info where repo_id=%s and is_pr=0 and (created_at>%s and created_at<=%s)",
												(repo,time_before_1_window,time_now_str))[0] 
		issues_before_2_window = dbop.select_one("select count(*) from issues_info where repo_id=%s and is_pr=0 and (created_at>%s and created_at<=%s)",
												(repo,time_before_2_window,time_before_1_window))[0]
		issues_before_3_window = dbop.select_one("select count(*) from issues_info where repo_id=%s and is_pr=0 and (created_at>%s and created_at<=%s)",
												(repo,time_before_3_window,time_before_2_window))[0]
		tits.append( ((issues_before_1_window - 2*issues_before_2_window + issues_before_3_window) + 1.0) /
						((issues_before_2_window - issues_before_3_window) + 1.0))

		# dcpt
		fans_before_1_window = sum(dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
												(repo,time_now_str),(0,0,0)))
		fans_before_2_window = sum(dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
												(repo,time_before_1_window),(0,0,0)))
		fans_before_3_window = sum(dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
												(repo,time_before_2_window),(0,0,0)))
		dcpts.append( ((fans_before_1_window - 2*fans_before_2_window + fans_before_3_window) + 1.0) /
						(fans_before_2_window - fans_before_3_window + 1.0))

		# UCPT
		fans_before_1_window = _socialfans_till_time(repo,time_now_str)
		fans_before_2_window = _socialfans_till_time(repo,time_before_1_window)
		fans_before_3_window = _socialfans_till_time(repo,time_before_2_window)
		ucpts.append( ((fans_before_1_window - 2*fans_before_2_window + fans_before_3_window) + 1.0) /
						(fans_before_2_window - fans_before_3_window + 1.0))


	for i in range(0,len(REPOS)):
		dbop.execute("insert into trend(repo_id,dit,tit,dcpt,ucpt) values(%s,%s,%s,%s,%s)",
						(REPOS[i],dits[i],tits[i],dcpts[i],ucpts[i]))
		


def main():
	logger.info(">>>>>metrics begins to work")
	while True:

		logger.info("\tstart another round of work")
		start_time = time.time()

		logger.info("\t  compute INF")
		computeINF()
		logger.info("\t  compute Maturity")
		computeMaturity()
		logger.info("\t  compute QualitySub")
		computeQualitySub()
		logger.info("\t  compute TeamHealth")
		computeTeamHealth()
		logger.info("\t  compute DevActv")
		computeDevActv()
		logger.info("\t  compute Trend")
		computeTrend()
		
		end_time = time.time()
		work_time = end_time - start_time
		if work_time < INTERVAL_TIME:
			logger.info("\tnot enough interval, sleep a while")
			time.sleep(INTERVAL_TIME - work_time)

def init():
	logger.info("init ...")
	readPrjLists()
	dbop.createINF()
	dbop.createMaturity()
	dbop.createQualitySub()
	dbop.createTeamHealth()
	dbop.createDevActv()
	dbop.createTrend()

if __name__ == '__main__':
	init()
	main()