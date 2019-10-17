#!/usr/bin/env python3
from flask import Flask, request, make_response, Response
from slackeventsapi import SlackEventAdapter
from slack import WebClient

class Bot(object):

    def __init__(self, slack_token=None, ss=None, host=None, port=None, nazwa_bota=None, app=None, client=None, eventLister=None):
        assert ss is not None, "Muszę mieć signing secret by żyć"
        assert slack_token is not None, "Muszę mieć slack token secret by żyć"
        self.slack_token = slack_token
        self.ss = ss
        self.host = host
        self.port = port
        self.nazwa_bota = nazwa_bota
        self.app = Flask("slack-integra")
        self.client = WebClient(token=slack_token)
        self.eventLister = SlackEventAdapter(signing_secret=ss, endpoint="/slack/events", server=app)
        
    def listern(self):
        @self.eventLister.on("message")
        def message(self,event_data):  
            print ("work") 
            try:
                cmd = re.split(r'\W+',event_data["event"]["text"])
            except KeyError:
                return
            channel = event_data["event"]["channel"]
            print("Channel:", channel)
            print(cmd)
            try:
                nazwa = cmd[0]
                komenda = cmd[1]
                try:
                    args = cmd[2:]
                except IndexError:
                    args = []
            except IndexError:
                return make_response("", 200)
            if not (nazwa in [self.nazwa_bota, 'all']):
                return make_response("", 200)
            if komenda == 'witaj':
                mess = self.client.chat_postMessage(
                channel=event_data["event"]["channel"],
                text='Witaj'
                )

    
    def run(self):
        self.app.run(host=self.host, port=self.port, debug=False)

