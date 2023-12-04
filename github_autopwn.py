#!/usr/bin/env python3
"""
Description: Github Autopwn - Github Scraper For Static Code Analysis
Author: Cody Winkler (twitter: c2thewinkler | github: m0rph-1)
Date: 2/12/2020
"""
import time
import requests
import json
from termcolor import colored
from base64 import b64decode
from indicators import *
from pprint import pprint
import argparse

headers = {
        'Authorization': '' # Add your token here, Example: Authorization: 'Token xxxxxxxxxxxxxxxxxxxxxx'
}

def check_token():
    if not headers['Authorization']:
        print(colored("[!] Authorization token is missing. Please add it to the 'Authorization' variable.", "red"))
        exit(1)

def parse_options():
    global parser
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50)
    parser = argparse.ArgumentParser(description='Github Autopwn - Static Code Analysis Scraper', formatter_class=formatter)
    parser.add_argument("-q", "--query", type=str, help="Bad code to scrape for", required=False)
    parser.add_argument("-o", "--org", type=str, help="Organization to search bad code in e.g. Microsoft", required=True)
    parser.add_argument("-g", "--get-code", dest="get_code", help="Get code snippets for detected indicators", action="store_true", required=False)
    parser.add_argument("-l", "--language", dest="language", type=str, help="Specify the programming language", required=False)
    parser.add_argument("-a", "--autopwn", help="Find all the bugs", action="store_true", required=False)
    parser.add_argument("-crl", "--check-rate-limit", dest="rate", help="Check current API request rate limit", action="store_true", required=False)
    args = parser.parse_args()
    return args

def get_code_snippet(git_url_key):
    this_req = requests.get(git_url_key, verify=True)
    json_data = json.loads(this_req.content)
    if this_req.status_code == 200:
        repo_code = str(b64decode(json_data["content"]).decode('utf-8')).split('\n')
        for payload in payloads:
            for i in range(len(repo_code)):
                if payload[0] + "(" in repo_code[i]:
                    print(str(repo_code[i]))

def check_rate_limit():
    this_req = requests.get("https://api.github.com/rate_limit", verify=True)
    json_data = json.loads(this_req.content)
    pprint(json_data["rate"])
    return

def main(args):
    separator = "-" * 100
    if args.rate:
        check_rate_limit()

    if args.query:
        print(colored("[+] Searching for payload: %s" % args.query, "green"))
        try:
            github_api = f"https://api.github.com/search/code?q=user:{args.org}+{args.query}"
            if args.language:
                github_api += f"+language:{args.language}"

            this_req = requests.get(github_api, headers=headers, verify=True)
            json_data = json.loads(this_req.content)

            if this_req.status_code == 200:
                if json_data["total_count"] == 0:
                    print(colored("[-] No results found for the specified query.", "yellow"))
                else:
                    for key in json_data["items"]:
                        try:
                            print(separator)
                            print(colored("[+] Found Potentially Vulnerable %s Code In The Following File!" % args.query, "green"))
                            pprint(key["html_url"])
                            print(separator)

                            if args.get_code:
                                print(colored("This should be printed if -g is specified", "yellow"))
                                git_url_key = key["git_url"]
                                get_code_snippet(git_url_key)

                        except KeyError:
                            print(colored("[-] Didn't find anything. Moving on!", "red"))

            if this_req.status_code != 200:
                print(colored("[!] Check rate limit.", "yellow"))
                pass

        except Exception as e:
            print(repr(e))

    if args.autopwn:
        for payload in payloads:
            print(colored("[+] Searching for payload: %s" % payload[0], "green"))
            try:
                github_api = f"https://api.github.com/search/code?q=user:{args.org}+{payload[0]}"
                if args.language:
                    github_api += f"+language:{args.language}"

                this_req = requests.get(github_api, headers=headers, verify=True)
                json_data = json.loads(this_req.content)
                print(colored("[!] Got status code: %d" % this_req.status_code, "yellow"))

                if this_req.status_code == 200:
                    if json_data["total_count"] == 0:
                        print(colored("[-] No results found for the specified payload.", "yellow"))
                    else:
                        print(colored("[+] Found Potentially %s Vulnerable Code In The Following Files!" % payload[0], "green"))

                        for key in json_data["items"]:
                            try:
                                pprint(key["html_url"])
                                time.sleep(0.5)

                                if args.get_code:
                                    git_url_key = key["git_url"]
                                    get_code_snippet(git_url_key)

                            except KeyError as e:
                                print(colored("[-] Didn't find anything. Moving on!", "red"))

                if this_req.status_code != 200:
                    print(colored("[!] Check rate limit. Sleeping for 15 seconds.", "yellow"))
                    check_rate_limit()
                    time.sleep(15)
                    pass

            except Exception as e:
                print(repr(e))

if __name__ == "__main__":
    check_token() 
    args = parse_options()
    main(args)
