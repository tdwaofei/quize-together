# 📚 信息学竞赛练习系统

一个简单易用的在线练习系统，帮助孩子练习信息学竞赛题目，家长可以轻松管理和查看进度。

🌐 **语言**: [English](../../README.md) | [简体中文](README.md)

---

## ✨ 主要功能 / Key Features

### 👦 孩子端 / Student Portal
- 📝 在线做题（单选、多选、判断）/ Online practice (Single choice, Multiple choice, True/False)
- 📊 实时查看答题进度 / Real-time progress tracking
- ✅ 自动评分和错题回顾 / Auto-scoring and wrong answer review
- 🎯 支持数学公式显示（LaTeX）/ Support for mathematical formulas (LaTeX)

### 👨‍👩‍👧 家长端 / Parent Portal
- 📤 上传题库（支持 Markdown 格式）/ Upload question banks (Markdown format supported)
- 📋 管理多个题单 / Manage multiple question sets
- 📈 查看孩子的完成情况 / View child's completion status
- 🔒 设置登录密码题（可选）/ Set login password questions (optional)
- 📥 下载题库样例参考 / Download question bank samples for reference

---

## 🚀 快速开始 / Quick Start

### 方式一：一键部署（推荐）/ Option 1: One-Click Deployment (Recommended)

如果你有云服务器，使用部署脚本一键安装：

If you have a cloud server, use the deployment script for one-click installation:

```bash
# 1. 下载代码到服务器 / Download code to server
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. 复制配置文件 / Copy configuration file
cp config.example.py config.py

# 3. 修改配置（可选）/ Edit configuration (optional)
# 编辑 config.py，修改默认账号密码 / Edit config.py to change default credentials

# 4. 运行部署脚本 / Run deployment script
chmod +x deploy.sh
./deploy.sh
```

部署成功后，访问你的服务器 IP 即可使用！

After deployment, access your server IP to use the system!

### 方式二：本地运行 / Option 2: Local Development

```bash
# 1. 克隆或下载代码 / Clone or download code
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. 复制配置文件 / Copy configuration file
cp config.example.py config.py

# 3. 安装依赖 / Install dependencies
pip install -r requirements.txt

# 4. 运行 / Run
python app.py
```

然后在浏览器访问 / Then access in browser：`http://localhost:5000`

---

## 📝 默认账号 / Default Accounts

| 角色 / Role | 用户名 / Username | 密码 / Password |
|------|--------|------|
| 孩子 / Student | `haizi` | `mima123` |
| 家长 / Parent | `jiazhang` | `mima456` |

⚠️ **重要 / Important**：请在部署后立即修改默认密码！

Please change the default passwords immediately after deployment!

---

## 📖 使用指南 / User Guide

### 家长如何出题？/ How do parents create questions?

1. 下载 `题库样例.md` 文件作为参考 / Download `题库样例.md` as reference
2. 按照样例格式编写题目 / Write questions following the sample format
3. 用家长账号登录 / Login with parent account
4. 在"上传新题单"区域上传你的 .md 文件 / Upload your .md file in the "Upload New Question Set" area

### 题库格式示例 / Question Bank Format Example

```markdown
# 题库标题 / Question Bank Title

### 考点 1.1 变量定义 / Topic 1.1 Variable Definition

**题目：** 以下代码的输出是？ / What is the output of the following code?

```cpp
int a = 10;
cout << a;
```

A. 10
B. 20
C. 编译错误 / Compilation error
D. 随机值 / Random value

<details>
<summary>点击查看答案与解析 / Click to view answer and explanation</summary>

**答案：** A

**解题过程：**
- 变量 a 赋值为 10 / Variable a is assigned 10
- cout 输出 a 的值 / cout outputs the value of a

**本题考点：** 变量定义和输出 / Variable definition and output

**复习要点：**
- int 表示整数类型 / int represents integer type
- cout 用于输出 / cout is used for output
</details>
```

更详细的格式请参考 `题库样例.md` 文件。

