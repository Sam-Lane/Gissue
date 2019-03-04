# Gissue
🐙 Github issue manager in the command line


## Installing
```bash
$ pip install -r requirements.txt
```

## Using Gissue

### Authenticating With Github.
Before you can use gissue you need to authenticate with GitHub. Gissue uses oauth2 to authenticate and it is super simple to get a token. Simply run:

```bash
$ gissue --generate-token <username> <password>
```

### Getting Issues.


#### Inside a directory with a .git folder
When running gissue inside a directory with a ```.git``` directory it will retrieve all issues on the project you are inside.
```bash
$ gissue

Error when not conected to internet - bug 🐛

Feature to add issue from cli - enhancement 💉
```


#### Inside a directory without a .git folder
When running gissue in a directory that does not contain a ```.git``` directory it will retrieve all issues assigned to ***you*** on Github.



### Adding issues (todo)
