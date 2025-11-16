import json

from app import create_app


def test_generate_endpoint_success():
    app = create_app()
    client = app.test_client()
    payload = {
        "fields": [
            {"name": "id", "type": "int", "params": {"min_value": 1, "max_value": 10}},
            {"name": "email", "type": "email", "params": {}},
        ],
        "count": 5,
    }
    resp = client.post("/api/generate", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["code"] == 0
    assert "rows" in data["data"] and data["data"]["total"] == 5


def test_generate_endpoint_validation_error():
    app = create_app()
    client = app.test_client()
    payload = {"fields": [], "count": 0}
    resp = client.post("/api/generate", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["code"] == 400


def test_export_csv_endpoint_success():
    app = create_app()
    client = app.test_client()
    payload = {
        "data": [{"id": 1, "email": "a@b.com"}],
        "format": "csv",
        "options": {"include_header": True, "delimiter": ","}
    }
    resp = client.post("/api/export", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    assert resp.headers["Content-Disposition"].endswith(".csv")


def test_export_sql_invalid_batch_size():
    app = create_app()
    client = app.test_client()
    payload = {
        "data": [{"id": 1, "email": "a@b.com"}],
        "format": "sql",
        "options": {"table_name": "users", "batch_size": 1000, "include_header": True}
    }
    resp = client.post("/api/export", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["message"] == "批量大小范围：1-100"