#!/usr/bin/python3
#	usage: python jira-notification.py
# export JIRA_TOKEN, JIRA_HOST, JIRA_PROJECT, JIRA_USER and GIT_REPO as env variable
#########################################################################################################
# coding=utf-8
from atlassian import Jira
import os

def jira_auth(host, user, token):
    # jira auth requirements
    jira = Jira(
        url="https://" + host + "",
        username="" + user + "",
        password="" + token + "",
        cloud=True)
    return jira

def check_existing_issue(jira, project, repo):
    # default jira JQL query string
    JQL = "project = " + project + " AND labels = " + repo + " AND labels = unit_test AND (statusCategory = 'To Do' OR statusCategory = 'In Progress')"

    data = jira.jql(JQL)
    # checking json total value
    get_total_issue_count = data["total"]

    return get_total_issue_count

def create_jira_issue(jira, project, repo):
    jira.issue_create(
        fields={
            "project": {
                "key": project
            },
            "labels": [
                "" + repo + "",
                "unit_test"
            ],
            "issuetype": {
                "name": "Problem"
            },
            "summary": "" + repo + " failure",
            "description": "unit test module failure",
        }
    )


def main():
    repo = os.environ["GIT_REPO"]
    jiraproject = os.environ["JIRA_PROJECT"]
    jiratoken = os.environ["JIRA_TOKEN"]
    jirahost = os.environ["JIRA_HOST"]
    jirauser = os.environ["JIRA_USER"]

    # auth to jira endpoint using host, user and token
    get_jira_auth = jira_auth(jirahost, jirauser, jiratoken)
    # checking if issue exist, creating issue if total count equals zero
    get_issue_count = check_existing_issue(get_jira_auth, jiraproject, repo)
    if get_issue_count == 0:
        create_jira_issue(get_jira_auth, jiraproject, repo)
    else:
        print('not creating issue, already exist........')


main()
