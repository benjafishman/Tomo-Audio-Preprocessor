#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 8/10/2022
# The purpose of this object is
# 1. rename the original file with a leading underscore
# 2. create copy of original file
#############################


import shutil
import os


class AudioFileHandler(object):

    def __init__(self):
        '''self.file_path = file_path
        self.copy_file_path = ''
        #print(self.file_path)
'''
    def copy_file_with_new_title(self, src, dst):
        # for now we are assuming the file destination will always be the same directory as the src file
        '''print('here')
        src_directory = os.path.dirname(self.file_path)
        print(f'current dir by init it: {src_directory}')

        print(f'current dir by copy_file is: {src_directory}')

        dst_file = os.path.join(src_directory, new_title)
        print(f'dst dir by copy_file is: {dst_file}')'''

        shutil.copy(src, dst)
        #self.copy_file_path = dst_file

    def rename_org_file(self):
        pass
