# -*- coding: utf-8 -*-

import logging
from rainbowenc.daemon import *
from rainbowenc.webui import *

class rainbowenc (Daemon):
        logger = logging.getLogger ('rainbow')
        def run (self):
                self.logger.info ('rainbowenc started.')
                while True:
                        startwebui ()

if __name__ == "__main__":
        logging.basicConfig(filename='/var/log/rainbow.log',
                format='%(asctime)s - %(module)s.%(funcName)s - %(levelname)s - %(message)s',
                level=logging.DEBUG)
        service = rainbowenc ('/var/run/rainbow.pid')
        #startwebui ()
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

