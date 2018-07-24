# -*- coding: utf-8 -*

import ConfigParser
import git
import helper
import pymysql

cf = ConfigParser.ConfigParser()
cf.read("config.conf")

conn = pymysql.connect(host=cf.get("DB","host"),
                       port=int(cf.get("DB","port")),
                       user=cf.get("DB","user"),
                       passwd=cf.get("DB","password"),
                       db=cf.get("DB","database"),
                       charset='utf8')

def gitPull(repoPullDir):
    helper.mkdir(repoPullDir)
    repo = git.Repo(repoPullDir)
    o = repo.remotes.origin
    o.pull()

def getCloneRepos():
    with conn.cursor() as cur:
        sql = "select proj_name,repo_name,git_addr,proj_id from git_clone_pull_status where is_clone = 1"
        cur.execute(sql)
        return cur.fetchall()

def updateCloneStatus(proName,repoName):
    with conn.cursor() as cur:
        sql = "update git_clone_pull_status set is_clone = 1 where proj_name = '%s' and repo_name = '%s'" % (proName,repoName)
        cur.execute(sql)
        conn.commit()

def PullProcess():
    for repo in getCloneRepos():
        proName,repoName,gitAddr,projId = repo
        gitPull(cf.get("server","gitCloneAddr")+"/"+repoName)
        updateCloneStatus(proName,repoName)
