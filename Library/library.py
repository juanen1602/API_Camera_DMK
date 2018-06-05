import sys
import gi
import time

import threading

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
gi.require_version('Gdk', '3.0')

from gi.repository import Tcam, Gst, Gdk, Gtk, GObject, GstVideo, Gio, GLib

sys.path.insert(0, 'Library/CameraVideo/')
import cameravideo
from cameravideo import CameraVideo

sys.path.insert(0, 'Library/Picture/')
import picture
from picture import Picture 

import datetime

class DMK(Gtk.ApplicationWindow):

    def __init__(self):

        super().__init__()
        self.hb = Gtk.HeaderBar()
        self.source = None

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

        self.CameraNotFound = False

        self.namePicture = None

        self.picture = None

#        self.state = list()

        self.listrequest = list()

        self.currenttask = 0
        self.n_request = 0
        self.n_erase = 0

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

        self.cameravideo = CameraVideo()

        self.pipeline = Gst.parse_launch('tcambin name=src ! queue max_size_buffers=2 ! videoconvert ! capsfilter caps="video/x-raw,format=BGRx" ! videoconvert ! gtksink name=sink')

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

        return device_list[selection]

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


    def GetParameters(self):
        self.GetInnerParameters(self.source)

    def SetParameters(self, name, value):
#        tcam = self.pipeline.get_by_name("src")
#        if tcam is None:
#            print("No source element")
#            return
#        return_value = tcam.set_tcam_property(name,
#                                              GObject.Value(int,
#                                                            int(slider.get_value())))
        return_value = self.source.set_tcam_property(name, value)
        print(return_value)

    def ShowAll(self):
        self.cameravideo.present()
        self.cameravideo.show_all()

        Gdk.threads_enter()
        Gtk.main()
        Gdk.threads_leave()

    def TakePicture(self, name): 
        print("TakingPicture")       
        self.picture = Picture(name)

    def on_eos(self, bus, msg):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                                   "Video stream has ended")
        dialog.format_secondary_text("The video capture device got disconnected")
        dialog.run()
        self.close()

    def DoList(self, timeexposure):
        self.n_request+=1
        self.listrequest.append([self.n_request, timeexposure, "Ready"])

    def DoTask(self):
        while True:
            if (self.n_request - self.n_erase > 0):
                self.listrequest[0][2] = "Running"
                time.sleep(self.listrequest[0][1])
                self.TakePicture(str(self.listrequest[0][0]))
                del self.listrequest[0]
                self.n_erase+=1

    def Task(self, texposicion):
        time.sleep(tiempoexposicion)
        self.state[0] = "Done"
            

         

  
    


