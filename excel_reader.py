import pandas

def get_repo_names_from_excel(file, sheet):
    """
    input: path and sheet name of an excel file containing 
        a column called "name" with <user>/<repo-name> on each entry

    output: list of <user>/<repo-name>
    """
    column = pandas.read_excel(file, sheet_name=sheet)
    return column["name"]
