#include <Brain.h>
#include <WiFi.h>
#include <PubSubClient.h>
char* signals;

// WiFi
//const char* ssid = "TP-Link_AP_6B1A";
//const char* password = "36538294";

const char* ssid = "INFINITUMBD74_2.4";
const char* password = "4484179056";
// MQTT Broker
const char *mqtt_broker = "mqtt.eclipseprojects.io";//"broker";
const char *topic = "EEG";
const char *mqtt_username = "";//"emqx";
const char *mqtt_password = "";//"public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
// Set up the brain parser, pass it the hardware serial object you want to listen on.
Brain brain(Serial);





void setup() {
    // Start the hardware serial.
    Serial.begin(9600);

WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
     delay(1000);
     Serial.println("Connecting to WiFi..");
 }
 Serial.println("Connected to the WiFi network");
 //connecting to a mqtt broker
 client.setServer(mqtt_broker, mqtt_port);
 client.setCallback(callback);
 while (!client.connected()) {
     String client_id = "esp32-client-";
     client_id += String(WiFi.macAddress());
     Serial.printf("The client %s connects to the  mqtt broker\n", client_id.c_str());
     if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
         Serial.println("broker connected");
     } else {
         Serial.print("failed with state ");
         Serial.print(client.state());
         delay(2000);
     }
 }
 // publish and subscribe
 //client.publish(topic, "Hi");
 client.subscribe(topic);
}



void callback(char *topic, byte *payload, unsigned int length) {
 Serial.print("Message arrived in topic: ");
 Serial.println(topic);
 Serial.print("Message:");
 for (int i = 0; i < length; i++) {
     Serial.print((char) payload[i]);
 }
 Serial.println();
 Serial.println("-----------------------");
}



void loop() {
    // Expect packets about once per second.
    // The .readCSV() function returns a string (well, char*) listing the most recent brain data, in the following format:
    // "signal strength, attention, meditation, delta, theta, low alpha, high alpha, low beta, high beta, low gamma, high gamma"
    if (brain.update()) {
        Serial.println(brain.readErrors());
    //    Serial.println(brain.readCSV());
        char* sig= brain.readCSV();
        char signals2 = *sig;
        String ab = String(sig);
        //client.publish(topic,signals2);
        Serial.println(ab);
        client.publish(topic,ab.c_str());

    }
}
