from datetime import timedelta
from urllib import parse

# 可以随便写 越长越安全解密越慢
SECRET_KEY = 'Flat-White'

# 访问令牌的过期时间为60分钟
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
# 刷新令牌的过期时间为30天
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# 本地数据库配置
HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'yanglao_order_sys'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI

# 远程数据库配置
REMOTE_HOSTNAME = '47.99.65.68'
REMOTE_PORT = 3306
REMOTE_USERNAME = 'dhgxjbgs'
REMOTE_PASSWORD = parse.quote_plus('D23@#hGb')
REMOTE_DATABASE = 'yanglao'
REMOTE_DB_URI = ('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.
                 format(REMOTE_USERNAME, REMOTE_PASSWORD,
                        REMOTE_HOSTNAME, REMOTE_PORT, REMOTE_DATABASE))
#SQLALCHEMY_DATABASE_URI = REMOTE_DB_URI

# 多SQL绑定配置
SQLALCHEMY_BINDS = {
    'local': DB_URI,
    'remote': REMOTE_DB_URI
}

