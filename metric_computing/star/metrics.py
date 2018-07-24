# coding:utf-8
# 计算排名指标

import numpy as np
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
# 用户判断缺失值的，比如某个项目在某个社区没有数据
NONE_GH, NONE_FB, NONE_TW = set(),set(),set()

####################
# 工具函数
####################
def readPrjLists():
	prjs = dbop.select_all("select prj_id,github_url,facebook_url,twitter_url from prj_list")
	for prj in prjs:
		REPOS.append(prj[0])
		if prj[1] is None:
			NONE_GH.add(prj[0])
		if prj[2] is None or len(prj[2].strip())==0:
			NONE_FB.add(prj[0])
		if prj[3] is None or len(prj[3].strip())==0:
			NONE_TW.add(prj[0])

def _my_sum(data):
	# 更能够处理包含none的数组
	data_del_none = [item for item in data if item is not None]
	if len(data_del_none) == 0:
		return None
	return sum(data_del_none)

def _my_avg(data):
	# 更能够处理包含none的数组
	data_del_none = [item for item in data if item is not None]
	if len(data_del_none) == 0:
		return None
	return sum(data_del_none)/len(data_del_none)

def _nor_data(dataSet):
	dataSetValid = [item for item in dataSet if item is not None]
	min_edge = min(dataSetValid)
	max_edge = max(dataSetValid)
	dur_edge = max_edge - min_edge
	
	# 如果数组内的元素都相同，防止除数为0
	if dur_edge == 0:
		dur_edge = 1
	result = []
	for item in dataSet:
		if item is None:
			result.append(None)
		else:
			result.append((item*1.0 - min_edge)/dur_edge)
	return result

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

def _gini(array):
	if len(array) == 0:
		return 0
	array = np.array([item+0.0 for item in array]) # changes a list to np array
	array = array.flatten() #all values are treated equally, arrays must be 1d
	if np.amin(array) < 0:
		array -= np.amin(array) #values cannot be negative
	array += 0.0000001 #values cannot be 0
	array = np.sort(array) #values must be sorted
	index = np.arange(1,array.shape[0]+1) #index per array element
	n = array.shape[0]#number of array elements
	return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array))) #Gini coefficient

# 专为 computeTrent函数服务
def _socialfans_till_time(repo, dateTime):
	fans_fb_before_1_window = dbop.select_one("select watches_num from facebook_data where coin_id=%s and created_time<=%s order by created_time desc limit 1",
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

		if repo in NONE_GH: #该项目在github上没有
			for i in range(0,3):
				fans[i].append(None)
		else:
			# 开发社区的值
			fans_now = dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
													(repo,time_now_str),(0,0,0))
			fans_before = dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
													(repo,time_before_1_window),(0,0,0))
			# 计算指标变化量, !!还真有变少的，
			for i in range(0,3):
				fans[i].append(fans_now[i] - fans_before[i])

		# 社交社区
		if repo in NONE_FB:
			fans_fb.append(None)
		else:
			fb_now = dbop.select_one("select watches_num from facebook_data where coin_id=%s and created_time<=%s order by created_time desc limit 1",
								(repo,time_now_str),(0,))
			fb_before = dbop.select_one("select watches_num from facebook_data where coin_id=%s and created_time<=%s order by created_time desc limit 1",
								(repo,time_before_1_window),(0,))
			fans_fb.append(fb_now[0]-fb_before[0])
		
		if repo in NONE_TW:
			fans_tw.append(None)
		else:
			tw_now = dbop.select_one("select followers_num from twitters_data where coin_id=%s and created_time<=%s order by created_time desc limit 1",
								(repo,time_now_str),(0,))
			tw_before = dbop.select_one("select followers_num from twitters_data where coin_id=%s and created_time<=%s order by created_time desc limit 1",
								(repo,time_before_1_window),(0,))
			fans_tw.append(tw_now[0]-tw_before[0])
		


	# 归一化
	fans.extend([fans_fb,fans_tw])
	fans = [_nor_data(item) for item in fans]
	for i in range(0,len(REPOS)):
		tmp_row = []
		for j in range(0,len(fans)):
			tmp_row.append(fans[j][i])
		dbop.execute("insert into inf(repo_id,inf_dev,inf_social) values(%s,%s,%s)", 
						(REPOS[i], _my_avg(tmp_row[0:3]), _my_avg(tmp_row[3:])))

def computeMaturity():
	# maturity: repo_id, issue_done, commit_total, age_dev, fans_dev
	
	issue_done, commit_total, age_dev = [],[],[]
	stars,watchs,forks = [],[],[]
	fans_fb, fans_tw = [],[]
	metrics = [issue_done, commit_total, age_dev, stars,watchs,forks, fans_fb,fans_tw]

	# 获取每个指标
	for repo_id in REPOS:
		if repo_id in NONE_GH:
			issue_done.append(None)
			commit_total.append(None)
			age_dev.append(None)
			stars.append(None)
			watchs.append(None)
			forks.append(None)
		else:
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

		if repo_id in NONE_FB:
			fans_fb.append(None)
		else:		
			# fans_social
			result = dbop.select_one("select watches_num from facebook_data where coin_id=%s order by id desc limit 1",
										(repo_id,),(0,))
			fans_fb.append(result[0])

		if repo_id in NONE_TW:
			fans_tw.append(None)
		else:	
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
						(REPOS[i],tmp_row[0],tmp_row[1],tmp_row[2],_my_avg(tmp_row[3:-2]),_my_avg(tmp_row[-2:])))

