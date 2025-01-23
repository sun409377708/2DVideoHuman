# 2D Video Human

这是一个基于video-retalking的数字人视频生成项目。可以根据输入的视频和文本，生成对应的数字人说话视频。

## 功能特性

- 支持任意视频源作为输入
- 支持中文文本转语音
- 自动进行人脸检测和特征点提取
- 生成高质量的唇形同步视频

## 环境要求

- Python 3.8
- PyTorch
- FFmpeg
- 其他依赖请参考 `video-retalking/requirements.txt`

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/sun409377708/2DVideoHuman.git
cd 2DVideoHuman
```

2. 安装依赖：
```bash
cd video-retalking
pip install -r requirements.txt
```

3. 下载预训练模型：
```bash
# 创建checkpoints目录
mkdir checkpoints
# 下载模型文件到checkpoints目录
```

## 使用方法

1. 准备一个人脸视频文件，放在`video-retalking/examples/face/`目录下

2. 运行测试：
```python
python app.py --test
```

3. 自定义生成：
```python
from app import process_video

# 处理视频
video_path = "examples/face/your_video.mp4"
text = "你想要数字人说的话"
output_path = process_video(video_path, text)
```

## 项目结构

```
2DVideoHuman/
├── video-retalking/       # 核心代码目录
│   ├── app.py            # 主应用程序
│   ├── inference.py      # 推理代码
│   ├── models/          # 模型定义
│   ├── utils/           # 工具函数
│   └── third_part/      # 第三方依赖
└── README.md
```

## 注意事项

- 确保输入视频中包含清晰的人脸
- 视频分辨率建议不要太大，可以预处理到320x320
- 生成的视频会保存在桌面上

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

本项目遵循MIT许可证。详见LICENSE文件。
