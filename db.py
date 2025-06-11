from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import date
from db_tables import Teacher, Labs, Group, TestResults, Student


engine = create_engine('sqlite:///labs.db', echo=True)

def get_groups():
    groups = ""
    with Session(engine) as session:
        groups = session.query(Group.group_number).all()
    return groups

def get_teacher_id(login, password):
    with Session(engine) as session:
        teacher_id = session.query(Teacher.full_name).where(Teacher.login == str(login)).where(Teacher.password == str(password)).all()
    return teacher_id

def add_group_db(group_num):
    with Session(engine) as session:
        new_group = Group(group_number=group_num)
        session.add(new_group)
        group_id = session.query(Group.id_group).where(Group.group_number == group_num).all()
        session.commit()
    return group_id

def get_students_db(group_num):
    with Session(engine) as session:
        students = session.query(Student.full_name).join(Group.students).where(Group.group_number == group_num).all()
    return students

def add_student_db(full_name, group_num):
    with Session(engine) as session:
        group = session.query(Group).filter(Group.group_number == group_num).first()
        new_student = Student(full_name = full_name, group = group)
        session.add(new_student)
        session.commit()
        
def get_student_id_db(student):
    with Session(engine) as session:
        student_id = session.query(Student.id_student).where(Student.full_name == student).first()
        return student_id

def get_student_results_db(student_id):
    with Session(engine) as session:
        results = session.query(TestResults.test_score).where(TestResults.student_id == student_id).all()
    return results

def save_results(student_id, true_answers_amount, answers_amount):
    with Session(engine) as session:
        student = session.query(Student).filter(Student.id_student == student_id).first()
        new_result = TestResults(test_score = f"{true_answers_amount}/{answers_amount}", student = student, date = date.today())
        session.add(new_result)
        try:
            session.commit()
        except:
            session.rollback()