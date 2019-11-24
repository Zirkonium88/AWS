# Run with python CallIoTCore.py
# Go to AWS IoT Core

import json
import random  # To get random numbers
import time  # To create delay
from datetime import date, datetime  # To get date and time

from AWSIoTPythonSDK.MQTTLib import \
    AWSIoTMQTTClient  # Import from AWS-IoT Library

myMQTTClient = AWSIoTMQTTClient("new_Client")
myMQTTClient.configureEndpoint(
    "a3nrmm2z1crnbl-ats.iot.eu-central-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/Users/mwalkowiak/Desktop/Trainings/Demos/IoT/Backlog/root-ca-cert.pem",
                                  "/Users/mwalkowiak/Desktop/Trainings/Demos/IoT/Backlog/a62755dc63-private.pem.key", "/Users/mwalkowiak/Desktop/Trainings/Demos/IoT/Backlog/a62755dc63-certificate.pem.crt")

# Infinite offline Publish queueing
myMQTTClient.configureOfflinePublishQueueing(-1)
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
    myMQTTClient.publish("IoT_TOPIC/info", "connected", 0)
    print("MQTT Client connection success!")

else:
    print("Error: Check your AWS details in the program")


while True:  # Publish random numbvers between 15-30 as long as not interupted
    var1 = random.randint(15, 31)
    var2 = random.randint(50, 71)
    var3 = ""

    temp = {"var1": var1, "var2": var2}
    data_out = json.dumps(temp)
    print(data_out)  # print payload for reference
    myMQTTClient.publish("IoT_TOPIC/recieve", data_out,
                         0)  # publish the payload
    myMQTTClient.subscribe("IoT_TOPIC/send", 1, customCallback)
    time.sleep(1)

while not done:  # interupt with CTRl+X
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            done = True
