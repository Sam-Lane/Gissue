#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import re
import argparse

from auth import Auth, InvalidTokenError
import issue



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
        'bug' : '🐛 ',
        'enhancement' : '💉 ',
        'help wanted' : '🙏🏻 ',
        'question' : '❓ ',
        'good first issue' : '🐣 ',
        'wontfix' : '⛔️ '
    }.get(label_data, "")

def print_issue(issue_data):
    if len(issue_data['labels']) > 0:
        label = get_label_type(issue_data['labels'][0]['name'])
        print(label + issue_data['labels'][0]['name'], " - ", issue_data['title'])
    else:
        print(issue_data['title'])


def get_user_and_pass():
    from getpass import getpass
    """
    get the users Github username and password
    Password input is in non echo mode from terminal so no on lookers can see password.

    returns a dictionary containing 'user' and 'password'
    """
    userpass = {'user' : '', 'password' : ''}

    userpass['user'] = input("Github Username: ")
    userpass['password'] = getpass()

    return userpass


def add_issue(args, token):
    newIssue = issue.create_new_issue(args.label)
    issue.send_issue(newIssue, token, get_repo_and_user())
    exit()

def show_issues(args, token):
    if args:
        issue.get_issues(token, get_repo_and_user(), args.label)
    else:
        issue.get_issues(token, get_repo_and_user(), None)

def main():
    auth = Auth()

    parser = argparse.ArgumentParser()
    parser.add_argument('--generate-token', nargs='*')
    parser.add_argument('--update-token', nargs=1)

    # Define shared optional arguments

    # TODO: Add help to the '--label' arg. Cant find a way to add it without throwing an error
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--label', choices=['bug', 'duplicate', 'enhancement', 'good first issue', 'help wanted', 'invalid', 'question', 'hotfix'], nargs='+')
    # The commands the user can use
    sp = parser.add_subparsers()
    sp_add = sp.add_parser('add', parents=[parent_parser], help='Add an issue to the current git repo')
    sp_show = sp.add_parser('show', parents=[parent_parser], help='Shows all the issues in the current git repo')

    sp_add.set_defaults(func=add_issue)
    sp_show.set_defaults(func=show_issues)


    args = parser.parse_args()


    if args.generate_token is not None:
        username_password = get_user_and_pass()
        auth.gen_token(username_password['user'], username_password['password'])
        exit()
    if args.update_token:
        auth.update_token(args.update_token[0])
        exit()


    try:
        token = auth.get_token()
    except InvalidTokenError as error:
        print(error)
        exit()

    if git_in_this_directory():
        try:
            args.func(args, token)
        except AttributeError:
            show_issues(None, token)
    else:
        print("This is not a git directory.")
        exit()


    if not git_in_this_directory():
        #if no .git in this directory lets get all your current issues.
        issues = get_all_my_issues(token)
        for issue in issues:
            print_issue(issue)
    else:
        issues = get_issues_for_dir(token, get_repo_and_user())
        for issue in issues:
            print_issue(issue)


if __name__ == "__main__":
    main()