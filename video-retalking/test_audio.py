from gtts import gTTS
import os
import subprocess

def test_tts():
    # 测试文本
    text = "你好，这是一个测试音频。"
    
    # 首先生成MP3文件
    mp3_path = "test_output.mp3"
    tts = gTTS(text=text, lang='zh-cn')
    tts.save(mp3_path)
    
    # 将MP3转换为WAV
    wav_path = "test_output.wav"
    subprocess.run([
        "ffmpeg", "-i", mp3_path,
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-y",  # 覆盖已存在的文件
        wav_path
    ], check=True)
    
    # 检查文件是否生成
    if os.path.exists(wav_path):
        print(f"音频文件已生成：{wav_path}")
        print(f"文件大小：{os.path.getsize(wav_path)} 字节")
        
        # 删除临时MP3文件
        os.remove(mp3_path)
    else:
        print("音频文件生成失败")

if __name__ == "__main__":
    test_tts()
