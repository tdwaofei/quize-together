# 信息学竞赛练习系统 - 部署说明

## 📋 系统概述

这是一个前后端分离的Web应用，用于信息学竞赛L1级在线练习系统。

### 主要功能
- **孩子端**：登录做题、查看进度、自动评分
- **家长端**：上传题库、管理题单、查看完成情况
- **文件存储**：不使用数据库，所有数据以JSON文件形式存储

### 技术栈
- **后端**：Python Flask
- **前端**：HTML + Tailwind CSS + JavaScript
- **部署**：腾讯轻量云服务器（119.45.100.64）

---

## 🚀 部署步骤

### 1. 服务器环境准备

```bash
# 连接到服务器
ssh root@119.45.100.64

# 更新系统
apt update && apt upgrade -y

# 安装Python和pip
apt install python3 python3-pip -y

# 安装Nginx（作为反向代理）
apt install nginx -y
```

### 2. 上传代码到服务器

```bash
# 在本地打包代码
cd exam_system
tar -czvf exam_system.tar.gz *

# 上传到服务器
scp exam_system.tar.gz root@119.45.100.64:/opt/

# 在服务器上解压
ssh root@119.45.100.64 "cd /opt && tar -xzvf exam_system.tar.gz && mv exam_system quiz_system"
```

### 3. 安装依赖

```bash
ssh root@119.45.100.64
cd /opt/quiz_system
pip3 install -r requirements.txt
```

### 4. 配置系统服务

创建系统服务文件 `/etc/systemd/system/quiz-system.service`：

```ini
[Unit]
Description=Quiz System Flask App
After=network.target

[Service]
User=root
WorkingDirectory=/opt/quiz_system
Environment="PATH=/usr/local/bin"
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=production"
ExecStart=/usr/bin/python3 /opt/quiz_system/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
systemctl daemon-reload
systemctl enable quiz-system
systemctl start quiz-system
systemctl status quiz-system
```

### 5. 配置Nginx反向代理

创建配置文件 `/etc/nginx/sites-available/quiz-system`：

```nginx
server {
    listen 80;
    server_name 119.45.100.64;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/quiz_system/static;
        expires 30d;
    }
}
```

启用配置：

```bash
ln -s /etc/nginx/sites-available/quiz-system /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

### 6. 配置防火墙

```bash
# 开放80端口
ufw allow 80/tcp
ufw allow 22/tcp
ufw enable
```

---

## 🔧 使用说明

### 访问地址
- **登录页面**：http://119.45.100.64/

### 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 孩子 | ejf | zhangshun |
| 家长 | jiazhang | songjiang |

### 家长上传题库

1. 使用家长账号登录
2. 在"上传新题单"区域选择.md文件
3. 系统自动解析并生成题库

#### .md文件格式要求

```markdown
# 题库标题

说明文字...

### 考点 1.1 考点名称

**题目：** 题目内容

A. 选项A
B. 选项B
C. 选项C
D. 选项D

**答案：** C

**解题过程：**
- 解析内容...

**本题考点：** 考点说明

**复习要点：**
- 复习内容...

---

### 考点 1.2 下一个考点...
```

---

## 📁 文件结构

```
quiz_system/
├── app.py                 # Flask主应用
├── config.py             # 配置文件
├── md_parser.py          # MD解析器
├── requirements.txt      # Python依赖
├── data/                 # 数据目录
│   ├── users/            # 用户数据
│   ├── questions/        # 题目数据（JSON）
│   └── progress/         # 答题进度
├── static/               # 静态文件
│   ├── uploads/          # 上传的.md文件
│   ├── css/
│   └── js/
└── templates/            # HTML模板
    ├── login.html
    ├── student/
    │   ├── dashboard.html
    │   └── exam.html
    └── parent/
        └── dashboard.html
```

---

## 🔒 安全建议

1. **修改默认密码**：在 `config.py` 中修改默认密码
2. **更换密钥**：修改 `SECRET_KEY`
3. **定期备份**：备份 `data` 目录
4. **使用HTTPS**：配置SSL证书

---

## 🐛 故障排查

### 查看日志

```bash
# 查看应用日志
journalctl -u quiz-system -f

# 查看Nginx日志
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### 常见问题

1. **无法访问**
   - 检查防火墙设置
   - 检查Nginx配置
   - 检查服务状态：`systemctl status quiz-system`

2. **上传失败**
   - 检查目录权限：`chmod -R 755 /opt/quiz_system/data`
   - 检查磁盘空间

3. **解析失败**
   - 检查.md格式是否符合要求
   - 查看详细错误日志

---

## 🔄 更新部署

```bash
# 停止服务
systemctl stop quiz-system

# 备份数据
cp -r /opt/quiz_system/data /opt/quiz_system_backup_$(date +%Y%m%d)

# 更新代码（重新上传并解压）
cd /opt/quiz_system

# 重启服务
systemctl start quiz-system
```

---

## 📞 技术支持

如有问题，请检查日志或联系技术支持。
