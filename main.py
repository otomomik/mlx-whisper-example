import sys
import mlx_whisper
from datetime import datetime, timedelta, timezone


model = "mlx-community/whisper-large-v3-turbo"
input = sys.argv[1]
output = sys.argv[2]

if input == "" or output == "":
    raise TypeError("Output file is required")

segments = mlx_whisper.transcribe(
    input,
    path_or_hf_repo=model,
    word_timestamps=True,
    language="ja",
)["segments"]

start_second = int(input.split("/")[-1].split("_")[0])


def convert_timestamp_with_seconds(milliseconds, added_seconds):
    # ミリ秒を日時に変換
    utc_time = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(
        milliseconds=milliseconds
    )

    # 秒数を加える
    modified_time = utc_time + timedelta(seconds=added_seconds)

    # JSTに変換（UTC+9時間）
    jst_time = modified_time.astimezone(timezone(timedelta(hours=9)))

    # フォーマット `yyyy-mm-dd hh:mm:ss`
    formatted_time = jst_time.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_time


with open(output, "w") as f:
    for segment in segments:
        text = segment["text"]

        if text == "":
            continue

        start_time = int(segment["start"])
        time_str = convert_timestamp_with_seconds(start_second, start_time)

        f.write(f"[{time_str}] {text}\n")
