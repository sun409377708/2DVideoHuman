# 2D Video Human

这是一个基于video-retalking的数字人视频生成项目。可以根据输入的视频和文本，生成对应的数字人说话视频。

## 功能特性

- 支持任意视频源作为输入
- 支持中文文本转语音
- 自动进行人脸检测和特征点提取
- 生成高质量的唇形同步视频
- 提供简单易用的 Web 界面

## 环境要求

- Python 3.12
- pip (最新版本)

详细的依赖和安装步骤请参考 `video-retalking/QUICK_START.md`。

## 快速开始

1. 进入项目目录：
```bash
cd video-retalking
```

2. 启动 Web 界面：
```bash
python app.py
```

3. 在浏览器中访问 http://127.0.0.1:7860

## 使用方法

### Web 界面（推荐）
1. 上传一个包含人脸的视频文件
2. 输入想要说的文字
3. 点击生成按钮
4. 等待处理完成后下载生成的视频

### 命令行方式
如果你需要更多控制，也可以使用命令行方式：

```bash
python inference.py \
    --face INPUT_VIDEO_PATH \
    --audio AUDIO_PATH \
    --outfile OUTPUT_PATH \
    --re_preprocess \
    --img_size 160
```

## 项目结构

- `app.py`: Web 应用入口
- `inference.py`: 核心推理代码
- `QUICK_START.md`: 详细的安装和使用指南
- `checkpoints/`: 模型检查点目录
- `models/`: 模型文件目录
- `examples/`: 示例文件
- `docs/`: 文档

## 注意事项

1. 首次运行时会自动下载必要的模型文件
2. 视频生成时间取决于输入视频的长度和电脑性能
3. 建议使用较短的视频和文本进行测试

## 问题排查

如果遇到问题，请：

1. 确认已经安装了所有必要的依赖
2. 检查是否有必要的模型文件
3. 查看 `QUICK_START.md` 中的常见问题部分

## 许可证

本项目基于 MIT 许可证开源。
