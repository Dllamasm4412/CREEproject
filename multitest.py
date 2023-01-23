import time  
import os
import subprocess
import paho.mqtt.client as mqtt
import json


broker_address="192.168.0.102"

mqtt_topic=[("Breathing",0),("Heartbeat",0),("GSR",0)]

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)   
    #playSingleShot()
    #obj = json.loads(str(message.payload.decode("utf-8")))
    #obj = json.loads(str(message)) 
    #val = obj[0]
    val = message.payload.decode("utf-8")
    print("received ", val)
    send2Pd(val)


def send2Pd(message=''):
    os.system("echo '" + message + "' | pdsend 12347 localhost udp")


print("creating new mqtt client instance")
client = mqtt.Client("Alvin")

print("connecting to broker")
client.connect(broker_address, 1883)

print("Subscribing to topic",mqtt_topic)
client.subscribe(mqtt_topic)


print("Publishing message to topic",mqtt_topic)
#client.publish(mqtt_topic,"Hallo!!!")

client.on_message=on_message
client.loop_start()


##################################################




while True:
        print(".")
        #client.publish(mqtt_topic,"Hallo!!!")
        time.sleep(3)