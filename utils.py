# utils.py
import os
from config import RESULTS_BASE_DIR, get_date_str, APIKEY, MESSAGE, tasks
from gigachat import GigaChat

def get_questions(file_id):
    questions = ""
    with GigaChat(credentials=APIKEY, verify_ssl_certs=False, model='GigaChat-2-Pro') as giga:
        response = giga.chat({
            "messages":[
                {
                    "role": "user",
                    "content": MESSAGE,
                    "attachments": [file_id],
                }
            ],
            "temperature": 0.1
        })
        questions = response.choices[0].message.content.strip()
    return questions
