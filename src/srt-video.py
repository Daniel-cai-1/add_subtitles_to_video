import subprocess


def add_subtitles_to_video(input_video, subtitle_file, output_video):
    command = [
        "ffmpeg",
        "-i", input_video,
        "-vf", f"subtitles={subtitle_file}",  # 使用滤镜将字幕渲染到视频上
        output_video
    ]
    subprocess.run(command, check=True)
