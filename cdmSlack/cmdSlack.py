#!/usr/bin/env python3
import os
import sys
import requests
import json
import time

mess = ""


for x in sys.argv:
    if x != sys.argv[0] and x != sys.argv[1]:
        mess = f"{mess} {x}"
url = 'https://0f86c6e7.ngrok.io/api/messages'
payload = {"text" : mess ,"ch" : sys.argv[1]}
r = requests.post(url=url, data=payload)
print(r.text)

