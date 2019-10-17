#!/usr/bin/env python3
from flask import Flask, request, make_response, Response
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from . import VERSION

import re

class Bot(object):
    app = None
    client = None
    def __init__(self, name=None, slack_token=None, signing_secret=None, host='127.0.0.1', port=8000):
        assert name is not None, "Please give the bot a name"
        assert signing_secret is not None, "Muszę mieć signing secret by żyć"
        assert slack_token is not None, "Muszę mieć slack token secret by żyć"
        self.slack_token = slack_token
        self.host = host
        self.port = port
        self.name = name
        self.app = Flask(name)
        self.client = WebClient(token=slack_token)
        self.eventListener = SlackEventAdapter(signing_secret=signing_secret, endpoint="/events", server=self.app)

        @self.eventListener.on("message")
        def message(event_data):
            try:
                cmd = re.split(r'\W+',event_data["event"]["text"])
            except KeyError:
                return
            channel = event_data["event"]["channel"]
            try:
                nazwa = cmd[0]
                komenda = cmd[1]
                try:
                    args = cmd[2:]
                except IndexError:
                    args = []
            except IndexError:
                return make_response("", 200)
            if not (nazwa in [self.name, 'all']):
                return make_response("", 200)
            if komenda == 'hello':
                mess = self.client.chat_postMessage(
                    channel=event_data["event"]["channel"],
                    text='Welcome!'
                )
            return make_response("", 200)

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=False)



def main():
    import argparse, sys
    parser = argparse.ArgumentParser(prog='slackin', description='Slack integration bot')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument('-i', '--ip', type=str, help='Hostname or ip for bot app to listen on. Default: 127.0.0.1', default='127.0.0.1')
    parser.add_argument('-n', '--name', type=str, help='Slack bot name. Default: "bot".', default='bot')
    parser.add_argument('-p', '--port', type=int, help='Port number for bot app to listen on. Default: 8000.', default=8000)
    parser.add_argument('-s', '--secret', type=str, help='Slack signing_secret value', required=True)
    parser.add_argument('-t', '--token', type=str, help='Slack token value', required=True)
    args = parser.parse_args()


    bot = Bot(name="bot", port=args.port, host=args.ip, slack_token=args.token, signing_secret=args.secret)
    bot.run()