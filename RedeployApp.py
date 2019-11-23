import requests
import json
from collections import namedtuple
import getopt
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Invokes the URL in Get mode and returns the json object returned if return status is 200 else null
def getResponse(url, verifyCertificate, userName, password):
    result = requests.get(url, verify=verifyCertificate, auth=(userName, password))
    if result.status_code == 200:
        return result.json()
    else:
        return None

# Retrieves the stages and the last run's pipeline counter
def getStagePipelineCounter(baseUrl, user, pwd, pipeline, stage):
    stageUrl = baseUrl + '/api/stages/' + pipeline + '/' + stage + '/history'
    stageHistory = getResponse(stageUrl, False, user, pwd)
    if stageHistory is None:
        return 0
    else:
        stages = stageHistory["stages"]
        return stages[0]["pipeline_counter"]

def rerunStagePipeline(baseUrl, user, pwd, pipeline, stage):
    plCounter = getStagePipelineCounter(pipeline, stage)
    rerunUrl = baseUrl + '/api/stages/' + pipeline + '/' + str(plCounter) + '/' + stage + '/run'
    payload = {}
    hdrs = {
        'X-GoCD-Confirm': 'true',
        'Accept': 'application/vnd.go.cd.v1+json',
        'Content-Type': 'application/json'
    }
    rerunResult = requests.post(rerunUrl, verify=False, auth=(user, pwd), data=json.dumps(payload), headers = hdrs)
    if (rerunResult.status_code != 202):
        print('Something is wrong')
    else:
        print('Stage rerun requested')

#rerunStagePipeline('Web-App', 'DEV')

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:s:b:u:w:")
        pipelineName = ''
        stageName = ''
		baseUrl = ''
		user = ''
		pwd = ''
        for o,a in opts:
            if (o == '-p'):
                pipelineName = a;
            if (o == '-s'):
                stageName = a;
            if (o == '-b'):
                baseUrl = a;
            if (o == '-u'):
                user = a;
            if (o == '-w'):
                pwd = a;

        print('Redeploying application from ' + pipelineName + ' - ' + stageName + '...')
        rerunStagePipeline(pipelineName, stageName)
    except getopt.GetoptError as err:
        print(str(err))
        exit(2)

if __name__ == "__main__":
    main()
