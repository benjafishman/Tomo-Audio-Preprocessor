import PySimpleGUI as sg      

sg.theme('SandyBeach')    # Keep things interesting for your users

albums = ['Album','Parshas Hashavuah','Moadim','Hilchos Tefilla', 'Shiur Klali']

artists = ['Artists','Moshe Meiselman', 'Avrahami', 'Fishman', 'Klein', 'Shurkin']

layout = [[sg.Text('Year', size = (3, 0)), sg.InputText(key = 'year')],
          [sg.Combo(albums, default_value = albums[0], key = 'album')],
          #[sg.Input(key='-IN-')],
          [sg.Combo(artists, default_value = artists[0], key= 'artist')],
          [sg.Text('Title type', size = (20, 1), font = 'Lucida', justification = 'left')],
          [sg.Radio('From file name','rd_title', key ='FileTitle'), sg.Radio('Create file name','rd_title', key='Create Title')],
          [sg.Text("Choose a file: "), sg.FileBrowse()],
          [sg.Text('Title', size = (3, 0)), sg.InputText()],
          [sg.Button('Generate'),sg.Button('Exit')]],    

window = sg.Window('Tomo File Preprocessor', layout)      

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Generate':
    	print("processing file!")

    '''
     if event == 'Show':
     # Update the "output" text element to be the value of "input" element
		window['-OUTPUT-'].update(values['-IN-'])
    '''
window.close()