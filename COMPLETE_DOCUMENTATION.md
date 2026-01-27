# Rutube Video Downloader - Complete Documentation

## Project Overview
The Rutube Video Downloader is a robust Python application designed to download videos from Rutube.ru platform with comprehensive features including rate limiting, error handling, file management, and integrated subtitle generation. Version 2.0.0 introduces seamless subtitle generation integration directly from the main menu.

## 📁 Project Structure
```
rutube_downloader/
├── rutube_downloader.py    # Main video downloader application (v2.0.0)
├── create_subtitles.py     # Interactive subtitle generator (full features)
├── quick_subtitles.py      # Quick subtitle generator (automatic)
├── requirements.txt        # Core dependencies (yt-dlp only)
├── requirements-full.txt   # Complete dependencies (incl. faster-whisper)
├── README.md               # User documentation
├── COMPLETE_DOCUMENTATION.md # This detailed documentation
├── downloads/              # Auto-created: Downloaded videos
├── subtitles/              # Auto-created: Generated subtitle files
└── failed_downloads.txt    # Auto-created: Log of failed downloads
```

## 🚀 Features

### Video Downloader Features
1. **Single Video Download**
   - Individual video downloads with original titles preserved
   - Clean filename sanitization (removes invalid filesystem characters)
   - Progress tracking with visual indicators and ETA
   - Platform-aware URL handling (Rutube-focused)

2. **Batch Download**
   - Multiple video downloads with sequential processing
   - Configurable delay settings (Normal/Conservative/Very Slow)
   - Automatic retry logic for failed downloads
   - Progress tracking across entire batch

3. **Rate Limiting**
   - Three delay presets: 5-10s (Normal), 10-20s (Conservative), 30-60s (Very Slow)
   - Random delay intervals to mimic human behavior
   - Special handling for 403 errors with extended 30-second waits
   - Adaptive delays based on error responses

4. **Error Handling**
   - Comprehensive error logging to `failed_downloads.txt`
   - Failed downloads tracked with timestamps and error messages
   - Automatic retry functionality with conservative settings (15-30s delays)
   - User-friendly error messages with platform-specific troubleshooting

5. **File Management**
   - Organized `downloads/` folder with automatic creation
   - File statistics and information display (counts, sizes, formats)
   - Failed downloads log management (view, clear, delete)
   - Folder browsing with automatic file explorer opening

6. **Subtitle Generator Integration** (NEW in v2.0.0)
   - Integrated access to subtitle tools from main menu (Option 6)
   - Smart detection of downloaded videos before offering subtitles
   - Automatic launch of available subtitle generators
   - Guidance for installing subtitle tools if missing
   - Statistics showing subtitle coverage for videos

### Subtitle Generator Features (Separate Tools)
7. **Speech Recognition**
   - Uses faster-whisper (optimized Whisper implementation) for accurate transcription
   - No FFmpeg required for audio extraction (built-in methods)
   - Multiple language support (Russian, English, auto-detect)
   - Five model sizes for speed/accuracy trade-off

8. **Subtitle Creation**
   - Generates professionally formatted SRT files with proper timestamps
   - Accurate timestamp synchronization (HH:MM:SS,mmm format)
   - Configurable confidence thresholds for transcription accuracy
   - Organized `subtitles/` folder output with matching filenames

9. **Batch Processing**
   - Process all videos in downloads folder or select specific files
   - Progress tracking with elapsed time and ETA display
   - Metadata preservation in JSON files (confidence, language, duration)
   - Error logging to `failed_files.txt` with detailed reasons

## 🔧 Technical Details

### Dependencies
- **yt-dlp**: Advanced video download library (auto-installed by main script)
- **faster-whisper**: Efficient speech recognition for subtitles (auto-installed by subtitle tools)
- **Python Standard Library**: os, re, sys, time, datetime, random, subprocess

### Key Functions

