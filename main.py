# print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
import sys

BROKER_ADDRESS = "thingsboard.cloud"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "PkSXWNyACzrxEtvM9Blv"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")
    temp_data = {'test': True}
    client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': "On"}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "Set sensor" and jsonobj['params'] == "On":
            temp_data['value'] = "On"
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
        elif jsonobj['method'] == "Set sensor" and jsonobj['params'] == "Off":
            temp_data['value'] = "Off"
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)

    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")

client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

f = open("./data/tram_1.txt", "r")
while f:
    data = f.readline().replace('\n', '')
    t = data.split(";")
    entry_dict = {
            "SEQ": "",
            "STT": "",
            "Hour": "",
            "Date": "",
            "pH": "",
            "Color": "",
            "Flow": "",
            "TSS": "",
            "temperature": "",
            "COD": "",
            "CLO": "",
            "SS": "",
            "TN": "",
            "NH4": "",
            "N-NH4": "",
            "N-NH4+": "",
            "MO": "",
            "VBAT": "",
            "VDDA": "",
            "INTEMP": "",
        }
    for x in range(len(t) - 1):
        t1 = t[x].split(',')
        if len(t1) > 1:
            if t1[0] == "COLOR":
                entry_dict["Color"] = t1[1]
            elif t1[0] == "PH":
                entry_dict["pH"] = t1[1]
            elif t1[0] == "FLOW":
                entry_dict["Flow"] = t1[1]
            elif t1[0] == "TEMP" or t1[0] == "Temp":
                entry_dict["temperature"] = t1[1]
            else:
                entry_dict[t1[0]] = t1[1]
        else:
            if t1[0].find(':') != -1:
                entry_dict["Hour"] = t1[0]
            else:
                entry_dict["Date"] = t1[0]

    print(json.dumps(entry_dict))
    client.publish('v1/devices/me/telemetry', json.dumps(entry_dict), 1)
    time.sleep(5)