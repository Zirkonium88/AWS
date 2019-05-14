# Simple publish and suscbribe example for AWS IoT

This example show how to use Python to communicate with AWS Iot Core. The script connects via certificates and [MQTT](http://mqtt.org) with an endpoint and publishes two random numbers. In doing so, the usage of [micro controllers, e.g. ESP8266](https://github.com/debsahu/ESP-MQTT-AWS-IoT-Core) is possible.

It be can be extended to recieve messages as well. A complete walkthrough can be find [here](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html).

## Presequities

* Install the [AWS IoT Pythin SDK].(https://docs.aws.amazon.com/de_de/iot/latest/developerguide/iot-sdks.html)
* [Onboard your IoT device].(https://docs.aws.amazon.com/iot/latest/developerguide/iot-provision.html)
* Figure out what your endpoint URI looks like. You can find the URI under Settings / Custom Endpoint withhin the WS Iot Core service.
* Copy all files accordingly to your (virtual) device.

## Usage

* Use `python CallIoTCore.py`to start the script
* Interupt the script with `CTRl+X`

````python

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient # Import from AWS-IoT Library
import time # To create delay
from datetime import date, datetime # To get date and time
import random # To get random numbers
import json

YOUR_IOT_ENDPOINT = "XXX-ats.iot.eu-central-1.amazonaws.com"
ROOT_CA_CERT = "path/to/root-ca-cert.pem"
PRIVATE_PEM_KEY = "path/to/xxx-private.pem.key"
CERTIFICATE_PEM_CRT = "path/to/xxx-certificate.pem.crt"
IOT_TOPIC_CHECK = "IoT_TOPIC/info"
IOT_TOPIC_SEND = "IoT_TOPIC/send"
IOT_TOPIC_RECIEVE = "IoT_TOPIC/recieve"
CLIENT = "new_Client"

myMQTTClient = AWSIoTMQTTClient(CLIENT)
myMQTTClient.configureEndpoint(YOUR_IOT_ENDPOINT, 8883)
myMQTTClient.configureCredentials(ROOT_CA_CERT, ROOT_PEM_KEY, CERTIFICATE_PEM_CRT)

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Custom MQTT message callback: Reacting on MQTT messages pblished on iot_test/send
def customCallback(client, userdata, message):
    print("Advertising: Your Company!")
    # sense.show_message("S-PG!", text_colour=white, back_colour=green)
    # sense.clear()

connecting_time = time.time() + 10
if time.time() < connecting_time:  # try connecting to AWS for 10 seconds
    myMQTTClient.connect()
    myMQTTClient.publish(IOT_TOPIC_CHECK, "connected", 0)
    print("MQTT Client connection success!")

else:
    print("Error: Check your AWS details in the program")

while True: # Publish random numbvers between 15-30 as long as not interupted
    var1 = random.randint(15,31)
    var2 = random.randint(50,71)

    payload = {"var1":var1,"var2":var2}
    publishPayload = json.dumps(payloaud)
    print(publishPayload) # print payload for reference
    myMQTTClient.publish(IOT_TOPIC_RECIEVE, publishPayload, 0) #publish the payload
    myMQTTClient.subscribe(IOT_TOPIC_SEND, 1, customCallback)
    time.sleep(1)

while not done: # interupt with CTRl+X
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            done = True
´´´´