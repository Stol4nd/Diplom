from gigachat import GigaChat
from config import MESSAGE

ApiKey = 'Y2RjNGI4ZWEtYWQ4MS00MDRmLTkzMDMtZDgwNjlkYzk3NWRiOjUzOGI2NGY1LWZiZmYtNGZjYy05MGNjLTU2ODA0M2U4NGU4ZA=='
message_1 = """
    Представь, ты преподаватель по предмету 'Сети и телекоммуникации'. Твоя задача задать 5 вопросов студенту на тему 'WAN и LAN' чтобы убедиться в понимании темы студентом.
    Студенты выполняют лабораторную работу по данной теме с помощью оборудования компании Cisco. При составлении вопросов учитывай данный факт.
    Опусти вводную и заключительную часть, выдай вопросы просто списком от 1 до 5.
"""
message_2 = """
    Представь, ты преподаватель по предмету 'Сети и телекоммуникации'. Твоя задача задать 6 вопросов студенту по данному файлу чтобы убедиться в понимании темы студентом.
    Данный файл является методическими указаниями для выполнения лабораторной работу с помощью оборудования компании Cisco. 
    Опусти вводную и заключительную часть, выдай вопросы просто списком от 1 до 6, 3 вопроса теоретических на понимание темы и 3 вопроса практических по выполнению работы.
    К вопросам добавь ожидаемые ответы от студента. Формат ответ
"""
           
questions = ""            
with GigaChat(credentials=ApiKey, verify_ssl_certs=False, model='GigaChat-2-Pro') as giga:
    response = giga.chat({
            "messages":[
                {
                    "role": "user",
                    "content": MESSAGE,
                    "attachments": ["47bc530a-1d5d-4de8-9fa9-43f009f62cdb"],
                }
            ],
            "temperature": 0.1
        })
    questions = response
    print(questions.choices[0].message.content.strip())
    # response = giga.get_files()
    # for file in response.data:
    #     giga.delete_file(file.id_)
    # response = giga.get_files()
    # print(response.data)
    # response = giga.chat({
    #         "messages":[
    #             {
    #                 "role": "user",
    #                 "content": message_2,
    #                 "attachments": ["b6901a74-d51f-497f-a7bf-f948d4efaad5"],
    #             }
    #         ],
    #         "temperature": 0.1
    #     }
    # )
    # print(response.choices[0].message.content)