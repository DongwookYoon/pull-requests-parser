# pull-requests-parser

## Dependencies
- BeautifulSoup4
- jsonpickle

## Running the application
(Optional) From root directory, create a `.token` file with personal Github access token as content. We won't be able to process a large amount of repo/PRs without a token.

From root directory, use command: `python main.py` and enter either
1. path of excel file as first argument and option "--sheetname" for the name of sheet one wishes to read
1. string of the format _user/repo-name_ (note: when using this approach, all attributes of thre repo below except for prs will be populated by default values)

## Program Behaviour
Program will output `out/<user> <repo-name>.json` from the specified repo names, with objects of the following format:

```perl
- repo
    - py/object         # "model.Repo" -- can ignore
    - name              # <author name>/<name of repository>
    - num_commits       # number of commits
    - num_releases      # number of releases
    - num_contributor   # number of contributors
    - num_watchers      # number of watchers
    - num_stargazers    # number of stars
    - num_forks         # number of forks
    - created_at        # timestamp at which the repository is created
    - updated_at        # timestamp at which the repository is last updated
    - prs[]             # list of all PRs retrived, see request_settings.py for options
        - py/object         # "model.PR" -- can ignore
        - url               # URL of HTML page of pull request
        - status            # status of the PR, one of (unknown, closed, merged, open)
        - comments[]        # list of comments
            - py/object         # "model.Comment" -- can ignore
            - timstamp          # 0, not implemented as of now
            - content           # plain text of user's comment
            - replies           # plain text quoted by the user (most likely as a reply)
            - links[]           # list of links embedded in comment
                - py/object         # "model.Link" -- can ignore
                - url               # URL of the link
                - type              # type of link, one of (unknown, media, issue, user)

```
See `model.py` for implementaion details.

## Customization
`request_settings.py` could be changed for different behaviour in retrieving PRs from a repository.

-------------
## 3/14 update
- the program currently retrieves and analyzes a maximum of 500 most commented PRs from the repo specified for time efficiency. This number is arbitrarily chosen, and can be easily tweaked to retrieve all PRs from a repo.
- adding functionality to filter likely pr discussions- this is done by selecting the PRs whose commits contain at least one of the following file types: html, css, js
- bot comments are filtered out
- timestamps are also retrieved for each comment when possible
- bug fixes (request headers and params, etc.)

The accuracy of these changes are not verified in details, but the current output with several test repos appears very reasonable.

### to be completed
- we discussed the potential to use the parser for repo selection. What would be a good metric for this and how should I present it?

## 3/24 update
- switched from user input to `argparse`, in which all options are specified in the run configuration
- reading from an excel file is now tested
- if reading from an excel file, more information about the repo such as the number of commits, number of forks, and creation time are recorded. The Repo class model is changed accordingly.
- added documentation and attribute definition in `models.py`
- minor code refactoring and bug fixes

### to be completed
- refactoring methods in `repo_parser.py` into appropriate classes in `models.py`

## 3/27 update
- refactored many methods of `repo_parser.py` into class static methods for better organization 
- created new `api_requests.py` fpr abstracting all API calls

## 4/5 update
### to be completed (from Cleidson's feedbacks)
repo:
- ~~add project URL information~~
- ~~add information of total number of PRs extracted~~
- ~~sort PRs by their timestamp~~

pr:
- ~~total number of comments extracted~~
- total number of different people involved in the PR

comment:
- information of author on comment (name)
- ~~total number of @ mentions~~ (same as num_user_links)
- ~~separate the different types of links~~
- ~~information about the total number of external links~~
- identify where a reply within a reply comes from (might be difficult)
- ~~examples of source code not detected~~
- eliminate link from reply as opposed to original comment
- ~~multiple quoted replies are integrated into one comment~~
- not extracting the associated information when someone does a “review" (might be difficult)

links
- suggest "image/media" by file name (should already do that, not sure why it didn't work?)
- if user is mentioned more than once, only show once




