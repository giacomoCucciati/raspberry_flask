from serial import Serial
import sys
import threading
import time
import requests
from random import randrange

class ArduinoController:
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
      # send request for data
      print("sending read command")
      self.ser.write('read'.encode('utf-8'))
      # wait some time
      time.sleep(1)
      
      startTime = time.time()
      newTime = time.time()
 
      print(newTime - startTime)      
      while newTime - startTime < 5:
        if self.ser.in_waiting>0:
          myByte = self.ser.read(1)
          if myByte == b'\n':
            print(messageByteArray)
            self.interpretMessage(messageByteArray)
            messageByteArray = []
          else:
            messageByteArray.append(myByte[0])
          #     # We have a new message. Before reading it, let's analyse what was in the previous one
          #     if len(messageByteArray) != 0:
          #         self.interpretMessage(messageByteArray)
          #     messageByteArray = []
          #     messageByteArray.append(myByte[0])
          # else:
          #     messageByteArray.append(myByte[0])
        else:
          time.sleep(0.01)
        newTime = time.time()
      time.sleep(300)

  def interpretMessage(self, bytesArray):
    mystring = ''
    for by in bytesArray:
      mystring += (chr(by))
    mystring = mystring[:-1]
    print('Message to interpret', mystring)
    values = mystring.split(' ')

    jsonToSend = {}

    # lum 83
    # tempDTH 26.00
    # humDTH 56.00
    for val in values:
      couple = val.split('=')
      if len(couple) == 2:
        jsonToSend[couple[0]]=float(couple[1])
    jsonToSend["timestamp"]=int(round(time.time() * 1000))
    if 'extTemp' in jsonToSend:
      requests.post('http://localhost:4001/api/addPointExt', json = jsonToSend)
    else:
      requests.post('http://localhost:4001/api/addPoint', json = jsonToSend)
      
  def thread_fake_function(self):
    while self.runningFlag:
      temperature = randrange(10)+10
      light = randrange(40)+30
      r = requests.post('http://localhost:4001/api/addPoint', json = {'temperature':temperature, 'light':light, 'humidity':0, "timestamp": int(round(time.time() * 1000))})
      time.sleep(1)
