import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker ="mqtt.eclipseprojects.io"

client = mqtt.Client("Smartphone")
client.connect("mqtt.eclipseprojects.io",1883) 

client.loop_start()

while True:
    client.subscribe([("Heartbeat", 0), ("GSR", 0),("BRPM:", 0)])
    client.on_message=on_message 
    time.sleep(1)

client.loop_stop()
