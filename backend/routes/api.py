"""
API 路由层：实现 4 个端点与统一响应格式。
- /api/generate：校验 + 生成引擎
- /api/export：按格式导出（JSON 返回包装，其余附件）
- /api/field-types：返回类型列表
- /api/validate-config：仅校验，不生成
"""
from flask import Blueprint, request, jsonify, make_response
from backend.services.validator import validate_config
from backend.services.generator import generate_rows
from backend.services.exporter import export_json, export_csv, export_sql
from backend.services.field_types import get_types

api_bp = Blueprint("api", __name__, url_prefix="/api")

def _ok(data):
    return jsonify({"code": 0, "message": "success", "data": data})

def _bad_request(msg):
    return jsonify({"code": 400, "message": msg, "data": None}), 400

def _server_error(msg):
    return jsonify({"code": 500, "message": msg, "data": None}), 500

@api_bp.route("/generate", methods=["POST"])
def generate():
    payload = request.get_json(force=True, silent=True) or {}
    is_valid, errors = validate_config(payload)
    if not is_valid:
        # 返回 400，并给出第一个错误提示
        first_msg = errors[0]["error_message"] if errors else "请求参数错误"
        return _bad_request(first_msg)
    try:
        result = generate_rows(payload)
        return _ok(result)
    except Exception as e:
        return _server_error(f"生成失败：{str(e)}")

@api_bp.route("/export", methods=["POST"])
def export():
    payload = request.get_json(force=True, silent=True) or {}
    rows = payload.get("data", [])
    fmt = payload.get("format", "csv")
    options = payload.get("options", {})

    try:
        if fmt == "json":
            pretty = bool(options.get("pretty", True))
            content, name, size_kb = export_json(rows, pretty=pretty)
            return _ok({"file_content": content, "file_name": name, "file_size_kb": size_kb})
        elif fmt == "csv":
            include_header = bool(options.get("include_header", True))
            delimiter = options.get("delimiter", ",")
            # 分隔符校验：必须为单字符字符串
            if not isinstance(delimiter, str) or len(delimiter) != 1:
                return _bad_request("分隔符不合法")
            content, name = export_csv(rows, include_header=include_header, delimiter=delimiter)
            resp = make_response(content)
            resp.headers["Content-Type"] = "text/plain; charset=utf-8"
            resp.headers["Content-Disposition"] = f"attachment; filename={name}"
            return resp
        elif fmt == "sql":
            table_name = options.get("table_name", "users")
            include_header = bool(options.get("include_header", True))
            # 批量大小校验：正整数且≤100
            try:
                batch_size = int(options.get("batch_size", 100))
            except Exception:
                return _bad_request("批量大小不合法")
            if batch_size < 1 or batch_size > 100:
                return _bad_request("批量大小范围：1-100")
            # 表名校验：仅字母/数字/下划线，长度 1-50
            import re
            if not isinstance(table_name, str) or len(table_name) == 0 or len(table_name) > 50 or not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table_name):
                return _bad_request("表名不合法")
            content, name = export_sql(rows, table_name=table_name, include_header=include_header, batch_size=batch_size)
            resp = make_response(content)
            resp.headers["Content-Type"] = "text/plain; charset=utf-8"
            resp.headers["Content-Disposition"] = f"attachment; filename={name}"
            return resp
        else:
            return _bad_request("导出格式不支持")
    except Exception as e:
        return _server_error(f"导出失败：{str(e)}")

@api_bp.route("/field-types", methods=["GET"])
def field_types():
    return _ok({"types": get_types()})

@api_bp.route("/validate-config", methods=["POST"])
def validate():
    payload = request.get_json(force=True, silent=True) or {}
    is_valid, errors = validate_config(payload)
    return _ok({"is_valid": is_valid, "errors": errors})