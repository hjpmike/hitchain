# -*- coding: utf-8 -*
import ConfigParser
import git
import helper
import pymysql
import csv


cf = ConfigParser.ConfigParser()
cf.read("config.conf")

conn = pymysql.connect(host=cf.get("DB","host"),
                       port=int(cf.get("DB","port")),
                       user=cf.get("DB","user"),
                       passwd=cf.get("DB","password"),
                       db=cf.get("DB","database"),
                       charset='utf8')

def gitClone(repoCloneDir,repo):
    proName, repoName, gitAddr = repo
    helper.mkdir(repoCloneDir)
    try:
        git.Git(repoCloneDir).clone(gitAddr)
        helper.configSonarProperty(repoName)

        updateCloneStatus(proName, repoName)
    except:
        print ("repo has been cloned!!!")

def getCloneRepos():
    with conn.cursor() as cur:
        sql = "select proj_name,repo_name,git_addr from git_clone_pull_status where is_clone = 0 and git_addr is not null"
        cur.execute(sql)
        return cur.fetchall()

def updateCloneStatus(proName,repoName):
    with conn.cursor() as cur:
        sql = "update git_clone_pull_status set is_clone = 1 where proj_name = '%s' and repo_name = '%s'" % (proName,repoName)
        cur.execute(sql)
        conn.commit()


def CloneProcess():
    # repoListFile = cf.get("server", "repoList")
    for repo in getCloneRepos():
        # proName,repoName,gitAddr = repo
        gitClone(cf.get("server","gitCloneAddr"),repo)


CloneProcess()