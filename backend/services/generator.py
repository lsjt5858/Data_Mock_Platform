"""
生成引擎：将字段配置映射到 Faker 方法，逐行生成数据。
支持 include_null 与 random_seed。
"""
import random
from time import perf_counter
from typing import Dict, Any, List
from datetime import date

from faker import Faker
from config import DEFAULT_LOCALE, NULL_PROBABILITY

def _should_be_null(include_null: bool) -> bool:
    return include_null and (random.random() < NULL_PROBABILITY)

def _gen_value(faker: Faker, field: Dict[str, Any]) -> Any:
    t = field.get("type")
    p = field.get("params", {})
    # 整数
    if t == "int":
        return faker.random_int(min=p.get("min_value", 1), max=p.get("max_value", 10000))
    # 浮点数
    if t == "float":
        return faker.pyfloat(
            min_value=p.get("min_value", 0.0),
            max_value=p.get("max_value", 999.99),
            left_digits=p.get("left_digits", 3),
            right_digits=p.get("right_digits", 2),
        )
    # 语义类型
    if t == "name":
        return faker.name()
    if t == "email":
        return faker.email()
    if t == "phone_number":
        return faker.phone_number()
    if t == "address":
        return faker.address().replace("\n", " ")
    # 日期
    if t == "date":
        start = p.get("start_date", "2020-01-01")
        end = p.get("end_date", "2024-12-31")
        d: date = faker.date_between(start_date=start, end_date=end)
        return d.isoformat()
    # 时间戳
    if t == "unix_time":
        return faker.unix_time()
    # 字符串
    if t == "string":
        length = p.get("length", 10)
        min_len = p.get("min_length", None)
        max_len = p.get("max_length", None)
        if isinstance(min_len, int) and isinstance(max_len, int):
            return faker.pystr(min_chars=min_len, max_chars=max_len)
        if isinstance(min_len, int) and max_len is None:
            return faker.pystr(min_chars=min_len, max_chars=min_len)
        if isinstance(max_len, int) and min_len is None:
            return faker.pystr(min_chars=max_len, max_chars=max_len)
        return faker.pystr(min_chars=length, max_chars=length)
    # 其他
    if t == "uuid":
        return faker.uuid4()
    if t == "boolean":
        return faker.pybool()  # 更稳定的 True/False
    if t == "ipv4":
        return faker.ipv4()
    if t == "credit_card_number":
        return faker.credit_card_number()
    if t == "company":
        return faker.company()
    if t == "job":
        return faker.job()
    # 未知类型兜底
    return None

def generate_rows(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    主入口：接受请求体，返回 rows/total/generated_at/generation_time_ms。
    - 初始化 Faker（应用 locale），并按 random_seed 设定种子
    - 逐行生成；每个字段独立；按 include_null 决定是否置 None
    """
    fields: List[Dict[str, Any]] = config["fields"]
    count: int = config["count"]
    include_null: bool = config.get("include_null", False)
    random_seed = config.get("random_seed", None)

    faker = Faker(locale=DEFAULT_LOCALE)
    # 保证可复现实验：将 Faker 实例与 random 都设定种子
    if isinstance(random_seed, int):
        Faker.seed(random_seed)
        faker.seed_instance(random_seed)
        random.seed(random_seed)

    start = perf_counter()
    rows: List[Dict[str, Any]] = []
    for _ in range(count):
        row: Dict[str, Any] = {}
        for f in fields:
            name = f["name"]
            if _should_be_null(include_null):
                row[name] = None
            else:
                row[name] = _gen_value(faker, f)
        rows.append(row)
    elapsed_ms = int((perf_counter() - start) * 1000)

    from datetime import datetime, timezone
    return {
        "rows": rows,
        "total": count,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generation_time_ms": elapsed_ms,
    }