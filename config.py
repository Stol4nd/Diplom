# config.py
from datetime import datetime

# Основные настройки
TEACHER_PASSWORD = "secretpassword123"
RESULTS_BASE_DIR = "student_results"
STATIC_FOLDER = "static"
LAB_TOPICS = [
    "OSPF",
    "IPv4 ACL",
    "NAT",
    "SNMP",
    "Syslog",
    "NTP", 
    "IPv4 адресация",
    "Telnet и SSH" 
]
APIKEY = 'Y2RjNGI4ZWEtYWQ4MS00MDRmLTkzMDMtZDgwNjlkYzk3NWRiOjUzOGI2NGY1LWZiZmYtNGZjYy05MGNjLTU2ODA0M2U4NGU4ZA=='

# Функция для получения даты без времени
def get_date_str():
    return datetime.now().strftime('%Y-%m-%d')