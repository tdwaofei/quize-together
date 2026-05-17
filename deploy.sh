#!/bin/bash
# 信息学竞赛练习系统 - 快速部署脚本

set -e

echo "🚀 开始部署信息学竞赛练习系统..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否以root运行
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用root权限运行此脚本${NC}"
    exit 1
fi

# 安装依赖
echo -e "${YELLOW}📦 安装系统依赖...${NC}"
apt update
apt install -y python3 python3-pip nginx git

# 创建应用目录
APP_DIR="/opt/quiz_system"
echo -e "${YELLOW}📁 创建应用目录: $APP_DIR${NC}"
mkdir -p $APP_DIR

# 检查代码是否存在
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ 错误：在当前目录找不到app.py文件${NC}"
    echo "请确保在exam_system目录中运行此脚本"
    exit 1
fi

# 复制代码到应用目录
echo -e "${YELLOW}📋 复制代码到应用目录...${NC}"
cp -r ./* $APP_DIR/
cd $APP_DIR

# 安装Python依赖
echo -e "${YELLOW}🐍 安装Python依赖...${NC}"
pip3 install -r requirements.txt

# 创建数据目录
echo -e "${YELLOW}💾 创建数据目录...${NC}"
mkdir -p data/users data/questions data/progress static/uploads
chmod -R 755 data static

# 创建系统服务
echo -e "${YELLOW}⚙️  创建系统服务...${NC}"
cat > /etc/systemd/system/quiz-system.service << 'EOF'
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
EOF

# 创建Nginx配置
echo -e "${YELLOW}🌐 配置Nginx...${NC}"
cat > /etc/nginx/sites-available/quiz-system << 'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

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
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用Nginx配置
if [ -f /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
fi
ln -sf /etc/nginx/sites-available/quiz-system /etc/nginx/sites-enabled/

# 测试Nginx配置
nginx -t

# 启动服务
echo -e "${YELLOW}▶️  启动服务...${NC}"
systemctl daemon-reload
systemctl enable quiz-system
systemctl start quiz-system
systemctl restart nginx

# 配置防火墙
echo -e "${YELLOW}🔒 配置防火墙...${NC}"
ufw allow 80/tcp
ufw allow 22/tcp
ufw --force enable

# 检查服务状态
echo -e "${YELLOW}✅ 检查服务状态...${NC}"
if systemctl is-active --quiet quiz-system; then
    echo -e "${GREEN}✅ Flask应用运行正常${NC}"
else
    echo -e "${RED}❌ Flask应用启动失败${NC}"
    systemctl status quiz-system
    exit 1
fi

if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx运行正常${NC}"
else
    echo -e "${RED}❌ Nginx启动失败${NC}"
    exit 1
fi

# 获取IP地址
IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo ""
echo -e "${GREEN}🎉 部署成功！${NC}"
echo ""
echo "📍 访问地址："
echo "  - 本机: http://localhost"
echo "  - 内网: http://$IP_ADDRESS"
echo "  - 公网: http://$(curl -s ifconfig.me 2>/dev/null || echo '请查看服务器公网IP')"
echo ""
echo "👤 默认账号："
echo "  - 孩子：haizi / mima123"
echo "  - 家长：jiazhang / mima456"
echo ""
echo "⚠️  请立即修改默认密码！"
echo ""
echo "📁 应用目录：$APP_DIR"
echo "📊 查看日志：journalctl -u quiz-system -f"
echo ""
echo -e "${YELLOW}⚠️  安全提示：请及时修改默认密码！${NC}"
