
import logging
import gst
import time

# preview pipeline
rainbowpre = ( 
"alsasrc device=hw:1 ! audio/x-raw-int,rate=44100 ! queue "
"! faac outputformat=1 profile=1 ! queue "
"! sptsmuxer name=muxer pushbufsize=7 ! queue ! tee name=s "
"! udpsink host=%s port=%s "
"v4l2src hue=-2147483647 contrast=-2147483647 brightness=-2147483647 saturation=-2147483647 ! queue "
"! videoscale ! video/x-raw-yuv,width=720,height=576 ! queue "
"! x264enc byte-stream=true threads=0 key-int-max=50 bitrate=1200 bframes=1 qp-min=1 qp-max=51 qp-step=50 vbv-buf-capacity=300 threads=4 ! queue "
"! muxer. "
"s. ! queue ! udpsink host=127.0.0.1 port=60001"
)

# recorder pipeline
rainbowrec = (
"udpsrc uri=udp://127.0.0.1:60001 ! filesink location=%s"
)

class RainbowRec:
        """
        Rainbow Recoder class.
        """
        def __init__ (self):
                self.logger = logging.getLogger('rainbowrec initializing...')
                self.satus = "ready"
                self.rainbowprepipe = gst.Pipeline ()
                self.rainbowrecpipe = gst.Pipeline ()

        def createprepipe (self, ip, port):
                rainbowprecmd = rainbowpre % (ip, port)
                self.rainbowprepipe = gst.parse_launch (rainbowprecmd)
                self.rainbowprepipe.set_state (gst.STATE_PLAYING)

        def destroypipe (self):
                self.rainbowprepipe.set_state (gst.STATE_NULL)

        def startrec (self):
                recfilename = "/var/www/%s.mpg" % time.strftime ("%Y%m%d_%H%M%S", time.gmtime())
                self.logger.debug ("starting recoding %s" % recfilename)
                rainbowreccmd = rainbowrec % recfilename
                self.rainbowrecpipe = gst.parse_launch (rainbowreccmd)
                self.rainbowrecpipe.set_state (gst.STATE_PLAYING)
                return "ok"

        def stoprec (self):
                self.rainbowrecpipe.set_state (gst.STATE_NULL)
                self.logger.debug ("stop recoder.")
                return "ok"
