from flask import Blueprint, request, jsonify, send_file
from services import DataGenerator, Exporter
from repos import ExportRepo
from utils.logger import get_logger
import os
import uuid

logger = get_logger(__name__)

exports_bp = Blueprint('exports', __name__)

@exports_bp.route('/api/exports', methods=['POST'])
def create_export():
    """
    创建导出
    
    请求体示例:
    {
        "fields": [...],
        "count": 1000,
        "format": "csv"  // 或 "json", "ndjson"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "请求体不能为空"}), 400
        
        fields = data.get('fields', [])
        count = data.get('count', 100)
        format_type = data.get('format', 'csv')
        
        if not fields:
            return jsonify({"error": "字段列表不能为空"}), 400
        
        if format_type not in ['csv', 'json', 'ndjson']:
            return jsonify({"error": "不支持的导出格式"}), 400
        
        # 构建schema
        schema = {"fields": fields}
        
        # 生成数据
        generator = DataGenerator()
        result_data = generator.generate_batch(schema, count)
        
        # 导出数据
        exporter = Exporter()
        filepath = exporter.export(result_data, format_type)
        
        # 记录导出
        export_repo = ExportRepo()
        job_id = str(uuid.uuid4())  # 简化版，实际应该先创建job
        export_id = export_repo.create(job_id, format_type, filepath)
        
        # 更新导出状态
        file_size = os.path.getsize(filepath)
        export_repo.update_status(export_id, 'completed', filepath, file_size)
        export_repo.close()
        
        return jsonify({
            "id": export_id,
            "status": "completed",
            "format": format_type,
            "size": file_size,
            "count": len(result_data)
        })
    
    except Exception as e:
        logger.error(f"创建导出失败: {str(e)}")
        return jsonify({"error": f"导出失败: {str(e)}"}), 500


@exports_bp.route('/api/exports/<export_id>', methods=['GET'])
def get_export(export_id):
    """获取导出信息"""
    try:
        export_repo = ExportRepo()
        export_record = export_repo.get_by_id(export_id)
        export_repo.close()
        
        if not export_record:
            return jsonify({"error": "导出记录不存在"}), 404
        
        return jsonify(export_record)
    
    except Exception as e:
        logger.error(f"获取导出信息失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@exports_bp.route('/api/exports/<export_id>/download', methods=['GET'])
def download_export(export_id):
    """下载导出文件"""
    try:
        export_repo = ExportRepo()
        export_record = export_repo.get_by_id(export_id)
        export_repo.close()
        
        if not export_record:
            return jsonify({"error": "导出记录不存在"}), 404
        
        filepath = export_record['path']
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({"error": "导出文件不存在"}), 404
        
        # 返回文件
        return send_file(
            filepath,
            as_attachment=True,
            download_name=os.path.basename(filepath)
        )
    
    except Exception as e:
        logger.error(f"下载导出失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@exports_bp.route('/api/exports', methods=['GET'])
def list_exports():
    """列出所有导出"""
    try:
        export_repo = ExportRepo()
        exports = export_repo.list_all()
        export_repo.close()
        
        return jsonify({"exports": exports, "total": len(exports)})
    
    except Exception as e:
        logger.error(f"列出导出失败: {str(e)}")
        return jsonify({"error": str(e)}), 500
