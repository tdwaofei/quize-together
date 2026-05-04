"""
Markdown题库解析器
将固定格式的.md文档解析为JSON格式
"""

import re
import json

def validate_md_format(content):
    """
    验证.md文件格式是否正确
    返回: (is_valid: bool, message: str)
    """
    required_sections = ['题目', '答案', '解题过程', '本题考点', '复习要点']
    
    # 检查基本结构
    if not content.strip():
        return False, "文件内容为空"
    
    # 检查是否有标题
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if not title_match:
        return False, "缺少文档标题（应以#开头）"
    
    # 检查是否有题目标记（支持多种格式）
    # 格式1: ### 考点 X.X 标题
    # 格式2: ### 第 X 题
    has_question_markers = ('### 考点' in content or 
                            '### 第' in content or 
                            '## 考点' in content)
    if not has_question_markers:
        return False, "未找到题目标记（应包含'### 考点'或'### 第X题'）"
    
    # 检查题目数量
    question_count = len(re.findall(r'(?:^###\s+(?:考点|第)|\*\*题目[：:]\*\*)', content, re.MULTILINE))
    if question_count == 0:
        # 可能是新格式，检查是否有选项
        option_count = len(re.findall(r'\n[A-D][\.．、\s]', content))
        if option_count < 4:
            return False, "未找到任何题目（请检查题目格式）"
    
    # 检查是否有答案（可能在details标签内）
    answer_count = len(re.findall(r'\*\*答案[:：]', content))
    if answer_count == 0:
        return False, "未找到答案标记（应包含'**答案：**'）"
    
    return True, "格式验证通过"

def parse_md_to_json(content):
    """
    解析.md内容转换为JSON格式
    支持两种格式：
    1. ### 考点 X.X 标题
    2. ### 第 X 题
    """
    result = {
        'title': '',
        'description': '',
        'questions': []
    }
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        result['title'] = title_match.group(1).strip()
    
    # 提取说明部分（标题和第一个题目之间的内容）
    desc_match = re.search(r'^#.+?\n(.+?)(?=\n##?\s+(?:一、|单项|不定项)|\n###\s+(?:考点|第)|\Z)', content, re.DOTALL | re.MULTILINE)
    if desc_match:
        desc = desc_match.group(1).strip()
        # 移除markdown标记
        desc = re.sub(r'\*\*', '', desc)
        result['description'] = desc
    
    # 按考点分割题目（支持两种格式）
    # 格式1: ### 考点 X.X 标题
    # 格式2: ### 第 X 题
    question_blocks = re.split(r'\n(?=###\s+(?:考点\s+\d+\.?\d*|第\s*\d+\s*题)\s*)', content)
    
    for block in question_blocks:
        if not block.strip():
            continue
        # 检查是否是题目块
        if '### 考点' in block or '### 第' in block:
            question = parse_question_block(block)
            if question:
                result['questions'].append(question)
    
    return result

