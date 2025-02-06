# Video-Retalking Quick Start Guide

## 环境要求
- Python 3.8 (必须是3.8版本)
- conda (推荐使用 miniconda)

## 环境配置
```bash
# 1. 创建并激活 conda 环境
conda create -n video-retalking python=3.8
conda activate video-retalking

# 2. 安装核心依赖包
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

## 使用方法

### 1. 使用 Web 界面（推荐）
```bash
# 1. 激活环境
conda activate video-retalking

# 2. 启动应用
python app.py
```
启动后访问 http://127.0.0.1:7861

### 2. 使用命令行
#### 2.1 生成语音文件
```bash
# 1. 生成 mp3 文件
python -c "
from gtts import gTTS
tts = gTTS(text='要说的话', lang='zh-cn')
tts.save('temp_audio.mp3')
"

# 2. 转换为 wav 格式
ffmpeg -i temp_audio.mp3 -acodec pcm_s16le -ar 16000 -ac 1 -y temp_audio.wav
```

#### 2.2 生成视频
```bash
# 1. 创建输出目录
mkdir -p results

# 2. 运行生成
python inference.py \
    --face examples/face/3.mp4 \
    --audio temp_audio.wav \
    --outfile results/output.mp4 \
    --re_preprocess
```

生成的视频将保存在 `results` 目录下。

## 日常使用（已安装环境）
如果你已经完成了上述环境配置，重启电脑后只需要：

1. 激活环境：
```bash
conda activate video-retalking
```

2. 进入项目目录：
```bash
cd /Users/jianqin/Desktop/2dHuman/video-retalking
```

3. 启动 web 应用：
```bash
python app.py
```

4. 在浏览器中访问 http://127.0.0.1:7861

## 参数说明
- `--face`: 输入视频路径
- `--audio`: 输入音频路径
- `--outfile`: 输出视频路径
- `--re_preprocess`: 重新预处理

## 注意事项
1. 必须使用 Python 3.8，其他版本可能会导致依赖包不兼容
2. 确保使用 conda 环境 `video-retalking`，不要在 base 环境中运行
3. 首次运行时会自动下载一些模型文件，需要等待一段时间
4. 视频生成过程可能需要几分钟到几十分钟不等，取决于视频长度和电脑性能

## 常见问题
1. 如果出现端口被占用的错误，可以：
   - 修改 app.py 中的端口号（默认 7861）
   - 或使用以下命令查找并关闭占用端口的进程：
   ```bash
   lsof -i :7861
   kill <PID>
   ```

2. 如果遇到 "No module named 'xxx'" 错误：
   - 确保已激活正确的 conda 环境
   - 重新安装对应的依赖包

3. 如果生成的视频质量不理想：
   - 使用更清晰的输入视频
   - 确保输入视频中人物面部清晰可见
