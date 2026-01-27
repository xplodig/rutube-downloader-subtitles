"""
Rutube Video Downloader
======================

A Python tool for downloading videos from Rutube.ru with original filenames,
rate limiting to avoid blocks, and comprehensive error handling.

Author: Andrew Gotham
Email: andreogotema@gmail.com
Telegram: https://t.me/SirAndrewGotham

Features:
- Download single videos with original titles
- Batch download multiple videos with configurable delays
- Retry failed downloads
- Rate limiting to avoid 403 errors
- Clean filename handling
- Progress tracking
- Failed downloads logging
- Downloads folder management
- Subtitle generator integration

Requirements:
- Python 3.7+
- yt-dlp library

Usage:
    python rutube_downloader.py

License: MIT
"""

import yt_dlp
import os
import re
import sys
import subprocess
import time
import random
from datetime import datetime

# Constants
FAILED_DOWNLOADS_FILE = "failed_downloads.txt"
DOWNLOADS_FOLDER = "downloads"
VERSION = "2.0.0"

def print_header():
    """Print the application header"""
    print("=" * 60)
    print("🎬 RUTUBE VIDEO DOWNLOADER")
    print(f"📱 Version: {VERSION}")
    print("=" * 60)
    print("📧 Contact: Andrew Gotham")
    print("📧 Email: andreogotema@gmail.com")
    print("📱 Telegram: https://t.me/SirAndrewGotham")
    print("=" * 60)

def clean_filename(filename):
    """
    Clean filename to be safe for filesystem

    Args:
        filename (str): Original filename

    Returns:
        str: Cleaned filename safe for filesystem
    """
    # Remove invalid characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace multiple spaces with single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Trim whitespace
    cleaned = cleaned.strip()
    # Limit length
    return cleaned[:100]

def progress_hook(d):
    """
    Show download progress

    Args:
        d (dict): Download status dictionary from yt-dlp
    """
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')

        # Create a simple progress bar
        bar_length = 30
        if percent != 'N/A' and percent.endswith('%'):
            try:
                # Safely extract percentage
                percent_clean = percent.replace('%', '').strip()
                if percent_clean.replace('.', '', 1).isdigit():
                    percent_num = float(percent_clean)
                    filled = min(bar_length, int(bar_length * percent_num / 100))
                    bar = '█' * filled + '░' * (bar_length - filled)
                    print(f"\r   [{bar}] {percent} | {speed} | ETA: {eta}", end='', flush=True)
                else:
                    print(f"\r   Downloading: {percent} at {speed}", end='', flush=True)
            except:
                print(f"\r   Downloading... {percent}", end='', flush=True)
    elif d['status'] == 'finished':
        print(f"\r   ✅ Download completed successfully!{' ' * 50}")

