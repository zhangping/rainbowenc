ch = [
(
"alsasrc device=%s" # alsa audio device
" ! audio/x-raw-int,rate=44100" # sample rate
" ! queue ! " 
"faac outputformat=1 profile=1 ! queue ! " 
"sptsmuxer name=muxer pushbufsize=7" # ts packets per udp packet
" ! queue ! " 
"udpsink host=%s" # destination ip adress
" port=%s " # destination port
"v4l2src hue=%s" # hue 
" contrast=%s" # contrast
" brightness=%s" # brightness
" saturation=%s" # saturation
" ! queue ! " 
"videoscale ! video/x-raw-yuv,width=720,height=576" #
" ! queue ! " 
"x264enc byte-stream=true threads=4" # threads number
" key-int-max=50"
" bitrate=1200" # bitrate
" bframes=1 qp-min=1 qp-max=51 qp-step=50 vbv-buf-capacity=300 ! queue ! muxer." 
)
]
