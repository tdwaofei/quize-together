import os
import secrets

# 基础配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

# 用户配置 - 请根据需要修改
USERS = {
    'haizi': {
        'password': 'mima123',  # 修改为你想要的密码
        'role': 'student',
        'name': '孩子'
    },
    'jiazhang': {
        'password': 'mima456',  # 修改为你想要的密码
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

# 会话密钥 - 自动生成随机密钥
SECRET_KEY = secrets.token_hex(32)

# AI大模型配置（可选）
# DeepSeek API
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

# 火山引擎（豆包）API
VOLCENGINE_API_KEY = os.getenv('VOLCENGINE_API_KEY', '')
VOLCENGINE_API_URL = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'

# 选择使用哪个API (deepseek 或 volcengine)
AI_PROVIDER = os.getenv('AI_PROVIDER', 'deepseek')
