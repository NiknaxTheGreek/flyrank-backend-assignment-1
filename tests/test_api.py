from copy import deepcopy

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)
INITIAL = deepcopy(main.tasks)

def setup_function():
    main.tasks[:] = deepcopy(INITIAL)

def test_root_and_health():
    assert client.get("/").json() == {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}
    assert client.get("/health").json() == {"status": "ok"}

def test_list_and_get():
    r = client.get("/tasks")
    assert r.status_code == 200 and len(r.json()) == 3
    assert set(r.json()[0]) == {"id", "title", "done"}
    assert client.get("/tasks/1").status_code == 200

def test_missing_get_error_shape():
    r = client.get("/tasks/99")
    assert r.status_code == 404 and r.json() == {"error": "Task 99 not found"}

def test_create_201_and_done_false():
    r = client.post("/tasks", json={"title": "Buy milk"})
    assert r.status_code == 201
    assert r.json() == {"id": 4, "title": "Buy milk", "done": False}
    assert len(client.get("/tasks").json()) == 4

def test_create_invalid_title_400_error_shape():
    for payload in ({}, {"title": ""}, {"title": "   "}):
        r = client.post("/tasks", json=payload)
        assert r.status_code == 400 and "error" in r.json()

def test_update_title_only():
    r = client.put("/tasks/1", json={"title": "Changed"})
    assert r.status_code == 200 and r.json()["title"] == "Changed" and r.json()["done"] is False

def test_update_done_only():
    r = client.put("/tasks/1", json={"done": True})
    assert r.status_code == 200 and r.json()["done"] is True and r.json()["title"] == "Learn FastAPI"

def test_update_both():
    r = client.put("/tasks/1", json={"title": "Changed", "done": True})
    assert r.status_code == 200 and r.json() == {"id": 1, "title": "Changed", "done": True}

def test_update_empty_invalid_and_missing():
    r = client.put("/tasks/1", json={})
    assert r.status_code == 400 and "error" in r.json()
    r = client.put("/tasks/1", json={"title": ""})
    assert r.status_code == 400 and "error" in r.json()
    r = client.put("/tasks/99", json={"done": True})
    assert r.status_code == 404 and r.json() == {"error": "Task 99 not found"}

def test_delete_204_empty_and_missing_404():
    r = client.delete("/tasks/1")
    assert r.status_code == 204 and r.content == b""
    r = client.delete("/tasks/99")
    assert r.status_code == 404 and r.json() == {"error": "Task 99 not found"}

def test_swagger_and_openapi_descriptions():
    assert client.get("/docs").status_code == 200
    spec = client.get("/openapi.json").json()
    for path, method in [
        ("/", "get"), ("/health", "get"), ("/tasks", "get"), ("/tasks", "post"),
        ("/tasks/{task_id}", "get"), ("/tasks/{task_id}", "put"), ("/tasks/{task_id}", "delete")
    ]:
        op = spec["paths"][path][method]
        assert op.get("summary") and op.get("description")
