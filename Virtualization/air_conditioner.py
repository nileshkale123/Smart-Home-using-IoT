'''
This file emulate AC appliance
'''
import time
import threading

from tkinter import *
from paho.mqtt import client
from PIL import Image, ImageTk

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = XXXX
CLIENT_ID = "ac"
PATH_TO_CERTIFICATE = "Certificates/ac_device.crt"
PATH_TO_PRIVATE_KEY = "Certificates/ac_private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "Certificates/AmazonRootCA1.pem"

def on_message_received(topic, payload, **kwargs):

    data = payload.decode('utf-8')
    ListTemp  = data.split('-')
    Device = str(ListTemp[0])
    Action = str(ListTemp[1])
    if(str(Device).upper() == "AC"):

        status['text'] = "Current Status :" + str(Action)

        if(str(Action).upper() == "ON"):
            status['fg'] = 'green'
        else:
            status['fg'] = 'red'


# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )

print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("AC Connected!")


def mqttProcess():
    
    subscribe_future, packet_id = mqtt_connection.subscribe(
    topic="smart_home/room/Device-Actions",
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
    )
    subscribe_result = subscribe_future.result()


tk = Tk()   #Creating Tkinter Object

tk.geometry("600x300")
tk.configure(bg='black')
title = Label(tk,text = "AC Appliance",pady = 5,bg='black',fg='white')
title.pack()
ac_image = ImageTk.PhotoImage(Image.open("Images/ac.png").resize((500,200)))

bg = Label(tk,image = ac_image,bd=0)
bg.pack()

display_pane = Frame(tk,bd=1,bg='white',relief = "raised")
display_pane.pack()

status = Label(display_pane,text ="Status : OFF",fg="red",bg="white",padx=5,pady=5)
status.pack()

threading.Thread(target=mqttProcess).start()

tk.mainloop()

while True:
    time.sleep(0.0001)