#### Video Downloader (Main Application)
- `clean_filename(filename)`: Sanitizes filenames for filesystem compatibility
- `progress_hook(d)`: Real-time download progress visualization with custom bar
- `download_rutube_video()`: Handles single video downloads with user confirmation
- `batch_download_mode()`: Manages batch downloads with configurable rate limiting
- `save_failed_downloads(failed_urls)`: Logs failed download attempts with timestamps
- `retry_failed_downloads()`: Automatically retries previously failed downloads
- `handle_subtitle_generation()`: Integrated subtitle generator launcher (NEW in v2.0)
- `check_downloads_for_subtitles()`: Validates video availability for subtitles
- `find_subtitle_generator()`: Locates available subtitle tools in directory
- `launch_subtitle_tool()`: Executes subtitle generator as separate subprocess

#### Subtitle Generator (Separate Tools)
- `format_timestamp(seconds)`: Converts seconds to SRT timestamp format (HH:MM:SS,mmm)
- `create_srt_from_segments()`: Creates SRT files from transcription segments
- `transcribe_video()`: Transcribes video audio using faster-whisper models
- `batch_process_videos()`: Processes multiple videos for subtitle generation

## ⚙️ Configuration Options

### Downloader Settings
1. **Delay Settings**:
   - **Normal**: 5-10 seconds between downloads (default, for small batches)
   - **Conservative**: 10-20 seconds between downloads (recommended for 5-20 videos)
   - **Very Slow**: 30-60 seconds between downloads (for large batches or if experiencing blocks)

2. **File Management**:
   - Downloads Folder: `downloads/` (auto-created on first download)
   - Log File: `failed_downloads.txt` (auto-managed, can be cleared or deleted)
   - Maximum Filename Length: 100 characters (safe for all filesystems)
   - Subtitle Integration: Automatic detection and launching

### Subtitle Generator Settings
1. **Model Selection** (when using create_subtitles.py):
   - **tiny**: Fastest, lowest accuracy (~150MB, ~1GB RAM, good for testing)
   - **base**: Balanced speed/accuracy (~300MB, ~1.5GB RAM, recommended for most uses)
   - **small**: Better accuracy, moderate speed (~1GB, ~3GB RAM)
   - **medium**: High accuracy, slower processing (~3GB, ~6GB RAM)
   - **large**: Best accuracy, slowest processing (~6GB, ~10GB RAM)

2. **Language Options**:
   - **Russian (ru)**: Default for Rutube content
   - **English (en)**: For English-language videos
   - **Auto-detect**: Let the model detect language automatically (slower)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher (check with `python --version`)
- Internet connection for downloads and model fetching
- Rutube account (for private videos, if needed)
- Disk space: 500MB-3GB for subtitle models (depending on chosen model size)

### Installation Methods

#### Method 1: Run Directly (Simplest)
```bash
# Clone and run - dependencies auto-install as needed
git clone https://github.com/yourusername/rutube-downloader-subtitles.git
cd rutube-downloader-subtitles
python rutube_downloader.py
```
*The script will auto-install yt-dlp on first run if missing.*

#### Method 2: Complete Installation
```bash
# Install all dependencies upfront
pip install -r requirements-full.txt
# or manually
pip install yt-dlp faster-whisper

# Run the application
python rutube_downloader.py
```

#### Method 3: Development Setup
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install core dependencies
pip install -r requirements.txt

# Run application
python rutube_downloader.py
```

### Dependency Files Explained

#### `requirements.txt` (Core Only)
```txt
# Core video downloading functionality
yt-dlp>=2023.11.16

# Note: faster-whisper NOT included because:
# 1. Optional feature (not all users need subtitles)
# 2. Large download (150MB-6GB)
# 3. Auto-installs when subtitle tools are used
# 4. Reduces initial installation time/space
```

#### `requirements-full.txt` (Complete)
```txt
# Complete dependency list
yt-dlp>=2023.11.16
faster-whisper>=0.9.0
```

### Platform-Specific Setup

#### Windows
```bash
# Should work out of the box
python rutube_downloader.py
```

#### macOS
```bash
# Recommended for optimal audio processing
brew install ffmpeg
python rutube_downloader.py
```

#### Linux
```bash
# Recommended for subtitle processing
sudo apt update
sudo apt install ffmpeg
python rutube_downloader.py
```

### Verifying Installation
```bash
# Check Python version
python --version  # Should show 3.7 or higher

