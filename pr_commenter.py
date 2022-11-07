"""Create or upgrade a comment in a given PR"""
import os
import sys
from docopt import docopt
import fileinput
from github import Github, GithubException

usage = """
Usage:
  pr_commenter (-h | --help)
  pr_commenter <repo> <pr> <file>... [--title=<title>] [--wrap=<language>] [--token=<token>] [--tag=<tag>...]

Options:
  -h --help                         Show this screen.  
  --title=<title>                   Title for the comment
  --wrap=<language>                 Wrap the comment as code language
  --token=<token>                   Github token. Default to the envvar PR_COMMENTER_GITHUB_TOKEN.
  --label=<label>                   Add label/s if there were a comment
"""

__version__ = "0.1"

def main(argv=None) -> None:
    args = docopt(__doc__ + usage, argv, version=__version__)
    comment = ""
    with fileinput.input(files=args["<file>"], encoding="utf-8") as f:
        for line in f:
            comment += line
    
    comment = comment.strip()
    if not comment:
        print("No comment found. Exiting.")
        return

    wrap_start = f"```{args['--wrap']}\n" if args['--wrap'] else ""
    wrap_end = f"\n```" if args['--wrap'] else ""
    title = f"{args['--title']}" if args["--title"] else "[AUTOMATIC COMMENT]"
    
    comment = f"{title}\n\n{wrap_start}{comment}{wrap_end}"

    gh = Github(args["--token"] or os.environ.get("PR_COMMENTER_GITHUB_TOKEN"))
    
    # update or create a comment
    existent_comment = None    
    for c_issue in pr.get_issue_comments():
        if c_issue.body.startswith(title):
            existent_comment = c_issue
            break
    if existent_comment:
        issue_comment = existent_comment.edit(comment)
        print("Comment updated")
    else:
        issue_comment = pr.create_issue_comment(comment)
        print("Comment created")
    
    print(issue_comment.url)

    if args["--label"]:        
        pr.add_to_labels(*args["--label"])



if __name__ == '__main__':
    main()    
