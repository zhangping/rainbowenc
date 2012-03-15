# -*- coding: utf-8 -*-

from rainbowenc import *

class rainbowenc (Daemon):
        def run (self):
                while True:
                        time.sleep (1)

if __name__ == "__main__":
        service = rainbowenc ('/var/run/rainbow.pid')
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

