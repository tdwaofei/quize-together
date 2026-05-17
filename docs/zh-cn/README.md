# 📚 信息学竞赛练习系统

一个简单易用的在线练习系统，帮助孩子练习信息学竞赛题目，家长可以轻松管理和查看进度。

🌐 **语言**: [English](../../README.md) | [简体中文](README.md)

---

## ✨ 主要功能

### 👦 孩子端
- 📝 在线做题（单选、多选、判断）
- 📊 实时查看答题进度
- ✅ 自动评分和错题回顾
- 🎯 支持数学公式显示（LaTeX）

### 👨‍👩‍👧 家长端
- 📤 上传题库（支持 Markdown 格式）
- 📋 管理多个题单
- 📈 查看孩子的完成情况
- 🔒 设置登录密码题（可选）
- 📥 下载题库样例参考

---

## 🚀 快速开始

### 方式一：一键部署（推荐）

如果你有云服务器，使用部署脚本一键安装：

```bash
# 1. 下载代码到服务器
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. 复制配置文件
cp config.example.py config.py

# 3. 修改配置（可选）
# 编辑 config.py，修改默认账号密码

# 4. 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

部署成功后，访问你的服务器 IP 即可使用！

### 方式二：本地运行

```bash
# 1. 克隆或下载代码
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. 复制配置文件
cp config.example.py config.py

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行
python app.py
```

然后在浏览器访问：`http://localhost:5000`

---

## 📝 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 孩子 | `haizi` | `mima123` |
| 家长 | `jiazhang` | `mima456` |

⚠️ **重要**：请在部署后立即修改默认密码！

---

## 📖 使用指南

### 家长如何出题？

1. 下载 `题库样例.md` 文件作为参考
2. 按照样例格式编写题目
3. 用家长账号登录
4. 在"上传新题单"区域上传你的 .md 文件

### 题库格式示例

```markdown
# 题库标题

### 考点 1.1 变量定义

**题目：** 以下代码的输出是？

```cpp
int a = 10;
cout << a;
```

A. 10
B. 20
C. 编译错误
D. 随机值

<details>
<summary>点击查看答案与解析</summary>

**答案：** A

**解题过程：**
- 变量 a 赋值为 10
- cout 输出 a 的值

**本题考点：** 变量定义和输出

**复习要点：**
- int 表示整数类型
- cout 用于输出
</details>
```

更详细的格式请参考 `题库样例.md` 文件。

---

## 🔧 配置说明

第一次使用前，请复制配置模板：

```bash
cp config.example.py config.py
```

然后编辑 `config.py`，修改以下内容：

- `USERS`：修改默认账号密码
- `SECRET_KEY`：已自动生成随机密钥，无需修改

---

## 📁 项目结构

```
exam_system/
├── app.py                 # 主程序
├── config.example.py      # 配置模板
├── config.py              # 你的配置（不会上传到 GitHub）
├── md_parser.py           # 题库解析器
├── requirements.txt       # Python 依赖
├── deploy.sh              # 一键部署脚本
├── 题库样例.md            # 题库格式参考
├── README.md              # 说明文档
├── docs/
│   └── zh-cn/
│       └── README.md      # 中文文档
├── .gitignore             # Git 忽略文件
├── data/                  # 数据目录（不会上传到 GitHub）
│   ├── users/
│   ├── questions/
│   └── progress/
├── static/
│   ├── kaotiyangli.md     # 题库样例
│   └── uploads/           # 上传的文件
└── templates/             # 网页模板
    ├── login.html
    ├── student/
    └── parent/
```

---

## 🔒 安全建议

1. **修改默认密码**：首次使用后立即修改
2. **不要上传 config.py**：已在 .gitignore 中配置
3. **不要上传 data 目录**：包含用户数据
4. **定期备份**：备份 data 目录
5. **使用 HTTPS**：生产环境建议配置 SSL

---

## 🐛 常见问题

### 无法访问？

- 检查服务器防火墙是否开放 80 端口
- 检查服务是否运行：`systemctl status quiz-system`

### 上传失败？

- 确保文件是 .md 格式
- 检查文件格式是否符合要求
- 查看浏览器控制台的错误信息

### 数学公式不显示？

- 确保格式正确（用 $ 包裹公式）
- 等待页面加载完成

---

## 🤝 贡献

欢迎其他家长一起完善这个项目！有问题可以提 Issue。

---

## 📞 求助

如果遇到问题：

1. 先看本页面的常见问题
2. 查看项目的 Issue 区
3. 或提交新的 Issue

---

## 💡 项目初衷

这个项目是为了帮助孩子练习信息学竞赛题目而做的。作为家长，我们希望有一个简单易用的工具来：

- 上传自己的题库
- 查看孩子的学习进度
- 让孩子可以随时随地练习

希望这个工具能帮助到更多的家长和孩子！加油！💪