def download_rutube_video():
    """
    Download a single Rutube video with original name to downloads folder

    This function:
    1. Asks for URL input
    2. Fetches video information
    3. Cleans the filename
    4. Downloads with progress tracking
    5. Shows download summary
    """
    # Create downloads folder if it doesn't exist
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)
        print(f"📁 Created folder: {DOWNLOADS_FOLDER}")

    # Ask for URL
    print("\n📥 SINGLE VIDEO DOWNLOAD")
    print("-" * 50)
    print("Paste the Rutube video URL below.")
    print("Example: https://rutube.ru/video/8e06c530938f25bf791a71251fe0f04d/")
    print("Note: For YouTube links, use yt-dlp directly instead.")
    print("-" * 50)

    url = input("URL: ").strip()

    if not url:
        print("❌ No URL provided. Exiting...")
        return

    # Only clean Rutube URLs, not other platforms
    if 'rutube.ru' in url and '?' in url:
        base_url = url.split('?')[0]
        print(f"⚠️  Removing query parameters from Rutube URL for better compatibility")
        print(f"   Using: {base_url}")
        url = base_url
    elif 'youtube.com' in url or 'youtu.be' in url:
        print(f"⚠️  Note: This tool is optimized for Rutube. YouTube may work but isn't fully supported.")
        print(f"   For best YouTube results, use yt-dlp directly: yt-dlp \"{url}\"")

    print("\n📥 Processing...")

    # Add a small delay before starting
    time.sleep(random.uniform(0.5, 1.5))

    # Set up download options - use different options for different platforms
    ydl_opts = {
        'format': 'best[ext=mp4]',  # Best MP4 quality
        'outtmpl': os.path.join(DOWNLOADS_FOLDER, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [progress_hook],
        # Add headers to mimic a real browser
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            print("🔍 Fetching video information...")
            info = ydl.extract_info(url, download=False)

            title = info.get('title', 'Unknown Title')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown Uploader')
            views = info.get('view_count', 0)

            # Clean the title for filename
            safe_title = clean_filename(title)

            print(f"\n📺 Video Information:")
            print(f"   Title: {title}")
            print(f"   Uploader: {uploader}")
            if duration and duration > 0:
                minutes, seconds = divmod(duration, 60)
                print(f"   Duration: {int(minutes)}:{int(seconds):02d}")
            if views and views > 0:
                print(f"   Views: {views:,}")

            # Warn if it looks like a homepage/playlist instead of video
            if duration == 0 and 'youtube.com' in url:
                print(f"\n⚠️  WARNING: This appears to be a YouTube homepage/playlist, not a video.")
                print(f"   YouTube video URLs should contain 'watch?v=' or 'youtu.be/'")

            # Confirm download
            print("\n" + "-" * 50)
            proceed = input(f"Download '{title[:50]}...'? (y/n): ").lower()

            if proceed != 'y':
                print("❌ Download cancelled.")
                return

            # Download the video
            print(f"\n⬇️  Downloading: {title}")
            print("-" * 50)

            # Use a simpler approach
            ydl_opts_simple = {
                'format': 'best[ext=mp4]',
                'outtmpl': os.path.join(DOWNLOADS_FOLDER, f'{safe_title}.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            }

            with yt_dlp.YoutubeDL(ydl_opts_simple) as ydl_simple:
                ydl_simple.download([url])

            # Check for downloaded file
            downloaded_file = None
            for file in os.listdir(DOWNLOADS_FOLDER):
                if file.startswith(safe_title):
                    downloaded_file = os.path.join(DOWNLOADS_FOLDER, file)
                    break

            if downloaded_file and os.path.exists(DOWNLOADS_FOLDER):
                file_size = os.path.getsize(downloaded_file) / (1024 * 1024)  # MB
                print(f"\n✅ Download complete!")
                print(f"📁 Saved to: {downloaded_file}")
                print(f"💾 File size: {file_size:.1f} MB")

                # Show absolute path
                abs_path = os.path.abspath(downloaded_file)
                print(f"📍 Full path: {abs_path}")

                # Suggest subtitles
                print("\n💡 Tip: You can now generate subtitles for this video")
                print("   Use option 6 from the main menu")
            else:
                print(f"\n⚠️  Download may have completed, but file not found.")
                print(f"   Check the {DOWNLOADS_FOLDER} folder manually.")
                # List files in downloads folder
                if os.path.exists(DOWNLOADS_FOLDER):
                    files = os.listdir(DOWNLOADS_FOLDER)
                    if files:
                        print(f"   Files in folder: {', '.join(files[:5])}")
                    else:
                        print(f"   Folder is empty")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Possible issues:")
        print("1. URL is incorrect or video is not available")
        print("2. Network connection problem")
        print("3. Video may be private or blocked")
        print("4. You may be rate-limited. Wait a few minutes and try again.")

        # Platform-specific advice
        if 'youtube.com' in url or 'youtu.be' in url:
            print("\nYouTube-specific issues:")
            print("5. For YouTube, ensure URL has 'watch?v=' followed by video ID")
            print("6. Example correct URL: https://www.youtube.com/watch?v=CfgMfMOnsRY")
            print("7. Short URLs should be: https://youtu.be/CfgMfMOnsRY")
            print("8. Try using yt-dlp directly: yt-dlp \"[URL]\"")
        else:
            print("5. Try removing any query parameters from the URL (?r=wd etc.)")

def batch_download_mode():
    """
    Download multiple videos with configurable delays to avoid rate limiting

    This function:
    1. Collects multiple URLs from user
    2. Applies rate limiting between downloads
    3. Tracks successes and failures
    4. Logs failed downloads for retry
    """
    print("\n" + "=" * 50)
    print("📋 BATCH DOWNLOAD MODE")
    print("=" * 50)
    print("Enter multiple URLs (one per line).")
    print("Type 'done' on a new line when finished.")
    print("Note: A delay will be added between downloads to avoid rate limiting.")
    print("-" * 50)

    urls = []
    while True:
        url = input("URL (or 'done'): ").strip()
        if url.lower() == 'done':
            break
        if url:
            # Clean URL - but only for Rutube URLs
            if 'rutube.ru' in url and '?' in url:
                url = url.split('?')[0]
            urls.append(url)

    if not urls:
        print("No URLs provided. Returning to main menu.")
        return

    # Ask for delay settings
    print("\n⏰ Rate limiting settings:")
    print("1. Normal (5-10 seconds between videos)")
    print("2. Conservative (10-20 seconds between videos)")
    print("3. Very slow (30-60 seconds between videos, for many videos)")

    delay_choice = input("Choose delay setting (1-3, default 1): ").strip()

    if delay_choice == '2':
        min_delay, max_delay = 10, 20
    elif delay_choice == '3':
        min_delay, max_delay = 30, 60
    else:
        min_delay, max_delay = 5, 10

    print(f"⏱️  Using delay: {min_delay}-{max_delay} seconds between videos")

    print(f"\n📥 Preparing to download {len(urls)} video(s)...")

    # Create downloads folder
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)

    success_count = 0
    failed_urls = []

    for i, url in enumerate(urls, 1):
        print(f"\n{'='*40}")
        print(f"📹 Video {i} of {len(urls)}")
        print(f"{'='*40}")

        # Add delay between downloads (except for first one)
        if i > 1:
            delay = random.uniform(min_delay, max_delay)
            print(f"⏳ Waiting {delay:.1f} seconds to avoid rate limiting...")
            time.sleep(delay)

        try:
            # Get info first
            print("🔍 Fetching video information...")
            ydl_info = yt_dlp.YoutubeDL({
                'quiet': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            })

            info = ydl_info.extract_info(url, download=False)
            title = info.get('title', f'video_{i}')
            safe_title = clean_filename(title)

            print(f"📺 Title: {title}")

            # Download
            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': os.path.join(DOWNLOADS_FOLDER, f'{safe_title}.%(ext)s'),
                'quiet': False,
                'no_warnings': True,
                'progress_hooks': [lambda d: print(f"\r   Progress: {d.get('_percent_str', '0%')}", end='') if d['status'] == 'downloading' else None],
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            }

            print(f"⬇️  Downloading...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"\r   ✅ Download completed!")
            success_count += 1

            # Small delay after successful download
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            error_msg = str(e)[:100]
            print(f"\r   ❌ Failed: {error_msg}")
            failed_urls.append((url, error_msg))

            # If it's a 403 error, wait longer before next attempt
            if "403" in error_msg or "Forbidden" in error_msg:
                print(f"⚠️  Got 403 error, waiting 30 seconds before next attempt...")
                time.sleep(30)

            continue

    print(f"\n{'='*40}")
    print(f"🎉 Batch download completed!")
    print(f"📊 Successfully downloaded: {success_count} of {len(urls)} videos")
    print(f"📁 Saved to: {os.path.abspath(DOWNLOADS_FOLDER)}")

    # Suggest subtitles
    if success_count > 0:
        print(f"\n💡 Tip: You can now generate subtitles for these {success_count} videos")
        print("   Use option 7 from the main menu")

    # Save failed URLs to a file for retry
    if failed_urls:
        save_failed_downloads(failed_urls)
        print(f"\n⚠️  {len(failed_urls)} downloads failed.")
        print(f"📝 Failed URLs saved to: {FAILED_DOWNLOADS_FILE}")
        print("   Use option 3 to retry them later.")

def save_failed_downloads(failed_urls):
    """
    Save failed downloads to a log file

    Args:
        failed_urls (list): List of tuples containing (url, error_message)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FAILED_DOWNLOADS_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Failed downloads log - {timestamp}\n")
        f.write(f"{'='*60}\n")
        for url, error in failed_urls:
            f.write(f"URL: {url}\n")
            f.write(f"Error: {error}\n")
            f.write(f"Time: {timestamp}\n")
            f.write("-"*40 + "\n")

def retry_failed_downloads():
    """
    Retry downloads that failed previously

    Reads URLs from the failed downloads log file and attempts
    to download them again with conservative delay settings.
    """
    if not os.path.exists(FAILED_DOWNLOADS_FILE):
        print(f"\n📄 No failed downloads file found: {FAILED_DOWNLOADS_FILE}")
        print("   Run batch download first to generate this file.")
        return

    print(f"\n🔄 Reading failed downloads from: {FAILED_DOWNLOADS_FILE}")

    urls = []
    with open(FAILED_DOWNLOADS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("URL: "):
                url = line.replace("URL: ", "").strip()
                urls.append(url)

    if not urls:
        print("   No URLs found in failed downloads file.")
        return

    print(f"📋 Found {len(urls)} failed URLs to retry.")
    print("   Starting retry with conservative delays...")

    # Use conservative settings for retry
    download_urls_with_delay(urls, min_delay=15, max_delay=30, mode="retry")

def download_urls_with_delay(urls, min_delay=5, max_delay=10, mode="normal"):
    """
    Helper function to download multiple URLs with delays

    Args:
        urls (list): List of URLs to download
        min_delay (int): Minimum delay between downloads in seconds
        max_delay (int): Maximum delay between downloads in seconds
        mode (str): Mode identifier for display purposes
    """
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)

    success_count = 0

    for i, url in enumerate(urls, 1):
        print(f"\n{'='*40}")
        print(f"📹 Video {i} of {len(urls)} ({mode})")
        print(f"{'='*40}")

        # Add delay between downloads
        if i > 1:
            delay = random.uniform(min_delay, max_delay)
            print(f"⏳ Waiting {delay:.1f} seconds...")
            time.sleep(delay)

        try:
            # Get info first
            print("🔍 Fetching video information...")
            ydl_info = yt_dlp.YoutubeDL({
                'quiet': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            })

            info = ydl_info.extract_info(url, download=False)
            title = info.get('title', f'video_{i}')
            safe_title = clean_filename(title)

            print(f"📺 Title: {title}")

            # Download
            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': os.path.join(DOWNLOADS_FOLDER, f'{safe_title}.%(ext)s'),
                'quiet': False,
                'no_warnings': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            }

            print(f"⬇️  Downloading...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"\r   ✅ Download completed!")
            success_count += 1

        except Exception as e:
            error_msg = str(e)[:100]
            print(f"\r   ❌ Failed: {error_msg}")

            if "403" in error_msg or "Forbidden" in error_msg:
                print(f"⚠️  Got 403 error, waiting 60 seconds...")
                time.sleep(60)

            continue

    return success_count

def delete_failed_downloads_log():
    """
    Delete the failed downloads log file

    This function removes the failed_downloads.txt file after
    confirming with the user.
    """
    if not os.path.exists(FAILED_DOWNLOADS_FILE):
        print(f"\n📄 No failed downloads file found: {FAILED_DOWNLOADS_FILE}")
        return

    # Show file information
    file_size = os.path.getsize(FAILED_DOWNLOADS_FILE)
    with open(FAILED_DOWNLOADS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        failed_count = sum(1 for line in lines if line.startswith("URL: "))

    print(f"\n📄 Failed Downloads Log Information:")
    print(f"   File: {FAILED_DOWNLOADS_FILE}")
    print(f"   Size: {file_size / 1024:.1f} KB")
    print(f"   Failed URLs recorded: {failed_count}")
    print(f"   Last modified: {datetime.fromtimestamp(os.path.getmtime(FAILED_DOWNLOADS_FILE))}")

    # Confirm deletion
    print("\n⚠️  WARNING: This will permanently delete the failed downloads log.")
    print("   You will not be able to retry these failed downloads.")

    confirm = input(f"\nAre you sure you want to delete {FAILED_DOWNLOADS_FILE}? (y/n): ").lower()

    if confirm == 'y':
        try:
            os.remove(FAILED_DOWNLOADS_FILE)
            print(f"✅ Successfully deleted: {FAILED_DOWNLOADS_FILE}")
        except Exception as e:
            print(f"❌ Error deleting file: {e}")
    else:
        print("❌ Deletion cancelled.")

def clear_failed_downloads_log():
    """
    Clear the contents of failed downloads log but keep the file

    This function empties the failed_downloads.txt file without
    deleting the file itself.
    """
    if not os.path.exists(FAILED_DOWNLOADS_FILE):
        print(f"\n📄 No failed downloads file found: {FAILED_DOWNLOADS_FILE}")
        return

    # Show file information
    file_size = os.path.getsize(FAILED_DOWNLOADS_FILE)

    print(f"\n📄 Failed Downloads Log Information:")
    print(f"   File: {FAILED_DOWNLOADS_FILE}")
    print(f"   Size: {file_size / 1024:.1f} KB")

    # Confirm clearing
    print("\n⚠️  WARNING: This will clear all contents from the failed downloads log.")
    print("   The file will be emptied but not deleted.")

    confirm = input(f"\nAre you sure you want to clear {FAILED_DOWNLOADS_FILE}? (y/n): ").lower()

    if confirm == 'y':
        try:
            with open(FAILED_DOWNLOADS_FILE, "w", encoding="utf-8") as f:
                f.write("Failed Downloads Log - Cleared\n")
                f.write(f"Cleared on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n")
            print(f"✅ Successfully cleared: {FAILED_DOWNLOADS_FILE}")
        except Exception as e:
            print(f"❌ Error clearing file: {e}")
    else:
        print("❌ Clear operation cancelled.")

def open_downloads_folder():
    """
    Open downloads folder and show contents

    This function:
    1. Lists files in the downloads folder
    2. Shows file sizes and counts
    3. Attempts to open the folder in file explorer
    """
    if os.path.exists(DOWNLOADS_FOLDER):
        print(f"\n📁 Opening downloads folder...")
        print(f"📍 Path: {os.path.abspath(DOWNLOADS_FOLDER)}")

        # List files
        files = os.listdir(DOWNLOADS_FOLDER)
        if files:
            total_size = 0
            video_files = []

            for file in files:
                file_path = os.path.join(DOWNLOADS_FOLDER, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    total_size += size
                    if file.lower().endswith(('.mp4', '.mkv', '.webm', '.avi', '.mov')):
                        video_files.append((file, size))

            print(f"📋 Total files: {len(files)}")
            print(f"📹 Video files: {len(video_files)}")
            print(f"💾 Total size: {total_size / (1024*1024*1024):.2f} GB")

            if video_files:
                print(f"\n🎬 Video files (showing first 10):")
                for i, (file, size) in enumerate(video_files[:10], 1):
                    print(f"   {i:2d}. {file[:50]} ({size / (1024*1024):.1f} MB)")
                if len(video_files) > 10:
                    print(f"   ... and {len(video_files) - 10} more")

                # Check for subtitles
                subtitles_folder = "subtitles"
                if os.path.exists(subtitles_folder):
                    srt_files = [f for f in os.listdir(subtitles_folder) if f.endswith('.srt')]
                    if srt_files:
                        print(f"\n📝 Found {len(srt_files)} subtitle files in '{subtitles_folder}' folder")
                        print(f"   💡 Subtitles are ready for use with your videos")
        else:
            print("   Folder is empty")

        # Try to open folder
        try:
            if sys.platform == 'darwin':  # macOS
                subprocess.call(['open', DOWNLOADS_FOLDER])
            elif sys.platform == 'win32':  # Windows
                os.startfile(DOWNLOADS_FOLDER)
            else:  # Linux
                subprocess.call(['xdg-open', DOWNLOADS_FOLDER])
            print("   📂 Folder opened in file explorer")
        except:
            print("   (Could not open folder automatically)")
    else:
        print(f"\n📁 Downloads folder doesn't exist yet.")
        print(f"   It will be created when you download your first video.")

def show_stats():
    """
    Show download statistics

    Displays information about downloaded files and failed downloads log.
    """
    print("\n📊 DOWNLOAD STATISTICS")
    print("-" * 40)

    # Downloads folder stats
    if os.path.exists(DOWNLOADS_FOLDER):
        files = os.listdir(DOWNLOADS_FOLDER)
        video_files = [f for f in files if f.lower().endswith(('.mp4', '.mkv', '.webm', '.avi', '.mov'))]

        print(f"📁 Downloads folder:")
        print(f"   Total files: {len(files)}")
        print(f"   Video files: {len(video_files)}")

        if video_files:
            total_size = sum(os.path.getsize(os.path.join(DOWNLOADS_FOLDER, f)) for f in video_files)
            print(f"   Total video size: {total_size / (1024*1024*1024):.2f} GB")

            # Check for subtitles
            subtitles_folder = "subtitles"
            if os.path.exists(subtitles_folder):
                srt_files = [f for f in os.listdir(subtitles_folder) if f.endswith('.srt')]
                if srt_files:
                    print(f"\n📝 Subtitle folder:")
                    print(f"   Subtitle files: {len(srt_files)}")
                    print(f"   Videos with subtitles: {len(srt_files)}/{len(video_files)}")
                    if len(srt_files) < len(video_files):
                        print(f"   💡 Use option 7 to generate subtitles for remaining videos")
    else:
        print(f"📁 Downloads folder: Not created yet")

    # Failed downloads log stats
    if os.path.exists(FAILED_DOWNLOADS_FILE):
        file_size = os.path.getsize(FAILED_DOWNLOADS_FILE)
        with open(FAILED_DOWNLOADS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            failed_count = sum(1 for line in lines if line.startswith("URL: "))

        print(f"\n📄 Failed downloads log:")
        print(f"   File: {FAILED_DOWNLOADS_FILE}")
        print(f"   Size: {file_size / 1024:.1f} KB")
        print(f"   Failed URLs: {failed_count}")
        print(f"   Last modified: {datetime.fromtimestamp(os.path.getmtime(FAILED_DOWNLOADS_FILE))}")
    else:
        print(f"\n📄 Failed downloads log: No log file found")

# --- SUBTITLE GENERATOR INTEGRATION FUNCTIONS ---

def check_downloads_for_subtitles():
    """Check if there are videos to process"""
    if not os.path.exists("downloads"):
        print("❌ No downloads folder found.")
        print("   Please download videos first (options 1 or 2).")
        return False

    videos = [f for f in os.listdir("downloads")
              if f.lower().endswith(('.mp4', '.mkv', '.webm', '.avi', '.mov'))]

    if not videos:
        print("❌ No video files found in downloads folder.")
        print("   Please download videos first (options 1 or 2).")
        return False

    print(f"✅ Found {len(videos)} video(s) ready for subtitles")
    return True

def find_subtitle_generator():
    """Find available subtitle generator script"""
    scripts = ["create_subtitles.py", "quick_subtitles.py"]
    for script in scripts:
        if os.path.exists(script):
            return script
    return None

def launch_subtitle_tool(script_name):
    """Launch the subtitle generator tool"""
    print(f"\n🚀 Launching {script_name}...")
    print("   This will open in a new window.")
    print("   Follow the instructions in that window.")
    print("-" * 50)

    try:
        # Launch as separate process
        if script_name == "create_subtitles.py":
            print("📝 Interactive version - you can choose:")
            print("   • Which videos to process")
            print("   • Language (Russian/English)")
            print("   • Model size (speed vs accuracy)")
        else:
            print("⚡ Quick version - automatic processing")
            print("   • Processes all videos")
            print("   • Uses default settings")
            print("   • Fast and simple")

        # Ask for confirmation
        confirm = input("\nLaunch now? (y/n): ").lower()
        if confirm == 'y':
            subprocess.run([sys.executable, script_name])
        else:
            print("❌ Launch cancelled.")

    except Exception as e:
        print(f"❌ Error launching: {e}")
        print(f"\n💡 Try running manually: python {script_name}")

def offer_subtitle_download():
    """Offer to help user get subtitle generator"""
    print("\n📥 SUBTITLE GENERATOR NOT FOUND")
    print("-" * 40)
    print("The subtitle generator is a separate tool that:")
    print("• Creates .srt files from your downloaded videos")
    print("• Uses AI to transcribe Russian/English audio")
    print("• Saves subtitles to 'subtitles/' folder")

    print("\n📋 To get it:")
    print("1. Download from the project repository")
    print("2. Save as 'create_subtitles.py' in this folder")
    print("3. Run this option again")

    print("\n⚡ Quick start (if you have it elsewhere):")
    print("   python /path/to/create_subtitles.py")

    print("\n📁 Your downloaded videos are in:")
    print(f"   {os.path.abspath('downloads')}")

def handle_subtitle_generation():
    """Handle subtitle generation with smart checking"""
    print("\n" + "=" * 50)
    print("🎬 SUBTITLE GENERATION")
    print("=" * 50)

    # Check prerequisites
    if not check_downloads_for_subtitles():
        return

    # Check if subtitle generator exists
    subtitle_script = find_subtitle_generator()

    if subtitle_script:
        launch_subtitle_tool(subtitle_script)
    else:
        offer_subtitle_download()

def main():
    """
    Main menu and application entry point

    Provides a user-friendly menu interface for all download options.
    """
    # Check if yt-dlp is installed
    try:
        import yt_dlp
    except ImportError:
        print("❌ yt-dlp is not installed.")
        print("Installing it now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            print("✅ yt-dlp installed successfully!")
            import yt_dlp
        except:
            print("❌ Failed to install yt-dlp.")
            print("Please install it manually: pip install yt-dlp")
            sys.exit(1)

    while True:
        print_header()
        print("\n📋 MAIN MENU")
        print("-" * 40)
        print("1. 📥 Download single video")
        print("2. 📋 Download multiple videos (with delays)")
        print("3. 🔄 Retry failed downloads")
        print("4. 🗑️  Delete failed downloads log")
        print("5. 🧹 Clear failed downloads log")
        print("6. 🎬 Generate subtitles for downloaded videos")
        print("7. 📊 Show download statistics")
        print("8. 📁 Open downloads folder")
        print("9. 🚪 Exit")
        print("-" * 40)

        choice = input("Choose option (1-9): ").strip()

        if choice == '1':
            download_rutube_video()
        elif choice == '2':
            batch_download_mode()
        elif choice == '3':
            retry_failed_downloads()
        elif choice == '4':
            delete_failed_downloads_log()
        elif choice == '5':
            clear_failed_downloads_log()
        elif choice == '6':
            handle_subtitle_generation()
        elif choice == '7':
            show_stats()
        elif choice == '8':
            open_downloads_folder()
        elif choice == '9':
            print("\n👋 Thank you for using Rutube Downloader!")
            print("📧 Contact: Andrew Gotham - andreogotema@gmail.com")
            print("📱 Telegram: https://t.me/SirAndrewGotham")
            print("\nGoodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please enter 1-9.")

        # Ask if user wants to continue
        if choice != '9':
            continue_choice = input("\nReturn to main menu? (y/n): ").lower()
            if continue_choice != 'y':
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    # Create README file with documentation
    readme_content = """# Rutube Video Downloader

A comprehensive Python tool for downloading videos from Rutube.ru with advanced features and rate limiting.

## Features
- Download single videos with original titles
- Batch download multiple videos with configurable delays
- Retry failed downloads automatically
- Rate limiting to avoid IP blocking (403 errors)
- Clean filename handling for filesystem compatibility
- Real-time progress tracking
- Failed downloads logging
- Downloads folder management
- Statistics and file information
- **Generate subtitles** with separate subtitle generator tool

## Requirements
- Python 3.7 or higher
- yt-dlp library (automatically installed if missing)

## Installation
1. Ensure Python is installed on your system
2. Run the script: `python rutube_downloader.py`
3. The script will automatically install yt-dlp if needed

## Usage
Run the script and choose from the menu:
1. **Single Download**: Download one video by URL
2. **Batch Download**: Download multiple videos with rate limiting
3. **Retry Failed**: Retry previously failed downloads
4. **Delete Log**: Remove failed downloads log file
5. **Clear Log**: Clear contents of failed downloads log
6. **Generate Subtitles**: Create subtitles for downloaded videos
7. **Show Stats**: Display download statistics
8. **Open Folder**: Open downloads directory
9. **Exit**: Quit the application

## Generate Subtitles (Integrated Feature)
After downloading videos, use option 6 to generate subtitles:

### Subtitle Generator Features:
- **Interactive Menu**: User-friendly interface
- **Multiple Model Options**: Choose accuracy vs speed
- **Language Selection**: Russian, English, or auto-detect
- **File Selection**: Process all or specific videos
- **Progress Tracking**: Real-time progress display
- **Metadata Saving**: JSON files with transcription info
- **Error Handling**: Failed files are logged
- **Subtitles Folder**: All SRT files organized in one place

### What the Subtitle Generator Does:
1. Scans `downloads/` folder for video files
2. Uses `faster-whisper` to transcribe audio (no FFmpeg needed!)
3. Generates `.srt` files with proper timestamps
4. Saves subtitles to `subtitles/` folder
5. Creates metadata files with transcription details

### Requirements for Subtitles:
- `faster-whisper` (will auto-install when needed)
- Video files in `downloads/` folder (from your downloader script)

### Output:
- `.srt` files in `subtitles/` folder (same name as videos)
- `.json` metadata files with transcription details
- Failed files list if any errors occur

The script will automatically match subtitle files with video files (same name, different extension). Just place both in the same folder and your video player should automatically detect the subtitles!

## Rate Limiting
To avoid getting blocked by Rutube:
- Normal: 5-10 seconds between downloads
- Conservative: 10-20 seconds between downloads
- Very Slow: 30-60 seconds between downloads (for large batches)

## File Locations
- Downloads: `downloads/` folder
- Failed downloads log: `failed_downloads.txt`
- Generated subtitles: `subtitles/` folder (after running subtitle generator)

## Author
**Andrew Gotham**
- Email: andreogotema@gmail.com
- Telegram: https://t.me/SirAndrewGotham

## License
MIT License - Feel free to use and modify for your needs.

## Version
Current version: 2.0.0
"""

    # Create README file if it doesn't exist
    if not os.path.exists("README.md"):
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("📄 Created README.md documentation file")

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
