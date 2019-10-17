#!/usr/bin/env python3
from flask import Flask, request, make_response, Response
from slackeventsapi import SlackEventAdapter
from slack import WebClient
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

