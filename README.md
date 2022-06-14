
# pull-requests-parser

## Dependencies
- [PyGithub](https://github.com/PyGithub/PyGithub)

## Running the application
First, [create a Github access token.](https://github.students.cs.ubc.ca/settings/tokens)  Place the token into the `token.txt` file. 

From the root directory, run `python3 main.py <organization name>`. The `organization name` argument is optional, and defaults to the `cpsc310-2020w-t1` organization. 

The application will crawl every single repo under the specified Github organization. 

## After running the application
The application saves a JSON file named `results.json`, that tallies the following:

1. The total number of Github issues crawled
2. The total number of Github pull requests crawled
3. The total number of Github issues and pull requests linked detected within all of the issues and pull requests crawled. Links are detected by searching for text strings of the type `#{number}` or hyperlinks directly linking to an issue or pull request.
4. The total number of Github repos crawled (within the specified Github organization)



