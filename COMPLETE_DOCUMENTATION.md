# Rutube Video Downloader - Complete Documentation

## Project Overview
The Rutube Video Downloader is a robust Python application designed to download videos from Rutube.ru platform with comprehensive features including rate limiting, error handling, file management, and integrated subtitle generation.

## 📁 Project Structure
```
rutube_downloader/
├── rutube_downloader.py    # Main video downloader application (with subtitle integration)
├── create_subtitles.py     # Subtitle generator (interactive) - optional
├── quick_subtitles.py      # Subtitle generator (quick version) - optional
├── README.md               # Project documentation
├── downloads/              # Downloaded videos folder (auto-created)
├── subtitles/              # Generated subtitles folder (auto-created)
└── failed_downloads.txt    # Log of failed downloads (auto-created)
```

## 🚀 Features

### Video Downloader Features
1. **Single Video Download**
   - Download individual videos with original titles
   - Clean filename sanitization
   - Progress tracking with visual indicators
   - Smart suggestions for next steps

2. **Batch Download**
   - Download multiple videos sequentially
   - Configurable delay settings to avoid rate limiting
   - Automatic retry logic for failed downloads
   - Progress tracking across all downloads

3. **Rate Limiting**
   - Three delay settings (Normal/Conservative/Very Slow)
   - Random delay intervals to mimic human behavior
   - Special handling for 403 errors with extended waits
   - Adaptive delays based on error responses

4. **Error Handling**
   - Comprehensive error logging to `failed_downloads.txt`
   - Failed downloads tracking with timestamps and error messages
   - Automatic retry functionality with conservative settings
   - User-friendly error messages with troubleshooting tips

5. **File Management**
   - Organized `downloads/` folder with automatic creation
   - File statistics and information display
   - Failed downloads log management (view, clear, delete)
   - Folder browsing with automatic file explorer opening

6. **Subtitle Generator Integration** (NEW in v2.0.0)
   - Integrated access to subtitle tools from main menu
   - Smart detection of downloaded videos
   - Automatic launch of available subtitle generators
   - Guidance for installing subtitle tools if missing
   - Statistics showing subtitle coverage for videos

### Subtitle Generator Features (Separate Tools)
7. **Speech Recognition**
   - Uses faster-whisper for accurate transcription
   - No FFmpeg required for audio extraction
   - Multiple language support (Russian, English, auto-detect)

8. **Subtitle Creation**
   - Generates properly formatted SRT files
   - Accurate timestamp synchronization
   - Multiple model sizes for speed/accuracy trade-off
   - Organized `subtitles/` folder output

9. **Batch Processing**
   - Process all videos in downloads folder
   - Selective file processing options
   - Progress tracking and error logging
   - Metadata preservation in JSON files

## 🔧 Technical Details

### Dependencies
- **yt-dlp**: Advanced video download library (auto-installed)
- **faster-whisper**: Efficient speech recognition (for subtitles, auto-installed when needed)
- **Python Standard Library**: os, re, sys, time, datetime, random, subprocess

### Key Functions

#### Video Downloader (Main Application)
- `clean_filename(filename)`: Sanitizes filenames for filesystem compatibility
- `progress_hook(d)`: Real-time download progress visualization
- `download_rutube_video()`: Handles single video downloads with user confirmation
- `batch_download_mode()`: Manages batch downloads with configurable rate limiting
- `save_failed_downloads(failed_urls)`: Logs failed download attempts with timestamps
- `retry_failed_downloads()`: Automatically retries previously failed downloads
- `handle_subtitle_generation()`: Integrated subtitle generator launcher (NEW)
- `check_downloads_for_subtitles()`: Validates video availability for subtitles
- `find_subtitle_generator()`: Locates available subtitle tools
- `launch_subtitle_tool()`: Executes subtitle generator in separate process

#### Subtitle Generator (Separate Tools)
- `format_timestamp(seconds)`: Converts seconds to SRT timestamp format (HH:MM:SS,mmm)
- `create_srt_from_segments()`: Creates SRT files from transcription segments
- `transcribe_video()`: Transcribes video audio using faster-whisper models
- `batch_process_videos()`: Processes multiple videos for subtitle generation

## ⚙️ Configuration Options

### Downloader Settings
1. **Delay Settings**:
   - Normal: 5-10 seconds between downloads (default)
   - Conservative: 10-20 seconds between downloads (recommended for many videos)
   - Very Slow: 30-60 seconds between downloads (for large batches or if experiencing blocks)

2. **File Management**:
   - Downloads Folder: `downloads/` (auto-created on first download)
   - Log File: `failed_downloads.txt` (auto-managed, can be cleared or deleted)
   - Maximum Filename Length: 100 characters (safe for all filesystems)
   - Subtitle Integration: Automatic detection and launching

