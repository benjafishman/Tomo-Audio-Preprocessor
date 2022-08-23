import audioFileMetadataController as afc

testFromFileNameSeries = {'year': '2022',
                          'album': 'Bava Metziah',
                          'artist': 'Moshe Meiselman',
                          'is_series': True,
                          'from_file_name': True,
                          'from_input_title': False,
                          'full_file_path': 'C:/Users/Ben/Desktop/TomoDev/tomo dev/tomo dev/_Bava-Metzia-Shiur-054.mp3',
                          'comments': 'Yeshivas Toras Moshe | Ner Michoel Alumni Association',
                          'composer': 'NerMichoel.org',
                          'album_art_file_path': '',
                          'input_title': 'this is a test',
                          'heb_year': '5782'

                          }
testCreateFileName = {
    'year': '2022',
    'album': 'Bubu Metziah',
    'artist': 'Moshe Meiselman',
    'is_series': False,
    'from_file_name': False,
    'from_input_title': True,
    'full_file_path': 'C:/Users/Ben/Desktop/TomoDev/tomo dev/tomo dev/Massei-5782-ry.mp3',
    'input_title': 'this is a test',
    'album_art_file_path': '',
    'comments': 'Yeshivas Toras Moshe | Ner Michoel Alumni Association',
    'composer': 'NerMichoel.org',
    'heb_year': '5782'

}

testCreateFileNameMishna = {
    'year': '2022',
    'album': 'Mishna Yomis',
    'artist': 'Moshe Meiselman',
    'is_series': False,
    'from_file_name': False,
    'from_input_title': True,
    'full_file_path': 'C:/Users/Ben/Desktop/TomoDev/tomo dev/tomo dev/Massei-5782-ry.mp3',
    'input_title': 'Eruvin Perek 3 Mishna 8-6',
    'album_art_file_path': '',
    'comments': 'Yeshivas Toras Moshe | Ner Michoel Alumni Association',
    'composer': 'NerMichoel.org',
    'heb_year': '5782'

}

testFromFileNameMishna = {
    'year': '2022',
    'album': 'Mishna Yomis',
    'artist': 'Moshe Meiselman',
    'is_series': False,
    'from_file_name': True,
    'from_input_title': False,
    'full_file_path': 'C:/Users/Ben/Desktop/TomoDev/tomo dev/tomo dev/Eruvin-Perek-3-Mishna-8-6.mp3',
    'input_title': '',
    'album_art_file_path': '',
    'comments': 'Yeshivas Toras Moshe | Ner Michoel Alumni Association',
    'composer': 'NerMichoel.org',
    'heb_year': '5782'

}

testFromFileNameShiurKlali = {
    'year': '2022',
    'album': 'shiur klali',
    'artist': 'Moshe Meiselman',
    'is_series': False,
    'from_file_name': True,
    'from_input_title': False,
    'full_file_path': 'C:/Users/Ben/Desktop/TomoDev/tomo dev/tomo '
                      'dev/_Bava-Metzia-16-Pshiah-in-Sofek-Sheilah-Bbaalim.mp3',
    'input_title': '',
    'album_art_file_path': '',
    'comments': 'Yeshivas Toras Moshe | Ner Michoel Alumni Association',
    'composer': 'NerMichoel.org',
    'heb_year': '5782'

}

testFromFileNameParsha = {
    'year': '2022',
    'album': 'parsha',
    'artist': 'Moshe Meiselman',
    'is_series': False,
    'from_file_name': True,
    'from_input_title': False,
    'full_file_path': 'C:/Users/Ben/Desktop/TomoDev/tomo dev/tomo '
                      'dev/_Massei-5782-Traveling-With-Hashem.mp3',
    'input_title': '',
    'album_art_file_path': '',
    'comments': 'Yeshivas Toras Moshe | Ner Michoel Alumni Association',
    'composer': 'NerMichoel.org',
    'heb_year': '5782'

}




try:
    m = afc.AudioFileMetaDataController(testFromFileNameSeries)
    m.updateFileAndTitle()
    print(f'testFromFileNameSeries: {m.getMetadataDic()}')
except Exception as e:
    print(f'error testFromFileNameSeries: {e}')
print('\n\n')

try:
    g = afc.AudioFileMetaDataController(testCreateFileName)
    g.updateFileAndTitle()
    print(f'testCreateFileName: {g.getMetadataDic()}')
except Exception as e:
    print(f'error testCreateFileName: {e}')
print('\n\n')
try:
    y = afc.AudioFileMetaDataController(testCreateFileNameMishna)
    y.updateFileAndTitle()
    print(f'testCreateFileNameMishna: {y.getMetadataDic()}')
except Exception as e:
    print(f'error testCreateFileNameMishna: {e}')
print('\n\n')

try:
    m = afc.AudioFileMetaDataController(testFromFileNameMishna)
    m.updateFileAndTitle()
    print(f'testFromFileNameMishna: {m.getMetadataDic()}')
except Exception as e:
    print(f'error testFromFileNameMishna: {e}')
print('\n\n')

try:
    m = afc.AudioFileMetaDataController(testFromFileNameShiurKlali)
    m.updateFileAndTitle()
    print(f'testFromFileNameShiurKlali: {m.getMetadataDic()}')
except Exception as e:
    print(f'error testFromFileNameShiurKlali: {e}')


try:
    m = afc.AudioFileMetaDataController(testFromFileNameParsha)
    m.updateFileAndTitle()
    print(f'testFromFileNameParsha: {m.getMetadataDic()}')
except Exception as e:
    print(f'error testFromFileNameParsha: {e}')
print('\n\n')