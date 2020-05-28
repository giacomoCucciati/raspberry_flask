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
import prometheus_client
import random
from flask import Response
from influxdb import InfluxDBClient
import datetime


apirouter = Blueprint("router", __name__)
# xbeeController = XbeeController()
xbeeController = ArduinoController()
xbeeController2 = ArduinoController()
pointList = []
portList = []

# I don't know where to put the creation of the port list
configFile = open(os.path.join("/home/pi/Documents/raspberry_flask/Backend/static", "config.json"), "r")
json_data = json.load(configFile)
print(json_data)
portList = json_data['portlist']

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('sensorexample')

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
  # Adding raspberry temp
  try:
    theFile = '/home/pi/Documents/scripts/pitemp.txt'
    exists = os.path.isfile(theFile)
    if exists:
      fileptr = open(theFile, 'r') 
      answer = fileptr.read()  
      fileptr.close()
  except:
    print('No valid command')
  else:
    params['pitemp']=float(answer[5:-3])
  pointList.append(params)
  if len(pointList) > 1000:
    pointList.pop(0)
  #try:
  print(params)

  s = params['timestamp'] / 1000
  stringtime = datetime.datetime.utcfromtimestamp(s).strftime('%Y-%m-%dT%H:%M:%SZ')
  # In case we want to use time at this moment and not from arduino controller:
  # stringtime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
  print(stringtime)
  influxPoint = {}
  influxPoint["measurement"] = "rasp_measurements"
  influxPoint["tags"] = {"host":"raspberry3"}
  influxPoint["time"] = stringtime
  influxPoint["fields"] = {"pitemp": params['pitemp']}
  influxPoint["fields"]["DTHtemp"] = params['tempDTH']
  influxPoint["fields"]["DTHhum"] = params['humDTH']
  influxPoint["fields"]["lum"] = params['lum']
  influxPointList = []
  influxPointList.append(influxPoint)
  print(influxPoint)
  success = client.write_points(influxPointList)
  print('Point written on influxdb:', success)
  #except:
  #print('Error writing on InfluxDB')
  socketio.emit('updateSinglePoint')
  return jsonify({"message":"points received"})

@apirouter.route('/getPageUpdate',methods=['GET'])
def getPageUpdate():
  answer = {
    "selectedPort": xbeeController.port,
    "selectedPortExt": xbeeController2.port,
    "portlist": portList, 
    "pointList": pointList
  }
  return jsonify(answer)

@apirouter.route('/getSinglePoint',methods=['GET'])
def getSinglePoint():
  singlePoint = {}
  if len(pointList) > 0:
      singlePoint = pointList[-1]
  answer = {
    "singlePoint": singlePoint
  }
  return jsonify(answer)

@apirouter.route('/startXbeeExt',methods=['POST'])
def startXbeeExt():
  message = 'Nothing appened'
  print(request)
  params = request.get_json(force=True)
  print(params)
  xbeeController2.openSerial(params['selectedPort'])
  message = 'Serial reading started'
  return jsonify({"message": message})

@apirouter.route('/stopXbeeExt',methods=['GET'])
def stopXbeeExt():
  message = 'Nothing appened'
  try:
    xbeeController2.stopSerial()
    message = 'Stop message sent'
  except Exception as e:
    print('Error: ', e)
    message = 'An error has occurred'
  return jsonify({"message": message})

@apirouter.route('/addPointExt',methods=['POST'])
def addPointsExt():
  print("Server contacted by ext")
  params = request.get_json(force=True)
  print(params)
  
  s = params['timestamp'] / 1000
  stringtime = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%dT%H:%M:%SZ')
  print(stringtime)
  influxPoint = {}
  influxPoint["measurement"] = "external_measurements"
  influxPoint["tags"] = {"host":"arduino_xbee"}
  influxPoint["time"] = stringtime
  influxPoint["fields"] = {"extTemp": params['extTemp']}
  influxPoint["fields"]["lum"] = params['lum']
  influxPointList = []
  influxPointList.append(influxPoint)
  print(influxPoint)
  success = client.write_points(influxPointList)
  print('Point written on influxdb:', success)
  #except:
  #print('Error writing on InfluxDB')
  socketio.emit('updateSinglePoint')
  return jsonify({"message":"points received"})
