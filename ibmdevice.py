import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

organization = "0ywc64"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    print(type(cmd.data))
    i=cmd.data['command']
    if i=='motor ON':
        print("motor is on")
    elif i=='motor OFF':
        print("motor is off")
        
    

try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions)

except Exception as e:
    print("caught exception connecting device: %s" % str(e))
    sys.exit()

deviceCli.connect()

while True:

    hum= random.randint(10,40)#print(hum)
    temp= random.randint(30,80)
    moist= random.randint(75,100)
    #send temparature and humidity to ibm watson
    data={'temperature' : temp, 'humidity' : hum, 'moisture' : moist}
    def myOnPublishCallback():
        print ("published temperature = %s C" % temp, "Humidity = %s %%" % hum, "moisture = %s %%" % moist, "to ibm watson")
    success = deviceCli.publishEvent("weather", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("not connected to IOTF")
    time.sleep(2)

    deviceCli.commandCallback = myCommandCallback

deviceCli.disconnect()    

    
       
