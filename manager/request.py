#!/usr/bin/python
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from manager.storage import MediaStorage
from manager.database import DBStorage

# for the welcome page (not included in setting.ini)
TEMPLATES_DIR = os.path.join(os.getcwd(), 'templates')
WELCOME_PAGE = 'welcome.html'


class SimpleHTTP(BaseHTTPRequestHandler):
    """
    Class to handle http requests GET/PUT/DELETE
     * GET request return list files and sub folders in JSON format with all available attributes.
     * PUT request save's file to media files directory
     * DELETE request deletes file from media directory
    """
    def do_GET(self, *args, **kwargs):
        """
        Return list of files in JSON format
        Renders welcome page /index.html
        """
        media = MediaStorage(self.path)
        if self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(os.path.join(TEMPLATES_DIR, WELCOME_PAGE)) as html_page:
                self.wfile.write(html_page.read())
            return
        else:
            if media.is_file() or media.is_dir():
                self.send_response(200)
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                self.wfile.write(media.get_json_structure())
            else:
                self.send_response(404)
                self.end_headers()

    def do_PUT(self):
        """
        Save file to media storage
        Save file info in database
        """
        if self.path and len(self.path) > 1:
            media = MediaStorage(self.path)

            # validate file extension
            if not media.validate_file_type():
                self.send_response(400)
                self.end_headers()
                return

            # read file from request
            length = self.headers['content-length']
            data = self.rfile.read(int(length))

            try:
                # make all necessary directories
                media.make_dirs()
                media.save_file(data)

                db = DBStorage()
                db.save(media.get_file_name(), length, media.get_file_type(), self.path)
                self.send_response(200)
                self.end_headers()
            except IOError:
                self.send_response(400)
                self.end_headers()


    def do_DELETE(self):
        """
        Delete file from file storage
        """
        if self.path and len(self.path) > 1:
            media = MediaStorage(self.path)

            # validate file extension
            if not media.validate_file_type():
                self.send_response(400)
                self.end_headers()
                return

            if not media.is_file():
                self.send_response(404)
                self.end_headers()
                return

            # Delete file
            try:
                media.delete_file()
                self.send_response(200)
                self.end_headers()
            except IOError:
                self.send_response(400)
                self.end_headers()
