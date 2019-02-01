import sys

import gi

# the two lines import the tcam introspection
gi.require_version("Tcam", "0.1")
from gi.repository import Tcam

gi.require_version("Gst", "1.0")
#gi.require_version("Gtk", "3.0")

from gi.repository import Gst, Gio, GObject, GLib #Gtk

class Picture():
    def __init__(self, name):
        Gst.init(sys.argv)

        self.filename = name

        self.pipeline = self.create_pipeline()
        self.start_pipeline(self.pipeline)
        self.save_image(self.pipeline, self.filename)
        self.close()        


    def create_pipeline(self):
        """Build the video capture and display pipeline."""

        # Here the video capture pipeline gets created. Elements that are
        # referenced in other places in the application are given a name, so
        # that they could later be retrieved.
        #
        # The pipeline consists of the following elements:
        #
        # tcambin: This is the main capture element that handles all basic
        #   operations needed to capture video images from The Imaging Source
        #   cameras.
        #
        # queue: The queue is a FIFO buffer element. It is set to a capacity of
        #   2 buffers at maximum to prevent it from filling up indifinitely
        #   should the camera produce video frames faster than the host computer
        #   can handle. The creates a new thread on the downstream side of the
        #   pipeline so that all elements coming after the queue operate in
        #   separate thread.
        #
        # videoconvert: This element converts the videoformat coming from the
        #   camera to match the specification given by the "capsfilter" element
        #   that comes next in the pipeline
        #
        # capsfilter: This element specifies the video format. This example just
        #   specifies a BGRx pixel format which means that we just want a color
        #   image format without any preferences on width, height or framerate.
        #   The tcambin will automatically select the biggest image size
        #   supported by the device and sets the maximum frame rate allowed for
        #   this format. If the camera only supports monochrome formats they get
        #   converted to BGRx by the preceeding 'videoconvert' element.
        #
        # videoconvert: The second videoconvert element in the pipeline converts
        #   the BGRx format to a format understood by the video display element.
        #   Since the gtksink should natively support BGRx, the videoconvert
        #   element will just pass the buffers through without touching them.
        #
        # gtksink: This element displays the incoming video buffers. It also
        #   stores a reference to the last buffer at any time so it could be
        #   saved as a still image
        pipeline = Gst.parse_launch(
            'tcambin name=src ! queue max_size_buffers=2 ! videoconvert ! capsfilter caps="video/x-raw,format=BGRx" ! videoconvert ! gtksink name=sink')

        # Enable the "last-sample" support in the sink. This way the last buffer
        # seen by the display element could be retrieved when saving a still
        # image is requested

        sink = pipeline.get_by_name("sink")
        sink.set_property("enable-last-sample", True)
#        sample = sink.get_property("last-sample")

        return pipeline


    def start_pipeline(self, pipeline):
        pipeline.set_state(Gst.State.PLAYING)

        src = pipeline.get_by_name("src")

#        sink = pipeline.get_by_name("sink")
#        sample = sink.get_property("last-sample")
        if pipeline.get_state(10 * Gst.SECOND)[0] != Gst.StateChangeReturn.SUCCESS:
            serial = src.get_property("serial")
            print("Error al hacer la foto")

        else:
            serial = src.get_property("serial")

        return False


    def save_image(self, pipeline, name):
        """
        This callback function gets called when the "Save" button gets clicked.

        To save an image file, this function first gets the last video buffer
        from the display sink element. The element needs to have the
        "enable-last-buffer" set to "true" to make this functionality work.

        Then a new GStreamer pipeline is created that encodes the buffer to JPEG
        format and saves the result to a new file.
        """

        sink = pipeline.get_by_name("sink")
        sample = sink.get_property("last-sample")

        filename = "/tmp/"
        filename += name
        if not filename.endswith(".jpg"):
            filename += ".jpg"

        buffer = sample.get_buffer()
        pipeline = Gst.parse_launch("appsrc name=src ! videoconvert ! jpegenc ! filesink location=%s" % filename)
        src = pipeline.get_by_name("src")
        src.set_property("caps", sample.get_caps())
        pipeline.set_state(Gst.State.PLAYING)
        src.emit("push-buffer", buffer)
        src.emit("end-of-stream")
        pipeline.get_state(Gst.CLOCK_TIME_NONE)
        pipeline.set_state(Gst.State.NULL)
        pipeline.get_state(Gst.CLOCK_TIME_NONE)


    def close(self):
        self.pipeline.set_state(Gst.State.NULL)

