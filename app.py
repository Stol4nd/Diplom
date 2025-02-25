from flask import Flask, render_template, request, redirect, url_for, session
import os
import ipaddress
from Task_1 import Task_1
from Task_2 import Task_2
from Task_3 import Task_3
from Task_4 import Task_4
from Task_5 import Task_5

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Needed for session management

# Создадим словарь с классами заданий для контрольной работы студентов
tasks = {
    1: Task_1,
    2: Task_2,
    3: Task_3,
    4: Task_4,
    5: Task_5
}

# Директория для загрузки результатов выполнения контрольной работы студентов
RESULTS_DIR = "student_results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# Обработка запросов к главной странице
@app.route('/')
def index():
    return render_template('index.html')

# Обработка запросов к странице студентов, здесь студент должен заполнить свои фамилию, имя и группу. Сервер запоминает эти данные, и в дальнейшем проверяет на их наличие в параметрах сессии
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

# Обработка зпросов к странице преподавателей, здесь преподаватель может посмотреть результаты сделанных контрольных работ студентами
@app.route('/teacher')
def teacher():
    results = []
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith('.txt'):
            with open(os.path.join(RESULTS_DIR, filename), 'r') as f:
                content = f.read()
                results.append({
                    'filename': filename,
                    'content': content
                })
    return render_template('teacher.html', results=results)

# Страница с формированием заданий для студентов. Данная страница является адаптируемой, то есть для каждого задания формируется своя страница, на которой студенту необходимо дать ответы на вопросы задания
@app.route('/task', methods=['GET', 'POST'])
def task():
    # Если данных о студенте нет в параметрах сессии, то необходимо отправить студента на страницу заполнения данных
    if 'student_info' not in session:
        return redirect(url_for('student'))
    
    # Также в параметрах сессии находится номер задания, который выполняет студент, от номера задания зависит, какой шаблон будет запущен для студента.
    task_num = session.get('current_task', 1)
    
    # Проверка на количество заданий в контрольной работе, если последнее выполненное задание было 5ым, то необходимо записать результаты выполения задания в файл, очистить сессию пользователя и перекинуть его на домашнюю страницу
    if task_num > 5:  
        student_id = f"{session['student_info']['surname']}_{session['student_info']['name']}_{session['student_info']['group']}"  # Создаем название файла для студента и открываем его на запись
        with open(os.path.join(RESULTS_DIR, f"{student_id}.txt"), 'w') as f:
            # print(session['results'])
            for t_num, result in session['results'].items():
                f.write(f"Task {t_num}:\n")
                if t_num == '5':
                    for subnet_num, subnet_result in enumerate(result):  # Для каждой подсети выполняем запись результатов оценки задания студента
                        f.write(f"Subnet {subnet_num + 1}:\n")
                        for key, value in subnet_result.items():
                            f.write(f"{key}: {value}\n")
                else:
                    for key, value in result.items():
                        f.write(f"{key}: {value}\n")
                f.write("\n")
        session.clear()  # Очищаем параметры сессии
        return redirect(url_for('index'))
    
    # Создаем новое задание в сессии пользователя, если его еще нет. Генерируем задание и запоминаем для дальнейшей передачи на страницу задания
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
    
    # Если метод отправки 'POST', значит студент отправил свой ответ на сервер и необходимо его обработакть, т.е. проверить на правильность ответы и записать.
    if request.method == 'POST':
        # Создаем новый объект класса, что в дальнейшем проверять результат выполнения задания. Мы не можем хранить данный экземпляр в сессии, так как он не может быть сериализован в JSON тип данных.
        task_obj = tasks[task_num]()
        # Восстанавливаем состояние объекта из сохраненных данных в task_data
        task_obj.__dict__.update(task_data)
        if task_num == 5:
            # Если выполнено задание под номером 5, то необходимо преобразовать словарь ответов студента в список словарей для каждой подсети
            student_answers = []
            form_data = request.form.to_dict()  # Получаем все данные формы как один словарь
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

if __name__ == '__main__':
    app.run(debug=True)