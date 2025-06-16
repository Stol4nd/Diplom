# config.py
from datetime import datetime
from sqlalchemy import create_engine
# Основные настройки
TEACHER_PASSWORD = "secretpassword123"
RESULTS_BASE_DIR = "student_results"
STATIC_FOLDER = "static"
APIKEY = 'Y2RjNGI4ZWEtYWQ4MS00MDRmLTkzMDMtZDgwNjlkYzk3NWRiOjUzOGI2NGY1LWZiZmYtNGZjYy05MGNjLTU2ODA0M2U4NGU4ZA=='
MESSAGE = """
Представь, ты преподаватель по предмету 'Сети и телекоммуникации'. Твоя задача задать 6 вопросов студенту по данному файлу чтобы убедиться в понимании темы студентом.
Данный файл является методическими указаниями для выполнения лабораторной работу с помощью оборудования компании Cisco. 
Опусти вводную и заключительную часть, выдай вопросы просто списком от 1 до 6, 3 вопроса теоретических на понимание темы и 3 вопроса практических по выполнению работы.
К вопросам добавь ожидаемые ответы от студента. Формат ответ не должен содержать спецсимволов или различного выделения. Вопросы должны быть пронумерованы и отделены друг от друга дополнительной строкой.
"""
engine = create_engine('sqlite:///labs.db', echo=True)
from Task_1 import Task_1
from Task_2 import Task_2
from Task_3 import Task_3
from Task_4 import Task_4
from Task_5 import Task_5

tasks = {
    1: Task_1,
    2: Task_2,
    3: Task_3,
    4: Task_4,
    5: Task_5
}

# Функция для получения даты без времени
def get_date_str():
    return datetime.now().strftime('%Y-%m-%d')