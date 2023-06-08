
import paho.mqtt.client as mqtt
import re
from pylsl import StreamInfo, StreamOutlet
import random
import sys

mqttBroker = "mqtt.eclipseprojects.io"
port = 1883

topic=[("Breathing",0),("Heartbeat",0),("GSR2",0),("EEG",0),("BRPM:",0)]
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'



def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    print("Topic: ", end = " ")
    print(message.topic)
    print("Message: ", end = " ")


    # Separete content of the payload by "," (comma) or " " (blank space), creating a list from the sapareted values  
    lst = re.split(',| ',msg)

    print(lst)
    print("---")
    
    
    if message.topic == 'Breathing':
        print("Sending Breathing")
        val = [int(lst[3])]
        print(val)
        outletStreamResp.push_sample(val)
    elif message.topic == 'Heartbeat':
        print("Sending HR")
        val = [int(lst[3])]
        print(val)
        outletStreamHeart.push_sample(val)
    elif message.topic == 'GSR2':
        print("Sending GSR")
        val = [int(lst[0])]
        print(val)
        outletStreamGSR.push_sample(val)
    elif message.topic == 'BRPM:':
        print("Sending EEG")
        # [signal strength, attention, meditation, delta, theta, low alpha, high alpha, low beta, high beta, low gamma, high gamma]
        val = [int(x) for x in lst]     # Converting list of strings to list of integers
        print(val)
        outletStreamEEG.push_sample(val)  
    print("------------------------------------------------")




    
if __name__ == "__main__":
    # Set up LabStreamingLayer stream.
    RespStream = StreamInfo('ESP_Breath', 'RBPM', 1, 10, 'float32', 'b')
    HeartStream = StreamInfo('ESP_Heart', 'BPM', 1, 10, 'float32', 'b')
    GSRStream = StreamInfo('ESP_GSR', 'GSR', 1, 10, 'float32', 'b')
    EEGStream = StreamInfo('ESP_EEG', 'EEG', 11, 10, 'float32', 'b')

    outletStreamResp = StreamOutlet(RespStream)
    outletStreamHeart = StreamOutlet(HeartStream)
    outletStreamGSR = StreamOutlet(GSRStream)
    outletStreamEEG = StreamOutlet(EEGStream)


    client = mqtt.Client(client_id)
    client.connect(mqttBroker,port) 

    client.subscribe(topic)
    client.on_message = on_message

    try: 
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        outletStreamResp.__del__()
        outletStreamHeart.__del__()
        outletStreamGSR.__del__()
        outletStreamEEG.__del__()
        sys.exit()

