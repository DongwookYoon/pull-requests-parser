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
        'sort': 'popularity',
        'direction': 'desc',
        'per_page': '100',
        'page' : str(page)
    }

def token_header():
    token = get_token()
    if token:
        return {'Authorization': 'token %s' % token}
    else:
        return {}