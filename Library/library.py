import sys
import gi
import time

import threading
from threading import Thread
from threading import Lock

import os
import signal

import sqlite3



gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
gi.require_version('Gdk', '3.0')

from gi.repository import Tcam, Gst, Gdk, Gtk, GObject, GstVideo, Gio, GLib


sys.path.insert(0, 'Library/Picture/')
import picture
from picture import Picture 

import datetime

max_request = 10000

lockVideo = Lock()

class DMK(Gtk.ApplicationWindow):

	def __init__(self):

		super().__init__()
		self.hb = Gtk.HeaderBar()
		self.source = None
		
		self.serialNumber = None

		self.model = None
		self.single_serial = None
		self.connection_type = None

		self.cameravideo = None

		self.pipeline = None

        #Value, #MinValue, #MaxValue, #DefaultValue, #Category, #Group
		self.Brightness = [None, None, None, None, None, None]
		self.Gamma = [None, None, None, None, None, None]
		self.Gain = [None, None, None, None, None, None]
		self.ExposureAuto = [None, None, None, None]
		self.Exposure = [None, None, None, None, None, None]
		self.Saturation = [None, None, None, None, None, None]
		self.Hue = [None, None, None, None, None, None]
		self.WhiteBalanceRed = [None, None, None, None, None, None]
		self.WhiteBalanceBlue = [None, None, None, None, None, None]

		self.CameraNotFound = False

		self.namePicture = None

		self.picture = None
		
		self.video = None
		
		self.n_ips = 0
		self.onstream = False

		self.listrequest = list()
		
		self.dataBase = sqlite3.connect('DataBase/database.db')
		self.cursor = self.dataBase.cursor()
		
		self.dataBase1 = None
		self.cursor1 = None
		
		self.dataBase2 = None
		self.cursor2 = None
		
		self.dataBase3 = None
		self.cursor3 = None
		
		self.dataBase4 = None
		self.cursor4 = None
		
		self.dataBase5 = None
		self.cursor5 = None
		
		self.dataBase6 = None
		self.cursor6 = None

#		This command must be uncommented untill the API is set.
#		Otherwise the table block the complete system.
		
		self.cursor.execute('''
		DROP TABLE IF EXISTS Pictures
		''')
		
		creationString = '''
		CREATE TABLE IF NOT EXISTS Pictures (
		id INTEGER,
		subid INTEGER,
		state VARCHAR(10),
		tag1 VARCHAR(30),
		tag2 VARCHAR(30),
		tag3 VARCHAR(30),
		tag4 VARCHAR(30),
		tag5 VARCHAR(30),
		name DATETIME,
		user VARCHAR(40))
		'''
		
		if(self.cursor.execute(creationString)):
			print("DataBase created successfully")
		else:
			print("Error")
		
		self.dataBase.close()
		
		self.dataBase = None
		self.cursor = None	

		self.currenttask = 1
		self.n_request = 0
		self.n_erase = 0
		
		self.pidVideo = None

		self.init()

	def init(self):

		Gst.init(sys.argv)  # init gstreamer
		Gtk.init(sys.argv)

		self.source = Gst.ElementFactory.make("tcambin")

		serial = None
		serials = self.source.get_device_serials()

		if len(serials) <= 0:
			self.CameraNotFound = True     

		for single_serial in serials:

			(return_value, model,
			identifier, connection_type) = self.source.get_device_info(single_serial)

			if return_value:

				print("Model: {} Serial: {} Type: {}".format(model,
                                                             single_serial,
                                                             connection_type))

				self.model = model
				self.single_serial = single_serial
				self.connection_type = connection_type

				if serial is None:
					serial = self.select_camera(self.source)

				if serial is not None:
					self.source.set_property("serial", serial)

					self.GetInnerParameters(self.source)

		self.pipeline = Gst.parse_launch('''tcambin name=src ! 
		queue max_size_buffers=2 ! videoconvert ! 
		capsfilter caps="video/x-raw,format=BGRx" ! 
		videoconvert ! gtksink name=sink''')

		sink = self.pipeline.get_by_name("sink")
		sink.set_property("enable-last-sample", True)
		sample = sink.get_property("last-sample")

		src = self.pipeline.get_by_name("src")       

		display_widget = self.pipeline.get_by_name("sink").get_property("widget")
		self.add(display_widget)
		self.hb.show_all()
		display_widget.show()

		if serial:
			src.set_property("serial", serial)

		src.set_state(Gst.State.READY)

		bus = self.pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect("message::eos", self.on_eos)


	def select_camera(self, source):

		# retrieve all available serial numbers
		serials = source.get_device_serials()

		# create a list to have an easy index <-> serial association
		device_list = []
		# we add None to have a default value for the case 'serial not defined'
		# this also pushes our first serial index to 1.
		device_list.append(None)

		print("Available devices:")
		index = 1
		print("0 - Use default device")

		for s in serials:

			device_list.append(s)
			print("{} - {}".format(index, s))
			index = index + 1

		# get input from user and only stop asking when
		# input is legal
		legal_input = False
		while not legal_input:
			selection = int(input("Please select a device: "))
			if 0 <= selection < len(device_list):
				legal_input = True
			else:
				print("Please select a legal device.")

		self.serialNumber = device_list[selection]

		return device_list[selection]
		
		
	def GetAmountParameters(self, source):	
		property_names = source.get_tcam_property_names()
