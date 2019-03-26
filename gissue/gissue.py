#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os, sys
import re
import argparse
from colr import color
from urllib.parse import urlparse

from auth import Auth, InvalidTokenError
import issue


def get_repo_and_user():
    with open(".git/config") as gitconfig:
        file = gitconfig.read()
        file = file.splitlines()

        url = urlparse(list(map(lambda x: x.strip(),
            filter(lambda line: 'url' in line, file)))[0][6:])

        if url.scheme in ['http', 'https']:
            path = url.path[1:]
            (user, repo) = path.split('/')
        else:
            # assume ssh url
            path = url.path.split(':')[1]
            print(path)
            (user, repo) = path.split('/')

        # strip '.git'
        return (user, repo[:-4])

def git_in_this_directory():
    """
    Returns true if a .git directory exists in the current directoy
    """
    return os.path.isdir(".git")

def get_label_type(label_data):
    """
    takes a label name and returns a matching emoji if we have it.
    """
    return {
        'bug' : '🐛',
        'enhancement' : '💉',
        'help wanted' : '🙏🏻',
        'question' : '❓',
        'good first issue' : '🐣',
        'wontfix' : '⛔️'
    }.get(label_data, label_data) # if we dont have a emoji for your label return the label text

def print_issue(issue_data):

    if len(issue_data['labels']) > 0:
        label = get_label_type(issue_data['labels'][0]['name'])

        issueString = color("(" + str(issue_data['number']) + ") ", fore=issue_data['labels'][0]['color']) + label + " - " + issue_data['title'][:150] #print the first 150 chars of the title

        print(issueString, "\n")
    else:
        print("(" + str(issue_data['number']) + ")", "-", issue_data['title'][:150], "\n")


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
    # TODO: add a choice to show all the user's issues
    # issues = get_all_my_issues(token)
    # for issue in issues:
    #     print_issue(issue)
    #
    if args is None:
        issues = issue.get_issues(token, get_repo_and_user(), None)
    else:
        issues = issue.get_issues(token, get_repo_and_user(), args)



    if len(issues) > 0:
        if args is not None and args.number:
            print_issue(issues)
        else:
            for i in issues:
                print_issue(i)
    else:
        print('🎉 Hooray. No issues in this repo! 🎉')

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

    sp_show.add_argument('--number', type=int, help='Show an issue with a given number')
    sp_show.add_argument('--state', choices=['open', 'closed', 'all'], default='open', help='Show issues with a given state')
    sp_show.set_defaults(which='show')

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
        print("\n")
        try:
            if not len(sys.argv) > 1:
                raise AttributeError('No arguments specified. Printing out all issues in the repo')

            args.func(args, token)
        except AttributeError:
            show_issues(None, token)
    else:
        print("This is not a git directory.")
        exit()


if __name__ == "__main__":
    main()

