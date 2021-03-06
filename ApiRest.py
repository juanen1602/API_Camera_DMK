import sys
import gi
import time

import urllib

import os
import os.path

import glob

import requests

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Tcam, Gst

from flask import Flask
from flask import request
from flask import jsonify
from flask import json
from flask import render_template
from flask import redirect
from flask import url_for
from flask import redirect
from flask import make_response
from flask import send_file


import datetime

import threading
from threading import Thread
from threading import Lock

mutex = Lock()

sys.path.insert(0, 'JsonFile/')
import JsonFile
from JsonFile import JSONFile

sys.path.insert(0, 'Library/')
import library
from library import DMK

sys.path.insert(0, 'Shell/')
import ShellCommands
from ShellCommands import Shell

sys.path.insert(0, 'ZIP/')
import dwlZip
from dwlZip import Zip

sem_change = None

task_active = False

dmk = DMK()

jsonfile = JSONFile()

shell = Shell()

fileZip = Zip()

texp = None
tout = 10
terror = 2



def SetParametersToDMK(name, value):
	global sem_change

	dmk.Brightness[0] = jsonfile.parameters.brightness.Values['CurrentValue']
	dmk.Gamma[0] = jsonfile.parameters.gamma.Values['CurrentValue']
	dmk.Gain[0] = jsonfile.parameters.gain.Values['CurrentValue']
	dmk.Exposure[0] = jsonfile.parameters.exposure.Values['CurrentValue']
	dmk.ExposureAuto[0] = jsonfile.parameters.exposureauto.Values['CurrentValue']

	dmk.SetParameters(name, value)

	sem_change = True


def SetExposureAutotoFalse():
	res = os.popen('tcam-ctrl -p -s "Exposure Auto=false" ' + str(dmk.serialNumber)).readlines()
	
	
def SetWhiteBalanceAutotoFalse():
	listParameters = dmk.GetListParameters()
	whitebalance = False
	for i in range(len(listParameters)):
		if listParameters[i] == "Whitebalance Auto":
			whitebalance = True
			break
	
	if whitebalance == True:
		res = os.popen('tcam-ctrl -p -s "Whitebalance Auto=false" ' + str(dmk.serialNumber)).readlines()	  


def GetDefaultValues(namefile):
	f = open('Default/' + str(namefile), 'r')
	dmk.textDefault = f.read()
	f.close()
	
	for i in range(len(dmk.textDefault)):
		if dmk.textDefault[i] == '\n':
			dmk.nbrLinesDefault += 1
					
	print(dmk.nbrLinesDefault)
	
	
			
	
	
def GetDefaultValue(parameter):
	a = 0
	for i in range(len(dmk.textDefault)):
		if dmk.textDefault[i] == '\n':
			a += 1
					
	print(a)
	
	textDefaultList = list()
	
	
	
	
def GetParametersFromDMK():
	global sem_change
	
#	print(dmk.serialNumber)

	dmk.GetParameters()

	jsonfile.parameters.brightness.Values['CurrentValue'] = dmk.Brightness[0]
	jsonfile.parameters.brightness.Values['MinValue'] = dmk.Brightness[1]
	jsonfile.parameters.brightness.Values['MaxValue'] = dmk.Brightness[2]
	jsonfile.parameters.brightness.Values['DefaultValue'] = dmk.Brightness[3]
	jsonfile.parameters.brightness.Brightness['Category'] = dmk.Brightness[4]
	jsonfile.parameters.brightness.Brightness['Group'] = dmk.Brightness[5]

	jsonfile.parameters.gamma.Values['CurrentValue'] = dmk.Gamma[0]
	jsonfile.parameters.gamma.Values['MinValue'] = dmk.Gamma[1]
	jsonfile.parameters.gamma.Values['MaxValue'] = dmk.Gamma[2]
	jsonfile.parameters.gamma.Values['DefaultValue'] = dmk.Gamma[3]
	jsonfile.parameters.gamma.Gamma['Category'] = dmk.Gamma[4]
	jsonfile.parameters.gamma.Gamma['Group'] = dmk.Gamma[5]

	jsonfile.parameters.gain.Values['CurrentValue'] = dmk.Gain[0]
	jsonfile.parameters.gain.Values['MinValue'] = dmk.Gain[1]
	jsonfile.parameters.gain.Values['MaxValue'] = dmk.Gain[2]
	jsonfile.parameters.gain.Values['DefaultValue'] = dmk.Gain[3]
	jsonfile.parameters.gain.Gain['Category'] = dmk.Gain[4]
	jsonfile.parameters.gain.Gain['Group'] = dmk.Gain[5]
	
#    jsonfile.parameters.exposure.Values['CurrentValue'] = dmk.Exposure[0]
	jsonfile.parameters.exposure.Values['CurrentValue'] = shell.ShellGet('Exposure','CurrentValue', dmk.serialNumber)
#    jsonfile.parameters.exposure.Values['MinValue'] = dmk.Exposure[1]
	jsonfile.parameters.exposure.Values['MinValue'] = shell.ShellGet('Exposure','MinValue', dmk.serialNumber)
