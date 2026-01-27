# **Rutube Downloader Project Context**

## **PROJECT OVERVIEW**
**Project Name**: Rutube Video Downloader with Subtitle Generator  
**Version**: 2.0.0  
**Author**: Andrew Gotham  
**Contact**: andreogotema@gmail.com  
**Telegram**: https://t.me/SirAndrewGotham  
**License**: MIT

## **CORE ARCHITECTURE**

### **File Structure**
```
rutube_downloader/
├── rutube_downloader.py              # MAIN APPLICATION (v2.0.0)
│   └── Entry point with integrated subtitle access
├── create_subtitles.py               # Interactive subtitle generator (optional)
├── quick_subtitles.py                # Quick subtitle generator (optional)
├── downloads/                        # Auto-created: Downloaded videos
├── subtitles/                        # Auto-created: Generated subtitle files
├── failed_downloads.txt              # Auto-created: Log of failed downloads
├── README.md                         # User documentation
└── COMPLETE_DOCUMENTATION.md         # Developer documentation
```

### **Dependencies**
- **Primary**: `yt-dlp` (auto-installs on first run)
- **Subtitle Feature**: `faster-whisper` (only if subtitle tools used)
- **Python Version**: 3.7+

## **MAIN APPLICATION (rutube_downloader.py)**

### **Core Functions**
1. **`main()`** - Entry point with menu system (options 1-9)
2. **`download_rutube_video()`** - Single video download with platform-aware URL handling
3. **`batch_download_mode()`** - Multiple videos with configurable delays
4. **`handle_subtitle_generation()`** - Integrated subtitle tool launcher (NEW in v2.0)

### **Key Features Implemented**
- **Rate Limiting**: Three levels (5-10s, 10-20s, 30-60s) with random intervals
- **Error Handling**: Failed downloads logged to `failed_downloads.txt` with automatic retry
- **File Management**: Auto-created folders, clean filenames (100 char limit)
- **Subtitle Integration**: Smart detection and launching of subtitle tools
- **Platform Awareness**: Rutube-focused but handles other URLs gracefully

### **Critical Code Patterns**
- **URL Cleaning**: Only for Rutube URLs (`rutube.ru` domain specific)
- **Progress Display**: Custom `progress_hook()` with visual bars
- **Filename Sanitization**: `clean_filename()` removes invalid filesystem chars
- **Menu System**: While-loop with numbered options 1-9

## **SUBTITLE INTEGRATION SYSTEM**

### **Integration Functions (NEW in v2.0)**
```python
def check_downloads_for_subtitles() -> bool
    # Returns True if videos exist in downloads/ folder
    
def find_subtitle_generator() -> str
    # Returns script name if create_subtitles.py or quick_subtitles.py exists
    
def launch_subtitle_tool(script_name: str) -> None
    # Runs subtitle generator as subprocess with user confirmation
    
def offer_subtitle_download() -> None
    # Guides user to install missing subtitle tools
    
def handle_subtitle_generation() -> None
    # Main integration point - called from menu option 6
```

### **Subtitle Tools (Separate Files)**
- **`create_subtitles.py`**: Interactive with model/language selection
- **`quick_subtitles.py`**: Automatic batch processing
- **Both use**: `faster-whisper` for transcription, output to `subtitles/` folder

## **CURRENT LIMITATIONS & DESIGN DECISIONS**

### **Platform Support**
- **Primary Target**: `rutube.ru` ONLY
- **YouTube Handling**: Warning messages, no full support
- **URL Cleaning**: ONLY applies to Rutube URLs (platform-specific)
- **Reason**: YouTube requires different handling (cookies, JavaScript, age restrictions)

### **User Experience Decisions**
1. **Auto-installation**: `yt-dlp` installs automatically if missing
2. **No External Config**: All settings in-code, no config files
3. **Folder Auto-creation**: `downloads/` and `subtitles/` created on demand
4. **Minimal Dependencies**: Only installs what's absolutely needed

### **Technical Constraints**
- **Filename Length**: Limited to 100 characters
- **Video Format**: Forces MP4 (`best[ext=mp4]`)
- **Delay Randomization**: Uses `random.uniform()` for human-like behavior
- **Error Recovery**: 403 errors trigger 30-60 second waits

## **RECENT CHANGES (v1.0 → v2.0)**

### **Added in v2.0.0**
1. **Subtitle Integration** (Option 6 in menu)
2. **Smart Detection**: Checks for videos before offering subtitles
3. **Enhanced Stats**: Shows subtitle coverage in statistics
4. **User Guidance**: Better error messages and suggestions
5. **Platform Awareness**: Selective URL cleaning (Rutube-only)

### **Bug Fixes Applied**
1. **Type Comparison Bug**: Fixed `'>' not supported between instances of 'NoneType' and 'int'`
2. **YouTube URL Issue**: No longer breaks Rutube URLs by over-cleaning
3. **Conditional Checks**: Added `if duration and duration > 0:` style checks

## **FUTURE DEVELOPMENT PATHS**

### **Option A: Keep Rutube-Focused**
- Enhance Rutube-specific features (playlists, channels)
- Improve rate limiting for Rutube's specific thresholds
- Add Rutube metadata preservation

