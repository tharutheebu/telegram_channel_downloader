# Telegram Channel Downloader

A Python tool to download all media (videos, photos, documents, audio) from any Telegram channel, including private channels, without needing bot permissions.

## ✨ Features

- ✅ **Works with private channels** - No admin or bot permissions needed
- ✅ **Downloads all media types** - Videos, photos, documents, audio files
- ✅ **Resume capability** - Continue from where you left off if interrupted
- ✅ **Automatic rate limiting** - Handles Telegram's flood protection
- ✅ **Progress tracking** - Live statistics and progress updates
- ✅ **Metadata preservation** - Saves message info as JSON files
- ✅ **Skip duplicates** - Won't re-download existing files
- ✅ **Organized structure** - Separate folders for different media types

## 📋 Requirements

- Python 3.7 or higher
- Telegram account
- API credentials from Telegram

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install telethon
```

### Step 2: Get Telegram API Credentials

1. Visit https://my.telegram.org
2. Log in with your phone number
3. Click on **"API development tools"**
4. Fill in the application form:
   - App title: e.g., "Channel Downloader"
   - Short name: e.g., "downloader"
   - Platform: Desktop
5. You'll receive:
   - **api_id** (number like: 12345678)
   - **api_hash** (string like: "abcdef1234567890...")

### Step 3: Find Your Channel ID

First, you need to find the ID of the channel you want to download from.

**Run the channel finder:**

```bash
python get_channel_id.py
```

**Before running**, edit `get_channel_id.py` and add your API credentials:

```python
API_ID = 12345678  # Your api_id
API_HASH = 'your_api_hash_here'  # Your api_hash
```

This will list all channels you're a member of with their IDs.

**Example output:**
```
📋 YOUR TELEGRAM CHANNELS

1. My Private Channel
   ID: 3089670048
   Username: No username (Private)
   Type: Private Channel
   Members: 133

2. Tech News
   ID: -1009876543210
   Username: @technews
   Type: Public Channel
   Members: 5000
```

Copy the **ID** of the channel you want to download.

### Step 4: Configure the Downloader

Edit `telegram_downloader.py` and update the configuration:

```python
# Required settings
API_ID = 12345678  # Your api_id from my.telegram.org
API_HASH = 'your_api_hash_here'  # Your api_hash

# Channel to download (use the ID from step 3)
CHANNEL_USERNAME = 3089670048  # For private channels, use the numeric ID
# or for public channels:
# CHANNEL_USERNAME = '@channelname'  # Use @username
# or use invite link:
# CHANNEL_USERNAME = 'https://t.me/+AbCdEfGhIjK'

# Download preferences
DOWNLOAD_VIDEOS = True
DOWNLOAD_PHOTOS = True
DOWNLOAD_DOCUMENTS = True
DOWNLOAD_AUDIO = True

# Optional settings
MAX_MESSAGES = None  # None = all messages, or set a number like 100
DOWNLOAD_FOLDER = 'downloads'  # Where to save files
```

### Step 5: Run the Downloader

```bash
python telegram_downloader.py
```

**First time only:**
- Enter your phone number with country code (e.g., `+919876543210`)
- Enter the verification code sent to your Telegram app
- A session file will be created for future use

## 📁 Output Structure

Files are organized in folders:

```
downloads/
├── videos/          # All video files
├── photos/          # All photo files
├── documents/       # All document files
├── audio/           # All audio files
└── metadata/        # Message metadata as JSON
```

**Filename format:** `YYYYMMDD_HHMMSS_msgID.extension`

Example: `20241005_143022_msg123.mp4`

## ⚙️ Configuration Options

### Download Settings

```python
DOWNLOAD_VIDEOS = True      # Download video files
DOWNLOAD_PHOTOS = True      # Download photo files
DOWNLOAD_DOCUMENTS = True   # Download document files
DOWNLOAD_AUDIO = True       # Download audio files
```

### Advanced Settings

```python
MAX_MESSAGES = None         # Limit number of messages (None = all)
RESUME_FROM_MESSAGE_ID = None  # Resume from specific message ID
SAVE_METADATA = True        # Save message info as JSON
DOWNLOAD_FOLDER = 'downloads'  # Output folder path
```

## 🔧 Advanced Usage

### Resume Interrupted Downloads

If download is interrupted, you can resume from a specific message:

```python
RESUME_FROM_MESSAGE_ID = 12345  # Message ID to resume from
```

The script will show the last processed message ID when interrupted.

### Download Specific Number of Messages

To test or limit downloads:

```python
MAX_MESSAGES = 100  # Download only 100 most recent messages
```

### Using Different Channel Identifiers

**For private channels:**
```python
CHANNEL_USERNAME = 3089670048  # Use numeric ID
```

**For public channels:**
```python
CHANNEL_USERNAME = '@channelname'  # Use @username
```

**Using invite links:**
```python
CHANNEL_USERNAME = 'https://t.me/+AbCdEfGhIjK'  # Full invite link
```

## 📊 Progress Tracking

The script shows real-time statistics:

```
📊 Statistics:
   Total messages: 150
   Videos: 45
   Photos: 60
   Documents: 30
   Audio: 10
   Skipped: 5
   Errors: 0
```

## ⚠️ Common Issues & Solutions

### "Could not find the input entity"
- Make sure you've **joined the channel** in your Telegram app first
- Verify the channel ID/username is correct
- For private channels, use the numeric ID from `get_channel_id.py`

### "The api_id/api_hash combination is invalid"
- Double-check your credentials from https://my.telegram.org
- `API_ID` should be a number without quotes
- `API_HASH` should be a string with quotes

### "FloodWaitError" or rate limiting
- This is normal - the script automatically waits
- Telegram has rate limits to prevent abuse
- The script will resume automatically after waiting

### Files already exist
- The script skips files that already exist
- Delete the file if you want to re-download it
- Check the "Skipped" count in statistics

### Session expired
- Delete the `session_name.session` file
- Run the script again to re-authenticate

## 🛡️ Privacy & Security

- Your API credentials are stored locally only
- Session files are stored on your computer
- No data is sent to third parties
- The script only accesses channels you're a member of
- Respects Telegram's rate limits and terms of service

## 📝 Legal & Ethical Use

- Only download content from channels you have permission to access
- Respect copyright and intellectual property rights
- Use responsibly and in accordance with Telegram's Terms of Service
- This tool is for personal archival purposes only

## 🤝 Support

If you encounter issues:

1. Check the "Common Issues" section above
2. Ensure you're using Python 3.7+
3. Verify you've joined the channel first
4. Make sure your API credentials are correct
5. Try with a public channel first to test

## 📄 License

This project is provided as-is for educational and personal use.

---

**Made with ❤️ for archiving your Telegram content**