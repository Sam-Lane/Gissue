# Gissue

[![Build Status](https://travis-ci.org/Sam-Lane/Gissue.svg?branch=master)](https://travis-ci.org/Sam-Lane/Gissue)
[![issues](https://img.shields.io/github/issues-raw/Sam-Lane/Gissue.svg)]()


🐙 Github issue manager in the command line

## Installing

##### clone the repository
```bash
$ git clone https://github.com/Sam-Lane/Gissue.git
```

##### install dependencies
```bash
$ pip install -r requirements.txt
```

##### link gissue.py to /usr/local/bin
```bash
$ ln -s $PWD/gissue/gissue.py /usr/local/bin/gissue
```

## Using Gissue

### Authenticating With Github.
Before you can use gissue you need to authenticate with GitHub. Gissue uses Githubs personal access tokens to authenticate and it is super simple to get a token. Simply run:

```bash
$ gissue --generate-token
```

You will then be prompted for your Github username & password.

If your account is secured with oauth this will not work. You will need to go to Github and generate a token in your user settings. Once you have your token run:

```bash
$ gissue --update-token <your token from github here>
```

You should now be authenticated with the Github servers.


### Getting Issues.


#### Inside a directory with a .git folder
When running gissue inside a directory with a ```.git``` directory it will retrieve all issues on the project you are inside.
```bash
$ gissue

(2)🐛 bug - Error when not conected to internet

(1)💉 enhancement - Feature to add issue from cli
```


#### Inside a directory without a .git folder
When running gissue in a directory that does not contain a ```.git``` directory it will retrieve all issues assigned to ***you*** on Github.



### Adding issues
Creating an issue is easy

```bash
$ gissue add
title your issue
> my new issue
```

- gissue will now open your editor defined in the users env variables or default to nano.

- Here you can write the body of your issue. Lines starting with # are ignored. Or leave it blank.

- Save and quit from the editor and your new issue will be posted to github.

```bash
my new issue has been created
```

### Adding issues with labels
You can add issues with one or more labels with the optional ```--label``` argument.
```bash
$ gissue add --label bug
```
You can specify one or more labels from the following labels
[bug, duplicate, enhancement, good first issue, help wanted, invalid, question, hotfix]

### Show the issues in the git repostitory
You can retrieve and print out all the issues in the current repo
```bash
$ gissue show
```

#### Additional Show arguments
There are optional arguments which can be written after the ```show``` command

```bash
$ gissue show --number [number]
```
Retrieves and gets the issue with number/id 1 in the repostitory.


```bash
$ gissue show --state [open, closed, all]
```

Displays issues with the defined state.



## Todo:
- [ ] Add testing suite
- [ ] Add labels to new issue
- [ ] Add comment to existing label
- [ ] Close an issue
- [ ] Open an issue to github website

## Contributors:
- [Erik Lange](https://github.com/eriklange)
