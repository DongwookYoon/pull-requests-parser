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

class Comment:
    """
    A user-created timeline object with text
    
    Attributes:
        timestamp   time of which the comment is made
        content     plain text of user's comment
        replies     plain text of quotes within a user's comments
        links       list of links embedded in comment
    """
    def __init__(self, timestamp = 0, content = "", replies = "", links = []):
        self.timestamp = timestamp
        self.content = content
        self.replies = replies
        self.links = links
        
class PR:
    """
    object representation of a pull request
    
    Attributes:
        url         text of URL to the pull request web page
        status      status of the PR, one of (unknown, closed, merged, open)
        comments    list of comments 
    """
    def __init__(self, url, comments = [], status = "unknown"):
        self.url = url
        self.comments = comments
        self.status = status
        
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
        self.prs = prs
        self.num_commits = num_commits
        self.num_releases = num_releases
        self.num_contributors = num_contributors
        self.num_watchers = num_watchers
        self.num_stargazers = num_stargazers
        self.num_forks = num_forks
        self.created_at = created_at
        self.updated_at = updated_at
        