For more details, please refer to the `题库样例.md` file.

---

## 🔧 配置说明 / Configuration

第一次使用前，请复制配置模板：

Before first use, copy the configuration template:

```bash
cp config.example.py config.py
```

然后编辑 `config.py`，修改以下内容：

Then edit `config.py` to modify the following:

- `USERS`：修改默认账号密码 / Change default account credentials
- `SECRET_KEY`：已自动生成随机密钥，无需修改 / Auto-generated random key, no need to modify

---

## 📁 项目结构 / Project Structure

```
exam_system/
├── app.py                 # 主程序 / Main application
├── config.example.py      # 配置模板 / Configuration template
├── config.py              # 你的配置（不会上传到 GitHub）/ Your config (not uploaded to GitHub)
├── md_parser.py           # 题库解析器 / Question bank parser
├── requirements.txt       # Python 依赖 / Python dependencies
├── deploy.sh              # 一键部署脚本 / One-click deployment script
├── 题库样例.md            # 题库格式参考 / Question bank format reference
├── README.md              # 说明文档 / Documentation
├── .gitignore             # Git 忽略文件 / Git ignore file
├── data/                  # 数据目录（不会上传到 GitHub）/ Data directory (not uploaded to GitHub)
│   ├── users/
│   ├── questions/
│   └── progress/
├── static/
│   ├── kaotiyangli.md     # 题库样例 / Question bank sample
│   └── uploads/           # 上传的文件 / Uploaded files
└── templates/             # 网页模板 / Web templates
    ├── login.html
    ├── student/
    └── parent/
```

---

## 🔒 安全建议 / Security Recommendations

1. **修改默认密码** / **Change default passwords**：首次使用后立即修改 / Change immediately after first use
2. **不要上传 config.py** / **Don't upload config.py**：已在 .gitignore 中配置 / Configured in .gitignore
3. **不要上传 data 目录** / **Don't upload data directory**：包含用户数据 / Contains user data
4. **定期备份** / **Regular backups**：备份 data 目录 / Backup the data directory
5. **使用 HTTPS** / **Use HTTPS**：生产环境建议配置 SSL / Configure SSL for production environment

---

## 🐛 常见问题 / FAQ

### 无法访问？/ Cannot access?

- 检查服务器防火墙是否开放 80 端口 / Check if port 80 is open in server firewall
- 检查服务是否运行 / Check if service is running：`systemctl status quiz-system`

### 上传失败？/ Upload failed?

- 确保文件是 .md 格式 / Ensure file is in .md format
- 检查文件格式是否符合要求 / Check if file format meets requirements
- 查看浏览器控制台的错误信息 / Check browser console for error messages

### 数学公式不显示？/ Math formulas not displaying?

- 确保格式正确（用 $ 包裹公式）/ Ensure correct format (wrap formulas with $)
- 等待页面加载完成 / Wait for page to finish loading

---

## 🤝 贡献 / Contributing

欢迎其他家长一起完善这个项目！有问题可以提 Issue。

Parents are welcome to improve this project together! Feel free to open issues for any questions.

---

## 📞 求助 / Support

如果遇到问题：

If you encounter issues:

1. 先看本页面的常见问题 / Check the FAQ section on this page
2. 查看项目的 Issue 区 / Check the project's Issues section
3. 或提交新的 Issue / Or submit a new Issue

---

## 💡 项目初衷 / Project Motivation

这个项目是为了帮助孩子练习信息学竞赛题目而做的。作为家长，我们希望有一个简单易用的工具来：

This project was created to help children practice informatics competition problems. As parents, we wanted a simple and easy-to-use tool to:

- 上传自己的题库 / Upload our own question banks
- 查看孩子的学习进度 / Track children's learning progress
- 让孩子可以随时随地练习 / Allow children to practice anytime, anywhere

希望这个工具能帮助到更多的家长和孩子！加油！💪

Hope this tool helps more parents and children! Keep it up! 💪
