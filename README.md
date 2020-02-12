# github_autopwn
Github Scraper For Static Code Analysis

## Usage:

![screenshot](autopwn.PNG)

### Examples

Search for all instances of `mysql_query()` in Microsoft repositories:
```
python3 github_autopwn.py --org Microsoft --query "mysql_query"
python3 github_autopwn.py -o Microsoft -q "mysql_query"
```

Search for all instances of every indicator in indicator.py in Github repositories:
```
python3 github_autopwn.py --org Github --autopwn
python3 github_autopwn.py -o Github -a
```

Indicators are not 100% accurate, so there is still a need for manual investigative effort to confirm if a bug exists or not. 

### Beta

Attempt printing out all code snippets for found indicators in all Github repositories:
```
python3 beta_test.py --org Github --autopwn --get-code
python3 beta_test.py -o Github -a -g
```

# To-do
- (maybe) add function to open an issue with author if a bug is found
- Fix regex to find code-snippets in detected files
- Explore searchcode.com
- Build optional auth to search globally/add to rate-limit
