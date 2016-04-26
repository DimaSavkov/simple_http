#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, time, os
from lib.daemon import Daemon
from manager.settings import Settings
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from manager.request import SimpleHTTP
from SocketServer import ThreadingMixIn


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class MyDaemon(Daemon):
    server = None

    def run(self):
        self.server = HTTPServer(('localhost', settings.HTTP_PORT_NUMBER), SimpleHTTP)
        # self.server = ThreadedHTTPServer(('', 8081), SimpleHTTP)
        self.server.serve_forever()


    def stop(self):
        if self.server:
            self.server.socket.close()


if __name__ == "__main__":
    settings = Settings()
    if not settings.valid:
        sys.exit(2)
    daemon = MyDaemon(settings.DAEMON_PID)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)