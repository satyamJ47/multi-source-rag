from fastapi import FastAPI
import uuid
from pydantic import BaseModel

app = FastAPI()

todos = []

@app.get("/")
def read_root():
    return {"messsage":"hello world 2"}

# query parameters example
# @app.post("/todo")
# def add(todo,status=False):
#     id = str(uuid.uuid4())
#     print(id)
#     todos.append({"id":id,"todo":todo,"is_done":status})
#     return {"message","todo created"}


class Todo(BaseModel):
    todo: str
    status: bool

# post request
@app.post("/todo")
def add(todo:Todo):
    id = str(uuid.uuid4())
    todos.append({
        "id":id,
        "todo":todo.todo,
        "is_done":todo.status
    })
    return {
        "message":"todo created",
        "todo":todo
    }

@app.get("/todos")
def retrive():
    return todos

@app.get("/todo/{todo_id}")
def get_todo(todo_id:str):
    todo = [todo for todo in todos if todo["id"]==todo_id]
    return todo

