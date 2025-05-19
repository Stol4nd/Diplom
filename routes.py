# routes.py
from flask import render_template, request, redirect, url_for, session
import ipaddress
import os
from config import TEACHER_PASSWORD, STATIC_FOLDER, RESULTS_BASE_DIR, FILES_DICT
from utils import save_results, get_questions, get_filenames
from tasks import tasks  # Импорт tasks из tasks.py

def configure_routes(app):
    @app.route('/')
    def index():
        return render_template('main.html')

    @app.route('/student', methods=['GET', 'POST'])
    def student():
        if request.method == 'POST':
            session['student_info'] = {
                'surname': request.form['surname'],
                'name': request.form['name'],
                'group': request.form['group']
            }
            session['current_task'] = 1
            session['results'] = {}
            return redirect(url_for('task'))
        return render_template('student.html')

    @app.route('/teacher', methods=['GET', 'POST'])
    def teacher():
        if request.method == 'POST':
            password = request.form.get('password')
            if password == TEACHER_PASSWORD:
                session['teacher_authenticated'] = True
                return redirect(url_for('teacher_dashboard'))
            else:
                return render_template('teacher.html', error="Неверный пароль")
        return render_template('teacher.html')

    @app.route('/teacher/dashboard')
    def teacher_dashboard():
        if not session.get('teacher_authenticated'):
            return redirect(url_for('teacher'))
        return render_template('teacher_dashboard.html')


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

    @app.route('/task', methods=['GET', 'POST'])
    def task():
        if 'student_info' not in session:
            return redirect(url_for('student'))
        
        task_num = session.get('current_task', 1)
        
        if task_num > 5:
            save_results(session['student_info'], session['results'])
            session.clear()
            return redirect(url_for('index'))
        
        if f'task_{task_num}' not in session:
            task = tasks[task_num]()
            task.generate_task()
            raw_task_data = task.__dict__
            task_data = {
                key: value 
                for key, value in raw_task_data.items() 
                if not isinstance(value, ipaddress.IPv4Network)
            }
            session[f'task_{task_num}'] = task_data
        
        task_data = session[f'task_{task_num}']
        
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
                results = task_obj.check_answers(student_answers)
            else:
                student_answers = request.form.to_dict()
                results = task_obj.check_answers(student_answers)
                
            session['results'][str(task_num)] = results
            session['current_task'] = task_num + 1
            return redirect(url_for('task'))
        
        return render_template(f'task_{task_num}.html', task_data=task_data)