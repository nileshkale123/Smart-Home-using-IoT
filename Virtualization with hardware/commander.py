# Import Module
from tkinter import *
'''
This file contains  code to  take input from user and it publish data on topic xyz and further controller consumed it and take necessary 
decisons to control appliances.
'''

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = XXXX
CLIENT_ID = "controller"
PATH_TO_CERTIFICATE = "Certificates/controller_device.crt"
PATH_TO_PRIVATE_KEY = "Certificates/controller_private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "Certificates/AmazonRootCA1.pem"

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
print("Controller Connected!")
            
# Create Object
root = Tk()

# Add Title
root.title('Smart Home Controller')

# Add Geometry
root.geometry("500x1000")

# Keep track of the button state on/off
#global is_on
is_on_fan= False
is_on_ac= False
is_on_bulb= False

# Define our switch function
def fan():
    global is_on_fan
	# Determine is on or off
    if is_on_fan:
        user_request = '{"status":"0"}'
        topic = "esp32/relay1"
        mqtt_connection.publish(topic=topic, payload=str(user_request), qos=mqtt.QoS.AT_LEAST_ONCE)
        on_button_fan.config(image = off)
        is_on_fan = False
    else:
        user_request = '{"status":"1"}'
        topic = "esp32/relay1"
        mqtt_connection.publish(topic=topic, payload=str(user_request), qos=mqtt.QoS.AT_LEAST_ONCE)
        on_button_fan.config(image = on)
        is_on_fan = True

def bulb():
    global is_on_bulb
	# Determine is on or off
    if is_on_bulb:
        user_request = '{"status":"0"}'
        topic = "esp32/relay2"
        mqtt_connection.publish(topic=topic, payload=str(user_request), qos=mqtt.QoS.AT_LEAST_ONCE)
        on_button_bulb.config(image = off)
        is_on_bulb = False
    else:
        user_request = '{"status":"1"}'
        topic = "esp32/relay2"
        mqtt_connection.publish(topic=topic, payload=str(user_request), qos=mqtt.QoS.AT_LEAST_ONCE)
        on_button_bulb.config(image = on)
        is_on_bulb = True

def ac():
    global is_on_ac
	# Determine is on or off
    if is_on_ac:
        user_request = '{"status":"0"}'
        topic = "esp32/relay3"
        mqtt_connection.publish(topic=topic, payload=str(user_request), qos=mqtt.QoS.AT_LEAST_ONCE)
        on_button_ac.config(image = off)
        is_on_ac = False
    else:
        user_request = '{"status":"1"}'
        topic = "esp32/relay3"
        mqtt_connection.publish(topic=topic, payload=str(user_request), qos=mqtt.QoS.AT_LEAST_ONCE)
        on_button_ac.config(image = on)
        is_on_ac = True

# Define Our Images
on = PhotoImage(file = "Images/on.png")
off = PhotoImage(file = "Images/off.png")
label = Label(text = "FAN",bg= "white",fg ="black",font =("Poppins bold", 22))
label.pack(pady = 20)
# Create A Button
on_button_fan = Button(root, image =off, bd = 0,
				command = fan)

on_button_fan.pack(pady = 50)
label = Label(text = "BULB",bg= "white",fg ="black",font =("Poppins bold", 22))
label.pack(pady = 20)
on_button_bulb = Button(root, image = off, bd = 0,
				command = bulb)

on_button_bulb.pack(pady = 50)
label = Label(text = "AC",bg= "white",fg ="black",font =("Poppins bold", 22))
label.pack(pady = 20)
on_button_ac = Button(root, image = off, bd = 0,
				command = ac)

on_button_ac.pack(pady = 50)
# Execute Tkinter
root.mainloop()
