import requests
from request_settings import *

current_page = 0
current_max_page = DEFAULT_MAX_PAGE

def get_prs_from_repo(url, reset_counter = False, max_count = DEFAULT_MAX_PAGE):
    """
    input: url of pull requests,
        whether the user wishes to reset the page counter,
        and the maximum page one wants to get

    output: the next page of pull requests from the url
    """
    global current_page, current_max_page

    if reset_counter:
        current_page = 0
    if max_count != DEFAULT_MAX_PAGE:
        current_max_page = max_count

    current_page += 1
    if current_page > current_max_page:
        current_page = 0
        return []
    print("---- getting page " + str(current_page))
    response = requests.get(url, params = get_PR_params(current_page), headers = token_header())
    temp_prs = response.json()
    if response.status_code != 200 or temp_prs == []:
        current_page = 0
        return []
    return temp_prs

def get_html(url):
    """
    input: url to html page
    output: content of html page
    """
    return requests.get(url).content

def get_github_content(url):
    """
    input: url of github api call
    output: data of the github api call as json
    """
    return requests.get(url, headers = token_header()).json()