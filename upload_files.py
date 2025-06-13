import os
from gigachat import GigaChat
from sqlalchemy.orm import Session
from db_tables import Labs
from config import engine

ApiKey = 'Y2RjNGI4ZWEtYWQ4MS00MDRmLTkzMDMtZDgwNjlkYzk3NWRiOjUzOGI2NGY1LWZiZmYtNGZjYy05MGNjLTU2ODA0M2U4NGU4ZA=='
LABS_BASE_DIR = 'labs'
QUESTIONS_BASE_DIR = 'questions'

os.makedirs(QUESTIONS_BASE_DIR, exist_ok=True)

with GigaChat(credentials=ApiKey, verify_ssl_certs=False, model='GigaChat-2-Pro') as giga:
    for course in os.listdir(LABS_BASE_DIR):
        course_labs_path = os.path.join(LABS_BASE_DIR, course)
        if not os.path.isdir(course_labs_path):
            continue
        
        course_lab_questions_path = os.path.join(QUESTIONS_BASE_DIR, course)
        os.makedirs(course_lab_questions_path, exist_ok=True)
        
        for file in os.listdir(course_labs_path):
            filename_no_ext = os.path.splitext(file)[0]
            resp = giga.upload_file(
                open(os.path.join(course_labs_path + '/' + file), 'rb'),
                purpose='general')
            file_id = resp.id_
            answer_file_path = os.path.join(course_lab_questions_path, f'{filename_no_ext}.txt')
            # Если файла для ответа нет — создаём
            if not os.path.exists(answer_file_path):
                with open(answer_file_path, 'w', encoding='utf-8') as f:
                    pass
            with Session(engine) as session:
                lab = Labs(
                    course=course,
                    title=filename_no_ext,
                    gigachat_id = file_id,
                    link = answer_file_path
                )
                session.add(lab)
                session.commit()
            