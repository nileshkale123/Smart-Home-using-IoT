'''
this file consumes request done from user and take action accordingly. Controller subscibed to "smart_home/room/user" to consume request from user
and further publish message accordingly to  corresponding appliance. 
'''

import time
import datetime
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = XXXX
CLIENT_ID = "controller"
PATH_TO_CERTIFICATE = "Certificates/controller_device.crt"
PATH_TO_PRIVATE_KEY = "Certificates/controller_private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "Certificates/AmazonRootCA1.pem"

def on_message_received(topic, payload, **kwargs):
    log_file = open("logs.txt", "a")
    #data = format(payload)
    data = payload.decode('utf-8')
   
    ListTemp  = data.split('-')
    Device = str(ListTemp[0])
    Action = str(ListTemp[1])

    log_file.write("["+str(datetime.datetime.now())+"]"+" Device :"+str(Device)+", Action :"+ str(Action) + "\n")
    log_file.close()
   

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


subscribe_future, packet_id = mqtt_connection.subscribe(
    topic="smart_home/room/Device-Actions",
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received
)
subscribe_result = subscribe_future.result()


while True:
    time.sleep(0.0001)
