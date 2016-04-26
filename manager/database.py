#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from manager.settings import Settings


class DBStorage(object):
    """
    Stores basic information about file that was uploaded
    used in PUT requests
    """
    def __init__(self):
        self.settings = Settings()

    def save(self, name, size, ext, path):
        con = None
        try:
            con = sqlite3.connect(self.settings.SQLITE_DB)
            cur = con.cursor()
            cur.execute("INSERT INTO uploaded_files (name, size, ext, path) "
                        "VALUES ( '%s', '%s', '%s', '%s' );" % (name, size, ext, path,))
            con.commit()
        except sqlite3.Error, e:
            # todo: logger
            # print "Error %s:" % e.args[0]
            pass
        finally:
            if con:
                con.close()
