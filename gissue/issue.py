import sys, tempfile, os
from subprocess import call

import requests


def send_issue(issueAsDictionary, authToken, repo_address):
    params = {'access_token' : authToken}
    response = requests.post('https://api.github.com/repos/{}/{}/issues'.format(repo_address[0], repo_address[1]), params=params, json=issueAsDictionary)
    if response.status_code != 201:
        print("Something went wrong")
    else:
        print(issueAsDictionary['title'], "has been created")

def create_new_issue():
    issue = {"title" : "", "body" : "", "labels": []}
    issue['title'] = input("title your issue\n> ")
    issue['body'] = write_issue_body(issue['title'])

    return issue



def write_issue_body(title):
    """
    open users editor set in env or defaults to vim.
    on save will return what user has written as str.
    """
    EDITOR = os.environ.get('EDITOR','vim')     

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