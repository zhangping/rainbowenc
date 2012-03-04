#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import time
import hashlib
import atexit
import subprocess
import web
import ConfigParser
import signal
import encoder
import configure
import systat
import genpage
import chpass
import ifconfig
import channel

web.config.debug = False

DEBUG = None

urls = (
    '/(.*)', 'index'
)

app = web.application(urls, globals())

web.config.session_parameters['timeout'] = 300 # 5 * 60 seconds
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['expired_message'] = "<html><head><meta http-equiv=\"refresh\" content=\"0;url=/\"></head><body></body></html>"
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': 0})

render = web.template.render('templates')

encoder_channels = channel.channel()

class rainbow:
    """
    A generic daemon class.
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        #os.chdir("/") #会影响到web.py的templates，因为templates是按照相对路径来查找的
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("Errno 3") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been
        daemonized by start() or restart().
        """
        encoder_channels.onstartup()
        logger = logging.getLogger('rainbow.rainbow')
        logger.debug("rainbow started!")
        app.run()

class index:
    """
    WEB UI, manage channels and encoder
    """
    logger = logging.getLogger('rainbow.rainbow')
    def GET(self, name):
        if not session.login:
            return render.login()

        header = genpage.get_header()
        headernavbar = genpage.get_headernavbar()
        footer = genpage.get_footer()
 
        if name == "" or name == "rainbow.html":
            osversion = os.uname()[0] + " " + os.uname()[2] + " " + os.uname()[3]
            uptime = systat.get_uptime()
            plateform = systat.get_plateform()
            loadavg = systat.get_loadavg()
            return render.rainbow(osversion, plateform, uptime, loadavg, header, headernavbar, footer)

        if name == "" or name == "netstatus.html":
            ifcfg = ifconfig.ifconfig()
            return render.netstatus(header, headernavbar, footer, ifcfg)

        if name == "change_passwd.html":
            return render.change_passwd(header, headernavbar, footer)

        if name == "netconfigure.html":
            netconf_data = configure.read_netconf()
            return render.netconfigure(header, headernavbar, footer, netconf_data)

        if name == "channel.html":
            channel_data = web.input()
            if 'act' in channel_data.keys() and channel_data.act == 'del':
                encoder_channels.stop(channel_data.channel) # stop before remove
                encoder_channels.rmchannel(channel_data.channel)
                raise web.seeother('/channel.html')

            if 'act' in channel_data.keys() and channel_data.act == 'stop':
                encoder_channels.stop(channel_data.channel)
                raise web.seeother('/channel.html')

            if 'act' in channel_data.keys() and channel_data.act == 'start':
                encoder_channels.start(channel_data.channel)
                raise web.seeother('/channel.html')

            channels = encoder_channels.read_channels()
            return render.channel(header, headernavbar, footer, channels)

        if name == "channeladd.html":
            vdevices, adevices = configure.read_free_devices()
            channels = configure.read_channels()
            for i in range(1,10): #found a free channel name when add channel
                channel_name = "Channel" + str(i)
                if not channel_name in channels:
                    break

            return render.channeladd(header, headernavbar, footer, channel_name, vdevices, adevices)

        if name == "channeledit.html":
            vdevices, adevices = configure.read_free_devices()
            channels = configure.read_channels()
            channel_data = web.input()
            channel_name = channel_data.channel_name
            if os.path.exists(channel_data.vdevice) or channel_data.vdevice == 'videotestsrc':
                vdevices.append(channel_data.vdevice)
            if os.path.exists(channel_data.adevice) or channel_data.adevice == 'audiotestsrc':
                adevices.append(channel_data.adevice)

            vdevices.sort()
            adevices.sort()

            return render.channeledit(header, headernavbar, footer, channel_data, vdevices, adevices)

        if name == "encoder.html":
            channels = encoder_channels.read_channels()
            if len(channels)==0:
                raise web.seeother("/nochannels.html")
            tabact = channels[1]
            encoder_data = web.input()
            if 'tabact' in encoder_data.keys():
                for i in range(1, len(channels)+1):
                    if channels[i]['name'] == encoder_data.tabact:
                        tabact = channels[i]

            return render.encoder(header, headernavbar, footer, channels, tabact)

        if name == "overlay.html":
            channels = encoder_channels.read_channels()
            if len(channels)==0:
                raise web.seeother("/nochannels.html")
            tabact = channels[1]
            overlay_data = web.input()
            if 'tabact' in overlay_data.keys():
                for i in range(1, len(channels)+1):
                    if channels[i]['name'] == overlay_data.tabact:
                        tabact = channels[i]

            return render.overlay(header, headernavbar, footer, channels, tabact)

        if name == "" or name == "channelstatus.html":
            channels = encoder_channels.read_channels()
            if len(channels)==0:
                raise web.seeother("/nochannels.html")
            tabact = channels[1]
            channel_data = web.input()
            if 'tabact' in channel_data.keys():
                for i in range(1, len(channels)+1):
                    if channels[i]['name'] == channel_data.tabact:
                        tabact = channels[i]

            return render.channelstatus(header, headernavbar, footer, channels, tabact)

        if name == "nochannels.html":
            return render.nochannels(header, headernavbar, footer)

        if name == "reboot.html":
            return render.reboot(header, headernavbar, footer)

        if name == "shutdown.html":
            return render.shutdown(header, headernavbar, footer)

        if name == "logout":
            session.login = 0
            session.kill()
            raise web.seeother('/')

    def POST(self, name):

        if (session.login == 1) and (name == 'systime'):
            return time.ctime()

        if (session.login == 1) and (name == 'uptime'):
            return systat.get_uptime()

        if (session.login == 1) and (name == 'loadavg'):
            return systat.get_loadavg()

        if (session.login == 1) and (name == 'memusage'):
            return systat.get_memusage()

        if (session.login == 1) and (name == 'cpusage'):
            return systat.get_cpusage()

        if (session.login == 1) and (name == 'save_netconfigure'):
            """
            Save network configure and restart network
            """
            netconf_data = web.input()
            configure.save_netconf(netconf_data)

            os.system('/etc/init.d/networking restart')

            return 'success' 

        if (session.login == 1) and (name == 'save_passwd'):
            passwd_data = web.input()
            return chpass.save_passwd(passwd_data)

        if (session.login == 1) and (name == 'save_channel'):
            channel_data = web.input()

            if 'Cancel' in channel_data.keys():
                raise web.seeother('/channel.html')

            if not ('vdevice' in channel_data.keys()):
                raise web.seeother('/channeladd.html?vdevice=null')

            if not ('adevice' in channel_data.keys()):
                raise web.seeother('/channeladd.html?adevice=null')

            if channel_data.Submit == 'Modi':
                encoder_channels.modichannel(channel_data)
            else:
                encoder_channels.addchannel(channel_data)

            raise web.seeother('/channel.html')

        if (session.login == 1) and (name == 'save_encoder'):
            encoder_data = web.input()
            encoder_channels.modiencoder(encoder_data)
            raise web.seeother("/encoder.html")

        if (session.login == 1) and (name == 'save_overlay'):
            overlay_data = web.input()
            encoder_channels.modioverlay(overlay_data)
            raise web.seeother("/overlay.html")

        if (session.login == 1) and (name == 'reboot'):
            reboot_data = web.input()
            if (reboot_data.Submit == "Yes"):
                subprocess.Popen("reboot")
            if (reboot_data.Submit == "No"):
                raise web.seeother("/")

        if (session.login == 1) and (name == 'shutdown'):
            reboot_data = web.input()
            if (reboot_data.Submit == "Yes"):
                subprocess.Popen("halt")
            if (reboot_data.Submit == "No"):
                raise web.seeother("/")

        if (session.login == 1) and (name == 'nochannels'):
            raise web.seeother("/")

        user, passwd = web.input().user, web.input().passwd
        if user != 'admin':
            return 'Invalid user name'

        if hashlib.md5(passwd).hexdigest() != open("passwd").readline():
            return 'Invalid password'

        session.login = 1
        raise web.seeother('/rainbow.html')

if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/rainbow.log',
                        format='%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    if DEBUG:
        enc_start()
        app.run()
    else:
        service = rainbow('/var/run/rainbow.pid')
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                sys.argv[1] = '8080'
                service.start()
            elif 'stop' == sys.argv[1]:
                service.stop()
            elif 'restart' == sys.argv[1]:
                service.restart()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart" % sys.argv[0]
            sys.exit(2)

