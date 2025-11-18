from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_html_page():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "FastAPI Calculation UI" in resp.text

def test_calc_alias_page():
    resp = client.get("/calc")
    assert resp.status_code == 200
    assert "FastAPI Calculation UI" in resp.text

def test_create_calculation_add():
    payload = {"type": "add", "a": 2, "b": 3}
    resp = client.post("/calculations/", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["a"] == 2
    assert data["b"] == 3
    assert data["type"] == "add"
    assert data["result"] == 5

def test_create_calculation_division_by_zero_fails():
    payload = {"type": "div", "a": 2, "b": 0}
    resp = client.post("/calculations/", json=payload)
    assert resp.status_code in (400, 422)

def test_invalid_type_fails():
    payload = {"type": "pow", "a": 2, "b": 3}
    resp = client.post("/calculations/", json=payload)
    assert resp.status_code == 422

def test_read_calculation_by_id():
    create_resp = client.post("/calculations/", json={"type": "mul", "a": 4, "b": 5})
    assert create_resp.status_code == 201
    created = create_resp.json()
    calc_id = created["id"]

    read_resp = client.get(f"/calculations/{calc_id}")
    assert read_resp.status_code == 200
    data = read_resp.json()
    assert data["id"] == calc_id
    assert data["result"] == 20