### Subtitle Generator Settings
1. **Model Selection** (when using create_subtitles.py):
   - tiny: Fastest, lowest accuracy (good for testing)
   - base: Balanced speed/accuracy (recommended for most uses)
   - small: Better accuracy, moderate speed
   - medium: High accuracy, slower processing
   - large: Best accuracy, slowest processing (requires significant resources)

2. **Language Options**:
   - Russian (ru) - Default for Rutube content
   - English (en) - For English-language videos
   - Auto-detect - Let the model detect language automatically

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Internet connection for downloads and model fetching
- Rutube account (for private videos, if needed)
- 500MB-3GB disk space for subtitle models (depending on chosen model size)

### Quick Start (All-in-One)
```bash
# 1. Download videos and access subtitle tools
python rutube_downloader.py

# Follow the menu:
# 1. Download videos first
# 6. Generate subtitles (when ready)
```

### Manual Installation (Advanced Users)
```bash
# Install required packages
pip install yt-dlp faster-whisper

# Run main application
python rutube_downloader.py

# Or run subtitle tools separately
python create_subtitles.py    # Interactive version
python quick_subtitles.py     # Quick automatic version
```

## 📖 Usage Guide

### Complete Workflow
1. **Download Videos**: Run `python rutube_downloader.py`
   - Option 1: Single video download (paste URL, confirm, download)
   - Option 2: Batch download (enter multiple URLs, choose delay, download all)
   - Option 3: Retry failed downloads (automatic retry of logged failures)

2. **Generate Subtitles**: Use option 6 from main menu
   - Smart check: Verifies videos exist in `downloads/` folder
   - Automatic launch: Opens available subtitle tool
   - If missing: Guides you to install subtitle tools
   - Options: Interactive (create_subtitles.py) or Quick (quick_subtitles.py)

3. **Watch with Subtitles**:
   - `.srt` files saved to `subtitles/` folder
   - Same base name as video files (e.g., video.mp4 → video.srt)
   - Open video in VLC/MPV/other players with subtitle support
   - Subtitles load automatically if names match and are in same folder

### Downloading Videos
1. **Single Video**:
   - Option 1 → Paste URL → View info → Confirm → Download with progress
   - Success: File saved to `downloads/` with cleaned filename
   - Tip: Suggests subtitle generation after successful download

2. **Multiple Videos**:
   - Option 2 → Enter URLs (one per line, 'done' when finished)
   - Choose delay setting based on batch size
   - Watch progress for each video
   - Summary shows success/failure counts
   - Failed URLs saved for retry

3. **Retry Failed**:
   - Option 3 → Reads `failed_downloads.txt`
   - Uses conservative delays (15-30 seconds)
   - Attempts all previously failed downloads

### Generating Subtitles
1. **Integrated Method** (Recommended):
   - Option 6 from main menu
   - Automatically checks for downloaded videos
   - Launches available subtitle tool
   - Returns to main menu when done

2. **Interactive Tool** (create_subtitles.py):
   - Full control over settings
   - Choose specific videos to process
   - Select language and model size
   - View detailed progress and statistics

3. **Quick Tool** (quick_subtitles.py):
   - One-command processing
   - Uses default settings (base model, auto-detect language)
   - Processes all videos in `downloads/` folder
   - Fast and simple for batch processing

### Managing Files
- **View Statistics** (Option 7): Shows download counts, file sizes, subtitle coverage
- **Open Folders** (Option 8): Opens `downloads/` in file explorer, lists contents
- **Delete/Clear Logs** (Options 4 & 5): Manage `failed_downloads.txt`
- **Automatic Organization**: All files neatly organized in designated folders

## 🎬 Subtitle Generator Details

### How It Works
The subtitle generator uses `faster-whisper`, an optimized version of OpenAI's Whisper model, to transcribe audio from video files. It automatically processes videos in the `downloads/` folder and creates `.srt` subtitle files in the `subtitles/` folder.

### Features Breakdown

#### Main Script (create_subtitles.py) - Interactive Version:
- **Interactive Menu**: User-friendly interface with numbered options
- **Multiple Model Options**: 5 whisper model sizes (tiny, base, small, medium, large)
- **Language Selection**: Explicit Russian, English, or auto-detect
- **File Selection**: Process all videos or select specific files
- **Progress Tracking**: Real-time display with elapsed time and ETA
- **Metadata Saving**: JSON files with transcription details, confidence scores, language info
- **Error Handling**: Failed files logged to `failed_files.txt` with error messages
- **Organized Output**: All SRT files in `subtitles/` folder with matching names

