import sys
import gi
import time

import urllib

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Tcam, Gst

from flask import Flask
from flask import jsonify
from flask import json
from flask import render_template
from flask import redirect
from flask import url_for
from flask import redirect
from flask import make_response

sys.path.insert(0, 'JsonFile/')
import JsonFile
from JsonFile import JSONFile

sys.path.insert(0, 'Library/')
import library
from library import DMK

sem_change = None

dmk = DMK()

jsonfile = JSONFile()

def SetParametersToDMK(name, value):
    global sem_change

    dmk.Brightness[0] = jsonfile.parameters.brightness.Values['CurrentValue']
    dmk.Gamma[0] = jsonfile.parameters.gamma.Values['CurrentValue']
    dmk.Gain[0] = jsonfile.parameters.gain.Values['CurrentValue']
    dmk.Exposure[0] = jsonfile.parameters.exposure.Values['CurrentValue']
    dmk.ExposureAuto[0] = jsonfile.parameters.exposureauto.Values['CurrentValue']

    dmk.SetParameters(name, value)

    sem_change = True

def GetParametersFromDMK():
    global sem_change

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

    jsonfile.parameters.exposure.Values['CurrentValue'] = dmk.Exposure[0]
    jsonfile.parameters.exposure.Values['MinValue'] = dmk.Exposure[1]
    jsonfile.parameters.exposure.Values['MaxValue'] = dmk.Exposure[2]
    jsonfile.parameters.exposure.Values['DefaultValue'] = dmk.Exposure[3]
    jsonfile.parameters.exposure.Exposure['Category'] = dmk.Exposure[4]
    jsonfile.parameters.exposure.Exposure['Group'] = dmk.Exposure[5]

    jsonfile.parameters.exposureauto.Values['CurrentValue'] = dmk.ExposureAuto[0]
    jsonfile.parameters.exposureauto.Values['DefaultValue'] = dmk.ExposureAuto[1]
    jsonfile.parameters.exposureauto.ExposureAuto['Category'] = dmk.ExposureAuto[2]
    jsonfile.parameters.exposureauto.ExposureAuto['Group'] = dmk.ExposureAuto[3] 

    sem_change = False  

def failureServer():
    if dmk.CameraNotFound == True:
        return True
    return False   
    

def init():
    jsonfile.File['Widget'] = dmk.model
    jsonfile.File['SingleSerial'] = dmk.single_serial
    jsonfile.File['ConnectionType'] = dmk.connection_type

    sem_change = False

    GetParametersFromDMK()     



app = Flask(__name__, template_folder = '/etc/udev/rules.d/')

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
    print("{}".format(sem_change))
    return jsonify(jsonFile)

@app.route('/TakePicture')
def GetDriver():
    return render_template('80-theimagingsource-cameras.rules')

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
    print("{}".format(sem_change))
    return jsonify(jsonParameters)

@app.route('/GetParameters/Brightness', methods = ['GET'])
def GetBrillo():
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
    print("{}".format(sem_change))
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
    print("{}".format(sem_change))
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
    print("{}".format(sem_change))
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
    print("{}".format(sem_change))
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
    print("{}".format(sem_change))
    return jsonify(jsonExposureAuto)

#POST Methods

@app.route('/SetParameters')
def SetParametros():
#    parameter1 = "Select one parameter you will to modify:\n"
#    parameter2 = "1-Brightness 2-Gamma 3-Gain\n"
#    parameter3 = "Example: /SetParameters/Brightness/20\n"
#    parameter = parameter1 + parameter2 + parameter3
#    return parameter
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

@app.route('/SetParameters/Brightness')
def SetBrightness():
    if failureServer():
        jsonfile.CodeFailureServer['Code'] = 500
        jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
        jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
        jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

        response = make_response(jsonify(jsonFailureServer), 500)
        return response

    jsonfile.CodeRedirection['Parameter'] = 'Brightness'
    jsonfile.CodeRedirection['Code'] = 300
    jsonfile.CodeRedirection['Message'] = "You must choose value within range"
    jsonfile.CodeRedirection['MinValue'] = jsonfile.parameters.brightness.Values['MinValue']
    jsonfile.CodeRedirection['MaxValue'] = jsonfile.parameters.brightness.Values['MaxValue'] 

    jsonRedirection = json.dumps(jsonfile.CodeRedirection)
    jsonRedirection = json.loads(jsonRedirection.replace("\'", '"'))
    response = make_response(jsonify(jsonRedirection), 300)
    return response 

