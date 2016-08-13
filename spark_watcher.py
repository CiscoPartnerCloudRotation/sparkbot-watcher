# -*- coding: utf-8 -*-

import requests
import json
import ast
import time
import os
import random

# This will hold a list of all messages that contain a keyword, that we've already seen
# so that we don't parse the same message twice
parsed_kw_messages = []
keywords = ["lunch", "food"]

AUTH_KEY = os.environ['AUTH_KEY']
ROOM_ID = os.environ['ROOM_ID']
sparkbot_gmaps_svc_endpoint = os.environ['HOST_SPARKBOT_GOOGLE'] + "/getnearby"

# Get the messages from the room
def get_room_messages():
    sparkroom_endpoint = "https://api.ciscospark.com/v1/messages"
    header = {
        'Content-type' : 'application/json; charset=utf-8',
        'Authorization': AUTH_KEY
    }
    param = {
        'roomId': ROOM_ID,
        'max' : 1
    }
    r = requests.get(url=sparkroom_endpoint, headers=header, params=param)
    return json.loads(r.text)

def parse_room_messages(messages):
    # NESTED LOOPS - Bad!
    for message in messages["items"]:
        msg = json.dumps(message)
        msg_dict = ast.literal_eval(msg)
        if (msg_dict['text'].lower() in keywords) & (msg_dict['id'] not in parsed_kw_messages):
            print "Keyword '" +  msg_dict['text'] + "' found in message " + msg_dict['id']
            parsed_kw_messages.append(msg_dict['id'])
            r = requests.get(sparkbot_gmaps_svc_endpoint)
            
if __name__ == "__main__":
    while (True):
        messages = get_room_messages()
        parse_room_messages(messages)
        time.sleep(2)
