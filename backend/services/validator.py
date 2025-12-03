import re

class Validator:
    """字段约束验证器"""
    
    @staticmethod
    def validate_field(value, field_config):
        """
        验证字段值是否满足约束
        
        Args:
            value: 字段值
            field_config: 字段配置，包含约束
        
        Returns:
            (is_valid, error_message): 验证是否通过和错误消息
        """
        if value is None:
            # 空值检查
            null_pct = field_config.get('constraints', {}).get('null_pct', 0.0)
            if null_pct == 0:
                return False, f"字段 {field_config['name']} 不允许为空"
            return True, None
        
        constraints = field_config.get('constraints', {})
        field_type = field_config.get('type', 'string')
        
        # 数值范围验证
        if field_type in ['int', 'float']:
            if 'min' in constraints and value < constraints['min']:
                return False, f"字段 {field_config['name']} 值 {value} 小于最小值 {constraints['min']}"
            if 'max' in constraints and value > constraints['max']:
                return False, f"字段 {field_config['name']} 值 {value} 大于最大值 {constraints['max']}"
        
        # 字符串长度验证
        if field_type == 'string' or isinstance(value, str):
            if 'min_length' in constraints and len(value) < constraints['min_length']:
                return False, f"字段 {field_config['name']} 长度不足"
            if 'max_length' in constraints and len(value) > constraints['max_length']:
                return False, f"字段 {field_config['name']} 长度超出限制"
            
            # 正则验证
            if 'regex' in constraints:
                pattern = constraints['regex']
                if not re.match(pattern, value):
                    return False, f"字段 {field_config['name']} 不符合正则规则 {pattern}"
        
        return True, None
    
    @staticmethod
    def check_uniqueness(value, field_name, seen_values):
        """
        检查唯一性
        
        Args:
            value: 字段值
            field_name: 字段名
            seen_values: 已见过的值的集合
        
        Returns:
            (is_unique, error_message)
        """
        if value in seen_values:
            return False, f"字段 {field_name} 值 {value} 重复"
        return True, None
