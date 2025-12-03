from flask import Flask
from flask_cors import CORS
from config import Config
from models import init_db
from routes import generate_bp, exports_bp
from utils.logger import get_logger

logger = get_logger(__name__)

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化配置
    Config.init_app()
    
    # 启用CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # 初始化数据库
    init_db()
    
    # 注册蓝图
    app.register_blueprint(generate_bp)
    app.register_blueprint(exports_bp)
    
    logger.info("Flask应用创建成功")
    
    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("启动Flask开发服务器...")
    app.run(host='0.0.0.0', port=5001, debug=Config.DEBUG)
