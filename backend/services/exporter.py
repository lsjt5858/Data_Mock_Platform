"""
导出器：按 JSON/CSV/SQL 生成文件内容与文件名。
遵循需求文档的格式规则与文件名规则。
"""
import io
import csv
from typing import List, Dict, Any, Tuple
from datetime import datetime
from config import JSON_INDENT

def _now_str() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def generate_filename(ext: str) -> str:
    return f"data_export_{_now_str()}.{ext}"

def export_json(rows: List[Dict[str, Any]], pretty: bool = True) -> Tuple[str, str, int]:
    """
    JSON 导出：包装 data/total/generated_at，并返回字符串与文件名。
    """
    import json
    payload = {
        "data": rows,
        "total": len(rows),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    content = json.dumps(payload, ensure_ascii=False, indent=JSON_INDENT if pretty else None)
    name = generate_filename("json")
    size_kb = round(len(content.encode("utf-8")) / 1024, 2)
    return content, name, size_kb

def export_csv(rows: List[Dict[str, Any]], include_header: bool = True, delimiter: str = ",") -> Tuple[str, str]:
    """
    CSV 导出：使用标准库 csv，自动处理双引号转义与逗号包裹。
    """
    if not rows:
        # 空数据也返回空 CSV
        content = ""
        return content, generate_filename("csv")
    headers = list(rows[0].keys())
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
    if include_header:
        writer.writerow(headers)
    for r in rows:
        writer.writerow([r.get(h, "") if r.get(h, "") is not None else "NULL" for h in headers])
    content = buf.getvalue()
    return content, generate_filename("csv")

def _sql_escape(val: str) -> str:
    # 需求：字符串中的单引号用 \' 转义
    return val.replace("\\", "\\\\").replace("'", "\\'")

def export_sql(rows: List[Dict[str, Any]], table_name: str, include_header: bool = True, batch_size: int = 100) -> Tuple[str, str]:
    """
    SQL 导出：按批生成 INSERT 语句，遵循 NULL 与数字不加引号的规则。
    """
    if not rows:
        return "", generate_filename("sql")
    cols = list(rows[0].keys())
    statements: List[str] = []
    if include_header:
        statements.append(f"-- Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # 分批构造 VALUES
    def fmt_value(v: Any) -> str:
        if v is None:
            return "NULL"
        if isinstance(v, (int, float)):
            return str(v)
        # 其他类型按字符串处理
        return f"'{_sql_escape(str(v))}'"

    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        values = []
        for r in batch:
            values.append(f"({', '.join(fmt_value(r.get(c, None)) for c in cols)})")
        stmt = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES\n" + ",\n".join(values) + ";"
        statements.append(stmt)
    content = "\n".join(statements)
    return content, generate_filename("sql")