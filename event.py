#!/usr/bin/env python3
import os
import slack
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from flask import Flask, request, make_response, Response
import json, re
import pprint

pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)

slack_event_listen = SlackEventAdapter(signing_secret='03daaddc7a79ed4326ddfec570d29bf8', endpoint="/slack/events", server=app)
token = 'xoxb-779874283382-779940814246-yydZ80ZBMny8reRy1Un2V7WX'
client = WebClient(token=token)

ch = ["DNXTNQ23Y","CNP70R1SM"]

#Nsłuchuje na kanale bota wiadomości
@slack_event_listen.on("message")
def message(event_data):
    print(event_data)
    # try:
    #     username = event_data["event"]['username']
    #     if username == 'TestBot':
    #         return make_response("", 200)
    # except KeyError:
    #     pass
    cmd = re.split(r'\W+',event_data["event"]["text"])
    print(cmd)

    if event_data["event"]["channel"] in ch and cmd[0] == "form":
        mess = client.chat_postMessage(
            channel= event_data["event"]["channel"],
            text="witaj",
            attachments=[
                {   
                    "text": "Twój wygenerowany formularz",
                    "fallback": "Nie możesz wybrać formularza",
                    "callback_id": f"fromSelect:{cmd}",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "cmd",
                            "text": "cmd",
                            "type": "hidden",
                            "value": str(cmd)
                        },
                        {
                            "name": "bt1",
                            "text": f"Otwórz formularz {cmd[1:]}",
                            "type": "button",
                            "value": "form1-button"
                        }
                    ],
                }
            ]
        )
    return make_response("", 200)

my_channel = 'CNXL9RRCP'

#Nałuchiwanie na odpowiedz z wiadomości z przyciskiem
@app.route("/slack/wiki", methods=["GET"])
def slack_wiki():
    mess = client.chat_postMessage(
        channel = my_channel,
        text="witaj z wiki",
        attachments=[]
    )
    return make_response("ok", 200)

#Nałuchiwanie na odpowiedz z wiadomości z przyciskiem
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    data = json.loads(request.form["payload"])
    pp.pprint(vars(request))
    rt = data['type']
    if rt == "dialog_submission":
        print(data['submission'])

    elif rt == "interactive_message":
        om = data['original_message']
        at = om['attachments']
        ci = at[0]['callback_id']
        cmd = []
        if ci.startswith("fromSelect:"):
            cmd = ci.replace("fromSelect:",'')
            cmd = eval(cmd)
        print(at)
        n = 1
        elements = []
        for e in cmd:
            if e == 'form':
                pass
            elif e == 'chbox':
                 elements.append(
                    {
                        "label": "Prawda/Fałsz",
                        "name": f"el_{e}_{n}",
                        "type": "select",
                        "value": "1",
                        "placeholder": "",
                        "options": [
                            {
                                "label": "Prawda",
                                "value": "1"
                            },
                            {
                                "label": "Fałsz",
                                "value": "2"
                            }

                        ]
                    }
                )
            elif e == 'dd':
                elements.append(
                    {
                        "label": "Imię zwierzątka",
                        "name": f"el_{e}_{n}",
                        "type": "select",
                        "value": "2",
                        "placeholder": "Wybierz imię",
                        "options": [
                            {
                                "label": "Ala",
                                "value": "1"
                            },
                            {
                                "label": "Ola",
                                "value": "2"
                            }

                        ]
                    }
                )

            elif e == 'text':
                elements.append(
                    {
                    "label": "Input text",
                    "name": f"el_{e}_{n}",
                    "type": "text",
                    "placeholder": "Wpisz cokolwiek"
                    }
                )
            elif e == 'area':
                elements.append(
                    {
                    "label": "Input textarea",
                    "name": f"el_{e}_{n}",
                    "type": "textarea",
                    "placeholder": "Wpisz cokolwiek"
                    }
                )
            else:
                elements.append(
                    {
                    "label": "Input text",
                    "name": f"el_{e}_{n}",
                    "type": "text",
                    "placeholder": "Wpisz cokolwiek"
                    }
                )
            n += 1

        dialog = {
                "title": "Formularz",
                "submit_label": "Wyślij",
                "callback_id": "formCallback",
                "elements": elements
        }
        pp.pprint(dialog)
        form1 = client.dialog_open(
            trigger_id = data["trigger_id"],
            dialog = dialog
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