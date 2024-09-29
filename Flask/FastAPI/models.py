from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    number_of_students = Column(Integer, default=0)

    students = relationship("Student", back_populates="course")

class Student(Base):        # schema name
    __tablename__ = 'students'   #table name

    id = Column(Integer, primary_key=True, index=True)
    name= Column(String, nullable=False)
    email = Column(String)
    avg_marks= Column(Float)
    course_id= Column(Integer, ForeignKey("courses.course_id"))

    course = relationship("Course", back_populates="students")