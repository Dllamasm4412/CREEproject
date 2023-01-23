import paho.mqtt.client as mqtt 
import time

mqttBroker ="mqtt.eclipseprojects.io" 

client = mqtt.Client("Temperature_Inside")
client.connect("mqtt.eclipseprojects.io",1883) 

while True:

    topic = 'hola2'
    topic2 = 'hola11111'
    client.publish("topico", topic)
    client.publish("topico2", topic2)
   # print("Just published " + str(randNumber) + " to topic TEMPERATURE")
    time.sleep(1)