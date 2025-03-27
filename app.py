import logging
import sqlalchemy
from flask_cors import CORS
from flask_session import Session
import config
import argparse
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from blueprint.work_order import bp as work_order


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy()
# 配置 Redis 作为会话存储
# 使用文件系统作为会话存储
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_sessions'
app.config['SESSION_PERMANENT'] = False  # 浏览器关闭时会话失效
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 0  # 设置为0可以保证关闭浏览器立即失效
# 配置 Flask 的日志级别
app.logger.setLevel(logging.INFO)
# 配置 Werkzeug 的日志级别
logging.getLogger('werkzeug').setLevel(logging.INFO)

db.init_app(app)


# 初始化 Flask-Session
Session(app)
migrate = Migrate(app, db)

app.register_blueprint(work_order, url_prefix='/work_order')
CORS(app, supports_credentials=True)

@app.before_request
def cleanup_expired_sessions():
    session_folder = app.config['SESSION_FILE_DIR']
    for filename in os.listdir(session_folder):
        file_path = os.path.join(session_folder, filename)
        if os.path.isfile(file_path):
            try:
                # 删除过期的会话文件
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting session file {file_path}: {e}")


def test_database_connection():
    with app.app_context():
        for bind_key, engine in db.engines.items():
            try:
                with engine.connect() as conn:
                    res = conn.execute(sqlalchemy.text("SELECT VERSION()"))
                    row = res.fetchone()
                    if row:
                        print(f"Database connection successful, version: {row[0]}")
                    else:
                        print("Database connection failed")

            except Exception as e:
                logging.error(f"Error connecting to {bind_key.capitalize()} database: {e}")





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Flask app exposing models")
    parser.add_argument("--port", default=5555, type=int, help="port number")
    args = parser.parse_args()
    logging.info('项目已启动')
    print(args.port)
    app.run(host="127.0.0.1", port=args.port, debug=False)
