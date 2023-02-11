#include <WiFi.h>
#include <PubSubClient.h>
#define DIN 13 // digital read
double value, volts;
char br[] = "respiracion";
int a=0;
int contadorA = 0;
int contadorB = 0;
int contadorAt = 0;
int contadorBt = 0;
int b= 0;
int c= 0;


// WiFi
//const char* ssid = "TP-Link_AP_6B1A";
//const char* password = "36538294";

const char* ssid = "INFINITUMBD74_2.4";
const char* password = "4484179056";

// MQTT Broker
const char *mqtt_broker = "mqtt.eclipseprojects.io";//"broker";
const char *topic = "Breathing";
const char *topic2 = "BRPM";
const char *topic3 = "BRPM:";
const char *mqtt_username = "";//"emqx";
const char *mqtt_password = "";//"public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);


//-------------------- TIMER -------------------
/*timer de hardware*/
hw_timer_t * timer = NULL;
volatile byte state = LOW;

void IRAM_ATTR onTimer(){
  state = !state;
 // digitalWrite(led, state);
}

//----------------------------------------------

void setup()
{
 //---------- TIMER
 timer = timerBegin(0, 80, true);
 timerAttachInterrupt(timer, &onTimer, true);
 timerAlarmWrite(timer, 10000000, true);
  timerAlarmEnable(timer);
 //--------------------  
pinMode(DIN, INPUT);
Serial.begin(115200);
delay(1000);
//-----------------------------
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


//-----------------------------------------------------------
void loop()
{
    client.loop();
value = digitalRead(DIN);
if (value == LOW){
  contadorA = 1;
}

 if (value == HIGH){
  contadorB = 1;
}

if (contadorA == 1 ){
  if(contadorB == 1){
    a = a + 1;
    }
  contadorA =0;
  contadorB= 0;
  }

if (state == HIGH){
     contadorAt = 1;
  }
  if (state == LOW){
     contadorBt = 1;
    }

if (contadorBt == 1 ){
  if(contadorAt == 1){
    b = a*3;
     a= 0;
    }
  
  contadorAt =0;
  contadorBt= 0;
  }
  Serial.print ("RPM ");
  Serial.println(b);
    String as = String(a);
    String bs = String(b);
  String ab = "Breaths: " + as + "  RPM " + bs ;
   Serial.print ("Respirations ");
    Serial.println(a);
 char bpm[8];
  char breath[8];
 itoa(b,bpm,10);
 itoa(a,breath,10);
   client.publish(topic,ab.c_str());
   client.publish(topic3,bpm);
 
  delay(100);
 
}
