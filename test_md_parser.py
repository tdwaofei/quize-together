#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试Markdown解析器"""

import sys
import os

from md_parser import parse_md_to_json, validate_md_format

# 读取实际的AI生成的Markdown文件
with open('static/uploads/20260524_082822_ai-generated-questions.md', 'r', encoding='utf-8') as f:
    test_markdown = f.read()

print("=" * 60)
print("测试Markdown解析")
print("=" * 60)
print("\n原始Markdown内容:")
print(test_markdown[:500] + "..." if len(test_markdown) > 500 else test_markdown)
print("\n" + "=" * 60)

# 验证格式
print("\n1. 验证格式:")
is_valid, message = validate_md_format(test_markdown)
print(f"   结果: {'通过' if is_valid else '失败'}")
print(f"   消息: {message}")

if not is_valid:
    sys.exit(1)

# 解析Markdown
print("\n2. 解析Markdown:")
result = parse_md_to_json(test_markdown)
print(f"   标题: {result['title']}")
print(f"   题目数量: {len(result['questions'])}")

# 打印每道题的详细信息
print("\n3. 题目详情:")
for i, q in enumerate(result['questions']):
    print(f"\n   题目 {i+1}:")
    print(f"   - 类型: {q['type']}")
    print(f"   - ID: {q['id']}")
    print(f"   - 标题: {q['title']}")
    print(f"   - 题目内容: {q['question'][:50]}...")
    print(f"   - 选项: {list(q['options'].keys())}")
    print(f"   - 答案: {q['answer']}")

# 保存为JSON文件用于调试
import json
with open('test_output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\n4. 解析结果已保存到: test_output.json")
