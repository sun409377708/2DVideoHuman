# Video-Retalking Mac 部署指南

本文档专门针对 Apple Silicon (M1/M2/M3/M4) Mac 的部署说明。

## 1. 系统要求

### 1.1 硬件要求
- Apple Silicon Mac (M1/M2/M3/M4)
- 内存：至少 16GB（推荐）
- 存储：至少 50GB 可用空间

### 1.2 软件要求
- macOS Sonoma 或更新版本
- Homebrew 包管理器
- Miniconda 或 Anaconda

## 2. 基础环境配置

### 2.1 安装 Homebrew
```bash
# 安装 Homebrew（如果尚未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2.2 安装系统依赖
```bash
# 安装 ffmpeg
brew install ffmpeg

# 安装 git（如果需要）
brew install git
```

### 2.3 Python 环境配置
```bash
# 安装 Miniconda（如果尚未安装）
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh

# 创建并激活环境
conda create -n video-retalking python=3.8
conda activate video-retalking
```

### 2.4 安装项目依赖
```bash
# 安装 PyTorch（Apple Silicon 优化版本）
pip install torch==2.0.1 torchvision==0.15.2

# 安装其他依赖
pip install basicsr==1.4.2
pip install kornia==0.7.3
pip install face-alignment==1.3.5
pip install facexlib==0.3.0
pip install dlib==19.24.2
pip install opencv-python==4.11.0.86
pip install librosa==0.10.2.post1
pip install gtts==2.5.4
```

## 3. 项目配置

### 3.1 克隆项目
```bash
git clone https://github.com/vinthony/video-retalking.git
cd video-retalking
```

### 3.2 启动服务
```bash
# 激活环境
conda activate video-retalking

# 启动 web 应用
python app.py
```
访问 http://127.0.0.1:7861

## 4. 性能优化

### 4.1 系统优化
- 关闭不必要的后台应用
- 确保有足够的可用内存
- 使用活动监视器监控系统资源

### 4.2 临时文件管理
```bash
# 创建清理脚本
cat > cleanup.sh << EOF
#!/bin/bash
find ./results -type f -mtime +7 -delete
EOF

chmod +x cleanup.sh

# 添加到 crontab（每天凌晨3点运行）
(crontab -l 2>/dev/null; echo "0 3 * * * $(pwd)/cleanup.sh") | crontab -
```

## 5. 故障排除

### 5.1 常见问题
1. 端口被占用
```bash
# 查看占用端口的进程
lsof -i :7861
# 关闭进程
kill <PID>
```

2. 内存不足
- 关闭其他应用程序
- 减少浏览器标签页
- 监控内存使用：活动监视器

3. 处理速度慢
- 确保使用 Apple Silicon 优化版本的 PyTorch
- 关闭其他资源密集型应用
- 使用较小的视频文件进行测试

### 5.2 日志查看
```bash
# 实时查看输出
tail -f nohup.out  # 如果使用 nohup 运行

# 或者直接在终端运行查看输出
python app.py
```

## 6. 开发建议

### 6.1 本地开发
```bash
# 使用 VS Code 进行开发
code .

# 安装开发依赖
pip install pytest
pip install black
pip install flake8
```

### 6.2 调试技巧
- 使用 VS Code 的调试器
- 添加日志输出
- 使用 Python 的 pdb 调试器

## 7. 维护命令

```bash
# 启动服务（后台运行）
nohup python app.py > nohup.out 2>&1 &

# 查看进程
ps aux | grep python

# 停止服务
pkill -f "python app.py"

# 查看日志
tail -f nohup.out
```

## 8. 注意事项

1. 环境管理：
   - 始终使用 conda 环境
   - 保持依赖版本一致
   - 定期更新依赖包

2. 资源管理：
   - 定期清理临时文件
   - 监控磁盘空间
   - 注意内存使用

3. 性能优化：
   - 利用 Apple Silicon 的优势
   - 适当的并发处理
   - 资源限制管理

4. 安全考虑：
   - 本地访问控制
   - 文件权限管理
   - 定期备份数据

## 9. 备份策略

```bash
# 创建备份脚本
cat > backup.sh << EOF
#!/bin/bash
backup_dir="$HOME/backups/video-retalking"
mkdir -p "$backup_dir"
date_str=$(date +%Y%m%d)
tar -czf "$backup_dir/video-retalking-$date_str.tar.gz" .
EOF

chmod +x backup.sh
```

## 10. 更新和升级

```bash
# 更新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 清理缓存
pip cache purge
conda clean -a
```
