import csv
import json
import os
from datetime import datetime
from utils.logger import get_logger
from config import Config

logger = get_logger(__name__)

class Exporter:
    """数据导出器"""
    
    def __init__(self):
        self.export_dir = Config.EXPORT_DIR
        os.makedirs(self.export_dir, exist_ok=True)
    
    def export_csv(self, data, filename=None):
        """
        导出为CSV格式
        
        Args:
            data: 数据列表（字典列表）
            filename: 文件名（可选）
        
        Returns:
            文件路径
        """
        if not data:
            raise ValueError("没有数据可导出")
        
        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.csv"
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = os.path.join(self.export_dir, filename)
        
        logger.info(f"开始导出CSV: {filepath}")
        
        # 获取所有字段名
        fieldnames = list(data[0].keys()) if data else []
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        file_size = os.path.getsize(filepath)
        logger.info(f"CSV导出完成: {filepath}, 大小: {file_size} bytes")
        
        return filepath
    
    def export_json(self, data, filename=None, pretty=True):
        """
        导出为JSON格式
        
        Args:
            data: 数据列表
            filename: 文件名（可选）
            pretty: 是否格式化输出
        
        Returns:
            文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(self.export_dir, filename)
        
        logger.info(f"开始导出JSON: {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            if pretty:
                json.dump(data, jsonfile, ensure_ascii=False, indent=2)
            else:
                json.dump(data, jsonfile, ensure_ascii=False)
        
        file_size = os.path.getsize(filepath)
        logger.info(f"JSON导出完成: {filepath}, 大小: {file_size} bytes")
        
        return filepath
    
    def export_ndjson(self, data, filename=None):
        """
        导出为NDJSON格式（每行一个JSON对象）
        
        Args:
            data: 数据列表
            filename: 文件名（可选）
        
        Returns:
            文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.ndjson"
        
        if not filename.endswith('.ndjson'):
            filename += '.ndjson'
        
        filepath = os.path.join(self.export_dir, filename)
        
        logger.info(f"开始导出NDJSON: {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as ndjsonfile:
            for item in data:
                ndjsonfile.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        file_size = os.path.getsize(filepath)
        logger.info(f"NDJSON导出完成: {filepath}, 大小: {file_size} bytes")
        
        return filepath
    
    def export(self, data, format_type='csv', filename=None):
        """
        统一导出接口
        
        Args:
            data: 数据列表
            format_type: 导出格式 ('csv', 'json', 'ndjson')
            filename: 文件名（可选）
        
        Returns:
            文件路径
        """
        if format_type == 'csv':
            return self.export_csv(data, filename)
        elif format_type == 'json':
            return self.export_json(data, filename)
        elif format_type == 'ndjson':
            return self.export_ndjson(data, filename)
        else:
            raise ValueError(f"不支持的导出格式: {format_type}")
