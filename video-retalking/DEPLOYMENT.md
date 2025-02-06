# Video-Retalking 服务器部署指南

本文档详细说明如何将 Video-Retalking 项目部署到服务器上，使其成为一个可供多人使用的在线服务。

## 1. 服务器要求

### 1.1 硬件配置
- CPU：至少 4核8线程（推荐 8核16线程）
- 内存：至少 16GB RAM（推荐 32GB）
- 存储：至少 100GB SSD
- 网络带宽：至少 10Mbps（推荐 100Mbps）

### 1.2 操作系统
- Ubuntu 20.04/22.04 LTS（推荐）
- CentOS 7/8 也可以

## 2. 基础环境配置

### 2.1 系统依赖安装
```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装基础工具
sudo apt install -y build-essential python3.8 python3.8-dev python3-pip
sudo apt install -y ffmpeg git nginx supervisor
```

### 2.2 Python 环境配置
```bash
# 安装 Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
source ~/.bashrc

# 创建并激活环境
conda create -n video-retalking python=3.8 -y
conda activate video-retalking
```

### 2.3 项目安装
```bash
# 克隆项目
git clone https://github.com/vinthony/video-retalking.git
cd video-retalking

# 安装依赖
pip install torch==2.0.1 torchvision==0.15.2
pip install basicsr==1.4.2
pip install kornia==0.7.3
pip install face-alignment==1.3.5
pip install facexlib==0.3.0
pip install dlib==19.24.2
pip install opencv-python==4.11.0.86
pip install librosa==0.10.2.post1
pip install gtts==2.5.4
```

## 3. 服务配置

### 3.1 Supervisor 配置
创建文件 `/etc/supervisor/conf.d/video-retalking.conf`:
```ini
[program:video-retalking]
directory=/path/to/video-retalking
command=/path/to/conda/envs/video-retalking/bin/python app.py
user=your_username
autostart=true
autorestart=true
stderr_logfile=/var/log/video-retalking.err.log
stdout_logfile=/var/log/video-retalking.out.log
environment=PATH="/path/to/conda/envs/video-retalking/bin"

# 设置进程数量限制
numprocs=1
process_name=%(program_name)s_%(process_num)02d
```

### 3.2 Nginx 配置
创建文件 `/etc/nginx/sites-available/video-retalking`:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    # SSL 配置（推荐）
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:7861;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 增加超时时间
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        
        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 限制上传文件大小
    client_max_body_size 100M;

    # 静态文件缓存
    location /static {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # 请求频率限制
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
    location /generate {
        limit_req zone=one burst=5;
    }
}
```

## 4. 安全配置

### 4.1 防火墙配置
```bash
# 安装 UFW
sudo apt install ufw

# 配置防火墙规则
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### 4.2 SSL 证书配置
```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your_domain.com
```

## 5. 性能优化

### 5.1 系统优化
```bash
# 设置系统文件描述符限制
echo "* soft nofile 65535" >> /etc/security/limits.conf
echo "* hard nofile 65535" >> /etc/security/limits.conf

# 优化内核参数
cat >> /etc/sysctl.conf << EOF
net.core.somaxconn = 1024
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_max_syn_backlog = 1024
EOF

sysctl -p
```

### 5.2 缓存清理
创建定时任务清理临时文件：
```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天凌晨 3 点清理）
0 3 * * * find /path/to/video-retalking/results -type f -mtime +7 -delete
```

## 6. 监控和维护

### 6.1 日志配置
```bash
# 配置日志轮转
sudo cat > /etc/logrotate.d/video-retalking << EOF
/var/log/video-retalking.*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 640 root root
}
EOF
```

### 6.2 监控配置
推荐使用以下工具之一：
- Prometheus + Grafana
- Zabbix
- Nagios

监控项目包括：
- CPU 使用率
- 内存使用情况
- 磁盘空间
- 网络带宽
- 进程状态
- 请求响应时间

## 7. 扩展建议

### 7.1 任务队列
建议使用 Celery + Redis 实现任务队列，避免同时处理过多请求：
```bash
# 安装依赖
pip install celery redis

# 配置 Celery
# 详细配置请参考 Celery 文档
```

### 7.2 负载均衡
如果有多台服务器，建议配置负载均衡：
- 使用 Nginx 的 upstream 模块
- 或使用云服务商提供的负载均衡服务

### 7.3 数据备份
```bash
# 创建备份脚本
#!/bin/bash
backup_dir="/path/to/backups"
date_str=$(date +%Y%m%d)
tar -czf "$backup_dir/video-retalking-$date_str.tar.gz" /path/to/video-retalking/results
```

## 8. 故障排除

### 8.1 常见问题
1. 服务无法启动
   - 检查日志文件
   - 确认环境变量是否正确
   - 验证端口是否被占用

2. 内存溢出
   - 增加交换空间
   - 限制并发处理数量
   - 清理临时文件

3. 处理超时
   - 调整 Nginx 超时设置
   - 优化处理流程
   - 添加进度反馈

### 8.2 性能调优
- 使用 `top` 和 `htop` 监控系统资源
- 使用 `nginx -t` 测试配置
- 使用 `supervisorctl status` 检查进程状态

## 9. 维护命令

```bash
# 启动服务
sudo supervisorctl start video-retalking

# 停止服务
sudo supervisorctl stop video-retalking

# 重启服务
sudo supervisorctl restart video-retalking

# 查看日志
tail -f /var/log/video-retalking.out.log

# 检查 Nginx 配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

## 10. 注意事项

1. 定期检查和更新：
   - 系统安全更新
   - Python 包更新
   - SSL 证书更新

2. 资源管理：
   - 定期清理临时文件
   - 监控磁盘使用情况
   - 检查日志大小

3. 安全措施：
   - 定期更改密码
   - 检查访问日志
   - 更新防火墙规则

4. 性能优化：
   - 监控系统负载
   - 优化处理队列
   - 调整资源限制
