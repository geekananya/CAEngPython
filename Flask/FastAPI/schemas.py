from typing import Optional     # doesnt work
from pydantic import BaseModel, EmailStr, conint


# defining type student so that all parameters dont need to be mentioned repeatedly.
class Student(BaseModel):
    id: int = None         # put gt 0 check
    name: str
    email: EmailStr = None
    avg_marks: Optional[float]
    course_id: int


class Course(BaseModel):
    course_id: int = None                  # pydantic models also validate different types of data eg. email
    name: str
    number_of_students: int
