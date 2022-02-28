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

def get_PR_header():
    """
    create header for requests retrieving PRs
    settings can be tweaked for different options
    """
    header = {
        'state': 'all',
        'sort': 'popularity',
        'direction': 'desc',
        'per_page': 5
    }
    token = get_token()
    if token:
        header['Autorization'] = 'token %s' % get_token()
    return header