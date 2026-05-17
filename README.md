# 📚 Informatics Competition Practice System

A simple and easy-to-use online practice system to help children practice informatics competition problems, with parents easily managing and tracking progress.

🌐 **Languages**: [English](README.md) | [简体中文](docs/zh-cn/README.md)

---

## ✨ Key Features

### 👦 Student Portal
- 📝 Online practice (Single choice, Multiple choice, True/False)
- 📊 Real-time progress tracking
- ✅ Auto-scoring and wrong answer review
- 🎯 Support for mathematical formulas (LaTeX)

### 👨‍👩‍👧 Parent Portal
- 📤 Upload question banks (Markdown format supported)
- 📋 Manage multiple question sets
- 📈 View child's completion status
- 🔒 Set login password questions (optional)
- 📥 Download question bank samples for reference

---

## 🚀 Quick Start

### Option 1: One-Click Deployment (Recommended)

If you have a cloud server, use the deployment script for one-click installation:

```bash
# 1. Download code to server
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Copy configuration file
cp config.example.py config.py

# 3. Edit configuration (optional)
# Edit config.py to change default credentials

# 4. Run deployment script
chmod +x deploy.sh
./deploy.sh
```

After deployment, access your server IP to use the system!

### Option 2: Local Development

```bash
# 1. Clone or download code
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Copy configuration file
cp config.example.py config.py

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

Then access in browser: `http://localhost:5000`

---

## 📝 Default Accounts

| Role | Username | Password |
|------|--------|------|
| Student | `haizi` | `mima123` |
| Parent | `jiazhang` | `mima456` |

⚠️ **Important**: Please change the default passwords immediately after deployment!

---

## 📖 User Guide

### How do parents create questions?

1. Download `题库样例.md` as reference
2. Write questions following the sample format
3. Login with parent account
4. Upload your .md file in the "Upload New Question Set" area

### Question Bank Format Example

```markdown
# Question Bank Title

### Topic 1.1 Variable Definition

**Question:** What is the output of the following code?

```cpp
int a = 10;
cout << a;
```

A. 10
B. 20
C. Compilation error
D. Random value

<details>
<summary>Click to view answer and explanation</summary>

**Answer:** A

**Explanation:**
- Variable a is assigned 10
- cout outputs the value of a

**Key Points:** Variable definition and output

**Review Notes:**
- int represents integer type
- cout is used for output
</details>
```

For more details, please refer to the `题库样例.md` file.

---

## 🔧 Configuration

Before first use, copy the configuration template:

```bash
cp config.example.py config.py
```

Then edit `config.py` to modify the following:

- `USERS`: Change default account credentials
- `SECRET_KEY`: Auto-generated random key, no need to modify

---

## 📁 Project Structure

```
exam_system/
├── app.py                 # Main application
├── config.example.py      # Configuration template
├── config.py              # Your config (not uploaded to GitHub)
├── md_parser.py           # Question bank parser
├── requirements.txt       # Python dependencies
├── deploy.sh              # One-click deployment script
├── 题库样例.md            # Question bank format reference
├── README.md              # Documentation (this file)
├── docs/
│   └── zh-cn/
│       └── README.md      # Chinese documentation
├── .gitignore             # Git ignore file
├── data/                  # Data directory (not uploaded to GitHub)
│   ├── users/
│   ├── questions/
│   └── progress/
├── static/
│   ├── kaotiyangli.md     # Question bank sample
│   └── uploads/           # Uploaded files
└── templates/             # Web templates
    ├── login.html
    ├── student/
    └── parent/
```

---

## 🔒 Security Recommendations

1. **Change default passwords**: Change immediately after first use
2. **Don't upload config.py**: Configured in .gitignore
3. **Don't upload data directory**: Contains user data
4. **Regular backups**: Backup the data directory
5. **Use HTTPS**: Configure SSL for production environment

---

## 🐛 FAQ

### Cannot access?

- Check if port 80 is open in server firewall
- Check if service is running: `systemctl status quiz-system`

### Upload failed?

- Ensure file is in .md format
- Check if file format meets requirements
- Check browser console for error messages

### Math formulas not displaying?

- Ensure correct format (wrap formulas with $)
- Wait for page to finish loading

---

## 🤝 Contributing

Parents are welcome to improve this project together! Feel free to open issues for any questions.

---

## 📞 Support

If you encounter issues:

1. Check the FAQ section on this page
2. Check the project's Issues section
3. Or submit a new Issue

---

## 💡 Project Motivation

This project was created to help children practice informatics competition problems. As parents, we wanted a simple and easy-to-use tool to:

- Upload our own question banks
- Track children's learning progress
- Allow children to practice anytime, anywhere

Hope this tool helps more parents and children! Keep it up! 💪
