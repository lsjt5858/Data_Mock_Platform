from .faker_adapter import FakerAdapter
from .validator import Validator
from utils.logger import get_logger
import random

logger = get_logger(__name__)

class DataGenerator:
    """数据生成引擎"""
    
    def __init__(self, locale=None):
        self.faker_adapter = FakerAdapter(locale)
        self.validator = Validator()
        self.unique_values = {}  # 存储唯一字段的值集合
    
    def generate_row(self, schema, context=None):
        """
        生成单行数据
        
        Args:
            schema: 数据模式，包含 fields 列表
            context: 上下文数据（用于计算字段等）
        
        Returns:
            生成的数据行（字典）
        """
        row = {}
        context = context or {}
        
        fields = schema.get('fields', [])
        
        for field_config in fields:
            field_name = field_config['name']
            
            # 检查是否有计算表达式
            if 'calc_expr' in field_config:
                # TODO: 表达式求值（简化版，后续可用 simpleeval 库）
                row[field_name] = self._eval_expression(field_config['calc_expr'], row, context)
            # 检查是否有数据源引用
            elif 'source_ref' in field_config:
                # TODO: 从数据源获取值
                row[field_name] = None
            else:
                # 使用Faker生成
                value = self.faker_adapter.generate_value(field_config)
                
                # 唯一性检查
                if field_config.get('unique', False):
                    max_retries = 100
                    retry_count = 0
                    
                    while retry_count < max_retries:
                        if field_name not in self.unique_values:
                            self.unique_values[field_name] = set()
                        
                        is_unique, _ = self.validator.check_uniqueness(
                            value, field_name, self.unique_values[field_name]
                        )
                        
                        if is_unique:
                            self.unique_values[field_name].add(value)
                            break
                        
                        # 重新生成
                        value = self.faker_adapter.generate_value(field_config)
                        retry_count += 1
                    
                    if retry_count >= max_retries:
                        logger.warning(f"字段 {field_name} 唯一性生成失败，达到最大重试次数")
                
                # 约束验证
                is_valid, error_msg = self.validator.validate_field(value, field_config)
                if not is_valid:
                    logger.warning(f"字段验证失败: {error_msg}")
                
                row[field_name] = value
        
        return row
    
    def generate_batch(self, schema, count):
        """
        批量生成数据
        
        Args:
            schema: 数据模式
            count: 生成数量
        
        Returns:
            生成的数据列表
        """
        logger.info(f"开始生成 {count} 条数据")
        
        # 重置唯一值集合
        self.unique_values = {}
        
        data = []
        for i in range(count):
            row = self.generate_row(schema)
            data.append(row)
            
            # 每1000条记录日志
            if (i + 1) % 1000 == 0:
                logger.info(f"已生成 {i + 1}/{count} 条数据")
        
        logger.info(f"数据生成完成，共 {len(data)} 条")
        return data
    
    def preview_sample(self, schema, count=100):
        """
        生成采样预览
        
        Args:
            schema: 数据模式
            count: 采样数量，默认100
        
        Returns:
            采样数据列表
        """
        logger.info(f"生成预览采样，数量: {count}")
        return self.generate_batch(schema, min(count, 100))
    
    def _eval_expression(self, expr, row, context):
        """
        简单的表达式求值（简化版）
        
        Args:
            expr: 表达式字符串
            row: 当前行数据
            context: 上下文
        
        Returns:
            计算结果
        """
        # TODO: 实现安全的表达式求值
        # 可以使用 simpleeval 库或自定义解析器
        try:
            # 非常简化的实现，仅作示例
            return eval(expr, {"__builtins__": {}}, {**row, **context})
        except Exception as e:
            logger.error(f"表达式求值失败: {expr}, 错误: {e}")
            return None
