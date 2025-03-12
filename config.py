# config.py
from datetime import datetime

# Основные настройки
TEACHER_PASSWORD = "secretpassword123"
RESULTS_BASE_DIR = "student_results"
STATIC_FOLDER = "static"

# Функция для получения даты без времени
def get_date_str():
    return datetime.now().strftime('%Y-%m-%d')