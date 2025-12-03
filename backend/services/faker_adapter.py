from faker import Faker
from datetime import datetime, timedelta
import random
import uuid
import re
from config import Config

class FakerAdapter:
    """Faker适配器，将字段类型映射到Faker生成方法"""
    
    def __init__(self, locale=None):
        self.locale = locale or Config.DEFAULT_LOCALE
        self.faker = Faker(self.locale)
    
    def generate_value(self, field_config):
        """
        根据字段配置生成值
        
        Args:
            field_config: 字段配置字典，包含 name, type, constraints, distribution 等
        
        Returns:
            生成的字段值
        """
        field_type = field_config.get('type', 'string')
        constraints = field_config.get('constraints', {})
        distribution = field_config.get('distribution', {})
        
        # 处理空值比例
        null_pct = constraints.get('null_pct', 0.0)
        if null_pct > 0 and random.random() < null_pct:
            return None
        
        # 基础类型
        if field_type == 'int':
            return self._generate_int(constraints, distribution)
        elif field_type == 'float':
            return self._generate_float(constraints, distribution)
        elif field_type == 'string':
            return self._generate_string(constraints)
        elif field_type == 'boolean':
            return self._generate_boolean()
        elif field_type == 'datetime':
            return self._generate_datetime(constraints, distribution)
        
        # 语义类型
        elif field_type == 'uuid':
            return str(uuid.uuid4())
        elif field_type == 'email':
            return self.faker.email()
        elif field_type == 'phone':
            return self.faker.phone_number()
        elif field_type == 'name':
            return self.faker.name()
        elif field_type == 'address':
            return self.faker.address()
        elif field_type == 'company':
            return self.faker.company()
        elif field_type == 'job':
            return self.faker.job()
        elif field_type == 'city':
            return self.faker.city()
        elif field_type == 'country':
            return self.faker.country()
        elif field_type == 'ipv4':
            return self.faker.ipv4()
        elif field_type == 'ipv6':
            return self.faker.ipv6()
        elif field_type == 'url':
            return self.faker.url()
        elif field_type == 'text':
            return self.faker.text(max_nb_chars=constraints.get('max_length', 200))
        elif field_type == 'paragraph':
            return self.faker.paragraph()
        elif field_type == 'sentence':
            return self.faker.sentence()
        
        # 枚举类型
        elif field_type == 'enum':
            values = field_config.get('values', [])
            weights = field_config.get('weights', None)
            if not values:
                return None
            if weights:
                return random.choices(values, weights=weights)[0]
            return random.choice(values)
        
        # 默认返回字符串
        return self.faker.word()
    
    def _generate_int(self, constraints, distribution):
        """生成整数"""
        min_val = constraints.get('min', 0)
        max_val = constraints.get('max', 100000)
        
        dist_type = distribution.get('type', 'uniform')
        
        if dist_type == 'uniform':
            return random.randint(min_val, max_val)
        elif dist_type == 'normal':
            mu = distribution.get('mu', (min_val + max_val) / 2)
            sigma = distribution.get('sigma', (max_val - min_val) / 6)
            value = int(random.gauss(mu, sigma))
            return max(min_val, min(max_val, value))
        else:
            return random.randint(min_val, max_val)
    
    def _generate_float(self, constraints, distribution):
        """生成浮点数"""
        min_val = constraints.get('min', 0.0)
        max_val = constraints.get('max', 1000.0)
        precision = constraints.get('precision', 2)
        
        dist_type = distribution.get('type', 'uniform')
        
        if dist_type == 'uniform':
            value = random.uniform(min_val, max_val)
        elif dist_type == 'normal':
            mu = distribution.get('mu', (min_val + max_val) / 2)
            sigma = distribution.get('sigma', (max_val - min_val) / 6)
            value = random.gauss(mu, sigma)
            value = max(min_val, min(max_val, value))
        else:
            value = random.uniform(min_val, max_val)
        
        return round(value, precision)
    
    def _generate_string(self, constraints):
        """生成字符串"""
        min_length = constraints.get('min_length', 1)
        max_length = constraints.get('max_length', 50)
        regex = constraints.get('regex', None)
        
        if regex:
            # 简单的正则匹配生成（可以使用 rstr 库进行更复杂的生成）
            return self.faker.bothify(text='?' * random.randint(min_length, max_length))
        
        length = random.randint(min_length, max_length)
        return self.faker.text(max_nb_chars=length).strip()
    
    def _generate_boolean(self):
        """生成布尔值"""
        return random.choice([True, False])
    
    def _generate_datetime(self, constraints, distribution):
        """生成日期时间"""
        dist_type = distribution.get('type', 'uniform')
        
        if dist_type == 'uniform':
            start = distribution.get('start', '2024-01-01')
            end = distribution.get('end', '2024-12-31')
            
            # 转换为datetime对象
            start_dt = datetime.fromisoformat(start) if isinstance(start, str) else start
            end_dt = datetime.fromisoformat(end) if isinstance(end, str) else end
            
            # 生成随机日期
            delta = end_dt - start_dt
            random_days = random.randint(0, delta.days)
            random_seconds = random.randint(0, 86400)
            
            result = start_dt + timedelta(days=random_days, seconds=random_seconds)
            return result.isoformat()
        
        return self.faker.date_time_this_year().isoformat()
