# -*- coding: utf-8 -*

import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("config.conf")


def mkdir(path):
    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)

    if not isExists:
        print (path+': create successfull')
        os.makedirs(path)
        return True
    else:
        print (path+': path already exist')
        return False

# 拷贝除.git外的所有文件和文件夹
def copyFiles(sourceDir, targetDir):
    import os
    if sourceDir.find(".svn") > 0:
        return
    for file in os.listdir(sourceDir):
        if file == ".git":
            continue
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or (
                os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            First_Directory = False
            copyFiles(sourceFile, targetFile)

def configSonarProperty(repoName):
    import os
    # sonar_longin = "sonar.login=%s" % sonar_token
    properties = ["sonar.projectKey=","sonar.projectName=","sonar.projectVersion=1.0","sonar.sourceEncoding=UTF-8","sonar.sources=.","sonar.java.binaries=."]
    # properties = ["sonar.projectKey=", "sonar.projectName=", "sonar.projectVersion=1.0", "sonar.sourceEncoding=UTF-8",
    #               "sonar.sources=."]

    properties[0] = properties[0] + repoName
    properties[1] = properties[1] + repoName
    sera = '\n'
    pro = sera.join(properties)
    path = cf.get("server","gitCloneAddr")+"/"+repoName
    fp = open(path + '/sonar-project.properties','w')
    fp.write(pro)
    fp.close()
    print('SUCCESS')