#    jsonfile.parameters.exposure.Values['MaxValue'] = dmk.Exposure[2]
	jsonfile.parameters.exposure.Values['MaxValue'] = shell.ShellGet('Exposure','MaxValue', dmk.serialNumber)
#    jsonfile.parameters.exposure.Values['DefaultValue'] = dmk.Exposure[3]
	jsonfile.parameters.exposure.Values['DefaultValue'] = shell.ShellGet('Exposure','DefaultValue', dmk.serialNumber)
	jsonfile.parameters.exposure.Exposure['Category'] = dmk.Exposure[4]
	jsonfile.parameters.exposure.Exposure['Group'] = dmk.Exposure[5]

#    jsonfile.parameters.exposureauto.Values['CurrentValue'] = dmk.ExposureAuto[0]
#	jsonfile.parameters.exposureauto.Values['CurrentValue'] = GetExposureFromShell('CurrentAuto')
	jsonfile.parameters.exposureauto.Values['CurrentValue'] = shell.ShellGet('Exposure Auto','CurrentValue', dmk.serialNumber)
#    jsonfile.parameters.exposureauto.Values['DefaultValue'] = dmk.ExposureAuto[1]
	jsonfile.parameters.exposureauto.Values['DefaultValue'] = shell.ShellGet('Exposure Auto','DefaultValue', dmk.serialNumber)
	jsonfile.parameters.exposureauto.ExposureAuto['Category'] = dmk.ExposureAuto[2]
	jsonfile.parameters.exposureauto.ExposureAuto['Group'] = dmk.ExposureAuto[3] 

	jsonfile.parameters.saturation.Values['CurrentValue'] = dmk.Saturation[0]
	jsonfile.parameters.saturation.Values['MinValue'] = dmk.Saturation[1]
	jsonfile.parameters.saturation.Values['MaxValue'] = dmk.Saturation[2]
	jsonfile.parameters.saturation.Values['DefaultValue'] = dmk.Saturation[3]
	jsonfile.parameters.saturation.Saturation['Category'] = dmk.Saturation[4]
	jsonfile.parameters.saturation.Saturation['Group'] = dmk.Saturation[5]
	
	jsonfile.parameters.hue.Values['CurrentValue'] = dmk.Hue[0]
	jsonfile.parameters.hue.Values['MinValue'] = dmk.Hue[1]
	jsonfile.parameters.hue.Values['MaxValue'] = dmk.Hue[2]
	jsonfile.parameters.hue.Values['DefaultValue'] = dmk.Hue[3]
	jsonfile.parameters.hue.Hue['Category'] = dmk.Hue[4]
	jsonfile.parameters.hue.Hue['Group'] = dmk.Hue[5]
	
	jsonfile.parameters.whitebalancered.Values['CurrentValue'] = dmk.WhiteBalanceRed[0]
	jsonfile.parameters.whitebalancered.Values['MinValue'] = dmk.WhiteBalanceRed[1]
	jsonfile.parameters.whitebalancered.Values['MaxValue'] = dmk.WhiteBalanceRed[2]
	jsonfile.parameters.whitebalancered.Values['DefaultValue'] = dmk.WhiteBalanceRed[3]
	jsonfile.parameters.whitebalancered.WhiteBalanceRed['Category'] = dmk.WhiteBalanceRed[4]
	jsonfile.parameters.whitebalancered.WhiteBalanceRed['Group'] = dmk.WhiteBalanceRed[5]
	
	jsonfile.parameters.whitebalanceblue.Values['CurrentValue'] = dmk.WhiteBalanceBlue[0]
	jsonfile.parameters.whitebalanceblue.Values['MinValue'] = dmk.WhiteBalanceBlue[1]
	jsonfile.parameters.whitebalanceblue.Values['MaxValue'] = dmk.WhiteBalanceBlue[2]
	jsonfile.parameters.whitebalanceblue.Values['DefaultValue'] = dmk.WhiteBalanceBlue[3]
	jsonfile.parameters.whitebalanceblue.WhiteBalanceBlue['Category'] = dmk.WhiteBalanceBlue[4]
	jsonfile.parameters.whitebalanceblue.WhiteBalanceBlue['Group'] = dmk.WhiteBalanceBlue[5]		

	sem_change = False 
 

def failureServer():
	dmk.FindCamera()
	if dmk.CameraNotFound == True:
		return True
	return False   


def init():
	jsonfile.File['Widget'] = dmk.model
	jsonfile.File['SingleSerial'] = dmk.single_serial
	jsonfile.File['ConnectionType'] = dmk.connection_type

	SetExposureAutotoFalse()
	SetWhiteBalanceAutotoFalse()
	
	GetDefaultValues(dmk.serialNumber)
	print(dmk.textDefault)
#	GetDefaultValue(20)

#	print("Hasta aqui todo bien")
	sem_change = False

#	print("Entro dentro del GET")
	GetParametersFromDMK()
#	print("Salgo fuera del get")
	
	th2 = threading.Thread(target = dmk.DoTask)
	th2.start()     



app = Flask(__name__, template_folder = '/etc/udev/rules.d/')


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


