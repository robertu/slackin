#!/usr/bin/env python3
import os
import slack, sys
from slack import RTMClient, WebClient

token = 'xoxb-779874283382-779940814246-Sd7ljdUos2qo0pFTM8e1tH1w'
client = WebClient(token=token)
channel_ids = ['CNXL9RRCP']

@RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    ch = data['channel']
    text = data.get('text', [])
    
    if ch in channel_ids and 'Hello' in text:

        # thread_ts = data['ts']
        user = data.get('user', None)
        if not user:
            print(data)
        if user:
            response = client.chat_postMessage(
                channel=ch,
                text=f"Hi <@{user}>! {text}"
            )
    
rtmc = RTMClient(token=token)
rtmc.start()

