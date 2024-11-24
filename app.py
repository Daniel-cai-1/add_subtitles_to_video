


def main(input_file):
    mp3_file = extract_audio(input_file)
    wav_file = convert_audio_to_wav(mp3_file)