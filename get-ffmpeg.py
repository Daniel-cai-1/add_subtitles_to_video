from gettext import textdomain

from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def audio_to_text_watson(audio_file, api_key, service_url):
    # 创建 IAM 认证器
    authenticator = IAMAuthenticator(api_key)

    # 创建 Speech to Text 客户端
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(service_url)

    # 读取音频文件
    with open(audio_file, "rb") as audio_file:
        response = speech_to_text.recognize(
            audio=audio_file,
            content_type="audio/wav",
            model="zh-CN_BroadbandModel"
        ).get_result()

    # 处理响应
    if "results" in response:
        for result in response["results"]:
            print("识别的文本: {}".format(result["alternatives"][0]["transcript"]))
    else:
        print("未识别到语音")



#提取视频中的音频
def extract_audio(input_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    output_file = "./docs/output.mp3"
    audio.write_audiofile(output_file)
    return output_file


# 将音频转化为可以wav格式，用于转成文本。
def convert_audio_to_wav(input_file, ):
    # 加载音频文件
    audio = AudioSegment.from_file(input_file)
    # 调整采样率为 16 kHz
    audio = audio.set_frame_rate(16000)
    # 增加音量
    audio = audio + 10
    # 导出为 WAV 格式
    output_file = "./docs/output.wav"
    audio.export(output_file, format="wav")
    return output_file


#将得到的文件转为文本
def audio_to_text(audio_file):
    # 创建 Recognizer 实例
    recognizer = sr.Recognizer()

    # 打开音频文件
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)  # 读取音频文件

    try:
        # 使用 Google Web Speech API 进行语音识别
        text = recognizer.recognize_google(audio, language="zh-CN")
        print("识别的文本: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API 无法理解音频")
    except sr.RequestError as e:
        print(f"无法请求 Google Web Speech API; {e}")




def main(input_file):
    mp3_file = extract_audio(input_file)
    wav_file = convert_audio_to_wav(mp3_file)
    text = audio_to_text_google(wav_file)



if __name__ == '__main__':
    # 输入和输出文件路径
    input_file = './docs/test.MOV'
    main(input_file)