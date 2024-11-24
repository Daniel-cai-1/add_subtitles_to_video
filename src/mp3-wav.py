from pydub import AudioSegment


# 将音频转化为可以wav格式，用于转成文本。
def convert_audio_to_wav(input_file):
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
