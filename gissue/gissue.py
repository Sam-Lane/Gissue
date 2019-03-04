#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import re
import argparse

from auth import Auth



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

def get_issues_for_dir(authToken, repo_address):
    """
    """
    params = {'access_token' : authToken}
    req = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_address[0], repo_address[1]), params=params)
    if req.status_code is not 200:
        print(req)
        raise IOError
    else:
        return req.json()

def get_repo_and_user():
    with open(".git/config") as gitconfig:
        file = gitconfig.read()
        file = file.splitlines()
        url = list(map(lambda x: x.strip(), filter(lambda line: 'url' in line, file)))[0].split("/")
        repo = list(filter(lambda line: ".git" in line, url))[0]
        repo = re.search('^[^.]+', repo).group(0)
        user = url[3]

        return (user, repo)

def git_in_this_directory():
    """
    Returns true if a .git directory exists in the current directoy
    """
    return os.path.isdir(".git")

def get_label_type(label_data):
    return {
        'bug' : ' 🐛',
        'enhancement' : ' 💉'
    }.get(label_data, "")

def print_issue(issue_data):
    label = get_label_type(issue_data['labels'][0]['name'])

    print(issue_data['title'], " - ", issue_data['labels'][0]['name'], label)



if __name__ == "__main__":
    auth = Auth()

    parser = argparse.ArgumentParser()
    parser.add_argument('--generate-token', nargs=2)
    parser.add_argument('--update-token', nargs=1)
    args = parser.parse_args()

    if args.generate_token:
        auth.gen_token(args.generate_token[0], args.generate_token[1])
        exit()
    if args.update_token:
        auth.update_token(args.update_token[0])
        exit()


    token = auth.get_token()

    if not git_in_this_directory():
        #if no .git in this directory lets get all your current issues.
        issues = get_all_my_issues(token)
        for issue in issues:
            print_issue(issue)
    else:
        issues = get_issues_for_dir(token, get_repo_and_user())
        for issue in issues:
            print_issue(issue)
