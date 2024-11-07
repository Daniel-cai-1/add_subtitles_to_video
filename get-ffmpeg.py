from gettext import textdomain
from gtts import gTTS
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







def main(input_file):
    # mp3_file = extract_audio(input_file) # 视频转语音
    # wav_file = convert_audio_to_wav(mp3_file) # 语音转wav格式
    # english_file = wav_to_text(wav_file) #wav转文本
    # # 英文转中文
    # translated_text = translate_long_text(english_file)
    # print(translated_text)
    translated_text = "我想告诉你，失去东西不仅仅意味着失去很多时间。当我们失去东西时，我们也会得到东西。现在，你离开学校的结构和框架，走上自己的道路。您做出的每一个选择都会导致下一个选择，从而导致下一个选择。我知道很难知道该走哪条路。生活中有些时候，你需要为自己挺身而出。当正确的事情实际上是退缩和道歉的时候。当正确的事情是战斗的时候。转身奔跑是正确的时刻。是时候坚持你所拥有的一切了。优雅地放手的时候。有时候，正确的做法是以进步和改革的名义抛弃旧的思想流派。有时候，正确的做法是坐下来倾听那些来到我们面前的人的智慧。在这些关键时刻，您如何知道正确的选择是什么？你不会的。我如何向这么多人提供有关他们人生选择的建议？我不会。可怕的消息是你现在只能靠你自己了。但好消息是，你现在只能靠自己了。我把这个留给你。我们是，我们被我们的直觉，我们的直觉，我们的欲望和恐惧，我们的伤疤和我们的梦想所引导。有时你会把它搞砸。我也是。当我这样做的时候，您很可能会在互联网上看到它。困难的事情会发生在我们身上。我们会康复的，我们会从中吸取教训的。因此，我们将变得更有韧性。王。"
    tts = gTTS(text=translated_text, lang="zh") #
    tts.save("output_zh.mp3")


if __name__ == '__main__':
    # 输入和输出文件路径
    input_file = './docs/data2.MP4'
    main(input_file)