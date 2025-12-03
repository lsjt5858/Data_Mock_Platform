from .base import BaseRepo
import uuid
from datetime import datetime

class ExportRepo(BaseRepo):
    """导出记录Repository"""
    
    def create(self, job_id, format_type, path=None):
        """
        创建导出记录
        
        Args:
            job_id: 任务ID
            format_type: 导出格式
            path: 文件路径
        
        Returns:
            导出ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        export_id = str(uuid.uuid4())
        
        cursor.execute('''
            INSERT INTO exports (id, job_id, format, path, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (export_id, job_id, format_type, path, 'pending'))
        
        conn.commit()
        return export_id
    
    def update_status(self, export_id, status, path=None, size=None):
        """更新导出状态"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if path and size:
            cursor.execute('''
                UPDATE exports
                SET status = ?, path = ?, size = ?
                WHERE id = ?
            ''', (status, path, size, export_id))
        else:
            cursor.execute('''
                UPDATE exports
                SET status = ?
                WHERE id = ?
            ''', (status, export_id))
        
        conn.commit()
    
    def get_by_id(self, export_id):
        """根据ID获取导出记录"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM exports WHERE id = ?', (export_id,))
        return cursor.fetchone()
    
    def list_all(self, limit=100):
        """列出所有导出记录"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM exports ORDER BY created_at DESC LIMIT ?', (limit,))
        return cursor.fetchall()
