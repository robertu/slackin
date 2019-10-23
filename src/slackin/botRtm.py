#!/usr/bin/env python3
from slack import WebClient, RTMClient
import json
from . import VERSION
from os import system, popen
import subprocess, time
import re
dm = {}

class Bot(object):
    rtmClient = None
    client = None
    def __init__(self, name=None, slack_token=None):
        assert name is not None, "Please give the bot a name"
        assert slack_token is not None, "Muszę mieć slack token secret by żyć"
        self.slack_token = slack_token
        self.name = name
        self.rtmClient = RTMClient(token=slack_token, connect_method='rtm.start')
        self.client = WebClient(token=slack_token)

        

        @RTMClient.run_on(event="message")
        def message(**payload):
            data = payload['data']
            try:
                args = re.split(r'\W+',data.get('text', []))
            except KeyError:
                return
            channel = data['channel']
            try:
                bot_name = args[0]
                command = args[1]
                try:
                    args = args[2:]
                except IndexError:
                    args = []
            except IndexError:
                return
            if not (bot_name in [self.name, 'all']):
                return
            try:
                cmd = getattr(self, f"cmd_{command}")
            except AttributeError:
                pass
            else:
                resp = cmd(data=data, args=args)
                if type(resp) == str and resp:
                    mess = self.client.chat_postMessage(
                        channel=data['channel'],
                        text=resp
                    )
                else:
                    mess = self.client.chat_postMessage(
                        channel=data['channel'],
                        text=f"Błędna odpowiedź z komendy {command}"
                    )
            return


    def run(self):
        self.rtmClient.start()

        


def main():
    import argparse, sys
    parser = argparse.ArgumentParser(prog='slackin', description='Slack integration bot')
    parser.add_argument('-n', '--name', type=str, help='Slack bot name. Default: "bot".', default='bot')
    parser.add_argument('-t', '--token', type=str, help='Slack token value', required=True)
    args = parser.parse_args()

    class MyBot(Bot):
        def cmd_hello(self, data=None, args=[]):
            return "Hello dude!"
        def cmd_xd(self, data=None, args=[]):
            return "Hello xd!"
        def cmd_pat(self, data=None, args=[]):
            return "Nie pij tyle!"
        def cmd_update(self, data=None, args=[]):
            print('ls ' + ' '.join(args))
            odp = None
            myShellCmd = subprocess.run(['ls ', ' '.join(args)], shell=True, stdout=subprocess.PIPE , stderr=subprocess.STDOUT)
            if myShellCmd.returncode == 0:
                opd = myShellCmd.stdout
            elif myShellCmd.returncode != 1:
                opd = f'Błąd: {myShellCmd.stdout}'
            else:
                opd = "Nieznany błąd komendy"
            return str(opd)

    bot = MyBot(name=args.name, slack_token=args.token)
    bot.run()