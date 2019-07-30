from flask import Blueprint, jsonify
from flask_socketio import emit, join_room, leave_room
from flask import request
from . import socketio
from .xbeeController import XbeeController
from .arduinoController import ArduinoController
import time
import logging
import os
import json

apirouter = Blueprint("router", __name__)
# xbeeController = XbeeController()
xbeeController = ArduinoController()
pointList = []
portList = []

# I don't know where to put the creation of the port list
configFile = open(os.path.join("static", "config.json"), "r")
json_data = json.load(configFile)
print(json_data)
portList = json_data['portlist']

@apirouter.route('/startXbee',methods=['POST'])
def startXbee():
  message = 'Nothing appened'
  print(request)
  params = request.get_json(force=True)
  print(params)
  xbeeController.openSerial(params['selectedPort'])
  message = 'Serial reading started'
  return jsonify({"message": message})

@apirouter.route('/startFakeAcq',methods=['GET'])
def startFakeAcq():
  try:
    xbeeController.openFake()
    message = 'Serial reading started'
  except Exception as e:
    print('Error: ', e)
    message = 'An error has occurred'
  return jsonify({"message": message})

@apirouter.route('/stopXbee',methods=['GET'])
def stopXbee():
  message = 'Nothing appened'
  try:
    xbeeController.stopSerial()
    message = 'Stop message sent'
  except Exception as e:
    print('Error: ', e)
    message = 'An error has occurred'
  return jsonify({"message": message})

@apirouter.route('/addPoint',methods=['POST'])
def addPoints():
  print("Server contacted")
  params = request.get_json(force=True)
  print(params)
  pointList.append(params)
  if len(pointList) > 5000:
    pointList.pop(0)
  
  socketio.emit('updateSinglePoint')
  return jsonify({"message":"points received"})

@apirouter.route('/getPageUpdate',methods=['GET'])
def getPageUpdate():
  answer = {
    "selectedPort": xbeeController.port, 
    "portlist": portList, 
    "pointList": pointList
  }
  return jsonify(answer)

@apirouter.route('/getSinglePoint',methods=['GET'])
def getSinglePoint():
  answer = {
    "singlePoint": pointList[-1]
  }
  return jsonify(answer)