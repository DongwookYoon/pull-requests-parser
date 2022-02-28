class Link:
    def __init__(self, url, type_ = "unknown"):
        self.url = url
        self.type_ = type_

class Comment:
    def __init__(self, timestamp = 0, content = "", replies = "", links = []):
        self.timestamp = timestamp
        self.content = content
        self.replies = replies
        self.links = links
        
class PR:
    def __init__(self, url, comments = [], status = "unknown"):
        self.url = url
        self.comments = comments
        self.status = status
        
class Repo:
    def __init__(self, prs = []):
        self.prs = prs