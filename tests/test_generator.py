from backend.services.generator import generate_rows


def _base_fields():
    return [
        {"name": "id", "type": "int", "params": {"min_value": 1, "max_value": 10}},
        {"name": "email", "type": "email", "params": {}},
        {"name": "name", "type": "name", "params": {}},
    ]


def test_seed_reproducibility():
    cfg = {"fields": _base_fields(), "count": 20, "include_null": False, "random_seed": 42}
    a = generate_rows(cfg)["rows"]
    b = generate_rows(cfg)["rows"]
    assert a == b


def test_no_null_when_include_null_false():
    cfg = {"fields": _base_fields(), "count": 50, "include_null": False}
    rows = generate_rows(cfg)["rows"]
    assert all(v is not None for r in rows for v in r.values())