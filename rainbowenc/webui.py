import web
import logging
import os
import hashlib
import time
import gettext
import subprocess
import __builtin__

execfile ("/usr/share/rainbowenc/rainbow.conf")
__builtin__.rainbowconf = conf

from rainbowenc import systat, genpage, changepass, recorderctl


web.config.debug = True
urls = (
        '/download', 'DownLoad',
        '/(.*)', 'LogIn',
)
rainbowebui = web.application(urls, globals())

# session
web.config.session_parameters['timeout'] = conf['global']['timeout'] # 5 * 60 seconds
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['expired_message'] = """
        <html><head><meta http-equiv=\"refresh\" content=\"0;url=/\"></head><body></body></html>
        """
session = web.session.Session(rainbowebui, web.session.DiskStore('sessions'), initializer={'login': 0})

# i18n support, template
gettext.install ('messages', '/usr/share/rainbowenc/i18n', unicode=True)
gettext.translation ('messages', '/usr/share/rainbowenc/i18n', languages=['zh_CN']).install(True)
render = web.template.render("/usr/share/rainbowenc/templates", globals={'_':_})

logger = logging.getLogger ("rainbow")

rainbowrec = recorderctl.RainbowRec ()

class DownLoad:
        """
        download, use yield.
        """
        def GET (self):
                 if session.login:
                         filename = web.input ()
                         n = os.stat("/var/www/%s" % filename.name).st_size
                         logger.debug ("download file %s, size %d" % (filename.name, n))
                         web.header ("Accept-Ranges", "bytes")
                         web.header ("Content-Length", n)
                         web.header ("Connection", "close")
                         web.header ("Content-Type", "application/force-download")
                         fd = open ("/var/www/%s" % filename.name, "rb")
                         while (n >= 1024*1024):
                                 if (n >= 1024*1024):
                                         i = 1024*1024
                                         n -= i
                                         yield fd.read (i)
                                 else:
                                         yield fd.read (n)
                                         fd.close ()

class LogIn:
        """
        Web user interface, based on web.py
        """
        def GET (self, name):
                """
                HTTP GET method.
                """
                if not session.login:
                        return render.login()

                header = genpage.get_header()
                headernavbar = genpage.get_headernavbar()
                footer = genpage.get_footer()
                logger.debug ("get %s" % name)

                if name == "" or name == "recorderctl.html":
                        return render.recorderctl(header, headernavbar, footer, web.ctx.ip)

                if name == "" or name == "recordfileman.html":
                        recordfiles = os.listdir (rainbowconf['global']['recorderpath'])
                        return render.recordfileman(header, headernavbar, footer, recordfiles)

                if name == "rainbow.html":
                        osversion = os.uname()[0] + " " + os.uname()[2] + " " + os.uname()[3]
                        uptime = systat.get_uptime()
                        plateform = systat.get_plateform()
                        loadavg = systat.get_loadavg()
                        return render.rainbow(osversion, plateform, uptime, loadavg, header, headernavbar, footer)

                if name == "changepass.html":
                        return render.changepass(header, headernavbar, footer)

                if name == "selectlang.html":
                        return render.selectlang(header, headernavbar, footer)

                if name == "reboot.html":
                        return render.reboot(header, headernavbar, footer)

                if name == "shutdown.html":
                        return render.shutdown(header, headernavbar, footer)

                if name == "logout":
                        rainbowrec.destroypipenow ()
                        logger.info ('logout from %s' % web.ctx.ip)
                        session.login = 0
                        session.kill()
                        raise web.seeother('/')

        def POST (self, name):
                """
                HTTP POST method.
                """
                logger.debug ("post %s" % name)
                if (session.login == 1) and (name == "record"):
                        logger.debug ("record")
                        return rainbowrec.startrec ()

                if (session.login == 1) and (name == "stoprecord"):
                        logger.debug ("stoprecord")
                        return rainbowrec.stoprec ()

                if (session.login == 1) and (name == "recordfileman"):
                        recordfileman = web.input()
                        logger.debug ("remove file %s" % recordfileman.filename)
                        os.remove ("/var/www/%s" % recordfileman.filename)
                        return "success"

                if (session.login == 1) and (name == 'systime'):
                        rainbowrec.gotheartbeat ()
                        return time.ctime()

                if (session.login == 1) and (name == 'uptime'):
                        return systat.get_uptime()

                if (session.login == 1) and (name == 'loadavg'):
                        return systat.get_loadavg()

                if (session.login == 1) and (name == 'memusage'):
                        return systat.get_memusage()

                if (session.login == 1) and (name == 'cpusage'):
                        return systat.get_cpusage()

                if (session.login == 1) and (name == 'selectlang'):
                        selectlang = web.input()
                        gettext.translation ('messages', '/usr/share/rainbowenc/i18n', languages = [selectlang.language]).install(True)
                        render = web.template.render("/usr/share/rainbowenc/templates", globals={'_':_})
                        raise web.seeother('/selectlang.html')
                        

                if (session.login == 1) and (name == 'savepass'):
                        password = web.input()
                        return changepass.savepass(password)

                if (session.login == 1) and (name == 'reboot'):
                        reboot_data = web.input()
                        if (reboot_data.Submit == "Yes"):
                                subprocess.Popen("reboot")
                                return _("Reboot")
                        if (reboot_data.Submit == "No"):
                                raise web.seeother("/")

                if (session.login == 1) and (name == 'shutdown'):
                        reboot_data = web.input()
                        if (reboot_data.Submit == "Yes"):
                                subprocess.Popen("halt")
                                return _("Shutdown")
                        if (reboot_data.Submit == "No"):
                                raise web.seeother("/")

                # authenticate and authorized
                user, passwd = web.input().user, web.input().passwd

                if user != 'admin':
                        return 'Invalid user name'
                if hashlib.md5(passwd).hexdigest() != open('passwd').readline():
                        return 'Invalid password'

                session.login = 1
                rainbowrec.createprepipe (web.ctx.ip, "60000")
                logger.info ('login from %s' % web.ctx.ip)
                raise web.seeother('/rainbow.html')

def startwebui ():
        logger.info ('timeout %d' % conf['global']['timeout'])
        logger.info ('language %s' % conf['global']['language'])
        rainbowebui.run ()
