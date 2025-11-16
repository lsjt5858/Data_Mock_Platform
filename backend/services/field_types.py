"""
字段类型服务：启动时从 SQLite 加载到内存缓存。
同时提供 required_params 与 default_params，供前端/校验使用。
"""
from typing import Dict, Any, List
from backend.models.db import get_connection
from config import DEFAULT_LOCALE

# 预置的必填参数与默认参数（与需求文档一致）
REQUIRED_PARAMS: Dict[str, List[str]] = {
    "int": ["min_value", "max_value"],
    "float": ["min_value", "max_value"],  # left_digits/right_digits 可选
    "date": ["start_date", "end_date"],
    "string": ["length"],  # min_length/max_length 可选
}
DEFAULT_PARAMS: Dict[str, Dict[str, Any]] = {
    "int": {"min_value": 1, "max_value": 10000},
    "float": {"min_value": 0.0, "max_value": 999.99, "left_digits": 3, "right_digits": 2},
    "date": {"start_date": "2020-01-01", "end_date": "2024-12-31"},
    "string": {"length": 10}
}

_CACHE: Dict[str, Dict[str, Any]] = {}

def load_types() -> Dict[str, Dict[str, Any]]:
    """
    从数据库加载类型，并填充辅助信息到缓存。
    """
    global _CACHE
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, type_name, type_label, faker_method FROM field_types ORDER BY id ASC;")
    rows = cur.fetchall()
    conn.close()
    _CACHE = {}
    for r in rows:
        type_name = r["type_name"]
        _CACHE[type_name] = {
            "type_id": r["id"],
            "type_name": type_name,
            "type_label": r["type_label"],
            "faker_method": r["faker_method"],
            "required_params": REQUIRED_PARAMS.get(type_name, []),
            "default_params": DEFAULT_PARAMS.get(type_name, {}),
        }
    return _CACHE

def get_types() -> List[Dict[str, Any]]:
    """
    提供给 GET /api/field-types 使用。
    """
    if not _CACHE:
        load_types()
    return list(_CACHE.values())