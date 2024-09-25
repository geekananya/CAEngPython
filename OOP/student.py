from select import select


class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

    def greet(self):
        print("Hello i am a person")

class Student(Person):
    def __init__(self, name, age, city, student_id):
        super().__init__(name, age, city)
        self.student_id = student_id
        self.courses = []

    def enroll(self, course):
        self.courses.append(course)
        course.add_student(self)

    def list_courses(self):
        return [course.name for course in self.courses]

    def greet(self):        # method overriding
        print("Hello i am a student")

class Course:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def list_students(self):
        return [student.name for student in self.students]


math_course = Course('Mathematics')

student1 = Student('Alice', 20, 'Delhi', 'S001')
student2 = Student('Bob', 21, 'Pune', 'S002')

student1.enroll(math_course)
student2.enroll(math_course)

student1.greet()
print("Courses enrolled:", student1.list_courses())
print("Students in the course:", math_course.list_students())

student2.greet()
print("Courses enrolled:", student2.list_courses())