### **Option B: Multi-Platform Expansion**
```python
# Potential architecture for multi-platform support
PLATFORM_CONFIGS = {
    'rutube': {
        'url_clean': True,      # Remove query params
        'delay_range': (5, 10), # Rutube-specific delays
        'headers': {...},       # Platform-specific headers
    },
    'youtube': {
        'url_clean': False,     # Keep all query params
        'cookies_needed': True, # May need cookie files
        'format_options': {...},
    },
    # Other platforms...
}
```

### **Option C: GUI Development**
- Tkinter/PyQt interface
- Drag-and-drop URL support
- Real-time progress visualization
- Subtitle preview/edit window

### **Option D: Advanced Features**
1. **Download Queue Management**: Pause/resume, priority scheduling
2. **Format Selection**: User chooses quality/format
3. **Metadata Tools**: Thumbnail extraction, description saving
4. **Cloud Integration**: Upload to Google Drive/OneDrive
5. **API Version**: REST API for remote control

## **CRITICAL CODE SECTIONS FOR MAINTENANCE**

### **URL Handling (Line ~110)**
```python
# CRITICAL: Only clean Rutube URLs
if 'rutube.ru' in url and '?' in url:
    base_url = url.split('?')[0]
    url = base_url
# DO NOT clean YouTube or other platform URLs
```

### **Progress Display (Line ~80)**
```python
# Custom progress hook - modifies yt-dlp's output
bar = '█' * filled + '░' * (bar_length - filled)
print(f"\r   [{bar}] {percent} | {speed} | ETA: {eta}", end='', flush=True)
```

### **Subtitle Integration (Line ~550)**
```python
# Smart launching system
subtitle_script = find_subtitle_generator()
if subtitle_script:
    launch_subtitle_tool(subtitle_script)  # User confirmation required
else:
    offer_subtitle_download()  # Guidance for missing tools
```

### **Error Recovery (Line ~350)**
```python
# Special handling for 403 errors
if "403" in error_msg or "Forbidden" in error_msg:
    print(f"⚠️  Got 403 error, waiting 30 seconds...")
    time.sleep(30)  # Extended wait for rate limiting
```

## **TESTING PROTOCOLS**

### **Core Functionality Tests**
1. **Rutube Download**: Single video with clean URL
2. **Batch Download**: 3+ videos with delays
3. **Error Handling**: Invalid URL, 403 simulation
4. **Subtitle Integration**: With/without subtitle tools present

### **Edge Cases to Consider**
1. **Very Long Titles**: >100 characters (should truncate)
2. **Special Characters**: In Rutube titles (should sanitize)
3. **Network Issues**: Interrupted downloads
4. **Disk Space**: Full disk during download

## **PERFORMANCE CONSIDERATIONS**

### **Memory Usage**
- **Downloader**: Minimal (yt-dlp handles streaming)
- **Subtitle Generation**: High (faster-whisper models: 150MB-6GB)
- **Recommendation**: Process videos in batches for large collections

### **Speed Optimizations**
- **Current**: Random delays prevent rate limiting
- **Potential**: Parallel downloads with careful rate control
- **Bottleneck**: Network speed and Rutube server responses

## **USER FLOW DIAGRAM**
```
Main Menu
    │
    ├─1. Single Download → URL → Info → Confirm → Download → Suggest Subtitles
    │
    ├─2. Batch Download → URLs → Delays → Download All → Summary
    │
    ├─3. Retry Failed → Read failed_downloads.txt → Conservative Retry
    │
    ├─6. Generate Subtitles → Check Downloads → Find Tools → Launch/Guide
    │
    └─7-9. Management Tools (Stats, Folder, Exit)
```

## **DEPENDENCY MANAGEMENT STRATEGY**

### **Current Approach**
- **yt-dlp**: Auto-installs on first run via `subprocess.check_call()`
- **faster-whisper**: Not auto-installed (only for subtitle tools)
- **Rationale**: Keep main downloader lightweight, add features optionally

### **Alternative Approach**
- `requirements.txt` with all dependencies
- Install everything upfront
- Pros: Predictable, Cons: Larger initial install

## **ERROR CODES & MEANINGS**

### **Common User Errors**
- `403 Forbidden`: Rate limited → Increase delays, wait longer
- `Video unavailable`: Private/deleted content → Cannot download
- `Invalid URL`: Malformed or homepage URL → Check format
- `No videos found`: Empty downloads folder → Download first

### **System Errors**
- `ModuleNotFoundError`: Missing yt-dlp → Auto-install should trigger
- `Disk full`: No space → Clear downloads folder
- `Network issues`: Connection problems → Check internet

## **CONTRIBUTION GUIDELINES**
1. **Platform Focus**: Keep Rutube as primary target
2. **Backward Compatibility**: Don't break existing v2.0 features
3. **User Experience**: Add helpful messages for errors
4. **Code Style**: Follow existing patterns (functions, error handling)
5. **Testing**: Test both Rutube and edge cases

## **NEXT VERSION CONSIDERATIONS**
- **v2.1**: Bug fixes and minor enhancements
- **v3.0**: Major feature (GUI, multi-platform, or advanced queue system)
- **Timeline**: Based on user feedback and Rutube API changes

---
**Last Updated**: December 2023  
**Current Focus**: Stable Rutube downloading with optional subtitle generation  
**Development Status**: Active maintenance, feature-complete for v2.0 scope

*This context file should be updated with each major change to the project.*