@app.route('/')
def JSONFile():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonFile = json.dumps(jsonfile.File)
	jsonFile = json.loads(jsonFile.replace("\'", '"'))
	return jsonify(jsonFile)
	
	
@app.route('/VideoStreaming', methods = ['GET'])
def VideoOutput():
	dmk.onstream = True
	
	th = threading.Thread(target = dmk.VideoStreaming)
	th.start()
	
	return 'ON'
	

@app.route('/VideoStreamingOff', methods = ['GET'])
def VideoOutputOff():
	dmk.onstream = False
	
	return 'OFF'
	
	
@app.route('/VideoStreaming2', methods = ['GET'])
def VideoOutput2():
	
	if dmk.onstream == False:
		dmk.onstream = True	
		pid = dmk.VideoStreaming2()
		
		keyword = {
			'PID': pid,
			'Message': "Success: Streaming activated"
		}
	elif dmk.onstream == True:
		keyword = {
			'Message': "Error. Someone is using the camera"
		}
	
	jsonSuccess = json.dumps(keyword)
	jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
						
	return jsonify(jsonSuccess)	


@app.route('/VideoStreamingOff2', methods = ['GET'])
def VideoOutputOff2():
	
	if dmk.onstream == True:
		dmk.VideoStreamingOff2()
		dmk.onstream = False
		
		keyword = {
			'Message': "Success: Streaming stopped"
		}
	elif dmk.onstream == False:
		keyword = {
			'Message': "Error. The camera is already stopped"
		}
		
	jsonSuccess = json.dumps(keyword)
	jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
						
	return jsonify(jsonSuccess)		


@app.route('/RecordVideo', methods = ['POST'])
def RecordVideo():
	if dmk.onstream == True and dmk.onrecord == False:
		dmk.onrecord = True
		return "He empezado a grabar el video"
	elif dmk.onstream == True and dmk.onrecord == True:
		return "Ya se está grabando el video"
	elif dmk.onstream == False:	
		return "La camara debe estar grabando para activar el modo video"
	else:
		return "INTERNAL ERROR"		


@app.route('/TakePicture', methods = ['POST'])
def GetPicture():
	contentRequest = request.get_json()
	
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response
	
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d__%H-%M-%S-%f")

	dmk.TakePicture(contentRequest['Name'])  

	jsonfile.CodeSuccessResource['Code'] = 201
	jsonfile.CodeSuccessResource['Message'] = "Picture taken successfully"
	jsonfile.CodeSuccessResource['ID'] = None
	jsonResource = json.dumps(jsonfile.CodeSuccessResource)
	jsonResource = json.loads(jsonResource.replace("\'", '"'))
	
	response = make_response(jsonify(jsonResource), 201)
	return response	


@app.route('/CreateTask', methods = ['POST'])
def CreateTask():  
	global task_active
	global mutex
	contentRequest = request.get_json()
	print(contentRequest)

	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	th1 = threading.Thread(target = dmk.DoList, args=(contentRequest, mutex))
	th1.start()
	
	mutex.acquire()

	jsonfile.CodeSuccessResource['Code'] = 201
	jsonfile.CodeSuccessResource['Message'] = "Task created successfully"
	jsonfile.CodeSuccessResource['ID'] = dmk.n_request
	jsonResource = json.dumps(jsonfile.CodeSuccessResource)
	jsonResource = json.loads(jsonResource.replace("\'", '"'))
	mutex.release()

	response = make_response(jsonify(jsonResource), 201)
	return response


@app.route('/CreateZip/<int:ID>', methods = ['GET'])
def CreateZIP(ID):
#	contentRequest = request.get_json()
	
	if ID <= dmk.n_request:		
		data = dmk.Task(ID)
#		print(data[1])
	
		if data[1] == 'Done':
			fileZip.CreateFile(ID)
			return send_file(fileZip.nameZipFile, mimetype='NewZip.Zip')
		else:
			return "ERROR"
	
	else:
		return "CRITICAL ERROR"	


@app.route('/GetAmountParameters', methods = ['GET'])
def GetAParameters():
	list_parameters = dmk.GetListParameters()
#	print(list_parameters)
	
	keyword = {
		'listParameters': list_parameters
	}
	
	jsonSuccess = json.dumps(keyword)
	jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
	
	return jsonify(jsonSuccess)


@app.route('/Task/<int:ID>', methods = ['GET'])
def Task(ID):
	if ID <= dmk.n_request:
		myString = str(ID)
	
		data = dmk.Task(ID)

		keyword = {
			'ID': data[0],
			'Status': data[1],
			'Amount': data[2],
			'nRequest': dmk.n_request,
			'currentTask': dmk.currenttask,
			'members': data[3],
			'Code': 200,
			'Message': "Success, ID is recorded"
		}
	
		jsonStatus = json.dumps(keyword)
		jsonStatus = json.loads(jsonStatus.replace("\'", '"'))

		return jsonify(jsonStatus)
	else:
		keyword = {
			'Code': 400,
			'Message': "ID " + str(ID) + " not exists"	
		}
		
		jsonFailure = json.dumps(keyword)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		
		response = make_response(jsonify(jsonFailure), 400)
		return response		


