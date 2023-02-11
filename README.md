# CREE Project
Repository for the CREE Project

![](imagen.pptx)

# Python scripts

## Recibir
This file is used to test that it is recieving data from the Cloud MQTT Broker.

## Enviar
 
This file is used to send data from a shell terminal to the Cloud MQTT Broker.

## Multitest

This file is used to recieve the data from the MQTT Broker and subscribe to diferent topics. 
This file also allows us to send the data to PD. 


# MQTT Instalation

After having your Raspberry Pi board prepared with Raspberry Pi OS, you can continue with this tutorial. 

Let’s install the Mosquitto Broker.

1) Open a new Raspberry Pi terminal window. 
2) Run the following command to upgrade and update your system:

```shell
sudo apt update && sudo apt upgrade
```
3) Press Y and Enter. It will take some time to update and upgrade (in my case, it took approximately 10 minutes).

4) To install the Mosquitto Broker enter these next commands:
```shell
sudo apt install -y mosquitto mosquitto-clients
```

5) To make Mosquitto auto start when the Raspberry Pi boots, you need to run the following command (this means that the Mosquitto broker will automatically start when the Raspberry Pi starts):

```shell
sudo systemctl enable mosquitto.service
```
6) Now, test the installation by running the following command:
```shell
mosquitto -v
```


### Mosquitto Broker Enable Remote Access (No Authentication)

1) Run the following command to open the ```shell mosquitto.conf ```file.
```shell
sudo nano /etc/mosquitto/mosquitto.conf
```

2) Move to the end of the file using the arrow keys and paste the following two lines:

```shell
listener 1883
allow_anonymous true
```
3) Then, press CTRL-X to exit and save the file. Press Y and Enter.
 
4) Restart Mosquitto for the changes to take effect.
```shell
sudo systemctl restart mosquitto
```
