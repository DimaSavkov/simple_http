#!/usr/bin/python
# -*- coding: utf-8 -*-
from manager.settings import Settings
from BaseHTTPServer import HTTPServer
from manager.request import SimpleHTTP

if __name__ == "__main__":
    settings = Settings()
    server = None
    try:
        print 'starting web server ... '
        server = HTTPServer(('', settings.HTTP_PORT_NUMBER), SimpleHTTP)
        server.serve_forever()

    except KeyboardInterrupt:
        print 'stopping web server ... '
        server.socket.close()
