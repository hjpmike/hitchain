import pymysql
import ConfigParser

conn = pymysql.connect(host="47.254.66.180",
                       port=3306,
                       user="root",
                       passwd="password",
                       db="ossean_coin_rank",
                       charset='utf8')

sqlGit = "select prj_id, github_url from prj_list where github_url is not null"

with conn.cursor() as curPrj:
    curPrj.execute(sqlGit)

def handleResult(githubRepo,projId):
    with conn.cursor() as curRepo:
        sql = "update git_clone_pull_status set git_addr = '%s' where proj_id = %s" % (githubRepo,projId)
        curRepo.execute(sql)
        conn.commit()

for prj in curPrj.fetchall():
    projId, githubUrl = prj
    handleResult(githubUrl+".git",projId)