#!/usr/bin/env python3
import os, json
import slack, sys
from slack import RTMClient, WebClient
from flask import Flask, request, make_response, Response

token = 'xoxb-779874283382-779940814246-yydZ80ZBMny8reRy1Un2V7WX'
client = WebClient(token=token)
channel_ids = ['CNXL9RRCP']

app = Flask(__name__)

@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    menu_options = {
        "options": [
            {
                "text": "Chess",
                "value": "chess"
            },
            {
                "text": "Global Thermonuclear War",
                "value": "war"
            }
        ]
    }

    return Response(json.dumps(menu_options), mimetype='application/json')

@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Check to see what the user's selection was and update the message
    selection = form_json["trigger_id"]


    from_ = client.dialog_open(
        trigger_id=selection ,
        dialog=[
            {
            "label": "Additional information",
            "name": "comment",
            "type": "textarea",
            "hint": "Provide additional information if needed."
        }
        ]
    )

    return make_response("", 200)

message_attachments = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "games_list",
                "text": "Forzmularz",
                "type": "button",
            }
        ],
        "trigger_id": "2"
    }
]


@RTMClient.run_on(event='message') 
def say_hello(**payload):
    data = payload['data']
    ch = data['channel']
    text = data.get('text', [])
    
    if ch in channel_ids and 'Formularz' in text:

        # thread_ts = data['ts']
        user = data.get('user', None)
        if not user:
            print(data)
        if user:
            
            res = client.chat_postMessage(
                channel=ch ,
                text = "Formularz",
                attachments=message_attachments
            )

rtmc = RTMClient(token=token)
rtmc.start()
if __name__ == "__main__":
    app.run()