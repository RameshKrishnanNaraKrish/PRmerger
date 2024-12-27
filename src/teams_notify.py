
# -*- coding: utf-8 -*-

import json
import argparse
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", action="store", type=str, help="Build User")
    parser.add_argument("-m", "--message", action="store", type=str, help="Version Number")
    parser.add_argument("-s", "--status", action="store", type=str, help="SUCCESS or FAILURE")
    parser.add_argument("-b", "--build_url", action="store", help="Jenkins build URL")
    parser.add_argument("-w", "--webhook_url", action="store", help="Teams Webhook URL")
    args = parser.parse_args()
    
    status_color = "red"
    if args.status=="SUCCESS":
        status_color="green"
    text = "<b>Job:</b> {}<br>".format(args.message.replace("\n","<br>"))
    text += "<b>Status:</b> <font color=\"{}\"><b>{}</b></font><br><br>".format(status_color,args.status)
    text += "<b>Run by</b>: {}<br>".format(args.user)
    text += "<b>More info:</b> <a href='{}'>Jenkins pipeline</a>, <a href='{}console'>Console Logs</a><br>".format(args.build_url, args.build_url)
  #  text += "<ul><li><a href='{}console'>Console Logs</a></li></ul>".format(args.build_url)

    message = {"text": text}
    requests.post(args.webhook_url, json=message)

if __name__ == '__main__':
    main()