@app.route('/Task/<int:ID>/<int:subID>', methods = ['GET'])
def TaskName(ID, subID):

	if ID < 0 or ID > dmk.n_request:

		keyword = {
			'Code': 400,
			'Message': "ID " + str(ID) + " not exists" 
		}
		
		jsonFailure = json.dumps(keyword)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		
		response = make_response(jsonify(jsonFailure), 400)
		return response
			
	elif subID < 0 or subID > dmk.CheckIDAmount(ID):
		keyword = {
			'Code': 400,
			'ID': int(ID),
			'Message': "ID " + str(ID) + " has no subID " + str(subID) 
		}
		
		jsonFailure = json.dumps(keyword)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		
		response = make_response(jsonify(jsonFailure), 400)
		return response
	
	else:
		data = dmk.Task(ID)
		if data[1] != 'Done':
			keyword = {
				'Code': 300,
				'ID': int(ID),
				'Message': "ID " + str(ID) + " has not finished Task",
				'Status': data[1]
			}
			
			jsonInfo = json.dumps(keyword)
			jsonInfo = json.loads(jsonInfo.replace("\'", '"'))
		
			response = make_response(jsonify(jsonInfo), 300)
			return response
					
		else:
			name = dmk.ReturnNameID(ID, subID)
			
			keyword = {
				'Code': 200,
				'ID': int(ID),
				'subID': int(subID),
				'Name': str(name)
			}
			
			jsonSuccess = json.dumps(keyword)
			jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
						
			return jsonify(jsonSuccess)	


@app.route('/GetCurrentTask', methods = ['GET'])
def GetCurrentTask():
	keyword = {
		'Value':  dmk.currenttask
	}
			
	Json = json.dumps(keyword)
	Json = json.loads(Json.replace("\'", '"'))
		
	return jsonify(Json)


@app.route('/Photo/<string:name>', methods = ['GET'])
def GetPhoto(name):
	addressFolder = '/tmp/'
	filename = addressFolder + name + '.jpg'
	
	checkingFile = os.path.isfile(filename)
	if checkingFile == True:
		return send_file(filename, mimetype='NewPhoto.jpg')
		
	elif checkingFile == False:
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "File not existing"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))
		
		response = make_response(jsonify(jsonFailureServer), 500)
		return response


#GET Methods

@app.route('/GetParameters', methods = ['GET'])
def GetParameters():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonParameters = json.dumps(jsonfile.parameters.Parameters)
	jsonParameters = json.loads(jsonParameters.replace("\'", '"'))
	return jsonify(jsonParameters)


@app.route('/GetParameters/Brightness', methods = ['GET'])
def GetBrightness():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonBrightness = json.dumps(jsonfile.parameters.brightness.Brightness)
	jsonBrightness = json.loads(jsonBrightness.replace("\'", '"'))

	return jsonify(jsonBrightness)


@app.route('/GetParameters/Gamma', methods = ['GET'])
def GetGamma():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonGamma = json.dumps(jsonfile.parameters.gamma.Gamma)
	jsonGamma = json.loads(jsonGamma.replace("\'", '"'))

	return jsonify(jsonGamma)


@app.route('/GetParameters/Gain', methods = ['GET'])
def GetGain():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonGain = json.dumps(jsonfile.parameters.gain.Gain)
	jsonGain = json.loads(jsonGain.replace("\'", '"'))

	return jsonify(jsonGain)


@app.route('/GetParameters/Exposure', methods = ['GET'])
def GetExposure():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonExposure = json.dumps(jsonfile.parameters.exposure.Exposure)
	jsonExposure = json.loads(jsonExposure.replace("\'", '"'))

	return jsonify(jsonExposure)


@app.route('/GetParameters/ExposureAuto', methods = ['GET'])
def GetExposureAuto():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonExposureAuto = json.dumps(jsonfile.parameters.exposureauto.ExposureAuto)
	jsonExposureAuto = json.loads(jsonExposureAuto.replace("\'", '"'))

	return jsonify(jsonExposureAuto)
	
	
@app.route('/GetParameters/Saturation', methods = ['GET'])
def GetSaturation():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonSaturation = json.dumps(jsonfile.parameters.saturation.Saturation)
	jsonSaturation = json.loads(jsonSaturation.replace("\'", '"'))

	return jsonify(jsonSaturation)	
	
	
@app.route('/GetParameters/Hue', methods = ['GET'])
def GetHue():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonHue = json.dumps(jsonfile.parameters.hue.Hue)
	jsonHue = json.loads(jsonHue.replace("\'", '"'))

	return jsonify(jsonHue)
	
	
@app.route('/GetParameters/WhiteBalanceRed', methods = ['GET'])
def GetWhiteBalanceRed():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonWhiteBalance = json.dumps(jsonfile.parameters.whitebalancered.WhiteBalanceRed)
	jsonWhiteBalance = json.loads(jsonWhiteBalance.replace("\'", '"'))

	return jsonify(jsonWhiteBalance)
	
	
