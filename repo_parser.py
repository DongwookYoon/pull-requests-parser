from api_requests import get_prs_from_repo
from model import *

def fetch_pr_info_in_repo(repo):
    """
    input: repo object with name in the format: <user>/<repo-name>

    output: object containing parsed repo information (top PRs)
        also output as a json file at <output_dir>/<user> <repo-name>.json
    """
    print("- parsing repo")
    # get all PRs to create repo object
    url = "https://api.github.com/repos/" + repo.name + "/pulls"
    prs = get_top_prs(url)
    repo.prs = prs

    # save object to file
    repo.save(filename = repo.name.replace("/", " ") + ".json", output_dir = "out")
    return repo

def get_top_prs(url):
    """
    input: Github API URL for top PRs in the repo. 
        See request_settings.py for options on retrived PRs

    output: list containing parsed top PRs information for specified repo

    note: "top pr" refers to PRs that are likely to contain UI discussions
        criterias of which are in the description for filter_likely_ui_discussions
    """
    print("-- getting top prs")
    prs = []
    temp_prs = get_prs_from_repo(url)

    while(temp_prs != []):
        prs.extend(temp_prs)
        temp_prs = get_prs_from_repo(url)

    return [PR.parse(pr) for pr in PR.filter_likely_ui_discussions(prs)]