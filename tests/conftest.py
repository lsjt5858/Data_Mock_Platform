import sys
from pathlib import Path

# 将项目根目录加入 sys.path，便于测试导入
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))