@app.route('/GetParameters/WhiteBalanceBlue', methods = ['GET'])
def GetWhiteBalanceBlue():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	if sem_change == True:
		GetParametersFromDMK()
	jsonWhiteBalance = json.dumps(jsonfile.parameters.whitebalanceblue.WhiteBalanceBlue)
	jsonWhiteBalance = json.loads(jsonWhiteBalance.replace("\'", '"'))

	return jsonify(jsonWhiteBalance)				

#PUT Methods

@app.route('/Gatherframes', methods = ['PUT'])
def GatherFrames():
	return "FRAMES RETURNED"


@app.route('/SetParameters', methods = ['PUT'])
def SetParameters():
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	Example = {
		'Brightness': "/SetParameters/Brightness/20",
		'Gamma': "/SetParameters/Gamma/100",
		'Gain': "/SetParameters/Gain/400"
	}
	jsonfile.CodeInformational['Code'] = 300
	jsonfile.CodeInformational['Info'] = "Select one parameter you will to modify"
	jsonfile.CodeInformational['Parameters'] = ['Brightness', 'Gamma', 'Gain', 'Exposure', 'ExposureAuto']
	jsonfile.CodeInformational['Example'] = Example

	jsonInformational = json.dumps(jsonfile.CodeInformational)
	jsonInformational = json.loads(jsonInformational.replace("\'", '"'))
	response = make_response(jsonify(jsonInformational), 300)
	return response 


@app.route('/SetParameters/Brightness', methods = ['PUT'])
def SetBrightnessNum():
	contentRequest = request.get_json()
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response
	
	elif jsonfile.parameters.brightness.Values['CurrentValue'] == None:
		jsonfile.CodeUnavailable['Parameter'] = 'Brightness'
		jsonfile.CodeUnavailable['Code'] = 400
		jsonfile.CodeUnavailable['Value'] = 0
		jsonfile.CodeUnavailable['MinValue'] = 0
		jsonfile.CodeUnavailable['MaxValue'] = 0
		jsonfile.CodeUnavailable['Message'] = "Value not available for this device"
		
		jsonUnavailable = json.dumps(jsonfile.CodeUnavailable)
		jsonUnavailable = json.loads(jsonUnavailable.replace("\'", '"'))
		response = make_response(jsonify(jsonUnavailable), 400)
		return response	

	elif contentRequest['Value'] >= jsonfile.parameters.brightness.Values['MinValue'] and contentRequest['Value'] <= jsonfile.parameters.brightness.Values['MaxValue']:
		jsonfile.parameters.brightness.Values['CurrentValue'] = contentRequest['Value']
		SetParametersToDMK("Brightness", contentRequest['Value'])

		jsonfile.CodeSuccess['Parameter'] = 'Brightness'
		jsonfile.CodeSuccess['Code'] = 200
		jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
		jsonfile.CodeSuccess['Value'] = contentRequest['Value']

		jsonSuccess = json.dumps(jsonfile.CodeSuccess)
		jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
		response = make_response(jsonify(jsonSuccess), 200)
		return response
		
	else:
		jsonfile.CodeFailure['Parameter'] = 'Brightness'
		jsonfile.CodeFailure['Code'] = 400
		jsonfile.CodeFailure['Message'] = "Value out of range"
		jsonfile.CodeFailure['MinValue'] = jsonfile.parameters.brightness.Values['MinValue']
		jsonfile.CodeFailure['MaxValue'] = jsonfile.parameters.brightness.Values['MaxValue']

		jsonFailure = json.dumps(jsonfile.CodeFailure)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response


@app.route('/SetParameters/Gamma', methods = ['PUT'])
def SetGammaNum():
	contentRequest = request.get_json()
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	elif jsonfile.parameters.gamma.Values['CurrentValue'] == None:
		jsonfile.CodeUnavailable['Parameter'] = 'Gamma'
		jsonfile.CodeUnavailable['Code'] = 400
		jsonfile.CodeUnavailable['Value'] = 0
		jsonfile.CodeUnavailable['MinValue'] = 0
		jsonfile.CodeUnavailable['MaxValue'] = 0
		jsonfile.CodeUnavailable['Message'] = "Value not available for this device"
		
		jsonUnavailable = json.dumps(jsonfile.CodeUnavailable)
		jsonUnavailable = json.loads(jsonUnavailable.replace("\'", '"'))
		response = make_response(jsonify(jsonUnavailable), 400)
		return response	

	elif contentRequest['Value'] >= jsonfile.parameters.gamma.Values['MinValue'] and contentRequest['Value'] <= jsonfile.parameters.gamma.Values['MaxValue']:
		jsonfile.parameters.gamma.Values['CurrentValue'] = contentRequest['Value']
		SetParametersToDMK("Gamma", contentRequest['Value'])

		jsonfile.CodeSuccess['Parameter'] = 'Gamma'
		jsonfile.CodeSuccess['Code'] = 200
		jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
		jsonfile.CodeSuccess['Value'] = contentRequest['Value']

		jsonSuccess = json.dumps(jsonfile.CodeSuccess)
		jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
		response = make_response(jsonify(jsonSuccess), 200)
		return response
	else:
		jsonfile.CodeFailure['Parameter'] = 'Gamma'
		jsonfile.CodeFailure['Code'] = 400
		jsonfile.CodeFailure['Message'] = "Value out of range"
		jsonfile.CodeFailure['MinValue'] = jsonfile.parameters.gamma.Values['MinValue']
		jsonfile.CodeFailure['MaxValue'] = jsonfile.parameters.gamma.Values['MaxValue']

		jsonFailure = json.dumps(jsonfile.CodeFailure)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response
   

