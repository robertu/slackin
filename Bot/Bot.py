#!/usr/bin/env python3
from flask import Flask, request, make_response, Response
from slackeventsapi import SlackEventAdapter
from slack import WebClient

class Bot(object):

    def __init__(self, slack_token=None, ss=None, host=None, port=None, app=None, client=None, eventLister=None):
        assert ss is not None, "Muszę mieć signing secret by żyć"
        assert slack_token is not None, "Muszę mieć slack token secret by żyć"
        self.slack_token = slack_token
        self.ss = ss
        self.host = host
        self.port = port
        self.app = Flask("slack-integra")
        self.client = WebClient(token=slack_token)
        self.eventLister = SlackEventAdapter(signing_secret=ss, endpoint="/slack/events", server=app)


    
    def run(self):
        self.app.run(host=self.host, port=self.port, debug=False)

