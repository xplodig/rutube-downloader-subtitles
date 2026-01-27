# 🎬 Rutube Video Downloader with Subtitle Generator

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)

**Download videos from Rutube.ru and generate AI-powered subtitles automatically.**

## ✨ Features

- **📥 Smart Video Downloading**
  - Single & batch downloads from Rutube
  - Configurable rate limiting to avoid blocks
  - Automatic retry for failed downloads
  - Clean filename handling

- **🎬 Integrated Subtitle Generation**
  - AI-powered transcription using faster-whisper
  - Russian & English language support
  - Multiple model sizes (speed vs accuracy)
  - SRT format with accurate timestamps

- **📊 Complete Management**
  - Download statistics & progress tracking
  - Organized folder structure
  - Failed downloads logging
  - User-friendly menu interface

## 🚀 Quick Start

```bash
# Clone and run
git clone https://github.com/yourusername/rutube-downloader-subtitles.git
cd rutube-downloader-subtitles
python rutube_downloader.py
```

Follow the menu:
1. Download videos (options 1 or 2)
2. Generate subtitles (option 6)
3. Watch with automatic subtitle detection
```

## **Additional Recommendations**

1. **Add a `.gitignore` file**:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Downloads (user data)
downloads/
subtitles/
failed_downloads.txt
*.log

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
```

2. **Consider adding a `requirements.txt`** (optional, since your script auto-installs):
```txt
yt-dlp>=2023.11.16
faster-whisper>=0.9.0
```

3. **License file** (you mentioned MIT):
```txt
MIT License
Copyright (c) 2023 Andrew Gotham
