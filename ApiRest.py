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

sys.path.insert(0, 'JsonFile/')
import JsonFile
from JsonFile import JSONFile

sys.path.insert(0, 'Library/')
import library
from library import DMK

dmk = DMK()

jsonfile = JSONFile()

def SetParametersToDMK(name, value):
    dmk.Brightness[0] = jsonfile.parameters.brightness.Values['CurrentValue']
    dmk.Gamma[0] = jsonfile.parameters.gamma.Values['CurrentValue']
    dmk.Gain[0] = jsonfile.parameters.gain.Values['CurrentValue']
    dmk.Exposure[0] = jsonfile.parameters.exposure.Values['CurrentValue']
    dmk.ExposureAuto[0] = jsonfile.parameters.exposureauto.Values['CurrentValue']

    dmk.SetParameters(name, value)

def GetParametersFromDMK():
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
    

def init():
    jsonfile.File['Widget'] = dmk.model
    jsonfile.File['SingleSerial'] = dmk.single_serial
    jsonfile.File['ConnectionType'] = dmk.connection_type

    GetParametersFromDMK()     



app = Flask(__name__, template_folder = '/etc/udev/rules.d/')

@app.route('/')
def JSONFile():
    jsonFile = json.dumps(jsonfile.File)
    jsonFile = json.loads(jsonFile.replace("\'", '"'))
    return jsonify(jsonFile)

@app.route('/TakePicture')
def GetDriver():
    return render_template('80-theimagingsource-cameras.rules')

#GET Methods

@app.route('/GetParameters', methods = ['GET'])
def GetParameters():
    GetParametersFromDMK()
    jsonParameters = json.dumps(jsonfile.parameters.Parameters)
    jsonParameters = json.loads(jsonParameters.replace("\'", '"'))
    return jsonify(jsonParameters)

@app.route('/GetParameters/Brightness', methods = ['GET'])
def GetBrillo():
    GetParametersFromDMK()
    jsonBrightness = json.dumps(jsonfile.parameters.brightness.Brightness)
    jsonBrightness = json.loads(jsonBrightness.replace("\'", '"'))
    return jsonify(jsonBrightness)

@app.route('/GetParameters/Gamma', methods = ['GET'])
def GetGamma():
    GetParametersFromDMK()
    jsonGamma = json.dumps(jsonfile.parameters.gamma.Gamma)
    jsonGamma = json.loads(jsonGamma.replace("\'", '"'))
    return jsonify(jsonGamma)
    
@app.route('/GetParameters/Gain', methods = ['GET'])
def GetGain():
    GetParametersFromDMK()
    jsonGain = json.dumps(jsonfile.parameters.gain.Gain)
    jsonGain = json.loads(jsonGain.replace("\'", '"'))
    return jsonify(jsonGain)

@app.route('/GetParameters/Exposure', methods = ['GET'])
def GetExposure():
    GetParametersFromDMK()
    jsonExposure = json.dumps(jsonfile.parameters.exposure.Exposure)
    jsonExposure = json.loads(jsonExposure.replace("\'", '"'))
    return jsonify(jsonExposure)

@app.route('/GetParameters/ExposureAuto', methods = ['GET'])
def GetExposureAuto():
    GetParametersFromDMK()
    jsonExposureAuto = json.dumps(jsonfile.parameters.exposureauto.ExposureAuto)
    jsonExposureAuto = json.loads(jsonExposureAuto.replace("\'", '"'))
    return jsonify(jsonExposureAuto)

#POST Methods

@app.route('/SetParameters')
def SetParametros():
    parameter1 = "Select one parameter you will to modify:\n"
    parameter2 = "1-Brightness 2-Gamma 3-Gain\n"
    parameter3 = "Example: /SetParameters/Brightness/20\n"
    parameter = parameter1 + parameter2 + parameter3
    return parameter

@app.route('/SetParameters/Brightness')
def SetBrightness():
    return "Select value between {} - {}".format(jsonfile.parameters.brightness.Values['MinValue'], jsonfile.parameters.brightness.Values['MaxValue'])   

@app.route('/SetParameters/Brightness/<int:num>')
def SetBrightnessNum(num):
    if num > jsonfile.parameters.brightness.Values['MinValue'] and num < jsonfile.parameters.brightness.Values['MaxValue']:
        jsonfile.parameters.brightness.Values['CurrentValue'] = num
        SetParametersToDMK("Brightness", num)
        return "Success: Brightness Value assigned to {}".format(num)
    else:
        string = "Fatal error. Value out of range. Select value between {} - {}".format(jsonfile.parameters.brightness.Values['MinValue'], jsonfile.parameters.brightness.Values['MaxValue'])
        return string

@app.route('/SetParameters/Gamma')
def SetGamma():
    return "Select value between {} - {}".format(jsonfile.parameters.gamma.Values['MinValue'], jsonfile.parameters.gamma.Values['MaxValue']) 

@app.route('/SetParameters/Gamma/<int:num>')
def SetGammaNum(num):
    if num > jsonfile.parameters.gamma.Values['MinValue'] and num < jsonfile.parameters.gamma.Values['MaxValue']:
        jsonfile.parameters.gamma.Values['CurrentValue'] = num
        SetParametersToDMK("Gamma", num)
        return "Success: Gamma Value assigned to {}".format(num)
    else:
        string = "Fatal error. Value out of range. Select value between {} - {}".format(jsonfile.parameters.gamma.Values['MinValue'], jsonfile.parameters.gamma.Values['MaxValue'])
        return string

@app.route('/SetParameters/Gain')
def SetGain():
    return "Select value between {} - {}".format(jsonfile.parameters.gain.Values['MinValue'], jsonfile.parameters.gain.Values['MaxValue'])     

@app.route('/SetParameters/Gain/<int:num>')
def SetGainNum(num):
    if num > jsonfile.parameters.gain.Values['MinValue'] and num < jsonfile.parameters.gain.Values['MaxValue']:
        jsonfile.parameters.gain.Values['CurrentValue'] = num
        SetParametersToDMK("Gain", num)              
        return "Success: Gain Value assigned to {}".format(num)
    else:
        string = "Fatal error. Value out of range. Select value between {} - {}".format(jsonfile.parameters.gain.Values['MinValue'], jsonfile.parameters.gain.Values['MaxValue'])
        return string
    
if __name__ == "__main__":
    init()
    app.run(debug = True , port = 8080)
