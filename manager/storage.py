#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import ntpath
import mimetypes
import json
from manager.settings import Settings


class MediaStorage(object):
    """
    MediaStorage provides basic capabilities for working with file system
    """

    def __init__(self, path):
        self.settings = Settings()
        # cut first slash from path
        if path.startswith('/'):
            self.path = path[1:]
        else:
            self.path = path
        self.full_path = os.path.join(self.settings.MEDIA_ROOT, self.path)
        print self.full_path

    def get_file_name(self):
        return ntpath.basename(self.full_path)

    def make_dirs(self):
        """
        Create's new folder is necessary
        """
        d = os.path.dirname(self.full_path)
        if not os.path.exists(d):
            os.makedirs(d)

    def save_file(self, data):
        with open(self.full_path, 'w') as file:
            file.write(data)

    def delete_file(self):
        if os.path.isfile(self.full_path):
            os.remove(self.full_path)

    def is_file(self):
        return os.path.isfile(self.full_path)

    def is_dir(self):
        return os.path.isdir(self.full_path)

    def get_file_type(self):
        """
        Return file extension (with ".")
        """
        filename, file_extension = os.path.splitext(self.full_path)
        return file_extension.lower()

    def validate_file_type(self):
        """
        Check's if file extension is allowed
        """
        return self.get_file_type() in self.settings.MEDIA_ALLOW_EXTENSIONS

    def get_json_structure(self):
        return json.dumps(MediaStorage.path_to_json(self.full_path))

    @staticmethod
    def path_to_json(path):
        """
        Return list files and sub folders in JSON format with all available attributes.
        """
        result = {'name': os.path.basename(path)}
        if os.path.isdir(path):
            result['type'] = "directory"
            result['children'] = [MediaStorage.path_to_json(os.path.join(path, child)) for child in os.listdir(path)]
        else:
            result['type'] = "file"
            result['mimetype'] = MediaStorage.get_file_mimetype(path)
            result['size'] = os.path.getsize(path)
        return result

    @staticmethod
    def get_file_mimetype(path):
        """
        Returns file mimetype
        """
        filename, file_extension = os.path.splitext(path)
        mimetypes.init()
        return mimetypes.types_map[file_extension]