@app.route('/SetParameters/Gain', methods = ['PUT'])
def SetGainNum():
	contentRequest = request.get_json()
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	elif jsonfile.parameters.gain.Values['CurrentValue'] == None:
		jsonfile.CodeUnavailable['Parameter'] = 'Gain'
		jsonfile.CodeUnavailable['Code'] = 400
		jsonfile.CodeUnavailable['Value'] = 0
		jsonfile.CodeUnavailable['MinValue'] = 0
		jsonfile.CodeUnavailable['MaxValue'] = 0
		jsonfile.CodeUnavailable['Message'] = "Value not available for this device"
		
		jsonUnavailable = json.dumps(jsonfile.CodeUnavailable)
		jsonUnavailable = json.loads(jsonUnavailable.replace("\'", '"'))
		response = make_response(jsonify(jsonUnavailable), 400)
		return response	

	elif contentRequest['Value'] >= jsonfile.parameters.gain.Values['MinValue'] and contentRequest['Value'] <= jsonfile.parameters.gain.Values['MaxValue']:
		jsonfile.parameters.gain.Values['CurrentValue'] = contentRequest['Value']
		SetParametersToDMK("Gain", contentRequest['Value'])              

		jsonfile.CodeSuccess['Parameter'] = 'Gain'
		jsonfile.CodeSuccess['Code'] = 200
		jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
		jsonfile.CodeSuccess['Value'] = contentRequest['Value']

		jsonSuccess = json.dumps(jsonfile.CodeSuccess)
		jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
		response = make_response(jsonify(jsonSuccess), 200)
		return response
		
	else:
		jsonfile.CodeFailure['Parameter'] = 'Gain'
		jsonfile.CodeFailure['Code'] = 400
		jsonfile.CodeFailure['Message'] = "Value out of range"
		jsonfile.CodeFailure['MinValue'] = jsonfile.parameters.gain.Values['MinValue']
		jsonfile.CodeFailure['MaxValue'] = jsonfile.parameters.gain.Values['MaxValue']

		jsonFailure = json.dumps(jsonfile.CodeFailure)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response


@app.route('/SetParameters/Exposure', methods = ['PUT'])
def SetExposureNum():
	global sem_change
	contentRequest = request.get_json()
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	elif jsonfile.parameters.exposure.Values['CurrentValue'] == None:
		jsonfile.CodeUnavailable['Parameter'] = 'Exposure'
		jsonfile.CodeUnavailable['Code'] = 400
		jsonfile.CodeUnavailable['Value'] = 0
		jsonfile.CodeUnavailable['MinValue'] = 0
		jsonfile.CodeUnavailable['MaxValue'] = 0
		jsonfile.CodeUnavailable['Message'] = "Value not available for this device"
		
		jsonUnavailable = json.dumps(jsonfile.CodeUnavailable)
		jsonUnavailable = json.loads(jsonUnavailable.replace("\'", '"'))
		response = make_response(jsonify(jsonUnavailable), 400)
		return response	

	elif contentRequest['Value'] >= jsonfile.parameters.exposure.Values['MinValue'] and contentRequest['Value'] <= jsonfile.parameters.exposure.Values['MaxValue']:
		if contentRequest['Value']%100 == 0:
			jsonfile.parameters.exposure.Values['CurrentValue'] = contentRequest['Value']
			shell.ShellPut('Exposure',contentRequest['Value'], dmk.serialNumber)
			sem_change = True
			print(sem_change)

			jsonfile.CodeSuccess['Parameter'] = 'Exposure'
			jsonfile.CodeSuccess['Code'] = 200
			jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
			jsonfile.CodeSuccess['Value'] = contentRequest['Value']

			jsonSuccess = json.dumps(jsonfile.CodeSuccess)
			jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
			response = make_response(jsonify(jsonSuccess), 200)
			return response
		else:
			jsonfile.CodeFailure['Parameter'] = 'Exposure'
			jsonfile.CodeFailure['Code'] = 400
			jsonfile.CodeFailure['Message'] = "Number must be multiple of 100"
				
			jsonFailure = json.dumps(jsonfile.CodeFailure)
			jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
			response = make_response(jsonify(jsonFailure), 400)
			return response
				
	else:
		jsonfile.CodeFailure['Parameter'] = 'Exposure'
		jsonfile.CodeFailure['Code'] = 400
		jsonfile.CodeFailure['Message'] = "Value out of range"
		jsonfile.CodeFailure['MinValue'] = jsonfile.parameters.exposure.Values['MinValue']
		jsonfile.CodeFailure['MaxValue'] = jsonfile.parameters.exposure.Values['MaxValue']

		jsonFailure = json.dumps(jsonfile.CodeFailure)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response
		

