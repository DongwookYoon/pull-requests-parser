import requests
from model import *
from request_settings import *
from bs4 import BeautifulSoup
import jsonpickle
import os
import json

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
    save_repo(repo)
    return repo

def save_repo(repo, output_dir = "out"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = output_dir + "/" + repo.name.replace("/", " ") + ".json"
    with open(filename, 'w') as outfile:
        outfile.write(jsonpickle.encode(repo))
        print("repo output as " + filename)

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
    temp_prs = requests.get(url, params = get_PR_params(), headers = token_header()).json()
    counter = 2

    # getting 500 PRs max from a repo, we  can tweak this as needed
    while(temp_prs != [] and counter <= 5):
        print("---- getting page " + str(counter))
        prs.extend(temp_prs)
        response = requests.get(url, params = get_PR_params(counter), headers = token_header())
        temp_prs = response.json()
        if response.status_code != 200:
            break
        counter += 1

    return [parse_pr(pr) for pr in filter_likely_ui_discussions(prs)]

def filter_likely_ui_discussions(prs_json):
    """
    given a list of json representing prs
    return a list of pr that likely contains UI discussions

    criterias considered:
        - user does not have [bot] tag
        - have commits containing html, css, or js files
    """
    print("---- filtering likely ui discussions")
    def author_is_bot(pr_json):
        pr_json["user"]["type"] == "Bot"

    def pr_contains_ui_changes(pr_json):
        # set up filter criteria on file types
        target_file_types = ("html", "css", "js")
        def is_target_file_type(filename):
            return filename.endswith(target_file_types)

        # retrieve all commits in the PR
        commits_link = pr_json["_links"]["commits"]["href"]
        commits = requests.get(commits_link, headers = token_header()).json()

        for commit in commits:
            # retrieve changed files for each commit, stop & return true when a target file type is found
            commit_details = requests.get(commit["url"], headers = token_header()).json()
            print(commit_details)
            filenames = [file["filename"] for file in commit_details["files"]] 
            filtered_filenames = list(filter(is_target_file_type, filenames))
            if len(filtered_filenames) > 0:
                return True
        return False
        
    return filter(lambda pr_json: not author_is_bot(pr_json) and pr_contains_ui_changes(pr_json), prs_json)


def parse_pr(pr_json):
    """
    input: json representation of PR retrived from GitHub API

    output: object containing parsed PR information (HTML link, comments, status)
    """
    print("-- parsing pr")
    # retrive html content of a page of PR
    html = pr_json["_links"]["html"]["href"]
        
    page = requests.get(html)
    soup = BeautifulSoup(page.content, "html.parser")

    # find status of PR
    status = soup.find("span", class_ = "State")["title"]

    # find comments
    comment_containers = soup.find_all(class_="timeline-comment")
    comments = [parse_comment(comment) for comment in comment_containers]

    # return a PR pbject
    return PR(html, comments, status)

def parse_comment(comment_container):
    """
    input: DOM element representing "comment-body"

    output: object containing parsed Comment information (timestamp, replies, content, links)
    """
    print("---- parsing comments")
    # find timestamp (default value is 0)
    relative_time_container = comment_container.find("relative-time")
    time = relative_time_container["datetime"] if relative_time_container else 0

    comment_block = comment_container.find(class_ = "comment-body")
    # find replies & content
    content, replies = get_comment_content_and_replies(comment_block)

    # find links embedded in comment
    link_blocks = comment_block.find_all("a")
    links = [parse_link(link) for link in link_blocks]

    # return a comment object
    return Comment(time, content, replies, links)

def get_comment_content_and_replies(comment_block):
    """
    input: DOM element with class "comment-body"

    output: string tuple representing plain comment content and quoted replies, respectively
    """

    replies = ""
    content = ""
    # iterate through entire comment to check for blockquotes (replies)
    for child in comment_block.findChildren(recursive=False):
        if (child.name == "blockquote"):
            replies += child.text + "\n"
        else:
            content += child.text + "\n"
    return (content, replies)


def parse_link(link_block):
    """
    input: DOM element with <a> tag inside elements of class "comment-body"

    output: object containing parsed Link information (URL, link type)
    """

    type_ = "unknown"
    if link_block.find("img"):
        type_ = "media"
    elif link_block.get("class"):
        if "user-mention" in link_block.get("class"):
            type_ = "user"
        elif "issue-link" in link_block.get("class"):
            type_ = "issue"
    return Link(link_block["href"], type_)