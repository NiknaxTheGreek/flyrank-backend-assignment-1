from fastapi import FastAPI

app = FastAPI(title="Task API", version="1.0")

@app.get("/", summary="Describe the Task API", description="Return basic API metadata and the primary task collection endpoint.")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health check", description="Return a simple JSON response confirming that the API server is alive.")
def health():
    return {"status": "ok"}
