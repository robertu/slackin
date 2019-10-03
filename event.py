#!/usr/bin/env python3
import os
import slack
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from flask import Flask, request, make_response, Response
import json

app = Flask(__name__)

event_listen = SlackEventAdapter(signing_secret='03daaddc7a79ed4326ddfec570d29bf8', endpoint="/slack/events", server=app)
token = 'xoxb-779874283382-779940814246-yydZ80ZBMny8reRy1Un2V7WX'
client = WebClient(token=token)

ch = "DNXTNQ23Y"

#Nsłuchuje na kanale bota wiadomości
@event_listen.on("message")
def message(event_data):
    try:
        username = event_data["event"]['username']
        if username == 'TestBot':
            return make_response("", 200)
    except KeyError:
        pass
    print(event_data)

    if ch in event_data["event"]["channel"] and "witaj" in event_data["event"]["text"]:
        mess = client.chat_postMessage(
            channel= event_data["event"]["channel"],
            text="witaj",
            attachments=[
            {
                "text": "Formularze",
                "fallback": "Nie możesz wybrać formularza",
                "callback_id": "fromSelect",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "Formularz 1",
                        "text": "Formularz 1",
                        "type": "button",
                        "value": "form1"
                    }
                ],
            }
        ]
    )
    # event_listen.remove_all_listeners()
    return make_response("", 200)

#Nałuchiwanie na odpowiedz z wiadomości z przyciskiem
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    data = json.loads(request.form["payload"])
    rt = data['type']
    if rt == "dialog_submission":
        print(data['submission'])
    elif rt == "interactive_message":
        form1 = client.dialog_open(
            trigger_id= data["trigger_id"],
            dialog= {
                "title": "Formularz 1",
                "submit_label": "Wyślij",
                "callback_id": "formCallback",
                "elements": [
                    {
                    "label": "Input text",
                    "name": "text",
                    "type": "text",
                    "placeholder": "Wpisz cokolwiek"
                    }
                ]
            }
        )
    else:
        print(f"nieznany typ messaga {rt}")
    # trigger_id= data["trigger_id"]
    # except KeyError:
    # try:
    #     form1 = client.dialog_open(
    #         trigger_id= data["trigger_id"] ,
    #         dialog= {
    #             "title": "Formularz 1",
    #             "submit_label": "Wyślij",
    #             "callback_id": "formCallback",
    #             "elements": [
    #                 {
    #                 "label": "Input text",
    #                 "name": "text",
    #                 "type": "text",
    #                 "placeholder": "Wpisz cokolwiek"
    #                 }
    #             ]
    #         }
    #     )
    # except KeyError:
    #     print("*" * 100)
    #     print(data)
    #     print("*" * 100)

    return make_response("", 200)




#Komendy
@app.route('/form1', methods=['POST'])
def formularz1():
    payload = request.form["trigger_id"]
    fromularzCall = client.dialog_open(
        trigger_id= payload ,
        dialog= {
            "title": "Formularz 1",
            "submit_label": "Wyślij",
            "callback_id": "formCallback",
            "elements": [
                {
                "label": "Input text",
                "name": "text",
                "type": "text",
                "placeholder": "Wpisz cokolwiek"
                }
            ]
        }
    )
    return make_response("", 200)

    
@app.route('/form2', methods=['POST'])
def formularz2():
    payload = request.form["trigger_id"]
    fromularzCall = client.dialog_open(
        trigger_id= payload ,
        dialog= {
            "title": "Formularz 2",
            "submit_label": "Wyślij",
            "callback_id": "formCallback",
            "elements": [
                {
                "label": "Input text",
                "name": "text",
                "type": "text",
                "placeholder": "Wpisz cokolwiek"
                }
            ]
        }
    )
    return make_response("", 200)



if __name__ == '__main__':
    app.run(port=4000, debug=True)