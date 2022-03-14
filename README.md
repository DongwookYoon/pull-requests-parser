# pull-requests-parser

## Dependencies
- BeautifulSoup4
- jsonpickle

## Running the application
(Optional) From root directory, create a `.token` file with personal Github access token as content. We won't be able to process a large amount of repo/PRs without a token.

From root directory, use command: `python main.py`

## Description
When prompted, enter either
1. path of excel file containing "Sheet 1", with column "name", with each entry of format _user/repo-name_ (NOT TESTED YET)
1. string of the format _user/repo-name_

Program will output `out/<user> <repo-name>.json` from the specified repo names, with objects of the following format:

```perl
- repo
    - py/object         # "model.Repo" -- can ignore
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

-------------
## 3/14

### update
- the program currently retrieves and analyzes a maximum of 500 most commented PRs from the repo specified for time efficiency. This number is arbitrarily chosen, and can be easily tweaked to retrieve all PRs from a repo.
- adding functionality to filter likely pr discussions- this is done by selecting the PRs whose commits contain at least one of the following file types: html, css, js
- bot comments are filtered out
- timestamps are also retrieved for each comment

The accuracy of these changes are not verified in details, but the current output with several test repos appears very reasonable.

### to be completed
- we discussed the potential to use the parser for repo selection. What would be a good metric for this and how should I present it?

