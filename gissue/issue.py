import sys, tempfile, os
from subprocess import call

import requests
git_api_url = 'https://api.github.com/repos/{}/{}/issues'

def get_url(repo_address):
    return git_api_url.format(repo_address[0], repo_address[1])

def get_issues(auth_token, repo_address, labels):
    #params = {'access_token' : authToken}
    params = {}
    # TODO: Filtering by labels does not work
    if labels:
        params['labels'] = ",".join(labels)
    print("Params:\n", params)
    issues = requests.get(get_url(repo_address), params=params)
    #print("Issues:\n ", issues)

def send_issue(issueAsDictionary, authToken, repo_address):
    params = {'access_token' : authToken}
    response = requests.post(get_url(repo_address), params=params, json=issueAsDictionary)
    if response.status_code != 201:
        print("Something went wrong")
    else:
        print(issueAsDictionary['title'], "has been created")

def create_new_issue(labels):
    issue = {"title" : "", "body" : "", "labels": []}
    issue['title'] = input("title your issue\n> ")
    issue['body'] = write_issue_body(issue['title'])
    if labels:
        issue['labels'] = labels
    return issue



def write_issue_body(title):
    """
    open users editor set in env or defaults to vim.
    on save will return what user has written as str.
    """
    EDITOR = os.environ.get('EDITOR','nano')

    initial_message = b"#\t" + bytes(title, encoding='utf-8') + b"\n#\n#write the body of your issue in here\n#lines starting with # are ignored"

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        tf.flush()
        call([EDITOR, '+set backupcopy=yes', tf.name])
        tf.seek(0)
        edited_message = tf.read()


    edited_message = edited_message.decode('ascii')
    edited_message = edited_message.splitlines()
    edited_message = list(filter(lambda line:  not line.startswith('#'), edited_message))
    return "".join(edited_message)
