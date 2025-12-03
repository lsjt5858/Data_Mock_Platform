from models.database import get_db

class BaseRepo:
    """基础Repository类"""
    
    def __init__(self):
        self.db = None
    
    def get_connection(self):
        """获取数据库连接"""
        if not self.db:
            self.db = get_db()
        return self.db
    
    def close(self):
        """关闭数据库连接"""
        if self.db:
            self.db.close()
            self.db = None