@app.route('/SetParameters/Saturation', methods = ['PUT'])
def SetSaturationNum():
	contentRequest = request.get_json()
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response
		
	elif jsonfile.parameters.saturation.Values['CurrentValue'] == None:
		jsonfile.CodeUnavailable['Parameter'] = 'Saturation'
		jsonfile.CodeUnavailable['Code'] = 400
		jsonfile.CodeUnavailable['Value'] = 0
		jsonfile.CodeUnavailable['MinValue'] = 0
		jsonfile.CodeUnavailable['MaxValue'] = 0
		jsonfile.CodeUnavailable['Message'] = "Value not available for this device"
		
		jsonUnavailable = json.dumps(jsonfile.CodeUnavailable)
		jsonUnavailable = json.loads(jsonUnavailable.replace("\'", '"'))
		response = make_response(jsonify(jsonUnavailable), 400)
		return response		

	elif contentRequest['Value'] >= jsonfile.parameters.saturation.Values['MinValue'] and contentRequest['Value'] <= jsonfile.parameters.saturation.Values['MaxValue']:
		jsonfile.parameters.saturation.Values['CurrentValue'] = contentRequest['Value']
		SetParametersToDMK("Saturation", contentRequest['Value'])

		jsonfile.CodeSuccess['Parameter'] = 'Saturation'
		jsonfile.CodeSuccess['Code'] = 200
		jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
		jsonfile.CodeSuccess['Value'] = contentRequest['Value']

		jsonSuccess = json.dumps(jsonfile.CodeSuccess)
		jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
		response = make_response(jsonify(jsonSuccess), 200)
		return response
	else:
		jsonfile.CodeFailure['Parameter'] = 'Saturation'
		jsonfile.CodeFailure['Code'] = 400
		jsonfile.CodeFailure['Message'] = "Value out of range"
		jsonfile.CodeFailure['MinValue'] = jsonfile.parameters.saturation.Values['MinValue']
		jsonfile.CodeFailure['MaxValue'] = jsonfile.parameters.saturation.Values['MaxValue']

		jsonFailure = json.dumps(jsonfile.CodeFailure)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response
		
		
@app.route('/SetParameters/Hue', methods = ['PUT'])
def SetHueNum():
	contentRequest = request.get_json()
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	elif jsonfile.parameters.hue.Values['CurrentValue'] == None:
		jsonfile.CodeUnavailable['Parameter'] = 'Hue'
		jsonfile.CodeUnavailable['Code'] = 400
		jsonfile.CodeUnavailable['Value'] = 0
		jsonfile.CodeUnavailable['MinValue'] = 0
		jsonfile.CodeUnavailable['MaxValue'] = 0
		jsonfile.CodeUnavailable['Message'] = "Value not available for this device"
		
		jsonUnavailable = json.dumps(jsonfile.CodeUnavailable)
		jsonUnavailable = json.loads(jsonUnavailable.replace("\'", '"'))
		response = make_response(jsonify(jsonUnavailable), 400)
		return response	

	elif contentRequest['Value'] >= jsonfile.parameters.hue.Values['MinValue'] and contentRequest['Value'] <= jsonfile.parameters.hue.Values['MaxValue']:
		jsonfile.parameters.hue.Values['CurrentValue'] = contentRequest['Value']
		SetParametersToDMK("Hue", contentRequest['Value'])

		jsonfile.CodeSuccess['Parameter'] = 'Hue'
		jsonfile.CodeSuccess['Code'] = 200
		jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
		jsonfile.CodeSuccess['Value'] = contentRequest['Value']

		jsonSuccess = json.dumps(jsonfile.CodeSuccess)
		jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
		response = make_response(jsonify(jsonSuccess), 200)
		return response
	else:
		jsonfile.CodeFailure['Parameter'] = 'Hue'
		jsonfile.CodeFailure['Code'] = 400
		jsonfile.CodeFailure['Message'] = "Value out of range"
		jsonfile.CodeFailure['MinValue'] = jsonfile.parameters.hue.Values['MinValue']
		jsonfile.CodeFailure['MaxValue'] = jsonfile.parameters.hue.Values['MaxValue']

		jsonFailure = json.dumps(jsonfile.CodeFailure)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response		
		

