"""
应用入口：
- 初始化 Flask 与 CORS
- 初始化数据库并加载字段类型缓存
- 注册 API 蓝图
- 提供健康检查
"""
from flask import Flask, jsonify
from flask_cors import CORS
from backend.models.db import init_db
from backend.services.field_types import load_types
from backend.routes.api import api_bp

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    # 初始化数据库与字段类型缓存
    init_db()
    load_types()

    # 注册 API
    app.register_blueprint(api_bp)

    # 健康检查（方便确认服务是否运行）
    @app.route("/", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)