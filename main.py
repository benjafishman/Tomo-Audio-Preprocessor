#!/usr/bin/python
# BS"D
# Bentzion Fishman
# 7/31/2022


import PySimpleGUI as sg
import audioFileController as afc

sg.theme('SandyBeach')  # Keep things interesting for your users

albums = ['Album', 'Bava Metziah', 'Parshas Hashavuah', 'Moadim', 'Hilchos Tefilla', 'Shiur Klali']

artists = ['Artists', 'Moshe Meiselman', 'Avrahami', 'Fishman', 'Klein', 'Shurkin']

layout = [[sg.Text('Year', size=(3, 0)), sg.InputText(key='year')],
          [sg.Combo(albums, default_value=albums[0], key='album')],
          # [sg.Input(key='-IN-')],
          [sg.Combo(artists, default_value=artists[0], key='artist')],
          [sg.Text('Title type', size=(20, 1), font='Lucida', justification='left')],
          [sg.Radio('From file name', 'rd_title', key='fileName'),
           sg.Radio('Create file name', 'rd_title', key='title')],
          [sg.Text("Choose a file: "), sg.FileBrowse()],
          [sg.Text('Title', size=(3, 0)), sg.InputText(key='title')],
          [sg.Button('Generate'), sg.Button('Exit')]],

window = sg.Window('Tomo File Preprocessor', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Generate':
        values['comment'] = 'Yeshivas Toras Moshe | Ner Michoel Alumni Association'
        values['composer'] = 'NerMichoel.org'
        values['albumArtFilePath'] = ''
        print("processing file!")
        m = afc.AudioFileMetaDataController(values)

    '''
     if event == 'Show':
     # Update the "output" text element to be the value of "input" element
		window['-OUTPUT-'].update(values['-IN-'])


    what needs to happen now:
    1. set the metadata: name, title, album, artists, year,
    2. compress file
    '''

window.close()
