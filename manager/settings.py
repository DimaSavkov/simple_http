#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser

PORT_NUMBER = 8080


class Settings(object):
    """
    Settings parser
    """
    HTTP_PORT_NUMBER = None
    MEDIA_ALLOW_EXTENSIONS = []
    MEDIA_ROOT = ''
    SQLITE_DB = ''
    DAEMON_PID = ''

    def __init__(self):
        try:
            config = ConfigParser.RawConfigParser()
            config.read('settings.ini')
            # media
            allow_extensions = config.get('media', 'allow_extensions')
            self.MEDIA_ALLOW_EXTENSIONS = [ a.strip() for a in allow_extensions.split(',')]
            self.MEDIA_ROOT = config.get('media', 'media_root')
            # database
            self.SQLITE_DB = config.get('database', 'sqlite_db')
            # http server
            self.HTTP_PORT_NUMBER = config.getint('http', 'port')
            # daemon
            self.DAEMON_PID = config.get('daemon', 'pid_file')

            # indicates that ini file was read successfully
            self.valid = True
        except ConfigParser.Error:
            self.valid = False
