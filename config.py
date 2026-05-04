import os

# 基础配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

# 用户配置
USERS = {
    'ejf': {
        'password': 'likui',
        'role': 'student',
        'name': '孩子'
    },
    'jiazhang': {
        'password': 'lujunyi',
        'role': 'parent',
        'name': '家长'
    }
}

# 数据文件路径
USERS_FILE = os.path.join(DATA_DIR, 'users', 'users.json')
QUESTIONS_DIR = os.path.join(DATA_DIR, 'questions')
PROGRESS_DIR = os.path.join(DATA_DIR, 'progress')
PASSWORD_FILE = os.path.join(DATA_DIR, 'password_question.json')  # 密码题存储

# 确保目录存在
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
os.makedirs(QUESTIONS_DIR, exist_ok=True)
os.makedirs(PROGRESS_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 会话密钥 - 32位随机数字字母组合
SECRET_KEY = 'a8f3k9m2p5q7r4t8v1w6x9y2z5a7b4c8'
