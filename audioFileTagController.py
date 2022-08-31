#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 8/10/2022
# The purpose of this object is simply to update the metadata of
# a audio file given the file and the dictionary of the updated metadata
#
############################
import music_tag


class AudioFileTagController(object):

    def __init__(self, data):
        self.data = data
        self.metaDataElements = ['year', 'album', 'artist', 'title', 'composer', 'comment']
        self.audioFile = music_tag.load_file(self.data["dst_file_info"]['path'])

    def update_metadata(self):
        for i in self.metaDataElements:
            self.audioFile[i] = self.data["metadata"][i]
        # set album art
        with open(self.data["metadata"]["album_art_file_path"], 'rb') as img_in:
            self.audioFile['artwork'] = img_in.read()
        self.audioFile.save()


