import json
import requests
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("config.conf")
root_url = "http://localhost:"+cf.get("sonar","sonar_port")+"/api"
issue_url = root_url + "/issues/search?severities=CRITICAL%2CMAJOR&"
metrics_url = root_url + "component?"



def getMetric(repoName,metricKeys):
    params = {"component":repoName}
    r = requests.get(metrics_url,params=params).json()
    try:
        return r["component"]["measures"]["value"]
    except:
        print ('No result')

def getMetricsOfRepo(repoName):
    loc = getMetric(repoName,"ncloc")
    return {"loc":loc}


def getIssueResult(repoName):

    params = {"componentKeys":repoName,"severities":"CRITICAL%2CMAJOR"}
    r = requests.get(issue_url, params = params)
    if not r.json():
        print("")
    else:
        return r.json()


def getIssueNumbers(json_result,repoName):
    # issues = []
    # count = 0
    if not json_result:
        print('No result')
    else:

        if not json_result['issues']:
            print('')
        else:
            return json_result["total"]

    # for eachFileIssue in issues:
    #     for eachIssue in eachFileIssue:
    #         if eachIssue["project"] == repoName and eachIssue["status"] == "OPEN" \
    #                 and eachIssue["severity"] in ["CRITICAL","MAJOR","BLOCKER"] :
    #             count += 1
    # return count

def getIssueNumberOfRepo(repoName):
    return getIssueNumbers(getIssueResult(repoName),repoName)

# print getIssueNumbers(getIssueResult("bitcoin"),"bitcoin")

# print  getIssueNumberOfRepo("bitcoin")

