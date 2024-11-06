from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
import io

def audio_to_text_google(audio_file):
    # 创建 Speech-to-Text 客户端
    client = speech.SpeechClient()

    # 读取音频文件
    with io.open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    # 配置音频文件
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="zh-CN",
    )

    # 发送请求
    response = client.recognize(config, audio)

    # 处理响应
    for result in response.results:
        print("识别的文本: {}".format(result.alternatives[0].transcript))




if __name__ == "__main__":
    audio_file = "input_audio.wav"  # 替换为你的音频文件路径
    audio_to_text(audio_file)