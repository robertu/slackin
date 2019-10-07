#!/usr/bin/env python3
import os
import slack
import cairo
from io import BytesIO
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from flask import Flask, request, make_response, Response
import json, re
import pprint
from PIL import Image, ImageDraw, ImageFont
import random, wget

pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)

slack_event_listen = SlackEventAdapter(signing_secret='512dccab767437d52268bef8f4c4160e', endpoint="/slack/events", server=app)
token = 'xoxb-779874283382-781917834228-yOwDUWiwPuVU7lTt4cvCeRzn'
client = WebClient(token=token)

ch = ["DP2HBSGDU","CNP70R1SM"]
dm = {}

#Nsłuchuje na kanale bota wiadomości
@slack_event_listen.on("message")
def message(event_data):
    print(event_data)
    if event_data["event"]["text"] == 'obrazek':
        wget.download('https://0f86c6e7.ngrok.io/obrazek.png')
        mess = client.chat_postMessage(
            channel = event_data["event"]["channel"],
            text = 'Work',
            attachments=[
                {
                "title": "Wykres",
                "image_url": "https://0f86c6e7.ngrok.io/brazek.png"
                }
            ]
            
        )
        return

    # try:
    #     username = event_data["event"]['username']
    #     if username == 'TestBot':
    #         return make_response("", 200)
    # except KeyError:
    #     pass
    try:
        cmd = re.split(r'\W+',event_data["event"]["text"])
    except KeyError:
        return
    channel = event_data["event"]["channel"]
    print("Channel:", channel)
    print(cmd)

    if cmd[0] == "start":
        #dm[cmd[1]] = event_data["event"]["channel"]
        mess = client.chat_postMessage(
            channel=event_data["event"]["channel"],
            text='',
            attachments=[
                {
                    'text': 'Zezwól na komunikację z botem',
                    "fallback": "",
                    "callback_id": "start",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {   
                        "name": "start",
                        "text": "Zacznij",
                        "type": "button",
                        "value": "ready"
                        },
                    ]                

                }

            ]

        )

        
        

    if cmd[0] == "form":
        mess = client.chat_postMessage(
            channel = channel,
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


@app.route("/api/messages", methods=['GET','POST'])
def cmd_slack():        
    if request.method == 'POST':
        message_text = request.form["text"]
        channel = request.form["ch"]
        print(channel)
        print (dm)

        try:
            channel_id = dm[channel]
            print("work")
            mess_pv = client.chat_postMessage(
                channel=channel_id,
                text = message_text
            )
        except KeyError:
            mess = client.chat_postMessage(
                channel=channel,
                text=message_text,
            )
        except IndexError:
            return make_response(f"Nie znam tego: {channel}", 400)

    return make_response(f"{message_text}", 200)

#Nałuchiwanie na odpowiedz z wiadomości z przyciskiem
@app.route("/slack/wiki", methods=["GET"])
def slack_wiki():
    mess = client.chat_postMessage(
        channel = my_channel,
        text="witaj z wiki",
        attachments=[]
    )
    return make_response("ok", 200)



def losuj_imie():
    imiona = [
        'Jan',
        'Anita',
        'Marek',
        'Ola',
        "Andrzej"

    ]
    return imiona[random.randint(0,len(imiona)-1)]

def losuj_nazwisko():
    nazwiska =[
        'Kowalski',
        'Skrzyniarski',
        "Adwokat",
        "Kowalczyk",
        'Literacki'
    ]
    return nazwiska[random.randint(0,len(nazwiska)-1)]

maxzad = 30
user_count = 0
def get_users():
    import random
    users = []
    for u in range(random.randint(5,10)):
        users.append(
            {
                'imie': losuj_imie(),
                'nazwisko': losuj_nazwisko(),
                'zadania': random.randint(1,maxzad)
            }
        )
        user_count=+1
    print("wyg tyle:", len(users))
    return users

size = 0
wys = 30
odstep = 10
margines=25
def drawSomethingCool(ctx, users):
    y = margines
    x = 300
    rect = (600 - x - margines)/maxzad
    max = 0
    for u in users:
        n = f"{u['imie']} {u['nazwisko']}"
        if max < len(n):
            max = len(n)
    x = max * wys*0.3 + margines * 2
    for u in users:
        print(x,y,u)
        zad = u['zadania']
        ctx.rectangle(x, y, zad*rect, wys)

        if zad > maxzad/2:
            ctx.set_source_rgb(1, 0, 0)
        else:
            ctx.set_source_rgb(0, 0.3, 0)
        ctx.set_font_size(wys*0.5)
        ctx.move_to(margines, y+wys*0.75)
        ctx.show_text(f"{u['imie']} {u['nazwisko']}")
        ctx.fill()
        #x =+ 100
        y += odstep+wys
        
    


#Nałuchiwanie na odpowiedz z wiadomości z przyciskiem
@app.route("/obrazek.png", methods=["GET"])
def obrazek_png():
    users = get_users()
    srf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, len(users)*wys+(len(users)-1)*odstep+2*margines)
    ctx = cairo.Context(srf)
    drawSomethingCool(ctx, users)
    flo = BytesIO()
    srf.write_to_png(flo)
    resp = make_response(flo.getvalue())
    resp.content_type = "image/png"
    return resp

def obrazek():
    png = Image.new('RGBA', (512,512), (255,255,255,0))
    d = ImageDraw.Draw(png)
    d.text((10,10), "Hello",fill=(255,255,255,128))
    png.save('zdj.png')
    # mess = client.files_upload(
    #     channel= 'CNP70R1SM',
    #     content="zdj.png",
    #     filetype='png'
    # )
    return make_response("",  200)


#Nałuchiwanie na odpowiedz z wiadomości z przyciskiem
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    
    data = json.loads(request.form["payload"])
    pp.pprint(vars(request))
    rt = data['type']
    if rt == "dialog_submission":
        print(data['submission'])
        mess = client.chat_postMessage(
            channel=data["channel"]["id"],
            text=f"Dziękujemy za formularz: {data['submission']}"
        )
    elif rt == "interactive_message" and data['callback_id'] == "start":
        dm[data['user']['name']] = data["channel"]["id"]
        print("Work")

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
# @app.route('/form1', methods=['POST'])
# def formularz1():
#     payload = request.form["trigger_id"]
#     fromularzCall = client.dialog_open(
#         trigger_id= payload ,
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
#     return make_response("", 200)

    
# @app.route('/form2', methods=['POST'])
# def formularz2():
#     payload = request.form["trigger_id"]
#     fromularzCall = client.dialog_open(
#         trigger_id= payload ,
#         dialog= {
#             "title": "Formularz 2",
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
#     return make_response("", 200)



if __name__ == '__main__':
    app.run(port=4000, debug=True)