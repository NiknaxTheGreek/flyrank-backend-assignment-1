from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
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

class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = None
    done: bool | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is not None:
            if not value.strip():
                raise ValueError("title must not be empty")
            return value.strip()
        return value

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})

def find_task(task_id: int):
    return next((task for task in tasks if task["id"] == task_id), None)

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
    task = find_task(task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return task

@app.post("/tasks", status_code=201, summary="Create a task", description="Create a new in-memory task with the next free id and done=false.")
def create_task(payload: TaskCreate):
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": payload.title, "done": False}
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", summary="Update a task", description="Update a task title and/or done state. Empty or invalid bodies return 400.")
def update_task(task_id: int, payload: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    supplied = payload.model_fields_set
    if not supplied or supplied.isdisjoint({"title", "done"}):
        return JSONResponse(status_code=400, content={"error": "Request body must include title and/or done"})
    if "title" in supplied:
        task["title"] = payload.title
    if "done" in supplied:
        task["done"] = payload.done
    return task

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task", description="Delete a task by id and return 204 No Content, or 404 when it does not exist.")
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    tasks.remove(task)
    return Response(status_code=204)
