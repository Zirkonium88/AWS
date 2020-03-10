
import I2C_LCD_driver
lcd = I2C_LCD_driver.lcd()

import json
import random  # To get random numbers
import time  # To create delay
from datetime import date, datetime  # To get date and time

import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import \
    AWSIoTMQTTClient  # Import from AWS-IoT Library

# Global vars
ENDPOINT="awvkkbwtsweza-ats.iot.eu-central-1.amazonaws.com"
PATH_ROOT_CA="/home/pi/Desktop/IotDemo/certs/root-ca-cert.pem"
PRIVATE_PEM="/home/pi/Desktop/IotDemo/certs/demo.private.key"
CERTIFICATE="/home/pi/Desktop/IotDemo/certs/demo.cert.pem"
FAN_ID="ABC123456"
TACHO_PIN = 8 # White wire
# Initial time point
t0=time.time()
rpm=0.0
freq=0.0


def connect_iotcore():
    '''Setting the mQTT connection to AWS'''
    # Set MQTT Client
    myMQTTClient = AWSIoTMQTTClient("new_Client")
    myMQTTClient.configureEndpoint(
        ENDPOINT,
        8883
    )
    myMQTTClient.configureCredentials(
        PATH_ROOT_CA,
        PRIVATE_PEM,
        CERTIFICATE
    )

    # Infinite offline Publish queueing
    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    
    # Establisch connection
    connecting_time = time.time() + 10
    if time.time() < connecting_time:  # try connecting to AWS for 10 seconds
        myMQTTClient.connect()
        myMQTTClient.publish("IoT_TOPIC/info", "connected", 0)
        print("MQTT Client connection success!")

    else:
        print("Error: Check your AWS details in the program")
    
    return myMQTTClient
        
# Get the GPIO events
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(TACHO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_rpm(n):
    '''Calculation of RPM afrom GPIO Board Pins'''
    global t0
    global rpm
    global freq
    dt = time.time() - t0
    try:
        freq = 1 / dt
        rpm = (freq / 2) * 60
    except ZeroDivisionError:
        pass
    t0 = time.time()

GPIO.add_event_detect(TACHO_PIN, GPIO.FALLING, get_rpm)

def send_data(client,topic,data,mode):
    '''Sending data to AWS IotCore'''
    
    client.publish(
        topic,
        data,
        mode
    )
        

def main():
    '''Calling AWS and sending values to IoT Core'''
    
    # Connect to AWS
    myMQTTClient = connect_iotcore()
    
    while True:  
        # generate and print payload for reference
        #rpm =  
        data = {'TIME': datetime.now().isoformat(),"FANID": FAN_ID,"FREQ": int(round(freq,0)), "RPM": int(round(rpm,0))}
        data_out = json.dumps(data)
        print(data_out)
        
        send_data(
            client=myMQTTClient,
            topic="IoT_TOPIC/recieve",
            data=data_out,
            mode=0,
        )
               
        # Display data on LCD screen
        lcd.lcd_display_string("RPM: %s" %int(round(rpm,0)), 1)
        lcd.lcd_display_string("Frequency: %s" %int(round(freq,0)), 2)
        time.sleep(1)

    while not done:  # interupt with CTRl+X
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                done = True

if __name__ == "__main__":
    main()
