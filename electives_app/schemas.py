from pydantic import BaseModel


class ElectiveRequestBase(BaseModel):
    subject_name: str
    description: str | None = None


class ElectiveRequestCreate(ElectiveRequestBase):
    pass


class ElectiveRequest(ElectiveRequestBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    index: int
    name: str
    surname: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int
    is_active: bool
    elective_requests: list[ElectiveRequest] = []

    class Config:
        orm_mode = True
