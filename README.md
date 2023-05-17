# README

## To run
Make sure that Zigbee2MQTT is running. This can be done by going to the folder: 
```
opt/zigbee2mqtt
```
and running the following command:
```
npm start
```

Next, go to the src directory of the project and run the following command:
```
python PGLmain.py
```
Make sure you have the following packages installed:
```
paho-mqtt
```
If the sensors and actuators are setup and named correctly, the program should run without any errors.