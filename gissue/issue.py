import sys, tempfile, os
from subprocess import call

import requests
git_api_url = 'https://api.github.com/repos/{}/{}/issues'

def get_url(repo_address):
    return git_api_url.format(repo_address[0], repo_address[1])

def get_issues(auth_token, repo_address, args):
    params = {'access_token' : auth_token}

    url = ""
    if args is None:
        url = get_url(repo_address)
    else:
        if args.label:
            params['labels'] = ",".join(args.label)

        if args.state:
            params['state'] = args.state

        if args.number:
            # Return a single issue
            url = get_url(repo_address) + "/" + str(args.number)
        else:
            url = get_url(repo_address)

    return get_json(url, params)



# Gets a json from github, either a list of issues or a single issue
def get_json(url, params):
    req = requests.get(url, params=params)
    if req.status_code is not 200:
        raise IOError
    else:
        return req.json()


def get_all_my_issues(authToken):
    """
    takes two params as string, user & passwd. which are used for auth.
    returns all the issues from github on a user account.
    """
    params = {'access_token' : authToken}
    req = requests.get('https://api.github.com/issues', params=params)

    if req.status_code is not 200:
        raise IOError
    else:
        return req.json()


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

    initial_message = b"\n#\t" + bytes(title, encoding='utf-8') + b"\n#\n#write the body of your issue in here\n#lines starting with # are ignored"

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
