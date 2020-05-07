# github_autopwn
Github Scraper For Static Code Analysis

## Usage:

![screenshot](/images/autopwn.PNG)

This script is only able to be ran against specific user repositories in its current form. 

### Examples

Search for all instances of `mysql_query()` in Microsoft repositories:
```bash
python3 github_autopwn.py --org Microsoft --query "mysql_query"
python3 github_autopwn.py -o Microsoft -q "mysql_query"
```

Search for all instances of every indicator in indicator.py in Docker repositories:
```bash
python3 github_autopwn.py --org Docker --autopwn
python3 github_autopwn.py -o Docker -a
```

Indicators are not 100% accurate, so there is still a need for manual investigative effort to confirm if a bug exists or not. 

### Code Snippets

Attempt printing out all code snippets for found indicators in all of [ethicalhack3r](https://github.com/ethicalhack3r)'s repositories:
```bash
python3 github_autopwn.py --org ethicalhack3r --autopwn --get-code
python3 github_autopwn.py -o ethicalhack3r -a -g
```

Example of this functionality using the --query argument:

![screenshot](/images/autopwn2.PNG)

## Resources

[indicators.py](/indicators.py) was taken from [swissykyrepo](https://github.com/swisskyrepo). If you would like to find out more about his Vulny-Code-Static-Analysis project you can reach him on his twitter here: [pentest_swissky](https://twitter.com/pentest_swissky)

## Important

This project is, unfortunately, banned from use for Offensive Security's OSWE exam. 

# To-do
- (maybe) add function to open an issue with author if a bug is found
- Fix regex finding code-snippets in detected files so results are not duplicated
- Explore searchcode.com functionality
- Build optional auth to search globally/add to rate-limit
