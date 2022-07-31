'''
This file contains  code to  take input from user and it publish data on topic xyz and further controller consumed it and take necessary 
decisons to control appliances.
'''

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = XXXX
CLIENT_ID = "user"
PATH_TO_CERTIFICATE = "Certificates/user_device.crt"
PATH_TO_PRIVATE_KEY = "Certificates/user_private.key"
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
print("Connected!")
            

print("Request with syntax DEVICE-ACTION formalt only")
while True:
    
    user_request = input("Request : ")
    mqtt_connection.publish(topic="smart_home/room/Device-Actions", payload=str(user_request), qos=mqtt.QoS.AT_LEAST_ONCE)