def parse_question_block(block):
    """
    解析单个题目块
    支持两种格式：
    1. ### 考点 X.X 标题 + **题目：**格式
    2. ### 第 X 题 + 直接题目内容（在details标签内有答案）
    """
    question = {
        'id': '',
        'title': '',
        'question': '',
        'options': {},
        'answer': '',
        'solution': '',
        'point': '',
        'review': ''
    }
    
    # 先提取details标签内容（答案和解析）
    details_content = ''
    details_match = re.search(r'<details>.*?<summary>.*?</summary>(.*?)</details>', block, re.DOTALL)
    if details_match:
        details_content = details_match.group(1)
        # 暂时移除details标签，简化后续解析
        block_for_options = re.sub(r'<details>.*?</details>', '', block, flags=re.DOTALL)
    else:
        block_for_options = block
    
    # 提取考点ID和标题
    # 格式1: ### 考点 1.1 标识符、关键字...
    # 格式2: ### 第 1 题
    header_match = re.search(r'###\s+考点\s+(\d+\.?\d*)\s+(.+?)(?=\n|$)', block)
    if header_match:
        question['id'] = header_match.group(1)
        question['title'] = header_match.group(2).strip()
    else:
        # 尝试格式2: ### 第 X 题
        header_match = re.search(r'###\s+第\s*(\d+)\s*题', block)
        if header_match:
            question['id'] = header_match.group(1)
            question['title'] = f'第{header_match.group(1)}题'
    
    # 提取题目内容
    # 尝试格式1: **题目：**后的内容
    question_match = re.search(
        r'(?:\*\*题目[:：]\*\*|题目[:：])\s*(.+?)(?=\n\s*[A-D][\.．、\s]|\n\s*<details>|\Z)',
        block_for_options, re.DOTALL
    )
    if question_match:
        question_text = question_match.group(1).strip()
        question_text = clean_markdown(question_text)
        question['question'] = question_text
    else:
        # 尝试格式2: 标题后直接跟题目内容（到第一个选项前）
        question_match = re.search(
            r'###\s+(?:考点\s+\d+\.?\d*\s+.+?|第\s*\d+\s*题)\n+(.+?)(?=\n\s*[A-D][\.．、\s]|\n\s*<details>|\Z)',
            block_for_options, re.DOTALL
        )
        if question_match:
            question_text = question_match.group(1).strip()
            question_text = clean_markdown(question_text)
            question['question'] = question_text
    
    # 提取选项（从移除details后的内容中提取）
    # 支持格式: A. xxx 或 A．xxx 或 A、xxx 或 A xxx
    # 在选项后停止的标记：下一选项、details标签、答案标记、分隔线、题目结束
    option_pattern = r'([A-D])[\.．、\s]\s*(.+?)(?=\n\s*[A-D][\.．、\s]|\n\s*<details>|\n\s*\*\*答案|\n\s*---|\Z)'
    options = re.findall(option_pattern, block_for_options, re.DOTALL)
    
    for opt_letter, opt_text in options:
        opt_text = opt_text.strip()
        opt_text = clean_markdown(opt_text)
        question['options'][opt_letter] = opt_text
    
    # 提取答案（优先从details内容中提取，否则从整个block）
    search_block = details_content if details_content else block
    # 支持格式: **答案：B** (字母在加粗内) 或 **答案：** B (字母在外)
    # 格式1: **答案：B** - 字母在加粗标记内
    answer_match = re.search(r'\*\*答案[:：]([A-D])\*\*', search_block)
    if not answer_match:
        # 格式2: **答案：** B - 字母在加粗标记外
        answer_match = re.search(r'\*\*答案[:：]\*\*\s*([A-D])', search_block)
    if answer_match:
        question['answer'] = answer_match.group(1)
    
    # 提取解题过程
    solution_match = re.search(
        r'\*\*解题过程[:：]\*\*\s*([\s\S]*?)(?=\n\s*\*\*本题考点|\n\s*\*\*复习要点|\Z)',
        search_block
    )
    if solution_match:
        solution = solution_match.group(1).strip()
        question['solution'] = clean_markdown(solution)
    
    # 提取本题考点
    point_match = re.search(
        r'\*\*本题考点[:：]\*\*\s*([\s\S]*?)(?=\n\s*\*\*复习要点|\Z)',
        search_block
    )
    if point_match:
        question['point'] = clean_markdown(point_match.group(1).strip())
    
    # 提取复习要点
    review_match = re.search(
        r'\*\*复习要点[:：]\*\*\s*([\s\S]*?)(?=\n---|\Z)',
        search_block
    )
    if review_match:
        review = review_match.group(1).strip()
        question['review'] = clean_markdown(review)
    
    return question if question['question'] else None

def clean_markdown(text):
    """
    清理markdown标记，但保留代码块格式
    """
    # 移除加粗标记
    text = re.sub(r'\*\*', '', text)
    # 移除斜体标记
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # 移除details和summary标签（保留内部内容已在前面处理）
    text = re.sub(r'<details>', '', text, flags=re.DOTALL)
    text = re.sub(r'</details>', '', text, flags=re.DOTALL)
    text = re.sub(r'<summary>.*?</summary>', '', text, flags=re.DOTALL)
    # 清理HTML注释
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # 清理多余的空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_code_blocks(text):
    """
    提取代码块并保留格式
    """
    code_blocks = {}
    counter = 0
    
    def replace_code_block(match):
        nonlocal counter
        placeholder = f"__CODE_BLOCK_{counter}__"
        code_blocks[placeholder] = match.group(0)
        counter += 1
        return placeholder
    
    # 替换代码块
    text = re.sub(r'```[\s\S]*?```', replace_code_block, text)
    
    return text, code_blocks

def restore_code_blocks(text, code_blocks):
    """
    恢复代码块
    """
    for placeholder, code in code_blocks.items():
        text = text.replace(placeholder, code)
    return text

# 测试代码
if __name__ == '__main__':
    # 读取测试文件
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证格式
        is_valid, message = validate_md_format(content)
        print(f"验证结果: {message}")
        
        if is_valid:
            # 解析
            result = parse_md_to_json(content)
            print(f"\n解析成功！")
            print(f"标题: {result['title']}")
            print(f"题目数量: {len(result['questions'])}")
            
            # 保存为JSON
            output_file = sys.argv[1].replace('.md', '.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"已保存到: {output_file}")
