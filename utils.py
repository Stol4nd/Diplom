# utils.py
import os
from config import RESULTS_BASE_DIR, get_date_str, APIKEY
from tasks import tasks
from gigachat import GigaChat

def get_questions(topic):
        message = f"""
            Представь, ты преподаватель по предмету 'Сети и телекоммуникации'. Твоя задача задать 5 вопросов студенту на тему '{topic}' чтобы убедиться в понимании темы студентом.
            Студенты выполняют лабораторную работу по данной теме с помощью оборудования компании Cisco. При составлении вопросов учитывай данный факт.
            Опусти вводную и заключительную часть, выдай вопросы просто ненумерованным списком от 1 до 5.
        """
        with GigaChat(credentials=APIKEY, verify_ssl_certs=False, model='GigaChat-2-Max') as giga:
            response = giga.chat(message)
            questions = response.choices[0].message.content.strip()
            print(questions)
            return questions
    
def ensure_directory(directory):
    """Создает директорию, если её нет."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_results(student_info, results):
    """Сохраняет результаты в файл с группировкой по группе."""
    group_dir = os.path.join(RESULTS_BASE_DIR, student_info['group'])
    ensure_directory(group_dir)
    
    date_str = get_date_str()
    student_id = f"{student_info['surname']}_{student_info['name']}_{date_str}"
    file_path = os.path.join(group_dir, f"{student_id}.txt")
    
    with open(file_path, 'w', encoding='UTF-8') as f:
        for t_num, result in results.items():
            f.write(f"Задание №{t_num}:\n")
            task_class = tasks[int(t_num)]  # Получаем класс по номеру задания
            if t_num == '5':
                for subnet_num, subnet_result in enumerate(result):
                    f.write(f"Подсеть №{subnet_num + 1}:\n")
                    for key in task_class.field_order:
                        if key in subnet_result:
                            # Получаем русское название
                            russian_key = task_class.field_translations.get(key, key)
                            # Изменяем строку результата, заменяя английский ключ на русский
                            result_str = subnet_result[key]
                            if "Неправильно" in result_str:
                                new_result = result_str.replace(key, russian_key)
                                f.write(f"{new_result}\n")
                            else:
                                f.write(f"{russian_key}: Правильно\n")
            else:
                for key in task_class.field_order:
                    if key in result:
                        # Получаем русское название
                        russian_key = task_class.field_translations.get(key, key)
                        # Изменяем строку результата, заменяя английский ключ на русский
                        result_str = result[key]
                        if "Неправильно" in result_str:
                            new_result = result_str.replace(key, russian_key)
                            f.write(f"{new_result}\n")
                        else:
                            f.write(f"{russian_key}: Правильно\n")
            f.write("\n")
