# create_subtitles.py
"""
Rutube Video Subtitles Generator
================================

A Python tool to generate SRT subtitle files for downloaded Rutube videos
using faster-whisper for speech recognition.

Author: Andrew Gotham
Email: andreogotema@gmail.com
Telegram: https://t.me/SirAndrewGotham

Features:
- Process all videos in downloads folder
- Generate accurate Russian subtitles
- Create properly formatted SRT files
- Progress tracking and error handling
- Configurable model settings

Requirements:
- Python 3.7+
- faster-whisper
- yt-dlp (for video metadata)

Usage:
    python create_subtitles.py

License: MIT
"""

import os
import sys
import subprocess
import time
import json
from datetime import timedelta
import re
from pathlib import Path

# Constants
DOWNLOADS_FOLDER = "downloads"
SUBTITLES_FOLDER = "subtitles"
SUPPORTED_EXTENSIONS = ('.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv', '.wmv')
VERSION = "1.0.0"

def print_header():
    """Print the application header"""
    print("=" * 60)
    print("🎬 RUTUBE SUBTITLES GENERATOR")
    print(f"📱 Version: {VERSION}")
    print("=" * 60)
    print("📧 Contact: Andrew Gotham")
    print("📧 Email: andreogotema@gmail.com")
    print("📱 Telegram: https://t.me/SirAndrewGotham")
    print("=" * 60)

def check_dependencies():
    """Check and install required packages"""
    print("🔍 Checking dependencies...")

    required_packages = ['faster-whisper']

    for package in required_packages:
        try:
            if package == 'faster-whisper':
                import faster_whisper
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False

    return True

def format_timestamp(seconds):
    """
    Convert seconds to SRT timestamp format (HH:MM:SS,mmm)

    Args:
        seconds (float): Time in seconds

    Returns:
        str: Formatted timestamp
    """
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    milliseconds = int((seconds - int(seconds)) * 1000)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds_int = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"

