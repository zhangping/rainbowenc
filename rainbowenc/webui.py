import web
import logging
import os
import hashlib

web.config.debug = True
web.config.session_parameters['timeout'] = 300 # 5 * 60 seconds
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['expired_message'] = """
        <html><head><meta http-equiv=\"refresh\" content=\"0;url=/\"></head><body></body></html>
        """

urls = (
        '/(.*)', 'LogIn',
)

rainbowebui = web.application(urls, globals())
session = web.session.Session(rainbowebui, web.session.DiskStore('sessions'), initializer={'login': 0})
render = web.template.render("/usr/share/rainbowenc/templates")

class LogIn:
        """
        Web user interface, based on web.py
        """
        logger = logging.getLogger('rainbow')

        def GET (self, name):
                """
                HTTP GET method.
                """
                self.logger.warning("LogIn:GET")
                if not session.login:
                        self.logger.warning("LogIn:login.html")
                        return render.login()

                if name == "logout":
                        session.login = 0
                        session.kill()
                        raise web.seeother('/')

        def POST (self, name):
                """
                HTTP POST method.
                """

                # authenticate and authorized
                user, passwd = web.input().user, web.input().passwd

                if user != 'admin':
                        return 'Invalid user name'
                if hashlib.md5(passwd).hexdigest() != open("passwd").readline():
                        return 'Invalid password'

                session.login = 1
                raise web.seeother('/rainbow.html')


def startwebui ():
        rainbowebui.run ()
