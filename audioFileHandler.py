#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 8/10/2022
# The purpose of this object is
# 1. rename the original file with a leading underscor
# 2. create copy of original file
# 3. compress file
#############################


import shutil
import os


class AudioFileHandler(object):

    def __init__(self, file_path):
        self.file_path = file_path
        print(self.file_path)

    def copy_file_with_new_title(self, new_title):
        # for now we are assuming the file destination will always be the same directory as the src file
        src_directory = os.path.dirname(self.file_path)
        print(f'current dir by init it: {src_directory}')

        print(f'current dir by copy_file is: {src_directory}')

        dst_file = os.path.join(src_directory, new_title)
        print(f'dst dir by copy_file is: {dst_file}')

        shutil.copy(self.file_path, dst_file)

    def rename_org_file(self):
        pass
