from flask import Flask, request, jsonify, render_template, session, send_from_directory
from flask_cors import CORS
from functools import wraps
import os
import json
import uuid
import re
from datetime import datetime
from werkzeug.utils import secure_filename
from config import *
from md_parser import parse_md_to_json, validate_md_format

# 简单的拼音映射（常用汉字）
PINYIN_MAP = {
    '一': 'yi', '二': 'er', '三': 'san', '四': 'si', '五': 'wu', '六': 'liu', '七': 'qi', '八': 'ba', '九': 'jiu', '十': 'shi',
    '零': 'ling', '百': 'bai', '千': 'qian', '万': 'wan',
    '李': 'li', '逵': 'kui', '宋': 'song', '江': 'jiang', '林': 'lin', '冲': 'chong',
    '独': 'du', '乐': 'le', '寺': 'si', '天': 'tian', '津': 'jin', '北': 'bei', '京': 'jing',
    '水': 'shui', '浒': 'hu', '传': 'zhuan', '人': 'ren', '物': 'wu',
    '昨': 'zuo', '天': 'tian', '今': 'jin', '明': 'ming',
}

def answer_to_pinyin(answer):
    """将答案转换为拼音（只保留字母和数字）"""
    result = ''
    for char in str(answer):
        if char in PINYIN_MAP:
            result += PINYIN_MAP[char]
        elif char.isalnum():  # 保留字母和数字
            result += char.lower()
        # 忽略其他字符（如标点、空格等）
    return result

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)

# 确保数据文件存在
def init_data_files():
    """初始化数据文件"""
    # 用户文件
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(USERS, f, ensure_ascii=False, indent=2)

init_data_files()

