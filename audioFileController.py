#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 7/31/2022

import re
import json
import subprocess
import os


class AudioFileMetaDataController(object):
    metadata = {'orgFileName': "",
                'fullFilePathName': "",
                'base': "",
                'title': "",
                'album': "",
                'year': "",
                'artist': "",
                'comment': "",
                'composer': "",
                'albumArtFilePath': "", }

    list_of_parshas = ['Bereishis',
                       'Noach',
                       'Lech Lecha',
                       'Vayeira',
                       'Chayei Sarah',
                       'Toldos',
                       'Vayeitzei',
                       'Vayishlach',
                       'Vayeishev',
                       'Miketz',
                       'Vayigash',
                       'Vayechi', ]


    def __init__(self, data):
        self.metadata['fullFilePath'] = data['Browse']
        self.metadata['base'] = os.path.basename(data['Browse'])
        self.metadata['album'] = data['album']
        self.metadata['artist'] = data['artist']
        self.metadata['year'] = data['year']
        self.metadata['comment'] = data['comment']
        self.metadata['composer'] = data['composer']
        self.metadata['albumArtFilePath'] = data['albumArtFilePath']
        self.metadata['title'] = data['title']

        # self.updateFileAndTitle(self)


    def createTitleTag(self, f):
        # replace dashes with spaces remove apostophes
        # caret is an exclusionary symbol s
        # so this means take anything that is not a lower case or uppercase letter or numeric or .
        # or new line and replace with a space (this will backfire if there are any other special chars like ! or $)
        # TODO: take the above problem into account

        self.title = re.sub('[^a-zA-Z0-9 \n\.]', ' ', f)


    def createFileName(self, f):
        # take file title and replace all spaces with dashes
        self.base = re.sub('[ ]', '-', f)


    def updateFileAndTitle(self):
        shiur_with_series = ['gemara', 'shiur klali', 'vaadim']

        shiur_with_year_in_end_of_title = ['halacha shiur', 'shiur klali', 'vaadim']

        if self.metadata['base']:
            # file has filename but needs title tag so we
            # create new filename by removing the initial underscore
            # create a title tag by replacing all dashes/apostophes with spaces
            self.createTitleTag(self.base[1:])  # hacky way to ignore the underscore
        else:
            # user has defined a title tag to use for filename aswell
            self.createFileName(self.metadata['title'])

            # add number sign to series and remove any zero that precedes a number
            if self.album in shiur_with_series:
                re.sub('[0]', '#', n, count=1)  # replace first 0 with a #
            elif self.album == 'mishnayos':
                print("TODO add comma between perek and mishma")
            elif self.album in shiur_with_year_in_end_of_title:
                self.title += '_' + self.year
            '''elif self.album == 'parsha':
                                        # assumption if given title the first word is te name of the parsha
                                        # or if given file name the first word until the dash is the parsha
                                        print('TODO: parsha name and year at beginning of file name but in title at end in parantheses!')
                                        tl = self.base.split('-')
                                        #update title and file name
                                        self.base = tl[0] + '''

    def getMetadataAsJson(self):
        #print("hello world")
        print(self.metadata['base'])

        return json.dumps(self.metadata, indent=4)



test_data = {'year': '2022', 'album': 'Bava Metziah', 'artist': 'Moshe Meiselman',
             'fileName': True, 'title': False,
             'Browse': 'C:/Users/Ben/Desktop/TomoDev/tomo dev/tomo dev/_Bava-Metzia-Shiur-154.mp3',
             'title0': '',
             'comment': 'Yeshivas Toras Moshe | Ner Michoel Alumni Association',
             'composer': 'NerMichoel.org',
             'albumArtFilePath': ''}

m = AudioFileMetaDataController(test_data)

print(m.getMetadataAsJson())
