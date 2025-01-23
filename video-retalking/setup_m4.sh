#!/bin/bash

# 设置错误时退出
set -e

echo "开始配置Video Retalking项目环境..."

# 1. 检查并创建项目目录
PROJECT_DIR="$HOME/Desktop/video-retalking"
if [ -d "$PROJECT_DIR" ]; then
    echo "项目目录已存在，将被备份..."
    mv "$PROJECT_DIR" "${PROJECT_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
fi

# 2. 复制项目文件
echo "复制项目文件..."
cp -r "$(pwd)" "$PROJECT_DIR"

# 3. 配置Conda环境
echo "配置Conda环境..."
if ! command -v conda &> /dev/null; then
    echo "错误: 未找到conda命令，请先安装Miniconda或Anaconda"
    exit 1
fi

# 创建新的conda环境
echo "创建conda环境..."
conda create -n video_retalking python=3.8 -y || {
    echo "创建conda环境失败"
    exit 1
}

# 激活环境并安装依赖
echo "安装依赖..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate video_retalking

# 设置pip镜像（可选，如果下载太慢可以取消注释）
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装PyTorch（针对M系列优化）
pip install torch torchvision torchaudio

# 安装其他依赖
pip install gradio==3.50.2
pip install edge-tts==6.1.9
pip install facexlib
pip install basicsr
pip install dlib
pip install librosa
pip install scipy
pip install numpy
pip install opencv-python
pip install pyyaml
pip install safetensors
pip install imageio
pip install imageio-ffmpeg

# 4. 检查模型文件
echo "检查模型文件..."
CHECKPOINTS_DIR="$PROJECT_DIR/checkpoints"
mkdir -p "$CHECKPOINTS_DIR"

# 列出需要的模型文件
MODEL_FILES=(
    "DNet.pt"
    "ENet.pth"
    "LNet.pth"
    "detection_Resnet50_Final.pth"
    "parsing_parsenet.pth"
)

# 检查每个模型文件
for MODEL in "${MODEL_FILES[@]}"; do
    if [ ! -f "$CHECKPOINTS_DIR/$MODEL" ]; then
        echo "警告: 缺少模型文件 $MODEL"
        echo "请确保将模型文件复制到 $CHECKPOINTS_DIR 目录"
    fi
done

# 5. 创建启动脚本
echo "创建启动脚本..."
cat > "$PROJECT_DIR/start_service.sh" << 'EOF'
#!/bin/bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate video_retalking
python app.py
EOF

chmod +x "$PROJECT_DIR/start_service.sh"

echo "
安装完成！

使用说明：
1. 请确保所有模型文件都在 $CHECKPOINTS_DIR 目录中
2. 启动服务：
   cd $PROJECT_DIR
   ./start_service.sh

3. 在浏览器中访问：http://127.0.0.1:7860

注意：
- 如果下载模型文件时遇到网络问题，请检查代理设置
- 首次运行时会自动下载一些额外的模型文件
- 确保有足够的磁盘空间（建议至少20GB）

如果遇到问题，请检查：
1. conda环境是否正确激活
2. 所有模型文件是否存在
3. 网络代理设置是否正确
"
