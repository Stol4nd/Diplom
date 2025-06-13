from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import date
from db_tables import Teacher, Labs, Group, TestResults, Student
from config import engine

def get_groups():
    groups = None
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
        results = session.query(TestResults.date, TestResults.test_score).where(TestResults.student_id == student_id).all()
    return results

def save_results(student_id, true_answers_amount, answers_amount):
    with Session(engine) as session:
        student = session.query(Student).filter(Student.id_student == student_id).first()
        new_result = TestResults(
            test_score = f"{true_answers_amount}/{answers_amount}", 
            student = student, 
            date = date.today(),
            passed = true_answers_amount == answers_amount)
        session.add(new_result)
        try:
            session.commit()
        except:
            session.rollback()

def get_group_results_db(group):
    with Session(engine) as session:
        results = (
            session.query(
                Student.full_name, 
                TestResults.date, 
                TestResults.test_score)
            .join(TestResults, Student.id_student == TestResults.student_id)
            .join(Group, Student.group_id == Group.id_group)
            .filter(Group.group_number == group)
            .order_by(Student.full_name, TestResults.date)
            .all()
            )
        return results
    
def get_courses_db():
    with Session(engine) as session:
        courses = (
            session.query(Labs.course)
            .distinct()
            .all()
        )
        return courses
    
def get_labs_for_course_db(course):
    with Session(engine) as session:
        labs = (
            session.query(Labs.title)
            .filter(Labs.course == course)
            .distinct()
            .all()
        )
        return labs
        
def get_file_id_db(lab):
    with Session(engine) as session:
        file_id = (
            session.query(Labs.gigachat_id, Labs.link)
            .filter(Labs.title == lab)
            .first()
        )
        return file_id