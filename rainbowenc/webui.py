import web
import logging
import os
import hashlib
import time
import gettext
import subprocess

from rainbowenc import systat, genpage, changepass

execfile ("/usr/share/rainbowenc/rainbow.conf")

web.config.debug = True
urls = (
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

                if name == "" or name == "rainbow.html":
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
                        logger.info ('logout from %s' % web.ctx.ip)
                        session.login = 0
                        session.kill()
                        raise web.seeother('/')

        def POST (self, name):
                """
                HTTP POST method.
                """

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
                logger.info ('login from %s' % web.ctx.ip)
                raise web.seeother('/rainbow.html')


def startwebui ():
        logger.info ('timeout %d' % conf['global']['timeout'])
        logger.info ('language %s' % conf['global']['language'])
        rainbowebui.run ()
