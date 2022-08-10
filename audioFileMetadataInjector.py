#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 8/10/2022
# The purpose of this object is simply to update the metadata of
# a audio file given the file and the dictionary of the updated metadata
#
#############################

import eyed3

class AudioFileMetaDataInjector(object):

    def __init__(self, data):
        self.metadata = data
        self.metaDataElements = ['year', 'album', 'artist', 'title', 'composer', 'comment']

        self.audioFile = eyed3.load(data['full_file_path'])

    def update_metadata(self):
        for i in self.metaDataElements:
            setattr(self.audioFile.tag, i, self.metadata[i])
        self.audioFile.tag.save()

