import os
import secrets

# 基础配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

# 用户配置
USERS = {
    'haizi': {
        'password': 'mima123',
        'role': 'student',
        'name': '孩子'
    },
    'jiazhang': {
        'password': 'mima456',
        'role': 'parent',
        'name': '家长'
    }
}

# 数据文件路径
USERS_FILE = os.path.join(DATA_DIR, 'users', 'users.json')
QUESTIONS_DIR = os.path.join(DATA_DIR, 'questions')
PROGRESS_DIR = os.path.join(DATA_DIR, 'progress')
PASSWORD_FILE = os.path.join(DATA_DIR, 'password_question.json')

# 确保目录存在
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
os.makedirs(QUESTIONS_DIR, exist_ok=True)
os.makedirs(PROGRESS_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 会话密钥 - 使用随机密钥
SECRET_KEY = secrets.token_hex(32)

# AI大模型配置（可选）
# DeepSeek API
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

# 火山引擎（豆包）API
VOLCENGINE_API_KEY = os.getenv('VOLCENGINE_API_KEY', '697b417c-75e9-49b5-bff1-2d0a5365fa1c')
VOLCENGINE_API_URL = 'https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions'

# 选择使用哪个API (deepseek 或 volcengine)
AI_PROVIDER = os.getenv('AI_PROVIDER', 'volcengine')
