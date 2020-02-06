#!/usr/bin/env python3
import requests
import json
from pprint import pprint
import argparse

def parse_options():

    global parser
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=50)
    parser = argparse.ArgumentParser(description='Use -sp to bypass SNMP ACL\'s that don\'t specify deny ip any any', formatter_class=formatter)
    parser.add_argument("-q", "--query", type=str, help="Bad code to scrape for", required=True)
    parser.add_argument("-o", "--org", type=str, help="Organization to search bad code in e.g. Microsoft", required=True)
    args = parser.parse_args()
    return args

def main(args):

    try:

        github_api = ("https://api.github.com/search/code?q=user:{} {}").format(args.org, args.query)
        this_req = requests.get(github_api, verify=True)
        json_data = json.loads(this_req.content)
        print(this_req.status_code)
        pprint(json_data)

    except (Exception, NameError):
        print(Exception, NameError)

if __name__ in "__main__":

    args = parse_options()
    main(args)