# Verify yt-dlp installation
python -c "import yt_dlp; print(f'yt-dlp version: {yt_dlp.version.__version__}')"

# Verify faster-whisper (if installed for subtitles)
python -c "import faster_whisper; print('faster-whisper available')"
```

## 📖 Usage Guide

### Complete Workflow

#### Phase 1: Download Videos
```bash
python rutube_downloader.py
```
**Options:**
- **Option 1**: Single video download (paste URL, view info, confirm)
- **Option 2**: Batch download (enter URLs, choose delays, download all)
- **Option 3**: Retry failed downloads (reads from `failed_downloads.txt`)

**Example Rutube URL format:**
```
https://rutube.ru/video/8e06c530938f25bf791a71251fe0f04d/
```

#### Phase 2: Generate Subtitles
```bash
python rutube_downloader.py
# Choose Option 6 from main menu
```
**Or run subtitle tools directly:**
```bash
# Interactive version (choose models, languages, specific files)
python create_subtitles.py

# Quick version (automatic, processes all videos)
python quick_subtitles.py
```

#### Phase 3: Watch with Subtitles
1. **Automatic Detection**: Most players auto-detect `.srt` files with same base name
2. **Manual Loading**: In VLC: `Subtitles → Add Subtitle File`
3. **File Location**: Subtitles saved to `subtitles/` folder with matching names

### Downloading Videos

#### Single Video Download
1. Run `python rutube_downloader.py`
2. Choose **Option 1**
3. Paste Rutube video URL
4. View video information (title, uploader, duration, views)
5. Confirm download (y/n)
6. Watch progress bar with download speed and ETA
7. File saves to `downloads/` folder with cleaned filename

#### Batch Download
1. Run `python rutube_downloader.py`
2. Choose **Option 2**
3. Enter URLs one per line, type 'done' when finished
4. Choose delay setting based on batch size:
   - **Normal**: 1-5 videos
   - **Conservative**: 5-20 videos
   - **Very Slow**: 20+ videos or if experiencing blocks
5. Watch progress for each video
6. View summary (success/failure counts)
7. Failed URLs saved to `failed_downloads.txt` for retry

#### Retry Failed Downloads
1. Run `python rutube_downloader.py`
2. Choose **Option 3**
3. Script reads `failed_downloads.txt`
4. Uses conservative delays (15-30 seconds)
5. Attempts all previously failed downloads
6. Updates log file with new results

### Generating Subtitles

#### Integrated Method (Option 6)
1. Run `python rutube_downloader.py`
2. Choose **Option 6**
3. Script checks for videos in `downloads/` folder
4. If found, checks for available subtitle tools
5. Launches tool with user confirmation
6. Returns to main menu when subtitle tool closes

#### Interactive Tool (create_subtitles.py)
```bash
python create_subtitles.py
```
**Features:**
- Choose specific videos to process
- Select from 5 model sizes
- Choose language (ru, en, auto)
- View detailed progress with timers
- Save metadata in JSON files
- Log failures to `failed_files.txt`

#### Quick Tool (quick_subtitles.py)
```bash
python quick_subtitles.py
```
**Features:**
- Automatic processing of all videos
- Uses base model (balanced speed/accuracy)
- Auto-detects language
- Simple progress display
- Just SRT files, no complex options

### Managing Files

#### View Statistics (Option 7)
- Download counts and total size
- Video file counts by format
- Subtitle coverage (if subtitles/ folder exists)
- Failed downloads count

#### Open Downloads Folder (Option 8)
- Lists files in `downloads/` folder
- Shows file sizes and counts
- Attempts to open folder in file explorer
- Checks for existing subtitles

#### Log Management (Options 4 & 5)
- **Option 4**: Delete `failed_downloads.txt` completely
- **Option 5**: Clear contents but keep file structure
- Both require user confirmation

## 🎬 Subtitle Generator Details

### How It Works: Technical Process
1. **File Discovery**: Scans `downloads/` folder for video files (`.mp4`, `.mkv`, `.webm`, `.avi`, `.mov`)
2. **Audio Extraction**: Uses faster-whisper's built-in audio extraction (no external FFmpeg needed)
3. **Transcription**: Processes audio through selected Whisper model
4. **Segment Processing**: Divides transcription into manageable segments with timestamps
5. **SRT Creation**: Formats segments into standard SRT format with proper timing
6. **File Output**: Saves `.srt` files to `subtitles/` folder with matching base names
7. **Metadata**: Creates `.json` files with transcription details for reference

### Model Comparison Table

| Model | Size | Speed | Accuracy | RAM Usage | Storage | Best Use Case |
|-------|------|-------|----------|-----------|---------|---------------|
| **tiny** | 150MB | ⚡⚡⚡⚡⚡ | 25% | ~1GB | Small | Testing, quick previews |
| **base** | 300MB | ⚡⚡⚡⚡ | 50% | ~1.5GB | Medium | General use (recommended) |
| **small** | 1GB | ⚡⚡⚡ | 75% | ~3GB | Large | Better accuracy needs |
| **medium** | 3GB | ⚡⚡ | 90% | ~6GB | X-Large | High accuracy requirements |
| **large** | 6GB | ⚡ | 95% | ~10GB | XX-Large | Best possible accuracy |

### Language Support
- **Russian (ru)**: Optimized for Rutube content
- **English (en)**: For English-language videos
- **Auto-detect**: Automatically detects language (adds ~20% processing time)
- **Note**: Models are multilingual but perform best on languages they were trained on

### Output Files

#### Primary Output
- **`.srt` files**: Subtitle files in `subtitles/` folder
   - Same base name as video files (e.g., `video.mp4` → `video.srt`)
   - Standard SRT format compatible with all video players
   - Accurate timestamps in `HH:MM:SS,mmm` format

#### Metadata Files
- **`.json` files**: Detailed transcription metadata
  ```json
  {
    "video_file": "example.mp4",
    "subtitle_file": "example.srt",
    "language": "ru",
    "model": "base",
    "duration_seconds": 125.5,
    "segments_count": 42,
    "confidence_avg": 0.85,
    "processing_time": 45.2
  }
  ```

#### Log Files
- **`failed_files.txt`**: List of files that failed processing with error reasons
- **Console output**: Real-time progress with percentage and ETA

### Performance Optimization

#### For Fast Processing
1. Use **tiny** or **base** models
2. Process during low system usage
3. Close other applications
4. Use SSD storage if available

#### For Best Accuracy
1. Use **small** or **medium** models
2. Ensure good audio quality in source videos
3. Use explicit language setting instead of auto-detect
4. Allow sufficient processing time

#### Memory Management
1. Smaller models use less RAM
2. Process videos one at a time for large collections
3. Monitor system resources during processing
4. Consider system swap space for large models

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Download Issues

**Problem**: 403 Forbidden errors from Rutube
**Solution**:
```bash
# 1. Use "Very Slow" delay setting (30-60 seconds)
# 2. Wait several hours between large batches
# 3. Consider using a VPN to change IP address
# 4. Use Option 3 to retry with conservative delays
```

**Problem**: "URL is incorrect or video is not available"
**Solution**:
1. Verify URL is correct and video is public
2. For Rutube: Ensure URL follows pattern: `https://rutube.ru/video/ID/`
3. Remove any tracking parameters manually if needed
4. Check if video requires login (private content)

