#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 7/31/2022


import PySimpleGUI as sg
import audioFileMetadataController as afc
import audioFileTagController as aftc
import audioFileHandler as fileHandler
import music_tag
import subprocess
import os
from openpyxl import load_workbook
import datetime
import re

year = datetime.date.today().year
sg.theme('SandyBeach')  # Keep things interesting for your users

# setup file path to import the settings spreadsheet
dir_path = os.path.dirname(os.path.realpath(__file__))
settings_file_name = "settings.xlsx"
settings_file_path = os.path.join(dir_path, settings_file_name)

# load spreadsheet
wb = load_workbook(filename=settings_file_path)
sheet = wb.active

# extract albums from spreadsheet and put them into an array
albums = []
for row in sheet:
    album = row[1].value
    albums.append(album)

# extract rabbis from spreadsheet and put them into an array
artists = []
for row in sheet:
    artist = row[0].value
    if artist:
        artists.append(str(artist))


# check for title tag/year

def check_pre_set_tags(audio_file_path):
    r = {'title': None, 'year': None}
    file_tags = music_tag.load_file(audio_file_path)

    if file_tags['title'] and not re.findall("^\d{4}.", str(file_tags['title'])):
        # check if the title is a real title and not a computer title
        # x = re.findall("^\d{4}.", txt)  # assuming that a man made title would not start with at least 4 digits
        r['title'] = file_tags['title']
        if file_tags['year']:
            r['year'] = file_tags['year']
        else:
            print("update gui values of title")
    else:
        print("nothing to update")
    print(r)
    return r


# setup gui
layout = [[sg.Text('Year', size=(3, 0)), sg.InputText(key='year', default_text=year, size=(5, 1))],
          [sg.Combo(albums[1:], default_value=albums[0], key='album'),
           sg.Combo(['Rabbi ' + i for i in artists[1:]], default_value=artists[0], key='artist')],
          [sg.Checkbox('Is Series', default=False, key='is_series')],
          [sg.Text('Title Type', size=(10, 1), font='Lucida', justification='left')],
          [sg.Radio('From file name', 'rd_title', key='from_file_name'),
           sg.Radio('Create file name', 'rd_title', key='from_input_title')],
          # [sg.Text("Choose a file: "), sg.FileBrowse(key='full_file_path')],
          [sg.Input(key="-IN-", change_submits=True), sg.FileBrowse(key="full_file_path")],
          [sg.Text('Title', size=(3, 0)), sg.InputText(key='input_title')],
          [sg.Button('Generate'), sg.Button('Exit')]],

window = sg.Window('Tomo File Preprocessor', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if values["-IN-"]:
        r = check_pre_set_tags(values["-IN-"])
        year = datetime.date.today().year
        title = ""
        if r['year']:
            year = r['year']
        window['year'].update(year)
        if r['title']:
            title = r['title']
        window['input_title'].update(title)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Generate':

        values['comment'] = sheet['C2'].value  # 'Yeshivas Toras Moshe | Ner Michoel Alumni Association'

        values['composer'] = sheet['D2'].value  # 'NerMichoel.org'

        values['album_art_file_path'] = sheet['E2'].value  # 'C:/Users/Win10/Desktop/tomo dev/audio_icon.jpg'

        values['heb_year'] = sheet['F2'].value  # we need to grab this from some api it really cannot be hard coded

        file_name, file_extension = os.path.splitext(values['full_file_path'])

        # field validation
        # check if user has selected a file
        if values['full_file_path'] == "":
            sg.popup('You must choose a file')

        # validate that user chose an audio file
        # if file_extension
        elif file_extension != '.mp3':
            sg.popup('You must select an audio file (extension .mp3) ')
        else:

            '''
           Here's where we tie it all together!
           1. Receive the input data and process it accordingly to create a dictionary of the metadata
           2. Copy original file and loaded with the metadata from step 1
           3. Compress copy if more than 45 kbps
           4. Prepend original file with '_' if it doesn't already have it
           '''
            m = afc.AudioFileMetaDataController(values)
            file_handler = fileHandler.AudioFileHandler()

            data = {}
            needs_compression = False

            try:
                m.updateFileAndTitle()
                data = m.getMetadataDic()
                print(data)
            except Exception as e:
                print(f'error {e}')

            org_file_tag = music_tag.load_file(data['src_file_info']['path'])


            # check fo preset title and year tag
            # if org_file_tag['title']:

            def needs_compression(music_tag_file):
                bitrate = int(music_tag_file.audioFile['#bitrate'])
                if bitrate >= 128000:
                    return True
                else:
                    return False


            # check if file needs compression FFMPEG

            if int(org_file_tag['#bitrate']) > 48000:

                try:
                    print('compressing')

                    src = data['src_file_info']['path']
                    dst = data['dst_file_info']['path']

                    ffmpeg_downgrade_kbps = 'ffmpeg -i ' + '"' + src + '"' + ' -codec:a libmp3lame -b:a 48k' + ' ' + '"' + dst + '"'
                    # ffmpeg command:            ffmpeg -i input.mp3 -codec:a libmp3lame -b:a 45k output.mp3
                    print(ffmpeg_downgrade_kbps)

                    command_output = subprocess.check_output(ffmpeg_downgrade_kbps, shell=True)  # Run the command


                except Exception as e:
                    print(f'error {e}')

            else:

                try:
                    print('copying file')
                    src = data['src_file_info']['path']

                    dst = data['dst_file_info']['path']

                    file_handler.copy_file_with_new_title(src, dst)

                except Exception as e:
                    print(f'error: {e}')
            try:
                # load copied file with metadata
                print('loading copied file with metadata')
                # print(data)
                meta_data_injector = aftc.AudioFileTagController(data)
                meta_data_injector.update_metadata()

            except Exception as e:
                print(f'error: {e}')
            print('done')

window.close()