#### Quick Script (quick_subtitles.py) - Automatic Version:
- **One-Command Processing**: Run and forget - processes everything automatically
- **Automatic Installation**: Checks and installs `faster-whisper` if missing
- **Basic Functionality**: Default settings optimized for speed and reliability
- **Batch Processing**: Automatically finds and processes all videos
- **Simple Output**: Just the SRT files, no complex options

### What the Script Does (Step by Step):
1. **Scans `downloads/` folder** for video files (MP4, MKV, WebM, AVI, MOV, etc.)
2. **Extracts audio** using built-in methods (no external FFmpeg required)
3. **Uses `faster-whisper`** to transcribe audio to text with timestamps
4. **Generates `.srt` files** with properly formatted timestamps and subtitles
5. **Saves subtitles** to organized `subtitles/` folder with matching base names
6. **Creates metadata** JSON files with transcription details for reference
7. **Logs failures** to error file for troubleshooting

### Requirements for Subtitles:
- `faster-whisper` (automatically installed by script on first run)
- Video files in `downloads/` folder (from downloader script)
- Sufficient disk space for model files:
   - tiny: ~150MB
   - base: ~300MB
   - small: ~1GB
   - medium: ~3GB
   - large: ~6GB

### Output Files:
- **`.srt` files**: Subtitle files in `subtitles/` folder (same base name as videos)
- **`.json` files**: Metadata with transcription details, language, duration, confidence
- **`failed_files.txt`**: List of files that couldn't be processed with error reasons

### Usage Tips:
1. **Name Matching**: Subtitle files automatically match video file names (video.mp4 → video.srt)
2. **Automatic Detection**: Most video players auto-detect SRT files when names match
3. **Manual Loading**: In VLC: Subtitles → Add Subtitle File (if auto-detection fails)
4. **Organization**: All files neatly organized in `subtitles/` folder for easy management
5. **Model Selection**: Use 'base' for balanced speed/accuracy, 'small' for better quality
6. **Language Setting**: Use 'ru' for Russian content, 'en' for English, 'auto' for mixed

## 🚨 Troubleshooting

### Common Issues & Solutions

#### 403 Forbidden Errors (Downloader)
**Problem**: Getting blocked by Rutube with 403 errors
**Solution**:
- Use "Very Slow" delay setting (30-60 seconds)
- Wait a few hours before retrying large batches
- Consider using a VPN to change IP address
- Use Option 3 to retry with conservative delays

#### Transcription Errors (Subtitles)
**Problem**: Whisper fails to transcribe or produces poor results
**Solution**:
- Try a smaller model (base instead of large) - sometimes more reliable
- Check audio quality in video (low volume or background noise affects results)
- Ensure sufficient disk space for model downloads
- Try different language setting (force Russian/English instead of auto-detect)

#### File Not Found Errors
**Problem**: Downloaded file or subtitle not appearing where expected
**Solution**:
- Check `downloads/` folder exists and has video files
- Check `subtitles/` folder for generated SRT files
- Verify filename sanitization didn't change names significantly
- Look for files with similar names or check all files in folder

#### Subtitle Generator Not Found
**Problem**: Option 6 says subtitle tools not found
**Solution**:
- Download `create_subtitles.py` or `quick_subtitles.py` to same folder
- Or run subtitle tools manually from their location
- The main downloader can guide you through installation

### Error Messages & Fixes
- **"URL is incorrect or video is not available"**: Verify the Rutube video URL is correct and video is public
- **"Video may be private or blocked"**: Requires login or is unavailable in your region
- **"Rate-limited"**: Wait 30-60 minutes and use higher delay settings
- **"Model download failed"**: Check internet connection and disk space, try smaller model
- **"No video files found"**: Download videos first using options 1 or 2
- **"faster-whisper not installed"**: Script will attempt to install it automatically

## 🔒 Privacy & Security

### Data Handling
- **No Data Collection**: No personal data collected or transmitted
- **Local Processing Only**: All processing happens on your computer
- **No External Servers**: Audio never sent to external servers (unlike cloud-based services)
- **Local Models**: Whisper models downloaded and stored locally on your machine
- **File Privacy**: Your video files and subtitles stay on your local storage

### Safe & Ethical Usage
- **Respect Terms of Service**: Follow Rutube's Terms of Service for downloads
- **Copyright Respect**: Download only content you have rights to access
- **Personal Use**: Generate subtitles only for legally obtained content
- **Rate Limiting**: Use appropriate delays to avoid overloading servers
- **Educational Use**: Great for language learning, accessibility, and study purposes

## 📈 Performance Tips

