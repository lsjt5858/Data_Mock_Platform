"""
SQLite 初始化与字段类型表定义、种子数据插入。
"""
import sqlite3
from typing import List, Dict
from pathlib import Path
from datetime import datetime

from config import DB_PATH

def get_connection():
    # 创建 SQLite 连接；row_factory 将每行转为 dict-like
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    初始化数据库与表结构，并插入 15 种字段类型的预置数据。
    在应用启动时调用一次，支持幂等（重复启动不会重复插入）。
    """
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cur = conn.cursor()
    # 创建字段类型表
    cur.execute("""
    CREATE TABLE IF NOT EXISTS field_types (
      id INTEGER PRIMARY KEY,
      type_name VARCHAR(50) UNIQUE NOT NULL,
      type_label VARCHAR(100),
      faker_method VARCHAR(100),
      description TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    # 检查是否已有数据
    cur.execute("SELECT COUNT(1) AS cnt FROM field_types;")
    cnt = cur.fetchone()["cnt"]
    if cnt == 0:
        # 插入 15 种类型（type_name 与 faker_method 映射）
        seed: List[Dict] = [
            {"id": 1, "type_name": "int", "type_label": "整数", "faker_method": "random_int"},
            {"id": 2, "type_name": "float", "type_label": "浮点数", "faker_method": "pyfloat"},
            {"id": 3, "type_name": "name", "type_label": "姓名", "faker_method": "name"},
            {"id": 4, "type_name": "email", "type_label": "邮箱", "faker_method": "email"},
            {"id": 5, "type_name": "phone_number", "type_label": "手机号", "faker_method": "phone_number"},
            {"id": 6, "type_name": "address", "type_label": "地址", "faker_method": "address"},
            {"id": 7, "type_name": "date", "type_label": "日期", "faker_method": "date_between"},
            {"id": 8, "type_name": "unix_time", "type_label": "时间戳", "faker_method": "unix_time"},
            {"id": 9, "type_name": "string", "type_label": "字符串", "faker_method": "pystr"},
            {"id": 10, "type_name": "uuid", "type_label": "UUID", "faker_method": "uuid4"},
            {"id": 11, "type_name": "boolean", "type_label": "布尔值", "faker_method": "boolean"},
            {"id": 12, "type_name": "ipv4", "type_label": "IP地址", "faker_method": "ipv4"},
            {"id": 13, "type_name": "credit_card_number", "type_label": "信用卡号", "faker_method": "credit_card_number"},
            {"id": 14, "type_name": "company", "type_label": "公司名", "faker_method": "company"},
            {"id": 15, "type_name": "job", "type_label": "职位", "faker_method": "job"},
        ]
        for s in seed:
            cur.execute(
                "INSERT INTO field_types (id, type_name, type_label, faker_method, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (s["id"], s["type_name"], s["type_label"], s["faker_method"], None, datetime.utcnow()),
            )
    conn.commit()
    conn.close()