# 登录验证装饰器
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return jsonify({'success': False, 'message': '请先登录'}), 401
            if role and session.get('role') != role:
                return jsonify({'success': False, 'message': '权限不足'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============ 页面路由 ============

@app.route('/')
def index():
    """首页 - 登录页面"""
    return render_template('login.html')

@app.route('/student')
def student_page():
    """学生端页面"""
    if 'username' not in session or session.get('role') != 'student':
        return render_template('login.html')
    return render_template('student/dashboard.html')

@app.route('/parent')
def parent_page():
    """家长端页面"""
    if 'username' not in session or session.get('role') != 'parent':
        return render_template('login.html')
    return render_template('parent/dashboard.html')

@app.route('/exam/<question_id>')
def exam_page(question_id):
    """考试页面"""
    if 'username' not in session:
        return render_template('login.html')
    return render_template('student/exam.html', question_id=question_id)

# ============ API路由 ============

def get_current_password_answer():
    """获取当前密码题的答案（拼音形式）"""
    if not os.path.exists(PASSWORD_FILE):
        return None
    try:
        with open(PASSWORD_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('answer_pinyin', '')
    except:
        return None

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    # 加载用户数据
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    if username not in users:
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
    
    user = users[username]
    
    # 家长使用固定密码
    if user['role'] == 'parent':
        if user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            session['name'] = user['name']
            return jsonify({
                'success': True,
                'role': user['role'],
                'name': user['name']
            })
    
    # 学生使用动态密码（密码题答案的拼音）
    elif user['role'] == 'student':
        # 获取当前密码题答案
        correct_password = get_current_password_answer()
        if correct_password is None:
            return jsonify({'success': False, 'message': '密码题尚未设置，请联系家长'}), 401
        
        # 将用户输入转换为拼音进行比较
        user_input_pinyin = answer_to_pinyin(password)
        
        if user_input_pinyin == correct_password:
            session['username'] = username
            session['role'] = user['role']
            session['name'] = user['name']
            return jsonify({
                'success': True,
                'role': user['role'],
                'name': user['name']
            })
    
    return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """退出登录"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/password-question', methods=['GET'])
def get_password_question():
    """获取当前密码题（公开接口，供登录页查看提示）"""
    if not os.path.exists(PASSWORD_FILE):
        return jsonify({
            'success': True,
            'hasQuestion': False,
            'question': '密码题尚未设置，请联系家长'
        })
    
    try:
        with open(PASSWORD_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({
            'success': True,
            'hasQuestion': True,
            'question': data.get('question', ''),
            'setTime': data.get('setTime', '')
        })
    except:
        return jsonify({
            'success': True,
            'hasQuestion': False,
            'question': '密码题加载失败'
        })

@app.route('/api/parent/password-question', methods=['POST'])
@login_required('parent')
def set_password_question():
    """家长设置密码题"""
    data = request.get_json()
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()
    
    if not question or not answer:
        return jsonify({'success': False, 'message': '请输入密码题和答案'}), 400
    
    # 将答案转换为拼音
    answer_pinyin = answer_to_pinyin(answer)
    
    if not answer_pinyin:
        return jsonify({'success': False, 'message': '答案无法转换为有效拼音'}), 400
    
    # 保存密码题（只保留最新的一道）
    password_data = {
        'question': question,
        'answer': answer,
        'answer_pinyin': answer_pinyin,
        'setTime': datetime.now().isoformat()
    }
    
    with open(PASSWORD_FILE, 'w', encoding='utf-8') as f:
        json.dump(password_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({
        'success': True,
        'message': '密码题设置成功',
        'answerPinyin': answer_pinyin
    })

@app.route('/api/user/info')
def get_user_info():
    """获取当前用户信息"""
    if 'username' in session:
        return jsonify({
            'success': True,
            'username': session['username'],
            'role': session.get('role'),
            'name': session.get('name')
        })
    return jsonify({'success': False, 'message': '未登录'}), 401

# ============ 题目相关API ============

@app.route('/api/questions', methods=['GET'])
@login_required()
def get_questions():
    """获取所有题目列表"""
    questions = []
    
    for filename in os.listdir(QUESTIONS_DIR):
        if filename.endswith('.json'):
            question_id = filename[:-5]
            filepath = os.path.join(QUESTIONS_DIR, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 获取进度信息
            progress_file = os.path.join(PROGRESS_DIR, f"{session['username']}_{question_id}.json")
            progress_data = {}
            if os.path.exists(progress_file):
                with open(progress_file, 'r', encoding='utf-8') as f:
                    progress_data = json.load(f)
            
            # 计算进度
            total = len(data.get('questions', []))
            answered = len(progress_data.get('answers', {}))
            progress_percent = int((answered / total * 100)) if total > 0 else 0
            
            questions.append({
                'id': question_id,
                'title': data.get('title', '未命名题单'),
                'createDate': data.get('createDate', ''),
                'totalQuestions': total,
                'answeredCount': answered,
                'progress': progress_percent,
                'lastScore': progress_data.get('lastScore', None),
                'completeDate': progress_data.get('completeDate', None),
                'status': progress_data.get('status', 'not_started')  # not_started, in_progress, completed, stopped
            })
    
    # 按创建日期排序
    questions.sort(key=lambda x: x['createDate'], reverse=True)
    
    return jsonify({'success': True, 'questions': questions})

@app.route('/api/questions/<question_id>', methods=['GET'])
@login_required()
def get_question_detail(question_id):
    """获取题目详情"""
    filepath = os.path.join(QUESTIONS_DIR, f"{question_id}.json")
    
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'message': '题目不存在'}), 404
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取进度
    progress_file = os.path.join(PROGRESS_DIR, f"{session['username']}_{question_id}.json")
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        data['progress'] = progress_data
    
    return jsonify({'success': True, 'data': data})

@app.route('/api/questions/<question_id>/submit', methods=['POST'])
@login_required('student')
def submit_answer(question_id):
    """提交答案"""
    data = request.get_json()
    answers = data.get('answers', {})
    
    # 加载题目
    filepath = os.path.join(QUESTIONS_DIR, f"{question_id}.json")
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'message': '题目不存在'}), 404
    
    with open(filepath, 'r', encoding='utf-8') as f:
        question_data = json.load(f)
    
    # 计算得分
    correct_count = 0
    correct_indices = []
    questions = question_data.get('questions', [])

    for idx, q in enumerate(questions):
        user_answer = extract_user_answer(answers, str(idx))
        if user_answer and is_answer_correct(user_answer, q):
            correct_count += 1
            correct_indices.append(idx)

    score = calculate_score(correct_indices, len(questions))

    # 保存进度
    progress_file = os.path.join(PROGRESS_DIR, f"{session['username']}_{question_id}.json")
    progress_data = {
        'answers': answers,
        'correctCount': correct_count,
        'totalCount': len(questions),
        'lastScore': score,
        'lastSubmitTime': datetime.now().isoformat(),
        'status': 'completed' if len(answers) == len(questions) else 'in_progress'
    }
    
    if len(answers) == len(questions):
        progress_data['completeDate'] = datetime.now().isoformat()
    
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({
        'success': True,
        'score': score,
        'correctCount': correct_count,
        'totalCount': len(questions)
    })

@app.route('/api/questions/<question_id>/autosave', methods=['POST'])
@login_required('student')
def autosave_progress(question_id):
    """自动保存进度（不提交，仅保存当前作答状态）"""
    data = request.get_json()
    answers = data.get('answers', {})
    
    filepath = os.path.join(QUESTIONS_DIR, f"{question_id}.json")
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'message': '题目不存在'}), 404
    
    with open(filepath, 'r', encoding='utf-8') as f:
        question_data = json.load(f)
    
    questions = question_data.get('questions', [])
    correct_count = 0
    correct_indices = []
    for idx, q in enumerate(questions):
        user_answer = extract_user_answer(answers, str(idx))
        if user_answer and is_answer_correct(user_answer, q):
            correct_count += 1
            correct_indices.append(idx)

    progress_file = os.path.join(PROGRESS_DIR, f"{session['username']}_{question_id}.json")
    progress_data = {
        'answers': answers,
        'correctCount': correct_count,
        'totalCount': len(questions),
        'lastScore': calculate_score(correct_indices, len(questions)),
        'lastSubmitTime': datetime.now().isoformat(),
        'status': 'in_progress'
    }
    
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)
    
    return jsonify({'success': True, 'message': '进度已保存'})

def extract_user_answer(answers, idx):
    """从 answers 中提取用户答案，兼容对象和字符串格式"""
    val = answers.get(idx)
    if isinstance(val, dict):
        return val.get('selected', '')
    return val

def get_question_points(question_index, total_questions):
    """获取指定题目的分值（整数分配方案，确保总分100）"""
    if total_questions == 0:
        return 0
    base = 100 // total_questions
    remainder = 100 % total_questions
    # 前 remainder 道题多1分
    return base + 1 if question_index < remainder else base

def calculate_score(correct_indices, total_questions):
    """计算得分（整数分配方案，总分100）
    correct_indices: 答对题目的索引列表
    """
    if total_questions == 0:
        return 0
    score = 0
    for idx in correct_indices:
        score += get_question_points(idx, total_questions)
    return score

def is_answer_correct(user_answer, question):
    """判断用户答案是否正确，支持单选、多选、判断题"""
    correct_answer = question.get('answer', '')
    q_type = question.get('type', 'single')
    
    if not user_answer or not correct_answer:
        return False
    
    if q_type == 'truefalse':
        user_norm = normalize_truefalse(user_answer)
        correct_norm = normalize_truefalse(correct_answer)
        return user_norm == correct_norm
    
    if q_type == 'multiple':
        user_set = set(user_answer.upper())
        correct_set = set(correct_answer.upper())
        return user_set == correct_set
    
    return user_answer.upper() == correct_answer.upper()

def normalize_truefalse(answer):
    """统一判断题答案为 'T' 或 'F'"""
    a = answer.strip().upper()
    if a in ('正确', '对', '√', 'T', 'TRUE'):
        return 'T'
    if a in ('错误', '错', '×', 'F', 'FALSE'):
        return 'F'
    return a

# ============ 家长端API ============

@app.route('/api/parent/upload', methods=['POST'])
@login_required('parent')
def upload_md():
    """上传MD文件"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '文件名为空'}), 400
    
    if not file.filename.endswith('.md'):
        return jsonify({'success': False, 'message': '请上传.md格式的文件'}), 400
    
    # 保存上传的文件
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    saved_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(UPLOAD_DIR, saved_filename)
    file.save(filepath)
    
    # 读取并验证文件内容
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 验证格式
        is_valid, message = validate_md_format(md_content)
        if not is_valid:
            return jsonify({'success': False, 'message': message}), 400
        
        # 解析为JSON
        question_data = parse_md_to_json(md_content)
        question_data['createDate'] = datetime.now().isoformat()
        question_data['sourceFile'] = saved_filename
        
        # 生成唯一ID
        question_id = f"quiz_{timestamp}"
        
        # 保存JSON文件
        json_filepath = os.path.join(QUESTIONS_DIR, f"{question_id}.json")
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(question_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': '上传成功',
            'questionId': question_id,
            'title': question_data.get('title', '未命名'),
            'questionCount': len(question_data.get('questions', []))
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'解析失败: {str(e)}'}), 500

@app.route('/api/parent/questions/<question_id>', methods=['DELETE'])
@login_required('parent')
def delete_question(question_id):
    """删除题目"""
    filepath = os.path.join(QUESTIONS_DIR, f"{question_id}.json")
    
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'message': '题目不存在'}), 404
    
    os.remove(filepath)
    
    # 同时删除所有相关进度文件
    for filename in os.listdir(PROGRESS_DIR):
        if filename.endswith(f"_{question_id}.json"):
            os.remove(os.path.join(PROGRESS_DIR, filename))
    
    return jsonify({'success': True, 'message': '删除成功'})

