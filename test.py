from gigachat import GigaChat
import requests

ApiKey = 'Y2RjNGI4ZWEtYWQ4MS00MDRmLTkzMDMtZDgwNjlkYzk3NWRiOjUzOGI2NGY1LWZiZmYtNGZjYy05MGNjLTU2ODA0M2U4NGU4ZA=='
ClientSecret = '538b64f5-fbff-4fcc-90cc-568043e84e8d'
ClientId = 'cdc4b8ea-ad81-404f-9303-d8069dc975db'

# url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

# payload = 'scope=GIGACHAT_API_PERS'
# headers = {
#   'Content-Type': 'application/x-www-form-urlencoded',
#   'Accept': 'application/json',
#   'RqUID': '7f3d0fea-83d9-4a01-8975-df1c360a0a5c',
#   'Authorization': 'Basic Y2RjNGI4ZWEtYWQ4MS00MDRmLTkzMDMtZDgwNjlkYzk3NWRiOjUzOGI2NGY1LWZiZmYtNGZjYy05MGNjLTU2ODA0M2U4NGU4ZA=='
# }

# response = requests.request("POST", url, headers=headers, data=payload, verify=False)

# print(response.text)

message = """
    Представь, ты преподаватель по предмету 'Сети и телекоммуникации'. Твоя задача задать 5 вопросов студенту на тему 'WAN и LAN' чтобы убедиться в понимании темы студентом.
    Студенты выполняют лабораторную работу по данной теме с помощью оборудования компании Cisco. При составлении вопросов учитывай данный факт.
    Опусти вводную и заключительную часть, выдай вопросы просто списком от 1 до 5.
"""
with GigaChat(credentials=ApiKey, verify_ssl_certs=False, model='GigaChat-2-Max') as giga:
    response = giga.chat(message)
    print(response.choices[0].message.content)