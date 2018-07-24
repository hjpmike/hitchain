from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import mainProcess

# 输出时间
def job():
    mainProcess.start()
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='0-6', hour=15, minute=10)
scheduler.start()