@app.route('/api/parent/questions/<question_id>/stop', methods=['POST'])
@login_required('parent')
def stop_question(question_id):
    """停止作答"""
    # 获取所有学生的进度文件并设置为stopped
    for filename in os.listdir(PROGRESS_DIR):
        if filename.endswith(f"_{question_id}.json"):
            filepath = os.path.join(PROGRESS_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['status'] = 'stopped'
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    return jsonify({'success': True, 'message': '已停止作答'})

@app.route('/api/parent/progress/<question_id>', methods=['GET'])
@login_required('parent')
def get_all_progress(question_id):
    """获取所有学生的完成情况（含逐题详情）"""
    progress_list = []
    
    # 加载题目数据获取题目信息
    question_filepath = os.path.join(QUESTIONS_DIR, f"{question_id}.json")
    question_data = None
    if os.path.exists(question_filepath):
        with open(question_filepath, 'r', encoding='utf-8') as f:
            question_data = json.load(f)
    
    for filename in os.listdir(PROGRESS_DIR):
        if filename.endswith(f"_{question_id}.json"):
            username = filename.replace(f"_{question_id}.json", "")
            
            filepath = os.path.join(PROGRESS_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 构建逐题详情
            question_details = []
            if question_data:
                for idx, q in enumerate(question_data.get('questions', [])):
                    user_ans = data.get('answers', {}).get(str(idx))
                    detail = {
                        'index': idx + 1,
                        'id': q.get('id', ''),
                        'title': q.get('title', ''),
                        'type': q.get('type', 'single'),
                        'userAnswer': user_ans.get('selected', '') if user_ans else '',
                        'correctAnswer': q.get('answer', ''),
                        'isCorrect': user_ans.get('correct', False) if user_ans else None,
                        'submitted': user_ans.get('submitted', False) if user_ans else False
                    }
                    question_details.append(detail)
            
            progress_list.append({
                'username': username,
                'lastScore': data.get('lastScore', 0),
                'correctCount': data.get('correctCount', 0),
                'totalCount': data.get('totalCount', 0),
                'completeDate': data.get('completeDate'),
                'status': data.get('status', 'not_started'),
                'questionDetails': question_details
            })
    
    return jsonify({'success': True, 'progress': progress_list})

# 静态文件服务
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
