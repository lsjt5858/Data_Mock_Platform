"""
配置项：集中管理可调整参数，便于后续扩展与环境切换。
"""
from pathlib import Path

# SQLite 数据库文件路径（相对项目根目录）
DB_PATH = str(Path(__file__).parent / "data_generator.db")

# Faker 默认语言（中文环境，更符合国内手机号/地址格式）
DEFAULT_LOCALE = "zh_CN"

# include_null = true 时，返回 null 的概率
NULL_PROBABILITY = 0.3

# 导出文件生成的目录（当前实现返回内容，不落地文件；此项为后续扩展）
EXPORT_DIR = str(Path(__file__).parent)

# JSON 是否美化缩进（导出接口可覆盖）
JSON_INDENT = 4