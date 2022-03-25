import pandas
from model import Repo

def get_repos_from_excel(file, sheet):
    """
    input: path and sheet name of an excel file containing 
        a column called "name" with <user>/<repo-name> on each entry

    output: list of <user>/<repo-name>
    """
    df = pandas.read_excel(file, sheet_name=sheet)
    names = df["name"]
    commits = df["commits"]
    releases = df["releases"]
    contributors = df["contributors"]
    forks = df["forks"]
    watchers = df["watchers"]
    stargazers = df["stargazers"]
    createdAt = df["createdAt"]
    updatedAt = df["updatedAt"]
    repos = []

    for i in range(len(df)):
        repos.append(
            Repo(
                names[i],
                num_commits=str(commits[i]),
                num_releases=str(releases[i]),
                num_contributors=str(contributors[i]),
                num_watchers=str(watchers[i]),
                num_forks=str(forks[i]),
                num_stargazers=str(stargazers[i]),
                created_at=str(createdAt[i]),
                updated_at=str(updatedAt[i])
            )
        )
    return repos