def create_srt_from_segments(segments, output_file, language="ru"):
    """
    Create SRT subtitles from whisper segments

    Args:
        segments (list): List of transcription segments
        output_file (str): Path to output SRT file
        language (str): Language code for subtitles
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments, 1):
                start_time = format_timestamp(segment.start)
                end_time = format_timestamp(segment.end)
                text = segment.text.strip()

                # Write SRT entry
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

        return True

    except Exception as e:
        print(f"❌ Error creating SRT file: {e}")
        return False

def transcribe_video(video_path, model_size="base", language="ru"):
    """
    Transcribe video file using faster-whisper

    Args:
        video_path (str): Path to video file
        model_size (str): Whisper model size (tiny, base, small, medium, large)
        language (str): Language code for transcription

    Returns:
        dict: Transcription results or None if failed
    """
    try:
        from faster_whisper import WhisperModel

        print(f"   🧠 Loading Whisper model ({model_size})...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

        print(f"   🎙 Transcribing audio...")

        # Transcribe with word timestamps for better accuracy
        segments, info = model.transcribe(
            video_path,
            language=language,
            word_timestamps=True,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
        )

        # Convert to list
        segments_list = list(segments)

        print(f"   📊 Language detected: {info.language}")
        print(f"   📊 Duration: {info.duration:.1f} seconds")
        print(f"   📊 Segments: {len(segments_list)}")

        return {
            "segments": segments_list,
            "language": info.language,
            "duration": info.duration,
            "model": model_size
        }

    except Exception as e:
        print(f"   ❌ Transcription error: {e}")
        return None

def process_video_file(video_path, model_size="base", language="ru"):
    """
    Process a single video file and generate subtitles

    Args:
        video_path (str): Path to video file
        model_size (str): Whisper model size
        language (str): Language code

    Returns:
        bool: True if successful, False otherwise
    """
    video_name = os.path.basename(video_path)
    print(f"\n📹 Processing: {video_name}")
    print(f"   📍 Path: {video_path}")

    # Get file size
    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"   💾 Size: {file_size_mb:.1f} MB")

    # Create subtitles folder if it doesn't exist
    os.makedirs(SUBTITLES_FOLDER, exist_ok=True)

    # Generate output filename
    base_name = os.path.splitext(video_name)[0]
    srt_filename = f"{base_name}.srt"
    srt_path = os.path.join(SUBTITLES_FOLDER, srt_filename)

    # Check if SRT already exists
    if os.path.exists(srt_path):
        print(f"   ⚠️  SRT file already exists: {srt_filename}")
        overwrite = input(f"   Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print(f"   ⏭️  Skipping...")
            return True

    # Transcribe video
    start_time = time.time()
    result = transcribe_video(video_path, model_size, language)

    if not result:
        print(f"   ❌ Failed to transcribe video")
        return False

    # Create SRT file
    print(f"   📝 Creating SRT file...")
    success = create_srt_from_segments(result["segments"], srt_path, language)

    if not success:
        print(f"   ❌ Failed to create SRT file")
        return False

    # Create additional metadata file
    metadata_path = os.path.join(SUBTITLES_FOLDER, f"{base_name}_info.json")
    metadata = {
        "video_file": video_name,
        "srt_file": srt_filename,
        "language": result["language"],
        "duration": result["duration"],
        "model": result["model"],
        "processing_time": time.time() - start_time,
        "segments_count": len(result["segments"]),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"   📊 Metadata saved: {os.path.basename(metadata_path)}")
    except:
        print(f"   ⚠️  Could not save metadata")

    print(f"   ✅ SRT created: {srt_filename}")
    print(f"   ⏱️  Processing time: {time.time() - start_time:.1f} seconds")

    return True

def find_video_files():
    """
    Find all video files in downloads folder

    Returns:
        list: List of video file paths
    """
    video_files = []

    if not os.path.exists(DOWNLOADS_FOLDER):
        print(f"❌ Downloads folder not found: {DOWNLOADS_FOLDER}")
        return video_files

    print(f"\n🔍 Scanning {DOWNLOADS_FOLDER} for video files...")

    for file in os.listdir(DOWNLOADS_FOLDER):
        file_path = os.path.join(DOWNLOADS_FOLDER, file)
        if os.path.isfile(file_path) and file.lower().endswith(SUPPORTED_EXTENSIONS):
            video_files.append(file_path)

    print(f"📹 Found {len(video_files)} video file(s)")
    return video_files

def show_processing_summary(processed, total, failed_files):
    """
    Show summary of processing results

    Args:
        processed (int): Number of successfully processed files
        total (int): Total number of files
        failed_files (list): List of failed file names
    """
    print("\n" + "=" * 60)
    print("📊 PROCESSING SUMMARY")
    print("=" * 60)
    print(f"📹 Total videos: {total}")
    print(f"✅ Successfully processed: {processed}")
    print(f"❌ Failed: {total - processed}")

    if processed > 0:
        print(f"\n📁 Subtitles saved in: {os.path.abspath(SUBTITLES_FOLDER)}")

        # List generated SRT files
        if os.path.exists(SUBTITLES_FOLDER):
            srt_files = [f for f in os.listdir(SUBTITLES_FOLDER) if f.endswith('.srt')]
            if srt_files:
                print(f"\n📝 Generated SRT files ({len(srt_files)}):")
                for i, srt_file in enumerate(srt_files[:10], 1):
                    print(f"   {i:2d}. {srt_file}")
                if len(srt_files) > 10:
                    print(f"   ... and {len(srt_files) - 10} more")

    if failed_files:
        print(f"\n⚠️  Failed files:")
        for file in failed_files:
            print(f"   ❌ {os.path.basename(file)}")

        # Save failed files list
        failed_list_path = os.path.join(SUBTITLES_FOLDER, "failed_files.txt")
        try:
            with open(failed_list_path, "w", encoding="utf-8") as f:
                f.write("Failed to process:\n")
                f.write("=" * 40 + "\n")
                for file in failed_files:
                    f.write(f"{os.path.basename(file)}\n")
            print(f"\n📝 Failed files list saved to: {failed_list_path}")
        except:
            pass

def select_model():
    """
    Let user select whisper model size

    Returns:
        str: Selected model size
    """
    print("\n🤖 SELECT WHISPER MODEL")
    print("-" * 40)
    print("Model sizes (larger = more accurate but slower):")
    print("1. tiny   - Fastest, lowest accuracy")
    print("2. base   - Balanced (recommended)")
    print("3. small  - Better accuracy")
    print("4. medium - High accuracy, slower")
    print("5. large  - Best accuracy, slowest")
    print("-" * 40)

    models = {
        '1': 'tiny',
        '2': 'base',
        '3': 'small',
        '4': 'medium',
        '5': 'large'
    }

    while True:
        choice = input("Choose model (1-5, default 2): ").strip()
        if not choice:
            return 'base'
        if choice in models:
            return models[choice]
        print("❌ Invalid choice. Please enter 1-5.")

def select_language():
    """
    Let user select language for transcription

    Returns:
        str: Language code
    """
    print("\n🌍 SELECT LANGUAGE")
    print("-" * 40)
    print("1. Russian (ru) - Default for Rutube")
    print("2. English (en)")
    print("3. Auto-detect")
    print("-" * 40)

    while True:
        choice = input("Choose language (1-3, default 1): ").strip()
        if not choice:
            return 'ru'
        if choice == '1':
            return 'ru'
        elif choice == '2':
            return 'en'
        elif choice == '3':
            return None  # Let whisper auto-detect
        print("❌ Invalid choice. Please enter 1-3.")

def batch_process_videos():
    """
    Process all videos in downloads folder
    """
    # Find video files
    video_files = find_video_files()

    if not video_files:
        print("❌ No video files found in downloads folder.")
        print(f"   Supported extensions: {', '.join(SUPPORTED_EXTENSIONS)}")
        return

    # Show found files
    print("\n📹 Found video files:")
    for i, file_path in enumerate(video_files, 1):
        file_name = os.path.basename(file_path)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"   {i:2d}. {file_name} ({size_mb:.1f} MB)")

    # Let user select which files to process
    print("\n🎯 SELECT FILES TO PROCESS")
    print("-" * 40)
    print("1. Process all files")
    print("2. Select specific files")
    print("-" * 40)

    choice = input("Choose option (1-2, default 1): ").strip()

    files_to_process = []

    if choice == '2':
        # Let user select specific files
        print("\nEnter file numbers to process (comma-separated, e.g., 1,3,5)")
        print("Or press Enter to process all files")

        selection = input("File numbers: ").strip()

        if selection:
            try:
                selected_indices = [int(idx.strip()) for idx in selection.split(',')]
                for idx in selected_indices:
                    if 1 <= idx <= len(video_files):
                        files_to_process.append(video_files[idx-1])
            except:
                print("❌ Invalid selection. Processing all files.")
                files_to_process = video_files
        else:
            files_to_process = video_files
    else:
        files_to_process = video_files

    if not files_to_process:
        print("❌ No files selected for processing.")
        return

    # Select model and language
    model_size = select_model()
    language = select_language()

    print(f"\n⚙️  Settings:")
    print(f"   Model: {model_size}")
    print(f"   Language: {language if language else 'auto-detect'}")

    # Confirm processing
    print(f"\n⚠️  Ready to process {len(files_to_process)} video(s)")
    print("   This may take a while depending on video lengths and model size.")

    confirm = input("\nStart processing? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Processing cancelled.")
        return

    # Process files
    processed_count = 0
    failed_files = []

    print(f"\n🚀 Starting processing...")

    for i, video_path in enumerate(files_to_process, 1):
        print(f"\n{'='*50}")
        print(f"🔄 Processing file {i} of {len(files_to_process)}")
        print(f"{'='*50}")

        success = process_video_file(video_path, model_size, language)

        if success:
            processed_count += 1
        else:
            failed_files.append(video_path)

        # Add delay between processing to prevent overheating
        if i < len(files_to_process):
            delay = 2  # 2 second delay between files
            print(f"\n⏳ Waiting {delay} seconds before next file...")
            time.sleep(delay)

    # Show summary
    show_processing_summary(processed_count, len(files_to_process), failed_files)

    # Instructions for using subtitles
    if processed_count > 0:
        print("\n🎬 HOW TO USE SUBTITLES:")
        print("-" * 40)
        print("1. Make sure video file and SRT file have the same name")
        print("2. Place both files in the same folder")
        print("3. Open video in a player that supports SRT subtitles:")
        print("   - VLC Media Player (recommended)")
        print("   - MPC-HC")
        print("   - PotPlayer")
        print("   - SMPlayer")
        print("\n4. In VLC: Subtitles → Add Subtitle File")
        print("5. Or simply rename SRT to match video exactly")
        print(f"\n📁 Your subtitles are in: {os.path.abspath(SUBTITLES_FOLDER)}")

def process_single_video():
    """
    Process a single video file
    """
    print("\n📥 SINGLE VIDEO PROCESSING")
    print("-" * 40)

    # Show files in downloads folder
    video_files = find_video_files()

    if not video_files:
        print("❌ No video files found in downloads folder.")
        return

    print("\n📹 Available video files:")
    for i, file_path in enumerate(video_files, 1):
        file_name = os.path.basename(file_path)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"   {i:2d}. {file_name} ({size_mb:.1f} MB)")

    # Let user select file
    try:
        choice = int(input(f"\nSelect file number (1-{len(video_files)}): "))
        if 1 <= choice <= len(video_files):
            video_path = video_files[choice-1]
        else:
            print("❌ Invalid selection.")
            return
    except:
        print("❌ Invalid input.")
        return

    # Select model and language
    model_size = select_model()
    language = select_language()

    print(f"\n⚙️  Settings:")
    print(f"   Model: {model_size}")
    print(f"   Language: {language if language else 'auto-detect'}")

    # Process the file
    success = process_video_file(video_path, model_size, language)

    if success:
        print(f"\n✅ Processing completed!")
        srt_name = os.path.splitext(os.path.basename(video_path))[0] + ".srt"
        print(f"📝 Subtitle file: {SUBTITLES_FOLDER}/{srt_name}")
    else:
        print(f"\n❌ Processing failed.")

def view_subtitles_folder():
    """
    View contents of subtitles folder
    """
    if not os.path.exists(SUBTITLES_FOLDER):
        print(f"\n📁 Subtitles folder not found: {SUBTITLES_FOLDER}")
        print("   Process some videos first to generate subtitles.")
        return

    print(f"\n📁 Subtitles Folder: {os.path.abspath(SUBTITLES_FOLDER)}")
    print("-" * 40)

    files = os.listdir(SUBTITLES_FOLDER)

    if not files:
        print("   Folder is empty")
        return

    # Count file types
    srt_files = [f for f in files if f.endswith('.srt')]
    json_files = [f for f in files if f.endswith('.json')]
    other_files = [f for f in files if not f.endswith(('.srt', '.json'))]

    print(f"📝 SRT files: {len(srt_files)}")
    print(f"📊 JSON metadata: {len(json_files)}")
    print(f"📄 Other files: {len(other_files)}")

    if srt_files:
        print(f"\n🎬 Generated subtitles:")
        for i, srt_file in enumerate(srt_files[:15], 1):
            file_path = os.path.join(SUBTITLES_FOLDER, srt_file)
            size_kb = os.path.getsize(file_path) / 1024
            print(f"   {i:2d}. {srt_file} ({size_kb:.1f} KB)")

        if len(srt_files) > 15:
            print(f"   ... and {len(srt_files) - 15} more")

    # Try to open folder
    try:
        open_folder = input(f"\nOpen subtitles folder? (y/n): ").lower()
        if open_folder == 'y':
            if sys.platform == 'darwin':  # macOS
                subprocess.call(['open', SUBTITLES_FOLDER])
            elif sys.platform == 'win32':  # Windows
                os.startfile(SUBTITLES_FOLDER)
            else:  # Linux
                subprocess.call(['xdg-open', SUBTITLES_FOLDER])
            print("   📂 Folder opened")
    except:
        pass

def main():
    """
    Main menu and application entry point
    """
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install required dependencies.")
        print("   Please install manually: pip install faster-whisper")
        sys.exit(1)

    while True:
        print_header()
        print("\n📋 MAIN MENU")
        print("-" * 40)
        print("1. 📥 Process single video")
        print("2. 📋 Process all videos in downloads folder")
        print("3. 📁 View subtitles folder")
        print("4. 🚪 Exit")
        print("-" * 40)

        choice = input("Choose option (1-4): ").strip()

        if choice == '1':
            process_single_video()
        elif choice == '2':
            batch_process_videos()
        elif choice == '3':
            view_subtitles_folder()
        elif choice == '4':
            print("\n👋 Thank you for using Rutube Subtitles Generator!")
            print("📧 Contact: Andrew Gotham - andreogotema@gmail.com")
            print("📱 Telegram: https://t.me/SirAndrewGotham")
            print("\nGoodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

        # Ask if user wants to continue
        if choice != '4':
            continue_choice = input("\nReturn to main menu? (y/n): ").lower()
            if continue_choice != 'y':
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    # Create subtitles folder if it doesn't exist
    os.makedirs(SUBTITLES_FOLDER, exist_ok=True)

    # Run the main application
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue to: andreogotema@gmail.com")
        sys.exit(1)
