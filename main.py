from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Read the assignment", "done": True},
]

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
