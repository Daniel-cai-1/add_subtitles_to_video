import math
import whisper
from future.standard_library import import_
from googletrans import Translator
import assemblyai as aai

from srt2video import add_subtitles_to_video


def transcribe_audio_with_timestamps(audio_file):
    # 加载 Whisper 模型
    model = whisper.load_model("base")
    # 转录音频并生成时间戳
    result = model.transcribe(audio_file)
    return result["segments"]

def wav_to_text(english_text):
    from googletrans import Translator
    # 创建翻译器
    translator = Translator()
    # 输入英文文本
    # 翻译英文文本为中文
    translated = translator.translate(english_text, src='en', dest='zh-cn')
    return translated


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


def generate_srt_from_translated_segments(translated_segments):
    filename = "translated_subtitles.srt"
    srt_content = ""
    for i, segment in enumerate(translated_segments):
        start = segment["start"]
        end = segment["end"]

        # 格式化 SRT 的时间戳
        start_hour = int(start // 3600)
        start_min = int((start % 3600) // 60)
        start_sec = int(start % 60)
        start_msec = int((start - int(start)) * 1000)

        end_hour = int(end // 3600)
        end_min = int((end % 3600) // 60)
        end_sec = int(end % 60)
        end_msec = int((end - int(end)) * 1000)

        srt_content += f"{i + 1}\n"
        srt_content += f"{start_hour:02}:{start_min:02}:{start_sec:02},{start_msec:03} --> {end_hour:02}:{end_min:02}:{end_sec:02},{end_msec:03}\n"
        srt_content += f"{segment['translated_text']}\n\n"

    # 将 SRT 内容写入文件
    with open(filename, "w", encoding="utf-8") as file:
        file.write(srt_content)
    return filename




if __name__ == '__main__':
    # 进行语音识别并获取每个段落的时间戳
    segments = transcribe_audio_with_timestamps("../docs/output.wav")
    # 打印识别结果
    for segment in segments:
        print(f"Start: {segment['start']}, End: {segment['end']}, Text: {segment['text']}")
    translated_segments = translate_segments(segments, target_language="zh-cn")
    # 生成翻译后的 SRT 字幕文件
    filename = generate_srt_from_translated_segments(translated_segments)
    input_video = "../docs/data.mp4"
    output_video = "../docs/output.mp4"
    add_subtitles_to_video(input_video, filename, output_video)
