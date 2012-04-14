
import logging
import gst

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
)

# recorder pipeline
rainbowrec = (
"alsasrc device=hw:1 ! audio/x-raw-int,rate=44100 ! queue "
"! faac outputformat=1 profile=1 ! queue "
"! sptsmuxer name=muxer pushbufsize=7 ! queue ! tee name=s "
"! udpsink host=%s port=%s "
"v4l2src hue=-2147483647 contrast=-2147483647 brightness=-2147483647 saturation=-2147483647 ! queue "
"! videoscale ! video/x-raw-yuv,width=720,height=576 ! queue "
"! x264enc byte-stream=true threads=0 key-int-max=50 bitrate=1200 bframes=1 qp-min=1 qp-max=51 qp-step=50 vbv-buf-capacity=300 threads=4 ! queue "
"! muxer. "
"s. ! queue ! filesink location=%s"
)

class RainbowRec:
        """
        Rainbow Recoder class.
        """
        def __init__ (self):
                self.logger = logging.getLogger('rainbowrec initializing...')
                self.satus = "ready"
                self.rainbowprepipe = gst.Pipeline ()

        def createprepipe (self, ip, port):
                rainbowprecmd = rainbowpre % (ip, port)
                self.rainbowprepipe = gst.parse_launch (rainbowprecmd)
                self.rainbowprepipe.set_state (gst.STATE_PLAYING)

        def destroypipe (self):
                self.rainbowprepipe.set_state (gst.STATE_NULL)

        def startrec (self):
                self.logger.debug ("starting recoder...")
                self.rainbowrec_pipeline.set_state (gst.STATE_PLAYING)
                self.logger.debug ("start recoder, done.")

        def stoprec (self):
                self.logger.debug ("stoping recoder...")
                self.rainbowrec_cmd.set_state (gst.STATE_NULL)
                self.logger.debug ("stop recoder, done.")
