import pytest

from backend.services.validator import validate_config


def test_empty_fields_error():
    ok, errors = validate_config({"fields": [], "count": 10})
    assert not ok
    assert any(e["error_message"].startswith("至少需要添加1个字段") for e in errors)


def test_duplicate_field_names():
    payload = {
        "fields": [
            {"name": "id", "type": "int", "params": {"min_value": 1, "max_value": 10}},
            {"name": "id", "type": "int", "params": {"min_value": 1, "max_value": 10}},
        ],
        "count": 10,
    }
    ok, errors = validate_config(payload)
    assert not ok
    assert any("已存在" in e["error_message"] for e in errors)


def test_field_name_rules_and_length():
    payload = {
        "fields": [
            {"name": "1bad", "type": "int", "params": {"min_value": 1, "max_value": 10}},
            {"name": "a" * 51, "type": "int", "params": {"min_value": 1, "max_value": 10}},
        ],
        "count": 10,
    }
    ok, errors = validate_config(payload)
    assert not ok
    assert any("不能以数字开头" in e["error_message"] for e in errors)
    assert any("长度范围" in e["error_message"] for e in errors)


def test_unsupported_type():
    payload = {
        "fields": [{"name": "x", "type": "not_a_type", "params": {}}],
        "count": 10,
    }
    ok, errors = validate_config(payload)
    assert not ok
    assert any("类型不支持" in e["error_message"] for e in errors)


def test_int_params_validation():
    payload = {
        "fields": [{"name": "age", "type": "int", "params": {"min_value": 20, "max_value": 10}}],
        "count": 10,
    }
    ok, errors = validate_config(payload)
    assert not ok
    assert any("最小值不能大于最大值" in e["error_message"] for e in errors)


def test_date_params_validation():
    payload = {
        "fields": [{"name": "d", "type": "date", "params": {"start_date": "2025-12-31", "end_date": "2025-01-01"}}],
        "count": 10,
    }
    ok, errors = validate_config(payload)
    assert not ok
    assert any("起始日期不能晚于终止日期" in e["error_message"] for e in errors)


def test_string_params_validation():
    payload = {
        "fields": [{"name": "s", "type": "string", "params": {"length": 0}}],
        "count": 10,
    }
    ok, errors = validate_config(payload)
    assert not ok
    assert any("字符串长度范围" in e["error_message"] for e in errors)


def test_float_params_validation():
    payload = {
        "fields": [{
            "name": "price",
            "type": "float",
            "params": {"min_value": 100.0, "max_value": 10.0, "left_digits": -1, "right_digits": 2}
        }],
        "count": 10,
    }
    ok, errors = validate_config(payload)
    assert not ok
    # 两类错误都可能出现
    assert any("最小值不能大于最大值" in e["error_message"] or "位数必须为非负整数" in e["error_message"] for e in errors)


def test_random_seed_range():
    payload = {
        "fields": [{"name": "id", "type": "int", "params": {"min_value": 1, "max_value": 10}}],
        "count": 10,
        "random_seed": 1000000,
    }
    ok, errors = validate_config(payload)
    assert not ok
    assert any("随机种子范围" in e["error_message"] for e in errors)