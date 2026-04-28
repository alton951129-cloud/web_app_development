import os
import sqlite3
from flask import Flask, render_template
from dotenv import load_dotenv
from .routes import main, places, plan

# 載入環境變數
load_dotenv()

def create_app():
    # 建立 Flask 實體
    app = Flask(__name__, instance_relative_config=True)
    
    # 設定基本配置
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/health')
    def health():
        return "OK"

    # 註冊 Blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(places.bp)
    app.register_blueprint(plan.bp)

    return app

def init_db():
    """從 database/schema.sql 初始化 SQLite 資料庫"""
    db_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')
    
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    if not os.path.exists(schema_path):
        print(f"錯誤：找不到 {schema_path}")
        return

    db = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
    print("資料庫初始化成功！")
