import ConfigParser
import os
import shutil
import helper

cf = ConfigParser.ConfigParser()
cf.read("config.conf")

# helper.mkdir("temp")

# shutil.copy2("repoClone","temp")
shutil.rmtree("sonarTemp\\bitcoin")