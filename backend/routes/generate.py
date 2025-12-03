from flask import Blueprint, request, jsonify
from services import DataGenerator
from utils.logger import get_logger

logger = get_logger(__name__)

generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/api/generate', methods=['POST'])
def generate_data():
    """
    生成数据API
    
    请求体示例:
    {
        "fields": [
            {"name": "user_id", "type": "uuid", "unique": true},
            {"name": "email", "type": "email"},
            {"name": "age", "type": "int", "constraints": {"min": 18, "max": 80}}
        ],
        "count": 100,
        "preview": true
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "请求体不能为空"}), 400
        
        fields = data.get('fields', [])
        count = data.get('count', 100)
        preview = data.get('preview', False)
        
        if not fields:
            return jsonify({"error": "字段列表不能为空"}), 400
        
        if count <= 0 or count > 1000000:
            return jsonify({"error": "数量必须在1到1000000之间"}), 400
        
        # 构建schema
        schema = {
            "fields": fields
        }
        
        # 初始化生成器
        generator = DataGenerator()
        
        # 如果是预览模式，只生成少量数据
        if preview:
            result_data = generator.preview_sample(schema, min(count, 100))
            return jsonify({
                "data": result_data,
                "total": len(result_data),
                "preview": True
            })
        
        # 批量生成
        result_data = generator.generate_batch(schema, count)
        
        return jsonify({
            "data": result_data,
            "total": len(result_data),
            "preview": False
        })
    
    except Exception as e:
        logger.error(f"生成数据失败: {str(e)}")
        return jsonify({"error": f"生成失败: {str(e)}"}), 500


@generate_bp.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({"status": "ok", "message": "Data Mock Platform API is running"})
