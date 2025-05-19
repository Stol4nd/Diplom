from gigachat import GigaChat
import os

ApiKey = 'Y2RjNGI4ZWEtYWQ4MS00MDRmLTkzMDMtZDgwNjlkYzk3NWRiOjUzOGI2NGY1LWZiZmYtNGZjYy05MGNjLTU2ODA0M2U4NGU4ZA=='

with GigaChat(credentials=ApiKey, verify_ssl_certs=False, model='GigaChat-2-Pro') as giga:
    path = 'labs/'
    filelist = os.listdir(path)
    for file in filelist:
        giga.upload_file(
            open(os.path.join('labs/' + file), 'rb'),
            purpose='general')
    response = giga.get_files()
    print(response.data)