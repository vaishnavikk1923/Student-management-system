from fastapi import FastAPI
from pathlib import Path
import json
from pydantic import BaseModel
app = FastAPI(title="vaishnavi")

FILE = Path(__file__).parent / "students.json"

# reading students
def read_students():
    with open(FILE, "r",encoding="utf-8") as file:
        return json.load(file)

# save
def save_students(students):
    with open(FILE, "w",encoding="utf-8") as file:
        json.dump(students,file,indent=4)

class Student(BaseModel):
    name : str
    dept : str

# post
@app.post("/add_student")
def add_student(student : Student):
    students = read_students()
    new_student = {
        "id" : max([i["id"] for i in students], default = 0) + 1,
        "name" : student.name,
        "dept" : student.dept
    }
    students.append(new_student)
    save_students(students)

    return {"message" : "Student added successfully",
            "student" : new_student}




# put - update the existing content
@app.put("/update_student/{student_id}")
def update_student(student_id : int, student : Student):
    students = read_students()
    for s in students:
        if s["id"] == student_id:
            s["name"] = student.name
            s["dept"] = student.dept

            save_students(students)
            return {"message" : "Students details are updated",
                    "student" : s}

    return {"message" : "Id not found"}

# delete a student info
@app.delete("/delete_student/{student_id}")
def delete_student(student_id : int):
    students = read_students()
    for s in students:
        if s["id"] == student_id:
            students.remove(s)

            save_students(students)
            return {"message" : "student info got deleted",
                    "student" : s}
        
    return {"message" : "id not found"}

# path parameters
@app.get("/students/{student_id}")
def get_student_id(student_id : int):
    students = read_students()
    for student in students:
        if student["id"] == student_id:
            return student
    return {"message" : "id is invalid"}

# if i give the dept name, i want all the students in that dept.
@app.get("/students")
def get_student_dept(dept : str | None = None):
    students = read_students()
    if dept is None:
        return students
    result = []
    for student in students:
        if student["dept"] == dept:
            result.append(student)
    return result