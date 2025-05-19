from gigachat import GigaChat

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
           
            
with GigaChat(credentials=ApiKey, verify_ssl_certs=False, model='GigaChat-2-Pro') as giga:
    # giga.upload_file(open('labs/2.7.2 Lab - Configure Single-Area OSPFv2.docx', 'rb'), purpose='general')
    response = giga.get_files()
    print(response.data[0])
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