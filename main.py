import random

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from electives_app import crud, models, schemas
from electives_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/students/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students


@app.get("/elective_requests/", response_model=list[schemas.ElectiveRequest])
def read_elective_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    elective_requests = crud.get_elective_requests(db, skip=skip, limit=limit)
    return elective_requests


@app.post("/new_student/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_index(db, index=student.index)
    if db_student:
        raise HTTPException(status_code=400, detail="Index already taken")
    return crud.create_student(db=db, student=student)


@app.post("/new_elective_request/{index}/", response_model=schemas.ElectiveRequest)
def create_elective_request_for_student(
        index: int, elective_request: schemas.ElectiveRequestCreate, db: Session = Depends(get_db)
):
    return crud.create_elective_request(db=db, elective_request=elective_request, index=index)


@app.get("/assign_electives/{index}", response_model=list[schemas.ElectiveRequest])
def assign_electives(index: int, gpa: float, db: Session = Depends(get_db)):
    elective_requests = crud.get_elective_requests_by_student_index(db=db, student_index=index)
    print(elective_requests)
    if gpa < 4:
        print("Your gpa is too low to assign any electives. Good luck next semester!")
        return []
    elif gpa < 4.25:
        return [random.choice(elective_requests)]
    else:
        return elective_requests
