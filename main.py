from typing import Any

from fastapi import Body, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, field_validator

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Read the assignment", "done": True},
]

class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must not be empty")
        return value.strip()

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})

@app.get("/", summary="Describe the Task API", description="Return basic API metadata and the primary task collection endpoint.")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health check", description="Return a simple JSON response confirming that the API server is alive.")
def health():
    return {"status": "ok"}

@app.get("/tasks", summary="List tasks", description="Return every task currently stored in memory.")
def list_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary="Get one task", description="Return one task by numeric id, or a 404 JSON error when it does not exist.")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.post("/tasks", status_code=201, summary="Create a task", description="Create a new in-memory task with the next free id and done=false.")
def create_task(payload: TaskCreate):
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": payload.title, "done": False}
    tasks.append(task)
    return task
