"""
Quick SRT Generator for Rutube Videos
Simple script to generate subtitles for all videos in downloads folder.
"""

import os
import sys
import subprocess
from faster_whisper import WhisperModel
from datetime import timedelta

def format_time(seconds):
    """Format seconds to SRT timestamp"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    milliseconds = int((seconds - int(seconds)) * 1000)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds_int = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds_int:02},{milliseconds:03}"

def create_subtitles():
    """Create subtitles for all videos in downloads folder"""

    # Check downloads folder
    downloads = "downloads"
    if not os.path.exists(downloads):
        print("❌ No downloads folder found")
        return

    # Find video files
    videos = []
    for file in os.listdir(downloads):
        if file.lower().endswith(('.mp4', '.mkv', '.webm', '.avi')):
            videos.append(os.path.join(downloads, file))

    if not videos:
        print("❌ No video files found")
        return

    print(f"Found {len(videos)} video(s)")

    # Create subtitles folder
    subs_folder = "subtitles"
    os.makedirs(subs_folder, exist_ok=True)

    # Load model
    print("Loading whisper model...")
    model = WhisperModel("base", device="cpu", compute_type="int8")

    # Process each video
    for i, video_path in enumerate(videos, 1):
        video_name = os.path.basename(video_path)
        print(f"\n[{i}/{len(videos)}] Processing: {video_name}")

        # Generate output filename
        base_name = os.path.splitext(video_name)[0]
        srt_file = os.path.join(subs_folder, f"{base_name}.srt")

        # Skip if already exists
        if os.path.exists(srt_file):
            print(f"  ⏭️  SRT already exists, skipping...")
            continue

        # Transcribe
        try:
            segments, info = model.transcribe(
                video_path,
                language="ru",
                word_timestamps=True,
                vad_filter=True
            )

            # Create SRT
            with open(srt_file, "w", encoding="utf-8") as f:
                for j, segment in enumerate(segments, 1):
                    start = format_time(segment.start)
                    end = format_time(segment.end)
                    text = segment.text.strip()

                    f.write(f"{j}\n")
                    f.write(f"{start} --> {end}\n")
                    f.write(f"{text}\n\n")

            print(f"  ✅ Created: {os.path.basename(srt_file)}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n✅ Done! Subtitles saved in '{subs_folder}' folder")

if __name__ == "__main__":
    # Check for faster-whisper
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Installing faster-whisper...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "faster-whisper"])
        from faster_whisper import WhisperModel

    create_subtitles()
