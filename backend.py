from typing import Union

from fastapi import FastAPI, HTTPException, status, Query, Response
from pydantic import BaseModel
from random import randrange

app = FastAPI()


my_list = [
    {"name": "Krish Kanojia", "level": 5, "marks": 99},
    {"name": "Rahul Garcia", "level": 8, "marks": 11},
]

class Student(BaseModel):
    name: str
    level: int
    marks: int
    
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/students")
def get_all_students():
    return {"data": my_list}

@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    student_dict = student.dict()
    for item in my_list:
        if student_dict["name"] in item["name"]:
            return {"Message" : "Username Already Exist"}
    my_list.append(student_dict)
    print(student)
    return {"data": student_dict}


@app.get("/students/latest")
def get_latest_student():
    latest_student = my_list[-1]
    return latest_student

@app.get("/student/{name}")
def get_student_by_name(name: str):
    student = find_student(name)
    print(f"student {student}")
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Student with Name {name} not found")
    return {"student_info" : student}


@app.delete("/student/{name}")
def delete_student(name: str):
    idx = student_index(name)
    if idx == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Student with Name {name} is NOT DELETED")
    my_list.pop(idx)
    return {"message" : f"Student {name} is DELETED SUCCESSFULLY"}

def find_student(name: str):
    temp_list = []
    for item in my_list:
        if name.lower() in item['name'].lower():
            temp_list.append(item)
    return temp_list


def student_index(name: str):
    for idx, item in enumerate(my_list):
        print(f"{idx}")
        if item["name"].lower() == name.lower():
            return idx
    return -1