#		print(property_names)
		return property_names
		
				
	def GetListParameters(self):
		property_names = self.GetAmountParameters(self.source)
#		print(property_names)
		return property_names
		

	def GetInnerParameters(self, source):
		property_names = source.get_tcam_property_names()
		for name in property_names:
			(ret, value,
             min_value, max_value,
             default_value, step_size,
             value_type, flags,
             category, group) = source.get_tcam_property(name)

			if name == "Brightness":
				self.Brightness[0] = value
				self.Brightness[1] = min_value
				self.Brightness[2] = max_value
				self.Brightness[3] = default_value
				self.Brightness[4] = category
				self.Brightness[5] = group

			if name == "Gamma":
				self.Gamma[0] = value
				self.Gamma[1] = min_value
				self.Gamma[2] = max_value
				self.Gamma[3] = default_value
				self.Gamma[4] = category
				self.Gamma[5] = group

			if name == "Gain":
				self.Gain[0] = value
				self.Gain[1] = min_value
				self.Gain[2] = max_value
				self.Gain[3] = default_value
				self.Gain[4] = category
				self.Gain[5] = group

			if name == "Exposure Auto":
				self.ExposureAuto[0] = value
				self.ExposureAuto[1] = default_value
				self.ExposureAuto[2] = category
				self.ExposureAuto[3] = group

			if name == "Exposure":
				self.Exposure[0] = value
				self.Exposure[1] = min_value
				self.Exposure[2] = max_value
				self.Exposure[3] = default_value
				self.Exposure[4] = category
				self.Exposure[5] = group
				
			if name == "Saturation":
				self.Saturation[0] = value
				self.Saturation[1] = min_value
				self.Saturation[2] = max_value
				self.Saturation[3] = default_value
				self.Saturation[4] = category
				self.Saturation[5] = group
				
			if name == "Hue":
				self.Hue[0] = value
				self.Hue[1] = min_value
				self.Hue[2] = max_value
				self.Hue[3] = default_value
				self.Hue[4] = category
				self.Hue[5] = group
				
			if name == "Whitebalance Red":
				self.WhiteBalanceRed[0] = value
				self.WhiteBalanceRed[1] = min_value
				self.WhiteBalanceRed[2] = max_value
				self.WhiteBalanceRed[3] = default_value
				self.WhiteBalanceRed[4] = category
				self.WhiteBalanceRed[5] = group
				
			if name == "Whitebalance Blue":
				self.WhiteBalanceBlue[0] = value
				self.WhiteBalanceBlue[1] = min_value
				self.WhiteBalanceBlue[2] = max_value
				self.WhiteBalanceBlue[3] = default_value
				self.WhiteBalanceBlue[4] = category
				self.WhiteBalanceBlue[5] = group			


	def GetParameters(self):
		self.GetInnerParameters(self.source)

	def SetParameters(self, name, value):
		return_value = self.source.set_tcam_property(name, value)

	def ShowAll(self):
		self.cameravideo.present()
		self.cameravideo.show_all()

		Gdk.threads_enter()
		Gtk.main()
		Gdk.threads_leave()

	def TakePicture(self, name): 
		print("TakingPicture")       
		self.picture = Picture(name)
		
	def TakePicture2(self, name):
		commandline = 'sudo fswebcam '
		deppendencyline = '-d /dev/video0 -r 640x480 --jpeg 85 '
		name += '.jpg'
		completeline = commandline + deppendencyline + name
		
		print("TakingPicture2")
		os.popen(completeline).readlines()
		
		os.popen('sudo mv ' + name + ' /tmp/').readline()
		
	def Streaming(self):
		self.video = Picture('Streaming')


	def VideoStreaming(self):
		while self.onstream == True:

			self.Streaming()
			time.sleep(1)
			self.n_ips+=1
			print(self.n_ips)
			
	def Streaming2(self):
		lockVideo.acquire()
		
		sudo = 'sudo'
		command = 'gst-launch-1.0'
		tCamBin = 'tcambin'
		videoRate = 'videorate'
		videoXRaw = '"video/x-raw,framerate=2/1"'
		videoConvert = 'videoconvert'
		xImageSink = 'ximagesink'
		jPegEnc = 'jpegenc'
		multiFileSink = 'multifilesink location=/tmp/video.jpg'
		
		completeLine = sudo + ' '
		completeLine += command + ' '
		completeLine += tCamBin + ' ! '
		completeLine += videoConvert + ' ! '
		completeLine += jPegEnc + ' ! '
		completeLine += multiFileSink
		
		lockVideo.release()
		pid = os.popen(completeLine).readlines()
			
			
	def VideoStreaming2(self):
		os.popen('killall gst-launch-1.0')
		
		thOn = Thread(target = self.Streaming2)
		thOn.start()
		
		lockVideo.acquire()

		pid = os.popen('ps -C gst-launch-1.0 -o pid').readlines()
		n = 0

		lockVideo.release()
		if len(pid) == 2:
			self.pidVideo = int(pid[1])
			return self.pidVideo
			
		else:
			return "ERROR"		

				
	def VideoStreamingOff2(self):
		os.popen('sudo killall gst-launch-1.0')		
		

	def on_eos(self, bus, msg):
		self.close()

	def DoList(self, jsonFile, mutex):
		mutex.acquire()
		self.dataBase1 = sqlite3.connect('DataBase/database.db')
		self.cursor1 = self.dataBase1.cursor()	
		
		self.n_request+=1
		n_subrequest = int(jsonFile['Amount'])

		for i in range(n_subrequest):
			name = 'image_' + str(self.n_request) + '_' + str(i).zfill(6)

			element = list()
			element.append(self.n_request)
			element.append(i)
			element.append("Pending")

			if(len(jsonFile['Tags']) == 1):
				element.append(jsonFile['Tags'][0])
				element.append("None")
				element.append("None")
				element.append("None")
				element.append("None")
			if(len(jsonFile['Tags']) == 2):
				element.append(jsonFile['Tags'][0])
				element.append(jsonFile['Tags'][1])
				element.append("None")
				element.append("None")
				element.append("None")
			if(len(jsonFile['Tags']) == 3):
				element.append(jsonFile['Tags'][0])
				element.append(jsonFile['Tags'][1])
				element.append(jsonFile['Tags'][2])
				element.append("None")
				element.append("None")
			if(len(jsonFile['Tags']) == 4):
				element.append(jsonFile['Tags'][0])
				element.append(jsonFile['Tags'][1])
				element.append(jsonFile['Tags'][2])
				element.append(jsonFile['Tags'][3])
				element.append("None")
			if(len(jsonFile['Tags']) == 5):
				element.append(jsonFile['Tags'][0])
				element.append(jsonFile['Tags'][1])
				element.append(jsonFile['Tags'][2])
				element.append(jsonFile['Tags'][3])
				element.append(jsonFile['Tags'][4])
				
			element.append(name)
			element.append(jsonFile['Author'])

			tupelement = tuple(element)

			insert = '''
			INSERT INTO Pictures
			VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
			'''
			self.cursor1.execute(insert, tupelement)
				

		self.dataBase1.commit()

		self.dataBase1.close()
		
		request = list()
		request.append(self.n_request)
		request.append(n_subrequest)
		
		self.listrequest.append(request)
		
		mutex.release()	
		
	
	def BurstPhotos(self, ID):

		tcambin = 'gst-launch-1.0 tcambin'
		videorate = 'videorate'
		videoxraw = '"video/x-raw,framerate=2/1"'
		videoconvert = 'videoconvert'
		jpegenc = 'jpegenc'
		multifilesink = 'multifilesink'
		folderfile = '/tmp/'
		namefile = 'image_' + str(ID) + '_%06d.jpg'
		location = 'location=' + folderfile + namefile
		
		completeCommand = tcambin + ' ! '
		
		if self.Exposure[0] < 500000:
			completeCommand += videorate + ' ! '
			completeCommand += videoxraw + ' ! '
			
		completeCommand += videoconvert + ' ! '
		completeCommand += jpegenc + ' ! '
		completeCommand += multifilesink + ' ' + location
		
		os.popen(completeCommand).readlines()
		
		

	def DoTask(self):
		self.dataBase2 = sqlite3.connect('DataBase/database.db')
		self.cursor2 = self.dataBase2.cursor()

		while True:
			if len(self.listrequest) > 0 and self.listrequest[0][0] == self.currenttask:
				ID = self.listrequest[0][0]
				amount = self.listrequest[0][1]
				value = (ID,)
				self.cursor2.execute('''
				SELECT * FROM Pictures WHERE id=?
				''', value)
				amount2 = len(self.cursor2.fetchall())

				self.cursor2.execute('''
				UPDATE Pictures SET state='Running' WHERE id=?
				''', value)
					
				self.dataBase2.commit()					
				
				th1 = Thread(target = self.BurstPhotos, args = (ID,))
				th1.start()
				
				folderfile = '/tmp/'
				namefile = 'image_' + str(self.currenttask) + '_' + str(amount-1).zfill(6) + '.jpg'
				completenamefile = folderfile + namefile
				checkingFile = os.path.isfile(completenamefile)
				while checkingFile == False:
					time.sleep(0.25)
					checkingFile = os.path.isfile(completenamefile)
					
				os.popen('killall gst-launch-1.0')

				self.cursor2.execute('''
				UPDATE Pictures SET state='Done' WHERE id=?
				''', value)				
					
				self.dataBase2.commit()					
					
				time.sleep(30)	
				self.currenttask += 1
				del(self.listrequest[0])
					
			else:
				time.sleep(5)


	def Task(self, ID):
		self.dataBase3 = sqlite3.connect('DataBase/database.db')
		self.cursor3 = self.dataBase3.cursor()
		
		value = (ID,)
		self.cursor3.execute('''
		SELECT * FROM Pictures WHERE id=?
		''', value)

		members = self.cursor3.fetchall()
		state = members[0][2]
		numberMembers = len(members)
		
		nameMembers = list()
		
		for i in range(numberMembers):
			name = members[i][8]
			nameMembers.append(name)
		
		data = list()
		data.append(ID)
		data.append(state)
		data.append(numberMembers)
		data.append(nameMembers)
		
		self.dataBase3.close()
		
		return data

		
	def CheckIDAmount(self, ID):
		self.dataBase4 = sqlite3.connect('DataBase/database.db')
		self.cursor4 = self.dataBase4.cursor()
		
		value = (ID,)
		self.cursor4.execute('''
		SELECT * FROM Pictures WHERE id=?
		''', value)
		
		members = self.cursor4.fetchall()
		amount = len(members)
		
		return amount

		
	def ReturnNameID(self, ID, subID):
		self.dataBase5 = sqlite3.connect('DataBase/database.db')
		self.cursor5 = self.dataBase5.cursor()
		
		value = (ID,)
		self.cursor5.execute('''
		SELECT * FROM Pictures WHERE id=?
		''', value)
		
		members = self.cursor5.fetchall()
		
		name = members[subID-1][8]
		return name
		
		
	def deletePicture(self, name):		
		self.dataBase6 = sqlite3.connect('DataBase/database.db')
		self.cursor6 = self.dataBase6.cursor()
		
		self.cursor6.execute('''
		SELECT * FROM Pictures
		''')
		
		completeName = None
		member = None
		
		members = self.cursor6.fetchall()
		
		n = 0
		for i in members:
			completeName = '/tmp/' + i[8] + '.jpg'
			
			if name == completeName:
				member = i
				n += 1
		
		if n == 0:

			return False
		
		value = (member[0], member[1])

		self.cursor6.execute('''
		UPDATE Pictures SET state='Deleted' WHERE (id,subid)=(?,?)
		''',value)
		
		commandline = 'sudo rm '
		
		completeline = commandline + name
		
		os.popen(completeline).readlines()
		
		return True					
		

	def FindCamera(self):
		serials = self.source.get_device_serials()        
    
		if len(serials) <= 0:
			self.CameraNotFound = True
		else:
			self.CameraNotFound = False


  



