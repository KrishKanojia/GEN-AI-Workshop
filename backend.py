from fastapi import FastAPI, HTTPException, status, Query, Response, Depends
from typing import Annotated
from pydantic import BaseModel
from random import randrange
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import func
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    
    # id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"auto_increment": True})


class Student(SQLModel, table=True):
    name: str = Field(index=True, primary_key=True)
    level: int | None = Field(default=0)
    marks: int
    

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread" : False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Create all table models
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Session to track changes in data
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/students")
def get_all_students(
    session: SessionDep
) -> list[Student]:
    students = session.exec(select(Student)).all()
    return students

@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student, session: SessionDep):
    session.add(student)
    session.commit()
    session.refresh(student)
    return {"data": student}


@app.get("/students/latest")
def get_latest_student(session: SessionDep) -> Student:
    student = session.exec(select(Student).order_by(Student.name)).first()
    return student

@app.get("/student/{name}")
def get_student_by_name(name: str, session: SessionDep) -> Student:
    student = session.exec(select(Student).where(func.lower(Student.name) == name.lower())).first()
    print(f"student {student}")
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Student with Name {name} not found")
    return student


@app.delete("/student/{name}")
def delete_student(name: str, session: SessionDep):
    student = session.exec(select(Student).where(func.lower(Student.name) == name.lower())).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Student with Name {name} is NOT DELETED")
    session.delete(student)
    session.commit()
    return {"message" : f"Student {name} is DELETED SUCCESSFULLY"}


