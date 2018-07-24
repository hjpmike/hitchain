# -*- coding: utf-8 -*

import ConfigParser
import helper
import pymysql
import pull
import os
import sonarScan
import sonarResultAnalysis
import datetime


# 代码clone
# git.Git("pythonClone/").clone("https://github.com/alecive/FlatWoken.git")

# 代码pull
# repo = git.Repo('pythonClone/FlatWoken')
# o = repo.remotes.origin
# o.pull()

cf = ConfigParser.ConfigParser()
cf.read("config.conf")

conn = pymysql.connect(host=cf.get("DB","host"),
                       port=int(cf.get("DB","port")),
                       user=cf.get("DB","user"),
                       passwd=cf.get("DB","password"),
                       db=cf.get("DB","database"),
                       charset='utf8')

# 拉代码
# clone.CloneProcess()

def addSonarResult(issueNum,projId,repoName):
    with conn.cursor() as cur:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into sonar_repo_issues_num (`proj_id`, `issue_num`, `repo_name`, `create_time`) values (%s,%s,'%s','%s')" % (projId,issueNum,repoName,dt)
        cur.execute(sql)
        conn.commit()

def start():
    pull.PullProcess()
    sourcePathBase = os.getcwd() + "\\" + cf.get("server", "gitCloneAddr")
    targetPathBase = os.getcwd() + "\\" + cf.get("server", "sonarTempAddr")
    for repo in pull.getCloneRepos():
        proName, repoName, gitAddr, projId = repo
        sourcePath = sourcePathBase + "\\" + repoName
        targetPath = targetPathBase + "\\" + repoName
        helper.mkdir(targetPath)
        helper.copyFiles(sourcePath, targetPath)

        sonarScan.runSonarScanner(targetPath)

        os.system('rmdir /S /Q "{}"'.format(targetPath))
        addSonarResult(sonarResultAnalysis.getIssueNumberOfRepo(repoName), projId, repoName)

if __name__ == "__main__":
    start()








