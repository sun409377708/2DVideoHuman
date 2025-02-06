import os
import sys
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("Python version:", sys.version)
print("Current working directory:", os.getcwd())
print("PYTHONPATH:", sys.path)

import gradio as gr
print("Gradio version:", gr.__version__)

import tempfile
import shutil
import subprocess

def text_to_speech(text, output_path, voice="zh-CN-XiaoxiaoNeural"):
    try:
        # 首先生成MP3文件
        mp3_path = output_path + ".mp3"
        from gtts import gTTS
        tts = gTTS(text=text, lang='zh-cn')
        tts.save(mp3_path)
        
        # 将MP3转换为WAV
        subprocess.run([
            "ffmpeg", "-i", mp3_path,
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-y",  # 覆盖已存在的文件
            output_path
        ], check=True)
        
        # 删除临时MP3文件
        os.remove(mp3_path)
        return True
    except Exception as e:
        logger.error(f"Error in text_to_speech: {str(e)}")
        # 如果转换失败，生成静音音频作为后备
        try:
            subprocess.run([
                "ffmpeg", "-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono",
                "-t", "6",  # 6秒长度
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                "-y",
                output_path
            ], check=True)
            return True
        except Exception as e2:
            logger.error(f"Error generating silent audio: {str(e2)}")
            return False

def process_video(video_path, text_input, fps=15, resolution=320):  
    # 创建临时目录来存储处理后的视频
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "output.mp4")
    audio_path = os.path.join(temp_dir, "temp_audio.wav")
    compressed_input = os.path.join(temp_dir, "compressed_input.mp4")
    final_output = None
    
    try:
        # 首先压缩输入视频
        compress_cmd = [
            "ffmpeg", "-i", video_path,
            "-vf", f"scale={resolution}:{resolution}",
            "-r", str(fps),
            compressed_input
        ]
        subprocess.run(compress_cmd, check=True)
        
        # 将文本转换为音频
        text_to_speech(text_input, audio_path)
        
        # 使用命令行方式调用inference.py，强制重新生成面部特征点
        cmd = [
            "python", "inference.py",
            "--face", compressed_input,
            "--audio", audio_path,
            "--outfile", output_path,
            "--re_preprocess"  # 添加这个参数强制重新生成面部特征点
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        if os.path.exists(output_path):
            # 直接复制到桌面
            desktop_path = os.path.expanduser("~/Desktop/output_video.mp4")
            shutil.copy2(output_path, desktop_path)
            final_output = desktop_path
            print(f"视频已保存到：{desktop_path}")
        
        return final_output
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return None
    finally:
        # 清理临时文件
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def test_video_retalking():
    # 测试参数
    video_path = "examples/face/2.mp4"  # 使用2.mp4作为源视频
    text = "您好，我是爱康医院的数字助理，请问有什么可以帮您？"
    
    # 处理视频
    output_path = process_video(video_path, text)
    
    if output_path:
        print(f"视频生成成功！输出路径：{output_path}")
    else:
        print("视频生成失败！")

# 创建Gradio界面
def create_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# Video ReTalking Demo")
        with gr.Row():
            with gr.Column():
                video_input = gr.Video(label="Upload Video")
                text_input = gr.Textbox(label="Input Text", placeholder="Enter the text you want the person to say...")
                with gr.Row():
                    fps_slider = gr.Slider(minimum=10, maximum=30, value=15, step=1, label="Output FPS")
                    resolution_slider = gr.Slider(minimum=128, maximum=256, value=160, step=16, label="Resolution")
                process_btn = gr.Button("Generate")
            with gr.Column():
                video_output = gr.Video(label="Output Video")
        
        process_btn.click(
            fn=process_video,
            inputs=[video_input, text_input, fps_slider, resolution_slider],
            outputs=[video_output]
        )
    
    return demo

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='Run test')
    args = parser.parse_args()
    
    if args.test:
        test_video_retalking()
    else:
        try:
            logger.info("Starting Gradio server...")
            demo = create_ui()
            logger.info("Created UI, launching server...")
            demo.launch(
                server_name="127.0.0.1",
                server_port=7861,  # 使用7861端口
                share=False
            )
            logger.info("Server launched!")
        except Exception as e:
            logger.error(f"Error starting server: {str(e)}")
            import traceback
            traceback.print_exc()
