from serial import Serial
import sys
import threading
import time
import requests
from random import randrange

class XbeeController:
  def __init__(self):
    self.port = ""
    self.ser = None
    self.runningFlag = False
    self.theThread = None

  def openSerial(self, port):
    self.ser = Serial(port, 9600, timeout=None)
    self.ser.flushInput()
    self.theThread = threading.Thread(target=self.thread_function, args=())
    self.runningFlag = True
    self.theThread.start()

  def openFake(self):
    self.theThread = threading.Thread(target=self.thread_fake_function, args=())
    self.runningFlag = True
    self.theThread.start()

  def stopSerial(self):
    self.runningFlag = False
    #self.ser.close() 

  def thread_function(self):
    messageByteArray = []
    while self.runningFlag:
      if self.ser.in_waiting>0:
        myByte = self.ser.read(1)
        if myByte[0] == 0x7E:

            # We have a new message. Before reading it, let's analyse what was in the previous one
            if len(messageByteArray) != 0:
                self.interpretMessage(messageByteArray)
            messageByteArray = []
            messageByteArray.append(myByte[0])
        else:
            messageByteArray.append(myByte[0])
      else:
        time.sleep(0.01)

  def interpretMessage(self, bytesArray):
    if len(bytesArray) != 18:
        print("Wrong message length: ", str(len(bytesArray)))
        return
    elif bytesArray[0] != 0x7E:
        print("Wrong message start", bytesArray[0])
        return
    else:
        # print("###################")
        # print("Byte 2-3, MSB and LSB: ",bytesArray[1],bytesArray[2]) # end of API frame
        # print("RX type frame: ",bytesArray[3])
        # print("Source address: ",bytesArray[4],bytesArray[5])
        # print("Received Signal Strength Indicator: ",bytesArray[6])
        # print("Options: ",bytesArray[7])
        # print("Number of samples: ",bytesArray[8])
        # print("Channels enabled: ",bytesArray[9],bytesArray[10])
        ( bytesArray[11] << 8 ) | bytesArray[12]
        temperature = ( bytesArray[11] << 8 ) | bytesArray[12]
        light = ( bytesArray[13] << 8 ) | bytesArray[14]
        humidity = ( bytesArray[15] << 8 ) | bytesArray[16]
        # print("First channel: ", temperature)
        # print("Second channel: ", light)
        # print("Checksum: ",bytesArray[-1])

        # We convert temperature ADC counts in degrees
        mVTemperature = temperature * (3300/1024)
        celsiusDeg = (mVTemperature - 500) / 10
        print(celsiusDeg)
        r = requests.post('http://localhost:5000/api/addPoint', json = {'temperature':celsiusDeg, 'light':light, 'humidity':humidity, "timestamp": int(round(time.time() * 1000))})

  def thread_fake_function(self):
    while self.runningFlag:
      temperature = randrange(10)+10
      light = randrange(40)+30
      r = requests.post('http://localhost:5000/api/addPoint', json = {'temperature':temperature, 'light':light, 'humidity':0, "timestamp": int(round(time.time() * 1000))})
      time.sleep(1)