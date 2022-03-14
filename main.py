from excel_reader import get_repo_names_from_excel
from repo_parser import parse_repo

def main():
    """
    entry point of the program, takes in either
    1. path of excel file with column "name", with each entry formatted <user>/<repo-name> 
    2. <user>/<repo-name>

    output: a json representation of parsed data
    """

    print("enter path to excel file or <user>/<repo>: ")
    answer = str(input())
    if answer.endswith(".xlsx"):
        print("excel file detected")
        print("enter sheet name: ")
        sheet = str(input())
        for url in get_repo_names_from_excel(answer, sheet):
            parse_repo(url)

    else:
        print("single repo detected")
        parse_repo(answer)

if __name__ == "__main__":
    main()