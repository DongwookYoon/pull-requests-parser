import os
import jsonpickle
from bs4 import BeautifulSoup
from api_requests import *
class Link:
    """
    An appearance of URL within any comments on the parsed PR page
    
    Attributes:
        url     text of URL of the link
        type    type of link, one of (unknown, media, issue, user)
    """
    def __init__(self, url, type_ = "unknown"):
        self.url = url
        self.type_ = type_

    def parse(link_block):
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
        else:
            if link_block["href"].startswith("https://github.com"):
                type_ = "other-internal"
            else:
                type_ = "other-external"
        return Link(link_block["href"], type_)

class Comment:
    """
    A user-created timeline object with text
    
    Attributes:
        timestamp   time of which the comment is made
        content     plain text of user's comment
        replies     plain text of quotes within a user's comments
        links       list of links embedded in comment
    """
    def __init__(self, timestamp = 0, content = "", replies = "", user_links = [], issue_links = [],
    media_links = [], code_blocks = [], other_internal_links = [], other_external_links = [], author = ""):
        self.timestamp = timestamp
        self.content = content
        self.replies = replies
        self.user_links = user_links
        self.num_user_links = len(user_links)
        self.issue_links = issue_links
        self.num_issue_links = len(issue_links)
        self.media_links = media_links
        self.num_media_links = len(media_links)
        self.code_blocks = code_blocks
        self.num_code_blocks = len(code_blocks)
        self.other_internal_links = other_internal_links
        self.num_other_internal_links = len(other_internal_links)
        self.other_external_links = len(other_external_links)
        self.num_other_external_links = len(other_external_links)
        self.author = author

    def get_comment_details(comment_block):
        """
        input: DOM element with class "comment-body"

        output: string tuple representing plain comment content and quoted replies, respectively
        """

        replies = []
        content = ""
        code_blocks = []

        user_links = []
        issue_links = []
        media_links = []
        other_internal_links = []
        other_external_links = []
        
        links = {
            "user": user_links,
            "issue": issue_links,
            "media": media_links,
            "other-internal": other_internal_links,
            "other-external": other_external_links,
            "unknown": []
        }
        # iterate through entire comment to check for blockquotes (replies)
        for child in comment_block.findChildren(recursive=False):
            if (child.name == "blockquote"):
                replies.append(child.text)
            elif (child.name == "code"):
                code_blocks.append(child.text)
            else:
                content += child.text + "\n"
                link_blocks = child.find_all("a")
                [links[link_obj.type_].append(link_obj) for link_obj in [Link.parse(link) for link in link_blocks]]
        return (content, replies, code_blocks, links)
        
    def parse(comment_container):
        """
        input: DOM element representing "comment-body"

        output: object containing parsed Comment information (timestamp, replies, content, links)
        """
        print("---- parsing comment")

        # find timestamp (default value is 0)
        relative_time_container = comment_container.find("relative-time")
        time = relative_time_container["datetime"] if relative_time_container else 0

        comment_block = comment_container.find(class_ = "comment-body")
        author = comment_container.find(class_ = "author").text
        # find replies & content
        content, replies, code_blocks, links = Comment.get_comment_details(comment_block)

        # return a comment object
        return Comment(timestamp = time, content = content, replies = replies, author = author,
            user_links = links["user"], issue_links = links["issue"], media_links = links["media"],
            code_blocks = code_blocks, other_internal_links= links["other-internal"], other_external_links= links["other-external"])

class PR:
    """
    object representation of a pull request
    
    Attributes:
        url         text of URL to the pull request web page
        status      status of the PR, one of (unknown, closed, merged, open)
        comments    list of comments 
    """
    def __init__(self, url, comments = [], status = "unknown", num_commenters = 0):
        self.url = url
        self.comments = comments
        self.num_comments = len(comments)
        self.status = status
        self.num_commenters = num_commenters

    # same as parse pr
    def parse(pr_json):
        """
        input: json representation of PR retrived from GitHub API

        output: object containing parsed PR information (HTML link, comments, status)
        """
        print("-- parsing pr")
        # retrive html content of a page of PR
        html = pr_json["_links"]["html"]["href"]
        soup = BeautifulSoup(get_html(html), "html.parser")

        # find status of PR
        status = soup.find("span", class_ = "State")["title"]

        # find comments
        comment_containers = soup.find_all(class_="timeline-comment")
        comments = [Comment.parse(comment) for comment in comment_containers]
        authors = {comment.author for comment in comments}

        # return a PR pbject
        return PR(html, comments, status, len(authors))

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
            commits = get_github_content(commits_link)

            for commit in commits:
                # retrieve changed files for each commit, stop & return true when a target file type is found
                commit_details = get_github_content(commit["url"])
                filenames = [file["filename"] for file in commit_details["files"]] 
                filtered_filenames = list(filter(is_target_file_type, filenames))
                if len(filtered_filenames) > 0:
                    return True
            return False
            
        return filter(lambda pr_json: not author_is_bot(pr_json) and pr_contains_ui_changes(pr_json), prs_json)
        
class Repo:
    """
    object representation of a repository
    
    Attributes:
        name            <author name>/<name of repository>
        prs             a list of pull requests within the repository
        num_commits     number of commits
        num_releases    number of releases
        num_contributor number of contributors
        num_watchers    number of watchers
        num_stargazers  number of stars
        num_forks       number of forks
        created_at      timestamp at which the repository is created
        updated_at      timestamp at which the repository is last updated
    """
    def __init__(self, name, prs = [], num_commits = 0, num_releases = 0, num_contributors = 0, 
    num_watchers = 0, num_stargazers = 0, num_forks = 0, created_at = None, updated_at = None):
        self.name = name
        self.url = "https://api.github.com/repos/" + name + "/pulls"
        self.setPRs(prs)
        self.num_commits = num_commits
        self.num_releases = num_releases
        self.num_contributors = num_contributors
        self.num_watchers = num_watchers
        self.num_stargazers = num_stargazers
        self.num_forks = num_forks
        self.created_at = created_at
        self.updated_at = updated_at

    # same as save_repo in 
    def save(self, filename, output_dir = "out"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_dir + "/" + filename, 'w') as outfile:
            outfile.write(jsonpickle.encode(self))
            print("repo output as " + filename)
    
    def setPRs(self, prs):
        self.prs = prs
        self.num_prs = len(prs)
        