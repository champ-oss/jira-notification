#!/usr/bin/python3
#	usage: jira-notification.py
# export JIRA_TOKEN, JIRA_HOST, JIRA_PROJECT and JIRA_REPO as env variable
#########################################################################################################


import requests
import json
import sys
import os

repo = os.environ["JIRA_REPO"]
jiraproject = os.environ["JIRA_PROJECT"]
jiratoken = os.environ["JIRA_TOKEN"]
jirahost = os.environ["JIRA_HOST"]

def check_existing_issue():
    url = "https://" + jirahost + "/rest/api/3/search?jql=project%20%3D%20" + jiraproject + "%20AND%20labels%20%3D%20unit_test%20AND%20labels%20%3D%20" + repo + "%20and%20(statusCategory%20%3D%20\"To%20Do\"%20OR%20statusCategory%20%3D%20\"In%20Progress\")"

    payload = ""
    headers = {
        'Authorization': 'Basic ' + jiratoken + "'",
        'Content-Type': 'application/json',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    get_total_issue_count = response.json().get("total")

    return get_total_issue_count

def create_jira_issue():
    url = "https://" + jirahost + "/rest/api/3/issue"

    payload = json.dumps({
        "update": {},
        "fields": {
            "summary":  "" + repo + " unit test failure",
            "issuetype": {
                "name": "Problem"
            },
            "project": {
                "key": jiraproject
            },
            "labels": [
                "" + repo + "",
                "unit_test"
            ],
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": "unit test module failure",
                                "type": "text"
                            }
                        ]
                    }
                ]
            }
        }
    })
    headers = {
        'Authorization': 'Basic ' + jiratoken + "'",
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)

def main():
    # checking if issue exist, creating issue if total count equals zero
    get_issue_count = check_existing_issue()
    if get_issue_count == 0:
        create_jira_issue()
    else:
        print('not creating issue, already exist........')

main()