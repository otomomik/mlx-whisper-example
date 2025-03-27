import mlx_whisper
import datetime

model = "mlx-community/whisper-large-v3-turbo"

segments = mlx_whisper.transcribe(
    "example.mp3", path_or_hf_repo=model, word_timestamps=True, language="ja"
)["segments"]

for segment in segments:
    start_time = segment["start"]
    text = segment["text"]

    time_str = str(datetime.timedelta(seconds=start_time))
    print(f"[{time_str}] {text}")
