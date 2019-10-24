#!/usr/bin/env python3
from slack import WebClient, RTMClient
import json
from . import VERSION
from os import system, popen
import subprocess, time
from subprocess import Popen, PIPE

import re
dm = {}

class Bot(object):
    rtm = None
    client = None
    def __init__(self, name=None, slack_token=None):
        assert slack_token is not None, "Muszę mieć slack token secret by żyć"
        self.slack_token = slack_token
        self.name = name
        self.rtm = RTMClient(token=self.slack_token)
        self.client = WebClient(token=slack_token)


        @RTMClient.run_on(event="message")
        def message(**payload):
            data = payload['data']
            try:
                args = re.split(r'\W+',data["text"])
            except KeyError:
                return
            channel = data["channel"]
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
                mess = self.client.chat_postMessage(
                        channel=data["channel"],
                        text=f"Nie znam takiej komendy \n wpisz ```{self.name} help``` aby uzyskać pomoc"
                    )
            else:
                resp = cmd(data=data, args=args)
                if type(resp) == str and resp:
                    mess = self.client.chat_postMessage(
                        channel=data["channel"],
                        text=resp
                    )
                else:
                    mess = self.client.chat_postMessage(
                        channel=data["channel"],
                        text=f"Błędna odpowiedź z komendy {command}"
                    )
            return


    def run(self):
        try:
            self.rtm.start()
        except TypeError as e:
            print("Muszisz poczekać chwile, i potem odpalic bota \n Bota mozna odpalac raz na minute!" + e)

        


def main():
    import argparse, sys
    parser = argparse.ArgumentParser(prog='slackin', description='Slack integration bot')
    parser.add_argument('-n', '--name', type=str, help='Slack bot name. Default: "bot".', default='bot')
    parser.add_argument('-t', '--token', type=str, help='Slack token value', required=True)
    args = parser.parse_args()

    class MyBot(Bot):
        def cmd_hello(self, data=None, args=[]):
            return "Hello dude!"
        def cmd_update(self, data=None, args=[]):
            myShellCmd = subprocess.Popen(['ls', ' '.join(args)],shell=True , stdout=PIPE, stderr=PIPE)
            out, err = myShellCmd.communicate()
            if myShellCmd.returncode == 0:
                return out.decode("utf-8")
            else:
                odp = err.decode("utf-8")
                return f'Bledna komenda: \n ```{odp}```:no_entry_sign:'
        def cmd_help(self, data=None, args=[]):
            odp = f'```{self.name} hello - Bot sie z toba przywita ```\n ```{self.name} update - Wykonuje komnde```'
            return odp

    bot = MyBot(name=args.name,slack_token=args.token)
    bot.run()