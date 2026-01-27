# 🎬 Rutube Video Downloader with Subtitle Generator

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)

**Download videos from Rutube.ru and generate AI-powered subtitles automatically.**

A comprehensive Python tool for downloading videos from Rutube.ru with advanced features including rate limiting, error handling, and integrated subtitle generation using AI transcription.

## ✨ Features

- **📥 Smart Video Downloading**
  - Single & batch downloads from Rutube
  - Configurable rate limiting to avoid blocks (5-60 second delays)
  - Automatic retry for failed downloads with logging
  - Clean filename handling for filesystem compatibility

- **🎬 Integrated Subtitle Generation**
  - AI-powered transcription using faster-whisper
  - Russian & English language support with auto-detection
  - Multiple model sizes (tiny, base, small, medium, large)
  - Professional SRT format with accurate timestamps

- **📊 Complete Management**
  - Download statistics & real-time progress tracking
  - Organized folder structure (auto-created downloads/ & subtitles/)
  - Failed downloads logging with automatic retry option
  - User-friendly menu interface with intuitive navigation

## 🚀 Quick Start

### Method 1: Run Directly (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/rutube-downloader-subtitles.git
cd rutube-downloader-subtitles

# Run the script - it will auto-install yt-dlp if needed
python rutube_downloader.py
```

### Method 2: Install Dependencies First
```bash
# Install all dependencies including subtitle tools
pip install -r requirements-full.txt

# Run the application
python rutube_downloader.py
```

## 📋 Main Menu Options

Run `python rutube_downloader.py` and choose from:

1. **📥 Download single video** - One video at a time
2. **📋 Download multiple videos** - Batch download with rate limiting
3. **🔄 Retry failed downloads** - Automatic retry of failed downloads
4. **🗑️ Delete failed downloads log** - Remove failed downloads record
5. **🧹 Clear failed downloads log** - Clear contents but keep file
6. **🎬 Generate subtitles** - Create subtitles for downloaded videos
7. **📊 Show download statistics** - View download and subtitle counts
8. **📁 Open downloads folder** - Browse downloaded videos
9. **🚪 Exit** - Quit the application

## 📁 Project Structure

```
rutube_downloader/
├── rutube_downloader.py          # Main application (v2.0.0)
├── create_subtitles.py           # Interactive subtitle generator
├── quick_subtitles.py            # Quick subtitle generator
├── requirements.txt              # Core dependencies (yt-dlp only)
├── requirements-full.txt         # Complete dependencies
├── README.md                     # This documentation
├── COMPLETE_DOCUMENTATION.md     # Detailed developer guide
├── downloads/                    # Auto-created: Downloaded videos
├── subtitles/                    # Auto-created: Generated subtitle files
└── failed_downloads.txt          # Auto-created: Log of failed downloads
```

## 📦 Installation Options

### Minimal Installation
```bash
# Just run the script - auto-installs yt-dlp if missing
python rutube_downloader.py
```

### Complete Installation
```bash
# Install all dependencies (video download + subtitle generation)
pip install -r requirements-full.txt
# or
pip install yt-dlp faster-whisper
```

### Subtitle Generator Only
```bash
# If you only need subtitle generation for existing videos
pip install faster-whisper
python create_subtitles.py
```

## 🎯 Basic Usage

### 1. Download Videos
```bash
python rutube_downloader.py
# Choose option 1 (single) or 2 (batch)
# Paste Rutube URLs (e.g., https://rutube.ru/video/8e06c530938f25bf791a71251fe0f04d/)
# Videos save to 'downloads/' folder
```

### 2. Generate Subtitles
```bash
python rutube_downloader.py
# Choose option 6 from main menu
# Or run subtitle tools directly:
# Interactive: python create_subtitles.py
# Quick: python quick_subtitles.py
# Subtitles save to 'subtitles/' folder
```

### 3. Watch with Subtitles
- Place `.srt` files in same folder as videos (already done automatically)
- Open video in VLC, MPC-HC, or any subtitle-supporting player
- Subtitles load automatically if file names match

## 🔧 Dependencies

### Core (`requirements.txt`)
```txt
yt-dlp>=2023.11.16
```
*(Auto-installs when you run the script)*

### Complete (`requirements-full.txt`)
```txt
yt-dlp>=2023.11.16
faster-whisper>=0.9.0
```

**Note**: `faster-whisper` is only needed for subtitle generation and is large (150MB-6GB). The main script works without it.

## 🚨 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **403 Forbidden errors** | Use "Very Slow" delay setting (30-60s), wait between batches |
| **"No module named yt_dlp"** | Script auto-installs it, or run `pip install yt-dlp` |
| **YouTube URLs not working** | This tool is optimized for Rutube. Use yt-dlp directly for YouTube |
| **Subtitles not generating** | Install faster-whisper: `pip install faster-whisper` |
| **Low disk space** | Clear `downloads/` folder or choose smaller whisper models |

### Platform Notes
- **Windows**: Works out of the box
- **macOS**: `brew install ffmpeg` recommended for best performance
- **Linux**: `sudo apt install ffmpeg` recommended for subtitle processing

## 📊 Subtitle Models Comparison

| Model | Size | Speed | Accuracy | RAM Usage | Best For |
|-------|------|-------|----------|-----------|----------|
| **tiny** | ~150MB | ⚡⚡⚡⚡⚡ | ⭐⭐ | ~1GB | Testing, quick previews |
| **base** | ~300MB | ⚡⚡⚡⚡ | ⭐⭐⭐ | ~1.5GB | General use (recommended) |
| **small** | ~1GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | ~3GB | Better accuracy |
| **medium** | ~3GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | ~6GB | High accuracy needs |
| **large** | ~6GB | ⚡ | ⭐⭐⭐⭐⭐ | ~10GB | Best possible accuracy |

## 🔒 Privacy & Security

- **100% Local Processing**: All videos and subtitles stay on your computer
- **No Data Collection**: No personal information is collected or transmitted
- **No External Servers**: Audio never sent to cloud services (unlike online tools)
- **Open Source**: Full transparency - inspect the code yourself

## 🤝 Support

### Getting Help
1. **Check Documentation**: Read this README and COMPLETE_DOCUMENTATION.md
2. **Check Logs**: Look in `failed_downloads.txt` for error details
3. **Contact Author**: For issues not covered in documentation

### Author Information
**Andrew Gotham**  
📧 Email: andreogotema@gmail.com  
📱 Telegram: https://t.me/SirAndrewGotham

## 📄 License

MIT License - Free to use, modify, and distribute for personal and commercial use.

Copyright (c) 2023 Andrew Gotham

## 🌟 Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Note**: This tool is designed specifically for Rutube.ru. For YouTube, use yt-dlp directly. Always respect copyright laws and platform terms of service.
