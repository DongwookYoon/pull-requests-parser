import requests
from model import *
from request_settings import get_PR_header
from bs4 import BeautifulSoup
import jsonpickle
import os

def parse_repo(name, output_dir = "out"):
    """
    input: name of repo in the format: <user>/<repo-name>

    output: object containing parsed repo information (top PRs)
        also output as a json file at <output_dir>/<user> <repo-name>.json
    """

    # get all PRs to create repo object
    url = "https://api.github.com/repos/" + name + "/pulls"
    prs = get_prs(url)
    repo = Repo(prs)

    # save object to file
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = output_dir + "/" + name.replace("/", " ") + ".json"
    with open(filename, 'w') as outfile:
        outfile.write(jsonpickle.encode(repo))
        print("repo output as " + filename)
    return repo

def get_prs(url):
    """
    input: Github API URL for top PRs in the repo. 
        See request_settings.py for options on retrived PRs

    output: list containing parsed top PRs information for specified repo
    """

    response = requests.get(url, get_PR_header())
    prs_json = response.json()
    return [parse_pr(pr) for pr in prs_json]

def parse_pr(pr_json):
    """
    input: json representation of PR retrived from GitHub API

    output: object containing parsed PR information (HTML link, comments, status)
    """
    # retrive html content of a page of PR
    html = pr_json["_links"]["html"]["href"]
        
    page = requests.get(html)
    soup = BeautifulSoup(page.content, "html.parser")

    # find status of PR
    status = soup.find("span", class_ = "State")["title"]

    # find comments
    comment_blocks = soup.find_all(class_="comment-body")
    comments = [parse_comment(comment) for comment in comment_blocks]

    # return a PR pbject
    return PR(html, comments, status)

def parse_comment(comment_block):
    """
    input: DOM element representing "comment-body"

    output: object containing parsed Comment information (timestamp, replies, content, links)
    """
    # TODO: find time stamp - do we have to?
    ts = 0

    # find replies & content
    content, replies = get_comment_content_and_replies(comment_block)

    # find links embedded in comment
    link_blocks = comment_block.find_all("a")
    links = [parse_link(link) for link in link_blocks]

    # return a comment object
    return Comment(ts, content, replies, links)

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