# routes.py
from flask import render_template, request, redirect, url_for, session
import ipaddress
import os
from config import STATIC_FOLDER, RESULTS_BASE_DIR, FILES_DICT
from utils import get_questions, get_filenames
from db import *
from tasks import tasks

def configure_routes(app):
    @app.route('/')
    def index():
        return redirect(url_for('main'))
    
    @app.route('/main')
    def main():
        session.clear()
        return render_template('main.html')

    @app.route('/student_groups')
    def student_groups():
        groups = [group_num for (group_num,) in get_groups()]
        if len(groups) == 0:
            return render_template('student_groups.html', message="Список групп пуст. Попросите преподавателя добавить группы в базу данных.")
        else:
            return render_template('student_groups.html', groups=groups)
    
    @app.route('/student_list/<group>')
    def student_list(group):
        students = sorted([student for (student,) in get_students_db(group)])
        return render_template('student_list.html', students=students, group=group)

    @app.route('/exercise_work_homepage/<student>')
    def exercise_work_homepage(student):
        session['student_id'] = get_student_id_db(student)[0]
        results = get_student_results_db(session['student_id'])
        session['current_task'] = 1
        session['true_answers'] = 0
        session['all_answers'] = 0
        return render_template('exercise_work_homepage.html', student=student, results=results)
    
    @app.route('/task', methods=['GET', 'POST'])
    def task():
        if 'student_id' not in session:
            return redirect(url_for('student_groups'))
        
        task_num = session.get('current_task', 1)
        
        if task_num > 5:
            save_results(session['student_id'], session['true_answers'], session['all_answers'])
            return redirect(url_for('test_results'))
        
        if f'task_{task_num}_data' not in session:
            task = tasks[task_num]()
            task.generate_task()
            raw_task_data = task.__dict__
            task_data = {
                key: value 
                for key, value in raw_task_data.items()
            }
            session[f'task_{task_num}_data'] = task_data
        
        task_data = session[f'task_{task_num}_data']
        
        if request.method == 'POST':
            task_obj = tasks[task_num]()
            task_obj.__dict__.update(task_data)
            
            if task_num == 5:
                student_answers = []
                form_data = request.form.to_dict()
                for i in range(task_data['subnets']):
                    subnet_answers = {
                        'first_host_decimal': form_data[f'subnet_{i}_first_host_decimal'],
                        'first_host_binary': form_data[f'subnet_{i}_first_host_binary'],
                        'last_host_decimal': form_data[f'subnet_{i}_last_host_decimal'],
                        'last_host_binary': form_data[f'subnet_{i}_last_host_binary'],
                        'subnet_decimal': form_data[f'subnet_{i}_subnet_decimal'],
                        'subnet_binary': form_data[f'subnet_{i}_subnet_binary'],
                        'subnet_mask_decimal': form_data[f'subnet_{i}_subnet_mask_decimal'],
                        'subnet_mask_binary': form_data[f'subnet_{i}_subnet_mask_binary']
                    }
                    student_answers.append(subnet_answers)
                task_5_results = task_obj.check_answers(student_answers)
                for result in task_5_results:
                    for key, value in result.items():
                        session['true_answers'] += int(value)
                        session['all_answers'] += 1
            else:
                student_answers = request.form.to_dict()
                task_1_4_results = task_obj.check_answers(student_answers)
                for key, value in task_1_4_results.items():
                    session['true_answers'] += int(value)
                    session['all_answers'] += 1
            session['current_task'] = task_num + 1
            return redirect(url_for('task'))
        
        return render_template(f'task_{task_num}.html', task_data=task_data)
    
    @app.route('/test_results')
    def test_results():
        if 'student_id' not in session:
            return redirect(url_for('student_groups'))
        
        student_id = session['student_id']
        result_string = f"{session['true_answers']}/{session['all_answers']}"
        result_percent = round((session['true_answers']/session['all_answers'])*100)
        session.clear()
        
    
    @app.route('/teacher', methods=['GET', 'POST'])
    def teacher():
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            teacher = get_teacher_id(login, password)
            try:
                session['teacher'] = teacher[0][0]
                session['teacher_authenticated'] = True
                print(session['teacher'])
                return redirect(url_for('teacher_dashboard'))
            except IndexError:
                return render_template('teacher.html', error="Не удалось выполнить вход. Проверьте правильность введенных данных.")
        return render_template('teacher.html')


    @app.route('/teacher/dashboard')
    def teacher_dashboard():
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        return render_template('teacher_dashboard.html', teacher=session['teacher'])
    
    @app.route('/teacher/add_group', methods=['GET', 'POST'])
    def add_group():
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        if request.method == 'POST':
            group_num = request.form.get('group_num')
            session['group_id'] = add_group_db(group_num)
            return redirect(url_for('add_student'))
        return render_template('add_group.html', teacher=session['teacher'])
    
    @app.route('/teacher/add_student_group')
    def add_student_group():
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        groups = [group_num for (group_num,) in get_groups()]
        if len(groups) == 0:
            return render_template('add_student_group.html', teacher = session['teacher'], message="Нет групп, к которым можно добавить студентов. Для начала добавьте группу.")
        else:
            return render_template('add_student_group.html', teacher = session['teacher'], groups=groups)

    @app.route('/teacher/add_student/<group>', methods=['GET', 'POST'])
    def add_student(group):
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        if request.method == 'POST':
            form_data = request.form.to_dict()
            full_name = form_data["full_name"]
            add_student_db(full_name, group)
            return redirect(url_for('add_student', group=group))
        students = sorted([student for (student,) in get_students_db(group)])
        return render_template('add_students.html', teacher=session['teacher'], students=students)

    @app.route('/teacher/view_results')
    def view_results():
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        results = []
        for group_dir in os.listdir(RESULTS_BASE_DIR):
            group_path = os.path.join(RESULTS_BASE_DIR, group_dir)
            if os.path.isdir(group_path):
                for filename in os.listdir(group_path):
                    if filename.endswith('.txt'):
                        file_path = os.path.join(group_path, filename)
                        # Добавляем только метаданные файла
                        results.append({
                            'group': group_dir,
                            'filename': filename,
                            'file_path': file_path,
                            'icon': f'/{STATIC_FOLDER}/images/document_icon.png'
                        })
        return render_template('view_results.html', results=results)

    @app.route('/teacher/view_result/<path:file_path>')
    def view_result_details(file_path):
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                group = os.path.basename(os.path.dirname(file_path))
                filename = os.path.basename(file_path)
                return render_template('view_result_details.html', content=content, group=group, filename=filename)
        except Exception as e:
            return render_template('view_result_details.html', error=f"Ошибка загрузки файла: {str(e)}")
    
    @app.route('/teacher/lab_list')
    def lab_list():
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        lab_topics = list(get_filenames().keys())
        return render_template('lab_list.html', lab_topics=lab_topics)
    
    @app.route('/teacher/lab_questions/<topic>')
    def lab_questions(topic):
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        if topic not in list(FILES_DICT.keys()):
            return render_template('lab_questions.html', error="Тема не найдена")
        questions = get_questions(topic).split("\n")
        return render_template('lab_questions.html', topic=topic, questions=questions)