### For Large Video Batches
1. **Downloads**: Use "Very Slow" delay setting and download during off-peak hours
2. **Subtitles**: Use 'base' or 'small' model for faster processing of many videos
3. **Monitoring**: Watch `failed_downloads.txt` and subtitle error logs
4. **Organization**: Consider creating subfolders in `downloads/` for different projects

### Speed Optimization
1. **Internet Connection**: Good bandwidth for faster downloads and model fetching
2. **Disk Space**: Adequate free space for videos (GBs) and models (MBs/GBs)
3. **System Resources**: Close other intensive applications during processing
4. **SSD Usage**: Use SSD for faster file operations and model loading

### Memory Management
1. **Whisper Models**: Smaller models use less RAM (tiny: ~1GB, large: ~10GB)
2. **Batch Size**: Process fewer videos at once if memory is limited
3. **Clear Logs**: Periodically clear `failed_downloads.txt` if it gets large
4. **Storage Management**: Move processed videos to archive if collection grows large

## 🤝 Support & Contact

### Author Information
- **Name**: Andrew Gotham
- **Email**: andreogotema@gmail.com
- **Telegram**: https://t.me/SirAndrewGotham
- **Role**: Developer & Maintainer

### Getting Help
1. **Check Documentation**: README.md and this COMPLETE_DOCUMENTATION.md first
2. **Review Error Messages**: Read error messages carefully for clues
3. **Check Log Files**: Look in `failed_downloads.txt` and subtitle error logs
4. **Contact Author**: Email or Telegram for technical issues not covered in docs

### Feature Requests & Feedback
Suggestions and improvements are welcome via email or Telegram:
- **Additional Platforms**: Support for other video sites
- **Enhanced Features**: Better subtitle editing, translation features
- **GUI Development**: Graphical user interface versions
- **More Languages**: Additional language support for subtitles
- **Bug Reports**: Report any issues or unexpected behavior

## 📄 License & Legal

### License
MIT License - Free to use, modify, and distribute for personal and commercial use.

### Legal Notice
- **Copyright Compliance**: Respect all copyright laws and platform terms of service
- **Author Responsibility**: The author is not responsible for misuse of this tool
- **Educational Purpose**: Intended for educational, accessibility, and personal use
- **Fair Use**: Use responsibly and ethically

## 🔄 Version History

### v2.0.0 (Current) - Januart 2026
- **Integrated Subtitle Generation**: Option 6 in main menu for subtitle tools
- **Smart Detection**: Automatically checks for videos and available subtitle tools
- **Enhanced Statistics**: Shows subtitle coverage alongside download stats
- **Improved User Guidance**: Better suggestions and error messages
- **Updated Documentation**: Comprehensive docs including subtitle integration
- **Version Bump**: Reflects major feature addition

### v1.0.0 - Initial Release
- **Core Downloader**: Single and batch video downloading
- **Rate Limiting**: Configurable delays to avoid blocks
- **Error Handling**: Failed download logging and retry functionality
- **File Management**: Organized downloads folder and statistics
- **Basic Features**: Clean filenames, progress tracking, user-friendly interface

## 🎯 Future Improvements & Roadmap

### Planned Features
- [ ] **GUI Interface**: Graphical user interface for both downloader and subtitle tools
- [ ] **Download Queue Management**: Pause/resume downloads, priority queuing
- [ ] **Format Selection**: Choose video quality and format (360p, 720p, 1080p, etc.)
- [ ] **Advanced Subtitle Tools**: Subtitle editing, synchronization, translation features
- [ ] **Metadata Preservation**: Keep original video metadata, descriptions, thumbnails
- [ ] **Playlist Support**: Download entire Rutube playlists or channels
- [ ] **Cloud Integration**: Sync downloads to cloud storage (Google Drive, Dropbox)
- [ ] **Multi-language Subtitles**: Generate subtitles in multiple languages simultaneously
- [ ] **Batch Renaming**: Organized file renaming with patterns and templates

### Known Limitations
- **Platform Specific**: Currently only supports Rutube.ru (not YouTube, Vimeo, etc.)
- **Manual URLs**: Requires manual URL input (no playlist or channel discovery)
- **Processing Power**: Subtitle generation requires decent CPU/GPU for good speed
- **Storage Requirements**: Large models require significant disk space (up to 6GB for large)
- **No GUI**: Command-line interface only (planned for future versions)
- **Language Support**: Primarily optimized for Russian and English content

---

*Last Updated: January 2026*  
*Version: 2.0.0*  
*Author: Andrew Gotham*  
*Contact: andreogotema@gmail.com*  
*Telegram: https://t.me/SirAndrewGotham*
