from googletrans import Translator
from speech_recognition.recognizers import whisper


def transcribe_audio_with_timestamps(audio_file):
    # 加载 Whisper 模型
    model = whisper.load_model("base")
    # 转录音频并生成时间戳
    result = model.transcribe(audio_file)
    return result["segments"]


# 将得到的文件转为文本
import speech_recognition as sr


def wav_to_text(wav_file):
    import assemblyai as aai

    # Replace with your API key
    aai.settings.api_key = "a64bef3a32ac4ff2bdf32e2b498df087"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(wav_file)
    print(transcript.text)
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


def parse_srt(file_path):
    """解析 SRT 文件为一个列表，每项包含时间戳和字幕"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n((?:.|\n)+?)(?=\n\d+\n|\Z)'
    matches = re.findall(pattern, content)
    return [{"index": m[0], "timestamp": m[1], "text": m[2].strip()} for m in matches]


def translate_segments(segments, target_language="zh-cn"):
    translator = Translator()
    translated_segments = []

    for segment in segments:
        # 原始文本
        original_text = segment["text"]
        # 翻译文本
        # translation = translator.translate(original_text, dest=target_language)
        translation = wav_to_text(original_text)
        print(translation)
        # 保存翻译结果
        translated_segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "original_text": original_text,
            "translated_text": translation.text
        })

    return translated_segments
