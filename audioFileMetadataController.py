#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 7/31/2022

import re
import os


class AudioFileMetaDataController(object):
    metadata = {
        'full_file_path': "",
        'base': "",
        'album': "",
        'year': "",
        'artist': "",
        'comment': "",
        'composer': "",
        'album_art_file_path': "",
        "title": "",
        "is_series": False,
        "heb_year": "",
    }

    def __init__(self, data):
        self.metadata['full_file_path'] = data['full_file_path']
        self.metadata['base'] = os.path.basename(data['full_file_path'])
        self.metadata['album'] = data['album']
        self.metadata['artist'] = data['artist']
        self.metadata['year'] = data['year']
        self.metadata['comment'] = data['comments']
        self.metadata['composer'] = data['composer']
        self.metadata['heb_year'] = data['heb_year']
        self.metadata['album_art_file_path'] = data['album_art_file_path']
        if data['is_series']:
            self.metadata['is_series'] = True
        if data['input_title']:
            self.metadata['input_title'] = data['input_title']
            self.metadata['title'] = data['input_title']  # slight duplication of data but i think it's justified

        self.has_file_name = False
        if data['from_file_name']:
            self.has_file_name = True

    def createTitleTag(self, f):
        # replace dashes with spaces remove apostrophes
        # caret is an exclusionary symbol s
        # so this means take anything that is not a lower case or uppercase letter or numeric or .
        # or new line and replace with a space (this will backfire if there are any other special chars like ! or $)
        # TODO: take the above problem into account

        updated_title = re.sub('[^a-zA-Z0-9 \n\.]', ' ', f)

        # get rid of initial space that was created if first char is '_'
        if updated_title[0] == ' ':
            updated_title = updated_title[1:]

        # remove file extension
        updated_title = os.path.splitext(updated_title)[0]
        self.metadata['title'] = updated_title

    def createFileName(self, f):
        # take file title and replace all spaces with dashes and add file extension
        self.metadata['base'] = re.sub('[ ]', '-', f) + '.mp3'

    def updateFileAndTitle(self):
        shiur_with_heb_year_in_end_of_title = ['halacha shiur', 'shiur klali', 'vaadim']

        if self.has_file_name:
            # file has filename but needs title tag so we
            # create new filename by removing the initial underscore
            # create a title tag by replacing all dashes/apostophes with spaces
            self.createTitleTag(self.metadata['base'])
        else:
            # user has defined a title tag to use for filename as well
            # l'choora 'from_input_title' is set to True - should I check this though for any reason?
            # and we should set their input as the updated_title
            self.createFileName(self.metadata['input_title'])

        # add number sign to series and remove any zero that precedes a number
        if self.metadata['is_series']:
            # get the series value
            ''' 
            The following code might be overkill to get the series value 
            but I'm keeping it for now if it proves to be a more complicated process
            series_number = re.search('-([0-9]*).mp3', self.metadata['base']).group(
                 1)  # returns just the value between the
             # demarcated characters
             # strip the series number of any leading zeros
             series_number = series_number.lstrip("0")  # that's a cool strip function
             print(f'series is:{series_number}')
             '''

            # assuming series is always at the end of the file name just before file extension
            title_list = self.metadata['title'].split(' ')  # create list of the file name in order
            # to replace the series number which is assumed to be at end of string

            updated_series_number = '#' + title_list[-1].lstrip("0")  # add '#' to string and strip any leading zeros

            # replace the series number in the title list with the above updated string
            title_list[-1] = updated_series_number

            # rejoin list to create the updated title tag
            updated_title = ' '.join(title_list)
            self.metadata['title'] = updated_title

            print(f'title tag with series is:{self.metadata["title"]}')

        elif self.metadata['album'] == 'Mishna Yomis':
            # add comma between perek and mishna
            # I think we're gonna have to hard code this one!
            # for now we'll just assume perek number is always the 3rd element of the string
            title_list = self.metadata['title'].split(' ')  # create list of the file name in order
            perek_num_with_comma = title_list[2] + ","
            title_list[2] = perek_num_with_comma
            # rejoin list to create the updated title tag
            updated_title = ' '.join(title_list)

            # in the case of multiple mishnas and we are creating the title tag from the file name
            # we again to have to hardcode the '-' since it was stripped previously out of the file name
            if self.has_file_name:
                if len(title_list) > 5:
                    mishna_num_with_dash = title_list[4] + "-" + title_list[5]
                    title_list[4] = mishna_num_with_dash
                # rejoin list to create the updated title tag
                updated_title = ' '.join(title_list[0:5])

            self.metadata['title'] = updated_title

        elif self.metadata['album'] in shiur_with_heb_year_in_end_of_title:
            # certain albums require a the Hebrew year in parentheses at end of title
            self.metadata['title'] += '(' + self.metadata['heb_year'] + ')'

        elif self.metadata['album'] == 'parsha':
            # assumption if given title the first word is the name of the parsha
            # or if given file name the first word until the dash is the parsha

            if self.has_file_name:
                # assume the first word in the file name is the parsha
                title_list = self.metadata['title'].split(' ')
                parsha = title_list[0]  # perhaps we want to verify with a list of parshas if this is not true
                year = title_list[1]  # this should always be year
                # update title tag
                parsha_year = '(' + parsha + ' ' + year + ')'
                title_list.append(parsha_year)
                updated_title = ' '.join(title_list[2:])
                self.metadata['title'] = updated_title

            # TODO: from input_title

    def getMetadataDic(self):
        return self.metadata