def computeQualitySub():

	# 缺陷修复比例，平均修复时间
	repair_ratio, repair_time = [],[]
	metrics = [repair_ratio, repair_time]
	for repo in REPOS:
		if repo in NONE_GH:
			repair_ratio.append(None)
			repair_time.append(None)
		else:
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
			repair_time.append(1.0 / (tmp_repair_time+1))

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

	ccrs, ngrs, tbrs = [], [], []
	for repo in REPOS:
		if repo in NONE_GH:
			ccrs.append(None)
			ngrs.append(None)
			tbrs.append(None)
		else:
			# 几个重要集合
			data_before_1_window = set([item[0] for item in 
										dbop.select_all("select author_id from commits_info where repo_id=%s and author_id is not null and (author_date>%s and author_date<%s)",
													(repo,time_before_1_window,time_now_str)) ] )
			data_before_2_window = set([item[0] for item in  
										dbop.select_all("select author_id from commits_info where repo_id=%s and author_id is not null and (author_date>%s and author_date<%s)",
													(repo,time_before_2_window,time_before_1_window))])
			data_before_3_window = set([item[0] for item in  
										dbop.select_all("select author_id from commits_info where repo_id=%s and author_id is not null and (author_date>%s and author_date<%s)",
													(repo,time_before_3_window,time_before_2_window))])
			# ccr
			data_common = _common_num(data_before_1_window, data_before_2_window)
			ccrs.append(data_common*1.0 / (len(data_before_2_window)+1)) #避免分母为0
			# ngr
			new_users_1 = len(data_before_1_window) - data_common  + 1 #避免分母为0
			data_common_2 =  _common_num(data_before_3_window, data_before_2_window)
			new_users_2 = len(data_before_2_window) - data_common_2 + 1 #避免分母为0
			ngrs.append((new_users_1-new_users_2)*1.0/new_users_2)
			# tbr 上一个窗口期的
			commits_dis = dbop.select_all("select count(*) from commits_info where repo_id=%s and author_id is not null group by author_id", (repo,))
			issues_dis = dbop.select_all("select count(*) from issues_info where repo_id=%s and user_id is not null group by user_id", (repo,))
			tbrs.append(1.0/(_gini([item[0] for item in commits_dis]) + 
								_gini([item[0] for item in issues_dis]) + 1))

	metrics = []
	metrics.append(_nor_data(ccrs))
	metrics.append(_nor_data(ngrs))
	metrics.append(_nor_data(tbrs))
	for i in range(0,len(REPOS)):
		tmp_row = [REPOS[i]]
		for j in range(0,len(metrics)):
			tmp_row.append(metrics[j][i])
		dbop.execute("insert into team_health(repo_id, ccr,ngr,tbr) values(%s,%s,%s,%s)",
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
		if repo in NONE_GH:
			cbw.append(None)
			ibw.append(None)
			rbw.append(None)
		else:
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
						(REPOS[i], _my_avg([nor_metrics[0][i],nor_metrics[1][i]]),nor_metrics[2][i]))

