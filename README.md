# pull-requests-parser

## Dependencies
- [PyGithub](https://github.com/PyGithub/PyGithub)
- Datetime

# Running the Application

In the root directory, create a `token.txt` file with your personal Github access token as content.

Run the parser by using `python3 main.py`. The `main.py` file detect and finds all mentions to issues/pull request within a GitHub project. The result is output to a file called `graph.txt`.

You can perform an analysis of `graph.txt` by running the provided `analysis.py` file using `python3 analysis.py`. Currently the tool detects source nodes, sink nodes, isolated nodes, and loop nodes. 

# Running the visualisation

Before running the visualisation, preprocessing of the `graph.txt` file is required. Run `python3 vis.py` to output a `D3.js`-friendly JSON file. The file is outputted into the `data` directory.

Finally, run the visualisation by starting a server (`python3 -m http.server`) from the root directory. 






