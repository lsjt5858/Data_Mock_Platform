"""
校验器：实现需求文档中的 VR 规则，并返回详细错误列表。
"""
import re
from typing import Dict, Any, List, Tuple
from backend.services.field_types import get_types

FIELD_NAME_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

def validate_config(payload: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
    errors: List[Dict[str, Any]] = []

    fields = payload.get("fields", [])
    count = payload.get("count")
    include_null = payload.get("include_null", False)
    random_seed = payload.get("random_seed", None)

    # 支持类型白名单（来源于缓存/数据库）
    supported_types = {t["type_name"] for t in get_types()}

    # VR-2.2.3.1 至少1个字段
    if not fields or len(fields) == 0:
        errors.append({"field_index": -1, "field_name": None, "error_message": "至少需要添加1个字段"})

    # VR-2.2.3.2 字段名重复
    seen = set()
    for i, f in enumerate(fields):
        name = f.get("name", "")
        if name in seen:
            errors.append({"field_index": i, "field_name": name, "error_message": f"字段'{name}'已存在"})
        else:
            seen.add(name)

    # VR-2.2.3.3 字段名合法
    for i, f in enumerate(fields):
        name = f.get("name", "")
        if not FIELD_NAME_RE.match(name):
            errors.append({"field_index": i, "field_name": name, "error_message": "字段名只能包含字母、数字、下划线，且不能以数字开头"})
        # 长度 1-50
        if not isinstance(name, str) or len(name) < 1 or len(name) > 50:
            errors.append({"field_index": i, "field_name": name, "error_message": "字段名长度范围：1-50"})

    # VR-2.2.3.4 count 范围
    if not isinstance(count, int) or count < 1 or count > 100000:
        errors.append({"field_index": -1, "field_name": None, "error_message": "数据行数范围：1-100000"})

    # 类型合法性校验
    for i, f in enumerate(fields):
        t = f.get("type")
        if not isinstance(t, str) or t not in supported_types:
            errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "字段类型不支持"})

    # 字段参数校验（整数、日期、字符串、浮点）
    for i, f in enumerate(fields):
        t = f.get("type")
        p = f.get("params", {})
        if t == "int":
            min_v = p.get("min_value", 1)
            max_v = p.get("max_value", 10000)
            if not isinstance(min_v, int) or not isinstance(max_v, int):
                errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "整数参数必须为整数"})
            elif min_v > max_v:
                errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "最小值不能大于最大值"})
        elif t == "float":
            min_v = p.get("min_value", 0.0)
            max_v = p.get("max_value", 999.99)
            left_d = p.get("left_digits", 3)
            right_d = p.get("right_digits", 2)
            if not isinstance(min_v, (int, float)) or not isinstance(max_v, (int, float)):
                errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "浮点数范围参数必须为数字"})
            elif float(min_v) > float(max_v):
                errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "最小值不能大于最大值"})
            if not isinstance(left_d, int) or not isinstance(right_d, int) or left_d < 0 or right_d < 0:
                errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "浮点数字段位数必须为非负整数"})
        elif t == "date":
            start = p.get("start_date", "2020-01-01")
            end = p.get("end_date", "2024-12-31")
            if str(start) > str(end):  # YYYY-MM-DD 字符串比较足够
                errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "起始日期不能晚于终止日期"})
        elif t == "string":
            length = p.get("length", 10)
            if not isinstance(length, int) or length < 1 or length > 1000:
                errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "字符串长度范围：1~1000"})
            min_len = p.get("min_length", None)
            max_len = p.get("max_length", None)
            if min_len is not None and max_len is not None and min_len > max_len:
                errors.append({"field_index": i, "field_name": f.get("name"), "error_message": "字符串最小长度不能大于最大长度"})

    # random_seed 校验（可选）
    if random_seed is not None:
        if not isinstance(random_seed, int) or random_seed < 0 or random_seed > 999999:
            errors.append({"field_index": -1, "field_name": None, "error_message": "随机种子范围：0-999999"})

    return (len(errors) == 0), errors