@app.route('/SetParameters/WhiteBalanceRed', methods = ['PUT'])
def SetWhiteBalanceRedNum():
	contentRequest = request.get_json()
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response

	elif jsonfile.parameters.whitebalancered.Values['CurrentValue'] == None:
		jsonfile.CodeUnavailable['Parameter'] = 'WhiteBalanceRed'
		jsonfile.CodeUnavailable['Code'] = 400
		jsonfile.CodeUnavailable['Value'] = 0
		jsonfile.CodeUnavailable['MinValue'] = 0
		jsonfile.CodeUnavailable['MaxValue'] = 0
		jsonfile.CodeUnavailable['Message'] = "Value not available for this device"
		
		jsonUnavailable = json.dumps(jsonfile.CodeUnavailable)
		jsonUnavailable = json.loads(jsonUnavailable.replace("\'", '"'))
		response = make_response(jsonify(jsonUnavailable), 400)
		return response	

	elif contentRequest['Value'] >= jsonfile.parameters.whitebalancered.Values['MinValue'] and contentRequest['Value'] <= jsonfile.parameters.whitebalancered.Values['MaxValue']:
		jsonfile.parameters.whitebalancered.Values['CurrentValue'] = contentRequest['Value']
		SetParametersToDMK("Whitebalance Red", contentRequest['Value'])              

		jsonfile.CodeSuccess['Parameter'] = 'WhiteBalanceRed'
		jsonfile.CodeSuccess['Code'] = 200
		jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
		jsonfile.CodeSuccess['Value'] = contentRequest['Value']

		jsonSuccess = json.dumps(jsonfile.CodeSuccess)
		jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
		response = make_response(jsonify(jsonSuccess), 200)
		return response
		
	else:
		jsonfile.CodeFailure['Parameter'] = 'WhiteBalanceRed'
		jsonfile.CodeFailure['Code'] = 400
		jsonfile.CodeFailure['Message'] = "Value out of range"
		jsonfile.CodeFailure['MinValue'] = jsonfile.parameters.whitebalancered.Values['MinValue']
		jsonfile.CodeFailure['MaxValue'] = jsonfile.parameters.whitebalancered.Values['MaxValue']

		jsonFailure = json.dumps(jsonfile.CodeFailure)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response	
		
		
@app.route('/SetParameters/WhiteBalanceBlue', methods = ['PUT'])
def SetWhiteBalanceBlueNum():
	contentRequest = request.get_json()
	if failureServer():
		jsonfile.CodeFailureServer['Code'] = 500
		jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
		jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
		jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

		response = make_response(jsonify(jsonFailureServer), 500)
		return response
		
	elif jsonfile.parameters.whitebalanceblue.Values['CurrentValue'] == None:
		jsonfile.CodeUnavailable['Parameter'] = 'WhiteBalanceBlue'
		jsonfile.CodeUnavailable['Code'] = 400
		jsonfile.CodeUnavailable['Value'] = 0
		jsonfile.CodeUnavailable['MinValue'] = 0
		jsonfile.CodeUnavailable['MaxValue'] = 0
		jsonfile.CodeUnavailable['Message'] = "Value not available for this device"
		
		jsonUnavailable = json.dumps(jsonfile.CodeUnavailable)
		jsonUnavailable = json.loads(jsonUnavailable.replace("\'", '"'))
		response = make_response(jsonify(jsonUnavailable), 400)
		return response			

	elif contentRequest['Value'] >= jsonfile.parameters.whitebalanceblue.Values['MinValue'] and contentRequest['Value'] <= jsonfile.parameters.whitebalanceblue.Values['MaxValue']:
		jsonfile.parameters.whitebalanceblue.Values['CurrentValue'] = contentRequest['Value']
		SetParametersToDMK("Whitebalance Blue", contentRequest['Value'])              

		jsonfile.CodeSuccess['Parameter'] = 'WhiteBalanceBlue'
		jsonfile.CodeSuccess['Code'] = 200
		jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
		jsonfile.CodeSuccess['Value'] = contentRequest['Value']

		jsonSuccess = json.dumps(jsonfile.CodeSuccess)
		jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
		response = make_response(jsonify(jsonSuccess), 200)
		return response
		
	else:
		jsonfile.CodeFailure['Parameter'] = 'WhiteBalanceBlue'
		jsonfile.CodeFailure['Code'] = 400
		jsonfile.CodeFailure['Message'] = "Value out of range"
		jsonfile.CodeFailure['MinValue'] = jsonfile.parameters.whitebalanceblue.Values['MinValue']
		jsonfile.CodeFailure['MaxValue'] = jsonfile.parameters.whitebalanceblue.Values['MaxValue']

		jsonFailure = json.dumps(jsonfile.CodeFailure)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response	
		
			
#DELETE Methods
		
@app.route('/DeletePhoto/<string:name>', methods = ['DELETE'])
def erasePhoto(name):	
	addressFolder = '/tmp/'
	filename = addressFolder + name + '.jpg'
		
	checkingFile = os.path.isfile(filename)
	if checkingFile == True:
		value = dmk.deletePicture(filename)
		keyword = {
			'Code': 200,
			'Message': "Picture successfully erased"
		}
		
		jsonSuccess = json.dumps(keyword)
		jsonSuccess = json.loads(jsonSuccess.replace("\'", '"'))
						
		return jsonify(jsonSuccess)
		
	elif checkingFile == False:
		keyword = {
			'Code': 400,
			'Message': "Picture not found"
		}
		
		jsonFailure = json.dumps(keyword)
		jsonFailure = json.loads(jsonFailure.replace("\'", '"'))
		response = make_response(jsonify(jsonFailure), 400)
		return response
		


if __name__ == "__main__":
	init()

	app.run(host='192.168.43.23', debug = True , port = 8000)
