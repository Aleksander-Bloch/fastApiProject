from sqlalchemy.orm import Session

from . import models, schemas


def get_student_by_index(db: Session, index: int):
    return db.query(models.Student).filter(models.Student.index == index).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(index=student.index, name=student.name, surname=student.surname)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_elective_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ElectiveRequest).offset(skip).limit(limit).all()


def get_elective_requests_by_student_index(db: Session, student_index: int):
    return db.query(models.ElectiveRequest).join(models.ElectiveRequest.owner).filter(
        models.Student.index == student_index).all()


def create_elective_request(db: Session, elective_request: schemas.ElectiveRequestCreate, index: int):
    db_elective_request = models.ElectiveRequest(**elective_request.model_dump(), owner_id=index)
    db.add(db_elective_request)
    db.commit()
    db.refresh(db_elective_request)
    return db_elective_request