**Problem**: YouTube URLs not working properly
**Solution**:
```bash
# This tool is optimized for Rutube, not YouTube
# For YouTube, use yt-dlp directly:
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Subtitle Generation Issues

**Problem**: "ModuleNotFoundError: No module named 'faster_whisper'"
**Solution**:
```bash
# Install faster-whisper
pip install faster-whisper

# Or let the subtitle tool install it automatically
# It will prompt to install when needed
```

**Problem**: Poor transcription accuracy
**Solution**:
1. Try a larger model (base → small → medium)
2. Check audio quality (background noise affects accuracy)
3. Use explicit language setting instead of auto-detect
4. Ensure sufficient volume in source video

**Problem**: "Out of memory" errors
**Solution**:
1. Use smaller model (tiny or base instead of large)
2. Close other applications during processing
3. Process fewer videos at once
4. Check system RAM and consider upgrading

#### File System Issues

**Problem**: Downloaded files not appearing
**Solution**:
1. Check `downloads/` folder exists
2. Look for files with similar but cleaned names
3. Check file permissions in the folder
4. Verify disk space is available

**Problem**: Subtitles not loading in video player
**Solution**:
1. Ensure `.srt` file has same base name as video
2. Check both files are in same folder
3. Verify video player supports SRT subtitles
4. Try manually loading subtitles in player settings

### Error Messages Reference

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `403 Forbidden` | Rate limited by Rutube | Increase delays, wait, use VPN |
| `Video unavailable` | Private/deleted content | Cannot download, skip |
| `Invalid URL` | Malformed URL | Check format, use correct Rutube URL |
| `No videos found` | Empty downloads folder | Download videos first |
| `ModuleNotFoundError` | Missing dependency | Install required package |
| `Disk full` | No storage space | Clear space, delete old files |
| `Network error` | Connection issues | Check internet, try later |

### Platform-Specific Issues

#### Windows
- **Permission errors**: Run as administrator if needed
- **Path length limits**: Filenames truncated to 100 characters
- **Antivirus blocking**: Add exception for Python scripts

#### macOS
- **FFmpeg missing**: `brew install ffmpeg` for best performance
- **Gatekeeper warnings**: Right-click → Open for first run
- **Python path issues**: Use `python3` if `python` not found

#### Linux
- **Permission denied**: Use `chmod +x` on scripts if needed
- **Missing dependencies**: `sudo apt install ffmpeg python3-pip`
- **Python version**: Ensure Python 3.7+ with `python3 --version`

## 🔒 Privacy & Security

### Data Handling Principles
- **Local Processing Only**: All video downloading and subtitle generation happens on your computer
- **No External Servers**: Audio is never sent to cloud services (unlike online transcription tools)
- **No Data Collection**: No personal information, usage statistics, or analytics are collected
- **Transparent Code**: Open source allows inspection of all operations

### Security Features
1. **No Network After Download**: Subtitle generation works offline once models are downloaded
2. **File System Sandboxing**: All operations confined to project folders
3. **Input Validation**: URL and filename sanitization prevents injection attacks
4. **Permission Awareness**: Respects system permissions and user privacy settings

### Ethical Usage Guidelines
1. **Respect Copyright**: Only download content you have rights to access
2. **Follow Terms of Service**: Adhere to Rutube's terms and conditions
3. **Personal Use**: Intended for personal, educational, and accessibility purposes
4. **Rate Limiting**: Use appropriate delays to avoid overloading servers
5. **Legal Compliance**: Follow applicable laws in your jurisdiction

## 📈 Performance Tips

### For Large Video Collections
1. **Batch Strategy**: Download in batches of 10-20 with "Very Slow" delays
2. **Time Scheduling**: Process during off-peak hours (late night/early morning)
3. **Incremental Processing**: Download → Generate subtitles → Repeat
4. **Monitoring**: Watch `failed_downloads.txt` and adjust delays accordingly

### Speed Optimization
1. **Network**: Use wired connection for large downloads
2. **Storage**: SSD for faster file operations during subtitle generation
3. **RAM**: Sufficient memory for whisper models (8GB+ recommended)
4. **CPU**: Multi-core helps with parallel processing in whisper

### Resource Management
1. **Disk Space**: Monitor `downloads/` folder size, archive old videos
2. **Model Selection**: Choose appropriate model size for your hardware
3. **Batch Size**: Adjust based on available system resources
4. **Cleanup**: Regularly clear `failed_downloads.txt` if not needed

## 🤝 Support & Development

### Getting Help
1. **Documentation First**: Check this COMPLETE_DOCUMENTATION.md and README.md
2. **Error Logs**: Examine `failed_downloads.txt` and console output
3. **Community**: Check GitHub issues for similar problems
4. **Contact Author**: For unresolved issues or security concerns

### Author Information
**Andrew Gotham**
- **Email**: andreogotema@gmail.com
- **Telegram**: https://t.me/SirAndrewGotham
- **Role**: Developer & Maintainer

### Feature Requests & Feedback
We welcome suggestions for:
- Additional platform support
- Enhanced subtitle features (translation, editing)
- GUI interface development
- Performance improvements
- Bug reports and fixes

### Contributing Guidelines
1. **Fork & Clone**: Create your own copy of the repository
2. **Branch**: Create feature branch for changes
3. **Test**: Ensure changes work with existing functionality
4. **Document**: Update documentation for new features
5. **Pull Request**: Submit changes for review

## 📄 License & Legal

### MIT License
```
Copyright (c) 2023 Andrew Gotham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Legal Notice
- **Copyright Compliance**: Users are responsible for complying with copyright laws
- **Platform Terms**: Respect Rutube's terms of service and usage policies
- **Educational Purpose**: Primarily intended for educational and accessibility use
- **No Warranty**: Software provided as-is without warranties
- **Author Liability**: The author is not responsible for misuse of this tool

