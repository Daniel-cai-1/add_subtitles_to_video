
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from srt2video import add_subtitles_to_video
from text2srt import generate_srt_from_translated_segments, translate_segments, \
    transcribe_audio_with_timestamps


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
    output_file = "../docs/output.mp3"
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
    output_file = "../docs/output.wav"
    audio.export(output_file, format="wav")
    return output_file


#将得到的文件转为文本
import speech_recognition as sr
def wav_to_text(wav_file):
    import assemblyai as aai

    # Replace with your API key
    aai.settings.api_key = "a64bef3a32ac4ff2bdf32e2b498df087"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(wav_file)
    print(transcript.text)

    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(text)
    return transcript.text


import requests

def split_text(text, max_length=500):
    # 将长文本分成多个小段，每段不超过指定的字符长度
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def mymemory_translate(text, lang_from="en", lang_to="zh-cn"):
    # MyMemory 翻译函数
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": f"{lang_from}|{lang_to}"}
    response = requests.get(url, params=params)
    return response.json()["responseData"]["translatedText"]

def translate_long_text(text, lang_from="en", lang_to="zh-cn"):
    # 分段翻译长文本
    segments = split_text(text)
    translated_segments = []

    for segment in segments:
        translation = mymemory_translate(segment, lang_from, lang_to)
        translated_segments.append(translation)

    return ''.join(translated_segments)


def main(input_file, output_video):
    mp3_file = extract_audio(input_file) # 视频转语音
    wav_file = convert_audio_to_wav(mp3_file) # 语音转wav格式
    # 进行语音识别并获取每个段落的时间戳
    segments = transcribe_audio_with_timestamps(wav_file)
    # 打印识别结果
    for segment in segments:
        print(f"Start: {segment['start']}, End: {segment['end']}, Text: {segment['text']}")
    translated_segments = translate_segments(segments, target_language="zh-cn")
    # 生成翻译后的 SRT 字幕文件
    filename = generate_srt_from_translated_segments(translated_segments)

    add_subtitles_to_video(input_file, filename, output_video)


if __name__ == '__main__':
    # 输入和输出文件路径
    input_file = '../docs/data.MP4'
    output_video = "../docs/output.mp4"
    main(input_file, output_video)