# Video-Retalking Quick Start Guide

## 环境要求
- Python 3.12
- pip (最新版本)

## 依赖安装
```bash
# 1. 安装特定版本的 numpy
pip install "numpy<2.0.0"

# 2. 安装 torch 和 torchvision
pip install torchvision==0.15.2

# 3. 安装其他必要依赖
pip install einops
pip install kornia
pip install facexlib
pip install librosa

# 4. 安装 gtts (用于文字转语音)
pip install gtts
```

## 使用方法

### 1. 使用 Web 界面（推荐）
```bash
python app.py
```
启动后访问 http://127.0.0.1:7860

### 2. 使用命令行
#### 2.1 生成语音文件
```python
from gtts import gTTS

# 生成中文语音
text = "要说的话"
tts = gTTS(text, lang='zh')
tts.save('temp_audio.wav')
```

#### 2.2 生成视频
```bash
python inference.py \
    --face INPUT_VIDEO_PATH \
    --audio AUDIO_PATH \
    --outfile OUTPUT_PATH \
    --re_preprocess \
    --img_size 160
```

例如：
```bash
python inference.py \
    --face examples/face/3.mp4 \
    --audio temp_audio.wav \
    --outfile output.mp4 \
    --re_preprocess \
    --img_size 160
```

## 日常使用（已安装环境）
如果你已经完成了上述环境配置，重启电脑后只需要：

1. 打开终端，进入项目目录：
```bash
cd /Users/jianqin/Desktop/2dHuman/video-retalking
```

2. 启动 web 应用：
```bash
python app.py
```

3. 在浏览器中访问 http://127.0.0.1:7860

## 参数说明
- `--face`: 输入视频路径
- `--audio`: 输入音频路径
- `--outfile`: 输出视频路径
- `--re_preprocess`: 重新预处理
- `--img_size`: 视频分辨率大小

## 注意事项
1. 首次运行时会自动下载一些模型文件，需要等待一段时间
2. 视频生成过程可能需要几分钟到几十分钟不等，取决于视频长度和电脑性能
3. 建议使用较短的视频和文本进行测试

## 常见问题
1. 如果出现端口被占用的错误，可以使用以下命令查找并关闭占用端口的进程：
```bash
lsof -i :7860
kill <PID>
```

2. 如果生成的视频质量不理想，可以：
   - 增加 `--img_size` 的值（如 256、512 等）
   - 使用更清晰的输入视频
   - 确保输入视频中人物面部清晰可见

## 模型文件位置
所有必要的模型文件应该位于 `checkpoints` 目录下：
- DNet.pt
- LNet.pth
- ENet.pth