@app.route('/SetParameters/Brightness/<int:num>')
def SetBrightnessNum(num):
    if failureServer():
        jsonfile.CodeFailureServer['Code'] = 500
        jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
        jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
        jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

        response = make_response(jsonify(jsonFailureServer), 500)
        return response

    elif num > jsonfile.parameters.brightness.Values['MinValue'] and num < jsonfile.parameters.brightness.Values['MaxValue']:
        jsonfile.parameters.brightness.Values['CurrentValue'] = num
        SetParametersToDMK("Brightness", num)

        jsonfile.CodeSuccess['Parameter'] = 'Brightness'
        jsonfile.CodeSuccess['Code'] = 200
        jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
        jsonfile.CodeSuccess['Value'] = num

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

@app.route('/SetParameters/Gamma')
def SetGamma():
    if failureServer():
        jsonfile.CodeFailureServer['Code'] = 500
        jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
        jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
        jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

        response = make_response(jsonify(jsonFailureServer), 500)
        return response

    jsonfile.CodeRedirection['Parameter'] = 'Gamma'
    jsonfile.CodeRedirection['Code'] = 300
    jsonfile.CodeRedirection['Message'] = "You must choose value within range"
    jsonfile.CodeRedirection['MinValue'] = jsonfile.parameters.gamma.Values['MinValue']
    jsonfile.CodeRedirection['MaxValue'] = jsonfile.parameters.gamma.Values['MaxValue'] 

    jsonRedirection = json.dumps(jsonfile.CodeRedirection)
    jsonRedirection = json.loads(jsonRedirection.replace("\'", '"'))
    response = make_response(jsonify(jsonRedirection), 300)
    return response  

@app.route('/SetParameters/Gamma/<int:num>')
def SetGammaNum(num):
    if failureServer():
        jsonfile.CodeFailureServer['Code'] = 500
        jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
        jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
        jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

        response = make_response(jsonify(jsonFailureServer), 500)
        return response

    elif num > jsonfile.parameters.gamma.Values['MinValue'] and num < jsonfile.parameters.gamma.Values['MaxValue']:
        jsonfile.parameters.gamma.Values['CurrentValue'] = num
        SetParametersToDMK("Gamma", num)

        jsonfile.CodeSuccess['Parameter'] = 'Gamma'
        jsonfile.CodeSuccess['Code'] = 200
        jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
        jsonfile.CodeSuccess['Value'] = num

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

@app.route('/SetParameters/Gain')
def SetGain():
    if failureServer():
        jsonfile.CodeFailureServer['Code'] = 500
        jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
        jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
        jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

        response = make_response(jsonify(jsonFailureServer), 500)
        return response

    jsonfile.CodeRedirection['Parameter'] = 'Gain'
    jsonfile.CodeRedirection['Code'] = 300
    jsonfile.CodeRedirection['Message'] = "You must choose value within range"
    jsonfile.CodeRedirection['MinValue'] = jsonfile.parameters.gain.Values['MinValue']
    jsonfile.CodeRedirection['MaxValue'] = jsonfile.parameters.gain.Values['MaxValue'] 

    jsonRedirection = json.dumps(jsonfile.CodeRedirection)
    jsonRedirection = json.loads(jsonRedirection.replace("\'", '"'))
    response = make_response(jsonify(jsonRedirection), 300)
    return response      

@app.route('/SetParameters/Gain/<int:num>')
def SetGainNum(num):
    if failureServer():
        jsonfile.CodeFailureServer['Code'] = 500
        jsonfile.CodeFailureServer['Message'] = "CameraNotFound"
        jsonFailureServer = json.dumps(jsonfile.CodeFailureServer)
        jsonFailureServer = json.loads(jsonFailureServer.replace("\'", '"'))

        response = make_response(jsonify(jsonFailureServer), 500)
        return response

    elif num > jsonfile.parameters.gain.Values['MinValue'] and num < jsonfile.parameters.gain.Values['MaxValue']:
        jsonfile.parameters.gain.Values['CurrentValue'] = num
        SetParametersToDMK("Gain", num)              

        jsonfile.CodeSuccess['Parameter'] = 'Gain'
        jsonfile.CodeSuccess['Code'] = 200
        jsonfile.CodeSuccess['Message'] = "Value successfully assigned"
        jsonfile.CodeSuccess['Value'] = num

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
    
if __name__ == "__main__":
    init()
    app.run(debug = True , port = 8080)
