from moviepy.video.io.VideoFileClip import VideoFileClip


# 提取视频中的音频
def extract_audio(input_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    output_file = "../docs/output.mp3"
    audio.write_audiofile(output_file)
    return output_file


if __name__ == '__main__':
    input_file = ""
    extract_audio(input_file)
