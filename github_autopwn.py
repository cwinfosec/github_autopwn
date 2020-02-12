#!/usr/bin/env python3
"""
Description: Github Autopwn - Github Scraper For Static Code Analysis
Author: Cody Winkler (twitter: c2thewinkler | github: m0rph-1)
Date: 2/12/2020
"""
import time
import requests
import json
import sys
from indicators import *
from pprint import pprint
import argparse

def parse_options():

    global parser
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=50)
    parser = argparse.ArgumentParser(description='Github Autopwn - Static Code Analysis Scraper', formatter_class=formatter)
    parser.add_argument("-q", "--query", type=str, help="Bad code to scrape for", required=False)
    parser.add_argument("-o", "--org", type=str, help="Organization/User to search bad code in e.g. Microsoft", required=True)
    parser.add_argument("-a", "--autopwn", help="Find all the bugs", action="store_true", required=False)
    parser.add_argument("-crl", "--check-rate-limit", dest="rate", help="Check current API request rate limit", action="store_true", required=False)
    args = parser.parse_args()
    return args

def check_rate_limit():

    this_req = requests.get("https://api.github.com/rate_limit", verify=True)
    json_data = json.loads(this_req.content)
    pprint(json_data["rate"])
    sys.exit()

def main(args):

    if args.rate:
        check_rate_limit()

    if args.query:

        print("[!] Searching for payload: %s" % args.query)

        try:

            github_api = ("https://api.github.com/search/code?q=user:{} {}").format(args.org, args.query)
            this_req = requests.get(github_api, verify=True)
            json_data = json.loads(this_req.content)
            if this_req.status_code == 200:
                print("[+] Found Potentially Vulnerable %s Code In The Following Files!" % args.query)
                for key in json_data["items"]:
                    try:
                        pprint(key["html_url"])

                    except KeyError:
                        print("[!] Didn't find anything. Moving on!")

        except Exception as e:
            print(repr(e))

    if args.autopwn:

        for payload in payloads:
            print("[!] Searching for payload: %s" % payload[0])

            try:

                github_api = ("https://api.github.com/search/code?q=user:{} {}").format(args.org, payload[0])
                this_req = requests.get(github_api, verify=True)
                json_data = json.loads(this_req.content)
                print("[!] Got status code: %d" % this_req.status_code)
                if this_req.status_code == 200:

                    print("[+] Found Potentially %s Vulnerable Code In The Following Files!" % payload[0])

                    for key in json_data["items"]:

                        try:

                            pprint(key["html_url"])
                            time.sleep(0.1)

                        except KeyError as e:
                            print("[!] Didn't find anything. Moving on!")

            except Exception as e:
                print(repr(e))

if __name__ in "__main__":

    args = parse_options()
    main(args)
