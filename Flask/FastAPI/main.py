from fastapi import FastAPI, Depends, HTTPException
import schemas, models
from sqlalchemy.orm import Session
from database import engine, SessionLocal

app = FastAPI()

# create db session instance
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(engine)    # initialise db with tables

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/students')           # read
async def fetch_students(limit=100, db: Session = Depends(get_db)):                     # add limit query param
    print(db.query(models.Student).all())
    students = db.query(models.Student).limit(limit).all()
    return students

@app.post("/students/create")    #create
async def create_student(req: schemas.Student, db: Session = Depends(get_db)):

    course = db.query(models.Course).filter(models.Course.course_id == req.course_id).first()
    if not course:
        raise HTTPException(status_code=400, detail="Course ID does not exist")

    new_student = models.Student(name=req.name, avg_marks=req.avg_marks, course_id=req.course_id)
    db.add(new_student)

    course.number_of_students += 1
    db.commit()
    db.refresh(new_student)
    return new_student

@app.put("/students/update")    #update
async def update_student(id: int, req: schemas.Student, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.course_id != req.course_id :
        new_course = db.query(models.Course).filter(models.Course.course_id == req.course_id).first()
        if not new_course:
            raise HTTPException(status_code=400, detail="New Course ID does not exist")
        old_course = db.query(models.Course).filter(models.Course.course_id == req.course_id).first()
        new_course.number_of_students += 1
        old_course.number_of_students -= 1

    student.name = req.name
    student.course_id = req.course_id
    student.email = req.email
    student.avg_marks = req.avg_marks
    return student

@app.delete("/students/delete")    #update
async def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.query(models.Course).filter(models.Course.course_id == student.course_id).first()
    course.number_of_students -= 1

    db.delete(student)
    db.commit()
    return student


@app.get('/students/{id}')           # read
async def fetch_student_from_id(id: int, db: Session = Depends(get_db)):                      # fastapi self validates arg and displays error message (pydantic model)
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# dynamic routes after static routes so that type validation doesnt make other nested routes erroneous.







# course routes

@app.post("/courses/create")    #create
async def create_course(req: schemas.Course, db: Session = Depends(get_db)):       # FastAPI's dependency injection
    new_course = models.Course(name=req.name, number_of_students=req.number_of_students)
    # add to db
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.put("/courses/update")    #update
async def update_course(id: int, new_name: str, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    course.name = new_name
    # id and #students cant be updated manually
    db.commit()
    db.refresh(course)
    return course


@app.delete("/courses/delete")    #delete
async def delete_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.number_of_students > 0:
        raise HTTPException(status_code=403, detail="Course can't be deleted as a student is enrolled in it.")

    db.delete(course)
    db.commit()
    return course


@app.get('/courses')           # read
async def fetch_courses(limit=100, db: Session = Depends(get_db)):
    print(db.query(models.Course).all())
    courses = db.query(models.Course).limit(limit).all()
    return courses


@app.get('/courses/{id}')           # read
async def fetch_course_from_id(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.course_id == id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course