#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 7/31/2022

'''


{
    org_file: {
        'full_file_path': 'C:/Users/Ben/Desktop/TomoDev/tomo dev/tomo dev/_Bava-Metzia-Shiur-154.mp3',
        'base': '_Bava-Metzia-Shiur-154.mp3'
    },
    new_file: {
        'full_file_path': "",
        'base': ""
    },
    metadata: {
        'album': 'Bava Metziah',
        'year': '2022',
        'artist': 'Rabbi Moshe Meiselman',
        'comment': 'Yeshivas Toras Moshe | Ner Michoel Alumni Association',
        'composer': 'NerMichoel.org',
        'album_art_file_path': '',
        'title': 'Bava Metzia Shiur #154',
        'is_series': True,
        'heb_year': '5782',
    }
}
'''

import re
import os
from utilities import is_parsha


class AudioFileMetaDataController(object):
    data = {
        'src_file_info': {
            'path': "",
            'base': "",
        },
        'dst_file_info': {
            'path': "",
            'base': "",
        },
        'metadata': {
            'album': "",
            'Year': "",
            'artist': "",
            'comment': "",
            'composer': "",
            'album_art_file_path': "",
            "title": "",
            "is_series": False,
            "heb_year": "",
        }
    }

    has_file_name = False
    shiur_with_heb_year_in_end_of_title = ['Halacha Shiur', 'Shiur Klali', 'Vaadim']
    shiur_with_year_prepended_to_file_name_appended_to_title = ['Parshas Hashavuah', 'Moadim']

    def __init__(self, data):

        self.data["metadata"]["is_series"] = False
        # update src file info
        self.data['src_file_info']['path'] = data['full_file_path']
        self.data['src_file_info']['base'] = os.path.basename(data['full_file_path'])
        # update metadata info
        self.data['metadata']['album'] = data['album']
        self.data['metadata']['artist'] = data['artist']
        self.data['metadata']['year'] = data['year']
        self.data['metadata']['comment'] = data['comment']
        self.data['metadata']['composer'] = data['composer']
        self.data['metadata']['heb_year'] = data['heb_year']
        self.data['metadata']['album_art_file_path'] = data['album_art_file_path']

        meta_album = self.data['metadata']['album']
        print(self.data['metadata']['album'] == 'Mishna Yomis')
        print(f'album: {meta_album}')
        # check if the audio file is part of a series
        print(f'input is series: {data["is_series"]}')
        print(f'is series: {self.data["metadata"]["is_series"]}')
        if data['is_series'] is True:
            self.data['metadata']['is_series'] = True

        print(f'is series: {self.data["metadata"]["is_series"]}')

        # check if the user opts to use the name of file already for the title tag
        if data['from_file_name']:
            self.has_file_name = True

        # check if the user has provided the title for the audio file then go with that and it should override filename
        elif data['input_title']:
            self.data['metadata']['title'] = data['input_title']  # slight duplication of data but I think it's
            self.has_file_name = False
            # justified

    def createTitleTag(self, f):
        # replace dashes with spaces remove apostrophes
        # caret is an exclusionary symbol s
        # so this means take anything that is not a lower case or uppercase letter or numeric or .
        # or new line and replace with a space (this will backfire if there are any other special chars like ! or $)
        # TODO: take the above problem into account

        print('CREATE TITLE TAG')
        print(f'base: {f}')
        # updated_title = re.sub('[^a-zA-Z0-9 \n\.]', ' ', f)
        updated_title = re.sub('[^a-zA-Z0-9 \n\'''.]', ' ', f)
        print(f'updated_title: {updated_title}')
        # get rid of initial space that was created if first char is '_'
        if updated_title[0] == ' ':
            updated_title = updated_title[1:]

        # remove file extension
        updated_title = os.path.splitext(updated_title)[0]
        self.data['metadata']['title'] = updated_title

    def createFileName(self, title):
        print(f'create file name with title: {title}')
        if self.data['metadata']['is_series'] is True:
            # must remove the dash from the string
            title = re.sub('[#]', '', title)

        # if album is mishna yomis we need to remove the comma
        if self.data['metadata']['album'] == 'Mishna Yomis':
            title = re.sub('[,]', '', title)  # regex to remove commas

        # TODO: remove?
        # I don't think we need this i believe the year is appended automatically
        # elif self.data["metadata"]["album"] in self.shiur_with_heb_year_in_end_of_title:
        #    # remove year
        #    print("SHIUR WITH HEB YR AT END OF TITLE @#$%")
        #    title = re.sub('[(0-9)]','', title)

        elif self.data["metadata"]["album"] in self.shiur_with_year_prepended_to_file_name_appended_to_title:

            if self.has_file_name:
                title = self.data['src_file_info']['base'].lstrip('_')
                print("here")
                self.data['dst_file_info']['base'] = title

                dirname, fname = os.path.split(self.data['src_file_info']['path'])

                self.data['dst_file_info']['path'] = os.path.join(dirname, self.data['dst_file_info']['base'])

                return  # very hacky! I did this because if we let the function keep going then it's going to add an additional .mp3 to file name
            else:
                print('input title name for shiur with year & title/file switch')
                print(f'title: {title}')
                if self.data["metadata"]["album"] == "Parshas Hashavuah":
                    # user has input the title so we'll use that for the file name
                    # assumption is that the there is a (parsha year) substring in that order
                    parsha, year = re.search(r"\((.+?)\)", title).group(1).split()

                    # take the parsha year out of title
                    title = re.sub(r" \((.+?)\)", '', title)

                    # put the parsha/year at the beginning of title
                    title = parsha + " " + year + " " + title
                # TODO: create more defined heuristics for other categories such as moadim...

        t = re.sub('[^a-zA-Z0-9 \n\.]', '', title)  # strip out anything that is not alphanumeric

        # take file title and replace all spaces with dashes and add file extension
        self.data['dst_file_info']['base'] = re.sub('[ ]', '-', t) + '.mp3'

        dirname, fname = os.path.split(self.data['src_file_info']['path'])

        self.data['dst_file_info']['path'] = os.path.join(dirname, self.data['dst_file_info']['base'])

    def updateFileAndTitle(self):
        if self.has_file_name:
            # file has filename but needs title tag so we
            # create new filename by removing the initial underscore
            # create a title tag by replacing all dashes/apostophes with spaces
            self.createTitleTag(self.data['src_file_info']['base'])
        '''else:
            # user has defined a title tag to use for filename as well
            # l'choora 'from_input_title' is set to True - should I check this though for any reason?
            # and we should set their input as the updated_title
            self.createFileName(self.data['metadata']['title'])
'''
        # add number sign to series and remove any zero that precedes a number
        if self.data['metadata']['is_series']:
            # get the series value

            '''The following code might be overkill to get the series value
            but I'm keeping it for now if it proves to be a more complicated process '''
            series_number = None
            if self.data['metadata']['title']:
                print('here 1.5')
                series_number = re.search("#([0-9]+)", self.data['metadata']['title']).group(
                    1)
            else:
                series_number = re.search('-([0-9]+)', self.data['src_file_info']['base']).group(
                    1)
                print('here 3')# returns just the value between the
            # demarcated characters
            # strip the series number of any leading zeros

            self.data['metadata']['title'] = self.data['metadata']['title'].replace(series_number,
                                                                                    '#' + series_number.lstrip("0"))

        elif self.data['metadata']['album'] == 'Mishna Yomis':
            # add comma between perek and mishna
            # I think we're gonna have to hard code this one!
            # for now we'll just assume perek number is always the 3rd element of the string
            title_list = self.data['metadata']['title'].split(' ')  # create list of the file name in order
            perek_num_with_comma = title_list[2] + ","
            title_list[2] = perek_num_with_comma
            # rejoin list to create the updated title tag
            updated_title = ' '.join(title_list)

            print(f'updated title is:{updated_title}')
            # in the case of multiple mishnas and we are creating the title tag from the file name
            # we again to have to hardcode the '-' since it was stripped previously out of the file name
            if self.has_file_name:
                if len(title_list) > 5:
                    mishna_num_with_dash = title_list[4] + "-" + title_list[5]
                    title_list[4] = mishna_num_with_dash
                # rejoin list to create the updated title tag
                updated_title = ' '.join(title_list[0:5])
                print(f'has file name updated title is:{updated_title}')

            self.data['metadata']['title'] = updated_title

        elif self.data['metadata']['album'] in self.shiur_with_heb_year_in_end_of_title:
            # certain albums require the Hebrew year in parentheses at end of title
            self.data['metadata']['title'] += '(' + self.data['metadata']['heb_year'] + ')'

        elif self.data['metadata']['album'] in self.shiur_with_year_prepended_to_file_name_appended_to_title:
            # assumption if given title the first word is the name of the parsha
            # or if given file name the first word until the dash is the parsha

            if self.has_file_name:
                # assume the first word in the file name is the parsha
                content_in_parenthesis = ""
                title_list = self.data['metadata']['title'].split(' ')
                if self.data['metadata']['album'] == 'Parshas Hashavuah':
                    parsha = title_list[0]  # perhaps we want to verify with a list of parshas if this is not true
                    year = title_list[1]
                    if is_parsha(parsha):
                        pass
                    elif is_parsha(parsha + ' ' + title_list[1]):
                        parsha = parsha.capitalize() + ' ' + title_list[1].capitalize()
                        year = title_list[2]
                    else:
                        print("error: parsha not found")

                    # update title tag
                    content_in_parenthesis = '(' + parsha + ' ' + year + ')'
                    title_list.append(content_in_parenthesis)
                    updated_title = ' '.join(title_list[2:])
                if self.data['metadata']['album'] == 'Moadim':
                    # assume year is last element in title
                    year = title_list[-1]
                    content_in_parenthesis = '(' + year + ')'
                    title_list[-1] = content_in_parenthesis
                    updated_title = ' '.join(title_list)
                self.data['metadata']['title'] = updated_title
            # if the user has input title then we just need to update the dst file name

        self.createFileName(self.data['metadata']['title'])

    def getMetadataDic(self):
        return self.data
