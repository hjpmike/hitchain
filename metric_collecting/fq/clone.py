# -*- coding: utf-8 -*

import ConfigParser
import git
import helper
import pymysql
import csv


# 代码clone
# git.Git("pythonClone/").clone("https://github.com/alecive/FlatWoken.git")

# 代码pull
# repo = git.Repo('pythonClone/FlatWoken')
# o = repo.remotes.origin
# o.pull()

cf = ConfigParser.ConfigParser()
cf.read("config.conf")


def gitClone(repoCloneDir,gitAddr):
    helper.mkdir(repoCloneDir)
    git.Git(repoCloneDir).clone(gitAddr)



def CloneProcess():
    repoListFile = cf.get("server", "repoList")
    with open(repoListFile,"r") as f:
        reader = csv.reader(f,delimiter = ",")
        for item in reader:
            proName,repoName,gitAddr = item
            gitClone(cf.get("server","gitCloneAddr"),gitAddr)
