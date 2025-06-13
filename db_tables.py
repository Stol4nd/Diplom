from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, Session, validates
import re


Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teacher'
    id_teacher = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    
class Labs(Base):
    __tablename__ = 'labs'
    id_lab = Column(Integer, primary_key=True, autoincrement=True)
    course = Column(String, nullable=False)
    title = Column(String, nullable=False)
    gigachat_id = Column(String)
    link = Column(String, nullable=False)   


class Group(Base):
    __tablename__ = 'groups'
    id_group = Column(Integer, primary_key=True, autoincrement=True)
    group_number = Column(String, nullable=False)
    
    students = relationship("Student", back_populates="group")
    

class TestResults(Base):
    __tablename__ = 'test_results'
    id_test = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id_student'))
    test_score = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    passed = Column(Boolean, nullable=False)
    
    student = relationship("Student", back_populates="test_results")
    
    @validates('test_score')
    def validate_test_score(self, key, value):
        if not re.match(r'^\d+/\d+$', value):
            raise ValueError(f'test_score должен быть в формате "число/число" (например, "85/100"). Данное значение {value}')
        try:
            score, total = map(int, value.split('/'))
            if score > total:
                raise ValueError('Полученный балл не может быть больше максимального')
        except ValueError:
            raise ValueError('Некорректный формат чисел в test_score')
        return value
    

class Student(Base):
    __tablename__ = 'students'
    id_student = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id_group'))
    
    group = relationship("Group", back_populates="students")
    test_results = relationship("TestResults", back_populates="student")
    
# engine = create_engine('sqlite:///labs.db', echo=True)
# Base.metadata.create_all(engine)
# with Session(engine) as session:
#     zhukovskyi = Teacher(
#         full_name = "Жуковский В.Е.",
#         login = "zhukovskyive",
#         password = "zhukovskyive"
#     )
#     matrohina = Teacher(
#         full_name = "Матрохина К.В.",
#         login = "matrohinakv",
#         password = "matrohinakv"
#     )
#     session.add_all([zhukovskyi, matrohina])
#     session.commit()