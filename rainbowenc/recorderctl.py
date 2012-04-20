
import logging
import gst
import time
import threading

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
                self.rainbowprepipe = gst.Pipeline ()
                self.encoding = 0 # idle 0; encoding 1.
                self.rainbowrecpipe = gst.Pipeline ()
                self.recording = 0 # idle 0; record 1.

        def createprepipe (self, ip, port):
                rainbowprecmd = rainbowpre % (ip, port)
                self.rainbowprepipe = gst.parse_launch (rainbowprecmd)
                self.rainbowprepipe.set_state (gst.STATE_PLAYING)
                self.encoding = 1
                self.timeout = 300
                self.heartbeat = threading.Timer (5, self.destroypipe)
                self.heartbeat.start ()

        # stop real time encoder right now
        def destroypipenow (self):
                self.logger.debug ("destroy pipe right now")
                self.timeout = 0
                self.destroypipe ()

        # stop real time encoder
        def destroypipe (self):
                self.logger.debug ("destroy pipe after %ds" % self.timeout)
                if self.timeout > 5:
                        self.timeout -= 5
                        self.heartbeat = threading.Timer (5, self.destroypipe).start ()
                else:
                        if self.recording == 1:
                                self.stoprec ()
                        self.rainbowprepipe.set_state (gst.STATE_NULL)
                        self.encoding = 0

        def startrec (self):
                recfilename = "/var/www/%s.mpg" % time.strftime ("%Y%m%d_%H%M%S", time.gmtime())
                self.logger.debug ("starting recoding %s" % recfilename)
                rainbowreccmd = rainbowrec % recfilename
                self.rainbowrecpipe = gst.parse_launch (rainbowreccmd)
                self.rainbowrecpipe.set_state (gst.STATE_PLAYING)
                self.recording = 1
                return "ok"

        # stop recoder
        def stoprec (self):
                self.rainbowrecpipe.set_state (gst.STATE_NULL)
                self.recording = 0
                self.logger.debug ("stop recoder.")
                return "ok"

        # got heart beat msg
        def gotheartbeat (self):
                self.logger.debug ("got heart beat msg, reset heart beat timeout")
                self.timeout = 300 # heart beat timeout, reset it.
