def get_token():
    """
    get personal access token from .token
    return None if no token found
    """

    token = None
    try:
        with open(".token") as f:
            token = f.read()
    except IOError:
        pass
    return token

def get_PR_params(page = 1):
    """
    create header for requests retrieving PRs
    settings can be tweaked for different options
    """
    return {
        'state': 'all',
        'sort': 'updated', # not sure if we're talking about creation date or last updated date
        'direction': 'desc',
        'per_page': '100',
        'page' : str(page)
    }

def token_header():
    """
    return a general header for any githb api request
    """
    token = get_token()
    if token:
        return {'Authorization': 'token %s' % token}
    else:
        return {}

"""
the maximum page of PRs one wishes to get
"""
DEFAULT_MAX_PAGE = float('inf')