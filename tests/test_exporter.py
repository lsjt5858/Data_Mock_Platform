from backend.services.exporter import export_json, export_csv, export_sql


def test_export_json_payload_and_filename():
    rows = [{"id": 1, "email": "a@b.com"}]
    content, name, size_kb = export_json(rows, pretty=True)
    assert "\"data\"" in content and "\"total\"" in content and "\"generated_at\"" in content
    assert name.endswith(".json") and name.startswith("data_export_")
    assert size_kb > 0


def test_export_csv_header_and_content():
    rows = [{"id": 1, "email": "a@b.com"}, {"id": 2, "email": None}]
    content, name = export_csv(rows, include_header=True, delimiter=",")
    assert name.endswith(".csv")
    assert content.splitlines()[0] == "id,email"
    assert "NULL" in content  # None 应转为 NULL


def test_export_sql_basic():
    rows = [{"id": 1, "email": "a@b.com", "name": "O'Hara"}]
    content, name = export_sql(rows, table_name="users", include_header=True, batch_size=100)
    assert name.endswith(".sql")
    assert "INSERT INTO users" in content
    assert "\\'" in content  # 单引号应转义为 \'