import os

class Config:
    """应用配置类"""
    
    # 基础配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # 数据库配置
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'mock_platform.db')
    
    # 导出配置
    EXPORT_DIR = os.path.join(BASE_DIR, 'exports')
    
    # 生成配置
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10000))
    MAX_CONCURRENCY = int(os.getenv('MAX_CONCURRENCY', 4))
    DEFAULT_LOCALE = os.getenv('DEFAULT_LOCALE', 'zh_CN')
    
    # CORS配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    @classmethod
    def init_app(cls):
        """初始化应用所需的目录"""
        os.makedirs(os.path.dirname(cls.DATABASE_PATH), exist_ok=True)
        os.makedirs(cls.EXPORT_DIR, exist_ok=True)
