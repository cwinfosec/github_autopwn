#!/usr/bin/env python3
"""
Description: Github Autopwn - Github Scraper For Static Code Analysis
Author: Cody Winkler (twitter: c2thewinkler | github: m0rph-1)
Date: 2/5/2020
"""

import requests
import json
from indicators import *
from pprint import pprint
import argparse

def parse_options():

    global parser
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=50)
    parser = argparse.ArgumentParser(description='Use -sp to bypass SNMP ACL\'s that don\'t specify deny ip any any', formatter_class=formatter)
    parser.add_argument("-q", "--query", type=str, help="Bad code to scrape for", required=False)
    parser.add_argument("-o", "--org", type=str, help="Organization to search bad code in e.g. Microsoft", required=True)
    parser.add_argument("-a", "--autopwn", help="Find all the bugs", action="store_true", required=False)
    args = parser.parse_args()
    return args

def main(args):

    if args.query:
        print("[!] Searching for payload: %s" % args.query)
        try:

            github_api = ("https://api.github.com/search/code?q=user:{} {}").format(args.org, args.query)
            this_req = requests.get(github_api, verify=True)
            json_data = json.loads(this_req.content)
            print("[!] Got status code: %d" % this_req.status_code)
            print("[+] Found Potentially Vulnerable Code In The Following Files!")
            for key in json_data["items"]:
                pprint(key["html_url"])

        except Exception as e:
            print(repr(e))

        except KeyError:
            print("[!] Didn't find anything. Moving on!")

    if args.autopwn:

        for payload in payloads:
            print("[!] Searching for payload: %s" % payload[0])

            try:

                github_api = ("https://api.github.com/search/code?q=user:{} {}").format(args.org, payload[0])
                this_req = requests.get(github_api, verify=True)
                json_data = json.loads(this_req.content)
                print("[!] Got status code: %d" % this_req.status_code)
                print("[+] Found Potentially Vulnerable %s Code In The Following Files!" % payload[0])

                for key in json_data["items"]:
                    pprint(key["html_url"])

            except Exception as e:
                print(repr(e))


if __name__ in "__main__":

    args = parse_options()
    main(args)
