from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from electives_app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    index = Column(Integer, unique=True, index=True)
    name = Column(String)
    surname = Column(String)
    is_active = Column(Boolean, default=True)
    elective_requests = relationship("ElectiveRequest", back_populates="owner")


class ElectiveRequest(Base):
    __tablename__ = "elective_requests"

    id = Column(Integer, primary_key=True)
    subject_name = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("students.index"))
    owner = relationship("Student", back_populates="elective_requests")