## 🔄 Version History

### v2.0.0 (Current) - January 2026
**Major Features:**
- Integrated subtitle generation access via main menu (Option 6)
- Smart detection of downloaded videos before offering subtitles
- Automatic launching of available subtitle tools
- Enhanced statistics showing subtitle coverage
- Improved user guidance and error messages
- Platform-aware URL handling (Rutube-specific optimizations)

**Technical Improvements:**
- Refactored URL cleaning to be Rutube-specific only
- Enhanced error handling for NoneType comparisons
- Better progress tracking and user feedback
- Updated documentation with comprehensive guides

### v1.0.0 - Initial Release
**Core Features:**
- Single and batch video downloading from Rutube
- Configurable rate limiting with three delay settings
- Failed download logging with automatic retry functionality
- Organized file management with auto-created folders
- Clean filename handling and progress tracking

## 🎯 Future Development Roadmap

### Planned Features
- [ ] **GUI Interface**: Graphical user interface for both tools
- [ ] **Download Queue Management**: Pause/resume, priority scheduling
- [ ] **Format Selection**: User-selectable video quality and formats
- [ ] **Advanced Subtitle Tools**: Editing, synchronization, translation
- [ ] **Metadata Preservation**: Original video metadata extraction
- [ ] **Playlist Support**: Rutube playlist and channel downloading
- [ ] **Cloud Integration**: Sync to cloud storage services
- [ ] **Multi-language Subtitles**: Simultaneous multiple language generation
- [ ] **Batch Renaming**: Pattern-based file organization

### Known Limitations
1. **Platform Specific**: Optimized for Rutube, limited YouTube support
2. **Manual URL Input**: No playlist discovery or channel scanning
3. **Processing Requirements**: Subtitle generation needs decent CPU/GPU
4. **Storage Needs**: Large models require significant disk space
5. **Interface**: Command-line only (GUI planned for future)
6. **Language Focus**: Primarily Russian and English content

### Development Priorities
1. **Stability**: Bug fixes and performance optimizations
2. **Usability**: Improved user experience and documentation
3. **Features**: Based on user feedback and usage patterns
4. **Compatibility**: Support for new Rutube features and changes

---

*Last Updated: January 2026*  
*Version: 2.0.0*  
*Author: Andrew Gotham*  
*Contact: andreogotema@gmail.com*  
*Telegram: https://t.me/SirAndrewGotham*  
*License: MIT*

*For the latest updates, check the GitHub repository.*