def computeTrend():
	# 几个重要时间点
	time_now = time.time()
	time_now_str = _strtime_before_days(time_now,0)
	time_before_1_window = _strtime_before_days(time_now, EXAMINE_WINDOW)
	time_before_2_window = _strtime_before_days(time_now, 2*EXAMINE_WINDOW)
	time_before_3_window = _strtime_before_days(time_now, 3*EXAMINE_WINDOW)
	
	dits,tits,dcpts,ucpts = [],[],[],[]
	for repo in REPOS:
		if repo in NONE_GH:
			dits.append(None)
			tits.append(None)
			dcpts.append(None)
		else:
			# dit
			commits_before_1_window = dbop.select_one("select count(*) from commits_info where repo_id=%s and (author_date>%s and author_date<=%s)",
													(repo,time_before_1_window,time_now_str))[0] 
			commits_before_2_window = dbop.select_one("select count(*) from commits_info where repo_id=%s and (author_date>%s and author_date<=%s)",
													(repo,time_before_2_window,time_before_1_window))[0]
			commits_before_3_window = dbop.select_one("select count(*) from commits_info where repo_id=%s and (author_date>%s and author_date<=%s)",
													(repo,time_before_3_window,time_before_2_window))[0]
			if (commits_before_2_window - commits_before_3_window) == 0:
				dits.append( ((commits_before_1_window - 2*commits_before_2_window + commits_before_3_window) + 1.0) /
							((commits_before_2_window - commits_before_3_window) + 1.0))
			else:
				dits.append( (commits_before_1_window - 2*commits_before_2_window + commits_before_3_window) /
							(commits_before_2_window - commits_before_3_window))

			# tit
			issues_before_1_window = dbop.select_one("select count(*) from issues_info where repo_id=%s and is_pr=0 and (created_at>%s and created_at<=%s)",
													(repo,time_before_1_window,time_now_str))[0] 
			issues_before_2_window = dbop.select_one("select count(*) from issues_info where repo_id=%s and is_pr=0 and (created_at>%s and created_at<=%s)",
													(repo,time_before_2_window,time_before_1_window))[0]
			issues_before_3_window = dbop.select_one("select count(*) from issues_info where repo_id=%s and is_pr=0 and (created_at>%s and created_at<=%s)",
													(repo,time_before_3_window,time_before_2_window))[0]
			if (issues_before_2_window - issues_before_3_window) == 0:
				tits.append( ((issues_before_1_window - 2*issues_before_2_window + issues_before_3_window) + 1.0) /
							((issues_before_2_window - issues_before_3_window) + 1.0))
			else:
				tits.append( (issues_before_1_window - 2*issues_before_2_window + issues_before_3_window)/
							(issues_before_2_window - issues_before_3_window))

			# dcpt
			fans_before_1_window = _my_sum(dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
													(repo,time_now_str),(0,0,0)))
			fans_before_2_window = _my_sum(dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
													(repo,time_before_1_window),(0,0,0)))
			fans_before_3_window = _my_sum(dbop.select_one("select watch,star,fork from html_info where repo_id=%s and fetched_at<=%s order by fetched_at desc limit 1",
													(repo,time_before_2_window),(0,0,0)))
			if (fans_before_2_window - fans_before_3_window) == 0:
				dcpts.append( ((fans_before_1_window - 2*fans_before_2_window + fans_before_3_window) + 1.0) /
							(fans_before_2_window - fans_before_3_window + 1.0))
			else:
				dcpts.append( (fans_before_1_window - 2*fans_before_2_window + fans_before_3_window) /
							(fans_before_2_window - fans_before_3_window))

			# UCPT
		if repo is NONE_FB and repo in NONE_TW:
			ucpts.append(None)
		else:
			fans_before_1_window = _socialfans_till_time(repo,time_now_str)
			fans_before_2_window = _socialfans_till_time(repo,time_before_1_window)
			fans_before_3_window = _socialfans_till_time(repo,time_before_2_window)
			if (fans_before_2_window - fans_before_3_window) == 0:
				ucpts.append( ((fans_before_1_window - 2*fans_before_2_window + fans_before_3_window) + 1.0) /
							(fans_before_2_window - fans_before_3_window + 1.0))
			else:
				ucpts.append( (fans_before_1_window - 2*fans_before_2_window + fans_before_3_window) /
							(fans_before_2_window - fans_before_3_window))
	dits,tits,dcpts,ucpts = _nor_data(dits),_nor_data(tits),_nor_data(dcpts),_nor_data(ucpts)
	for i in range(0,len(REPOS)):
		dbop.execute("insert into trend(repo_id,dit,tit,dcpt,ucpt) values(%s,%s,%s,%s,%s)",
						(REPOS[i],dits[i],tits[i],dcpts[i],ucpts[i]))

def computeScore():
	M1,M2,M3,M4,M5,M6 = [],[],[],[],[],[]
	score = []
	dateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	for repo in REPOS:
		M1.append(_my_avg(dbop.select_one("select inf_dev,inf_social from inf where repo_id=%s and computed_at<=%s order by id limit 1",
						(repo,dateTime),(0,0))))
		M2.append(_my_avg(dbop.select_one("select issue_done, commit_total, age_dev, fans_dev, fans_social from maturity where repo_id=%s and computed_at<=%s order by id limit 1",
						(repo,dateTime),(0,0))))
		M3.append(_my_avg(dbop.select_one("select repair_ratio,repair_time from quality_sub where repo_id=%s and computed_at<=%s order by id limit 1",
						(repo,dateTime),(0,0))))
		M4.append(_my_avg(dbop.select_one("select  ccr,ngr,tbr from team_health where repo_id=%s and computed_at<=%s order by id limit 1",
						(repo,dateTime),(0,0))))
		M5.append(_my_avg(dbop.select_one("select  dev,rel from dev_actv where repo_id=%s and computed_at<=%s order by id limit 1",
						(repo,dateTime),(0,0))))
		M6.append(_my_avg(dbop.select_one("select  dit,tit,dcpt,ucpt from trend where repo_id=%s and computed_at<=%s order by id limit 1",
						(repo,dateTime),(0,0))))
		score.append((repo,_my_avg([M1[-1],M2[-1],M3[-1],M4[-1],M5[-1],M6[-1]])))
	score = sorted(score, key=lambda x: x[1],reverse=True)

	field_sql_str = "prj_id,rank,score,m1_inf,m2_maturity,m3_quality,m4_team_healty,m5_activatin,m6_trend"
	for i in range(0,len(score)):
		repo,r_score = score[i]
		dbop.execute("insert into daily_rank(" + field_sql_str+") values(%s" + ",%s"*8+")",
					(repo,i+1,r_score,M1[i],M2[i],M3[i],M4[i],M5[i],M6[i]))




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
		logger.info("\t  compute score")
		computeScore()
		
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