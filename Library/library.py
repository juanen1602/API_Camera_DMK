import sys
import gi
import time

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GstVideo", "1.0")
gi.require_version('Gdk', '3.0')

from gi.repository import Tcam, Gst, Gdk, Gtk, GObject, GstVideo

sys.path.insert(0, 'Library/CameraVideo/')
import cameravideo
from cameravideo import CameraVideo

class DMK:

    def __init__(self):

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

        self.pipeline = Gst.parse_launch('tcambin name=src ')


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

    def ShowAll(self):
        self.cameravideo.present()
        self.cameravideo.show_all()

        Gdk.threads_enter()
        Gtk.main()
        Gdk.threads_leave()   


         

  
    


