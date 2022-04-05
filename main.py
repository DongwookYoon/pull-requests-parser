from excel_reader import get_repos_from_excel
from repo_parser import fetch_pr_info_in_repo
from model import *
import argparse

def main():
    """
    entry point of the program, takes in either
    1. path of excel file with column "name", with each entry formatted <user>/<repo-name> 
    2. <user>/<repo-name>

    output: a json representation of parsed data
    """
    argparser = argparse.ArgumentParser()
    argparser.add_argument("dest", help = "path to excel file or <user>/<repo>: ")
    argparser.add_argument("--sheetname", type=str, help = "sheetname if inputting excel sheets")
    args = argparser.parse_args()
    answer = args.dest

    if answer.endswith(".xlsx"):
        print("excel file detected")
        if (args.sheetname == None):
            print("sheetname option is required")
        for repo in get_repos_from_excel(answer, args.sheetname):
            print(repo)
            fetch_pr_info_in_repo(repo)

    else:
        print("single repo detected")
        fetch_pr_info_in_repo(Repo(answer))

if __name__ == "__main__":
    main()