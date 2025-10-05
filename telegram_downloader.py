#!/usr/bin/env python3
"""
Telegram Channel Video Downloader
Downloads all media from a Telegram channel (works with private channels)
"""

import os
import asyncio
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.errors import FloodWaitError
import time

# ===================== CONFIGURATION =====================
API_ID = '23811293'  # Replace with your api_id from my.telegram.org
API_HASH = '5d43e3bbb7fe7e63a697af4e088ea04e'  # Replace with your api_hash

# Channel to download from (can be username or invite link)
CHANNEL_USERNAME = -1003089670048  # e.g., 'telegram' or full link

# Download settings
DOWNLOAD_FOLDER = 'downloads'
DOWNLOAD_VIDEOS = True
DOWNLOAD_PHOTOS = True
DOWNLOAD_DOCUMENTS = True
DOWNLOAD_AUDIO = True

# Advanced settings
MAX_MESSAGES = None  # None for all messages, or set a number like 100
RESUME_FROM_MESSAGE_ID = None  # Set to message ID to resume from specific point
SAVE_METADATA = True  # Save message info as JSON
# =========================================================


class ChannelDownloader:
    def __init__(self, api_id, api_hash, channel, download_folder):
        self.api_id = api_id
        self.api_hash = api_hash
        self.channel = channel
        self.download_folder = download_folder
        self.client = None
        self.stats = {
            'total_messages': 0,
            'videos_downloaded': 0,
            'photos_downloaded': 0,
            'documents_downloaded': 0,
            'audio_downloaded': 0,
            'skipped': 0,
            'errors': 0
        }
        
    async def initialize(self):
        """Initialize the Telegram client and authenticate"""
        print("🚀 Initializing Telegram client...")
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)
        await self.client.start()
        print("✅ Successfully authenticated!")
        
        # Verify we can access the channel
        try:
            entity = await self.client.get_entity(self.channel)
            print(f"📢 Channel found: {entity.title}")
            return entity
        except Exception as e:
            print(f"❌ Error accessing channel: {e}")
            print("Make sure you've joined the channel and the username/link is correct")
            raise
    
    def create_download_structure(self):
        """Create folder structure for downloads"""
        os.makedirs(self.download_folder, exist_ok=True)
        os.makedirs(f"{self.download_folder}/videos", exist_ok=True)
        os.makedirs(f"{self.download_folder}/photos", exist_ok=True)
        os.makedirs(f"{self.download_folder}/documents", exist_ok=True)
        os.makedirs(f"{self.download_folder}/audio", exist_ok=True)
        os.makedirs(f"{self.download_folder}/metadata", exist_ok=True)
        print(f"📁 Download folder created: {self.download_folder}")
    
    def get_safe_filename(self, message, extension):
        """Generate a safe filename for the downloaded file"""
        timestamp = message.date.strftime("%Y%m%d_%H%M%S")
        message_id = message.id
        return f"{timestamp}_msg{message_id}{extension}"
    
    async def download_media(self, message):
        """Download media from a message"""
        if not message.media:
            return None
        
        try:
            media_type = None
            folder = None
            
            # Determine media type and folder
            if message.video and DOWNLOAD_VIDEOS:
                media_type = 'video'
                folder = 'videos'
                extension = '.mp4'
            elif message.photo and DOWNLOAD_PHOTOS:
                media_type = 'photo'
                folder = 'photos'
                extension = '.jpg'
            elif message.document:
                # Check if it's audio
                if message.document.mime_type and 'audio' in message.document.mime_type and DOWNLOAD_AUDIO:
                    media_type = 'audio'
                    folder = 'audio'
                    extension = '.mp3'
                elif DOWNLOAD_DOCUMENTS:
                    media_type = 'document'
                    folder = 'documents'
                    # Try to get original extension
                    for attr in message.document.attributes:
                        if hasattr(attr, 'file_name'):
                            extension = os.path.splitext(attr.file_name)[1] or '.bin'
                            break
                    else:
                        extension = '.bin'
            else:
                return None
            
            if not folder:
                return None
            
            # Generate filename
            filename = self.get_safe_filename(message, extension)
            filepath = os.path.join(self.download_folder, folder, filename)
            
            # Skip if already downloaded
            if os.path.exists(filepath):
                print(f"⏭️  Skipping (already exists): {filename}")
                self.stats['skipped'] += 1
                return filepath
            
            # Download the media
            print(f"⬇️  Downloading {media_type}: {filename}")
            path = await self.client.download_media(message, filepath)
            
            # Update stats
            if media_type == 'video':
                self.stats['videos_downloaded'] += 1
            elif media_type == 'photo':
                self.stats['photos_downloaded'] += 1
            elif media_type == 'document':
                self.stats['documents_downloaded'] += 1
            elif media_type == 'audio':
                self.stats['audio_downloaded'] += 1
            
            return path
            
        except FloodWaitError as e:
            print(f"⏳ Rate limit hit. Waiting {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)
            return await self.download_media(message)
        except Exception as e:
            print(f"❌ Error downloading media from message {message.id}: {e}")
            self.stats['errors'] += 1
            return None
    
    def save_message_metadata(self, message, media_path):
        """Save message metadata as JSON"""
        if not SAVE_METADATA:
            return
        
        metadata = {
            'message_id': message.id,
            'date': message.date.isoformat(),
            'text': message.text or '',
            'views': message.views or 0,
            'forwards': message.forwards or 0,
            'media_path': media_path,
            'sender_id': message.sender_id,
            'has_media': message.media is not None
        }
        
        metadata_file = os.path.join(
            self.download_folder, 
            'metadata', 
            f'msg{message.id}_metadata.json'
        )
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    async def download_channel(self):
        """Main function to download all media from the channel"""
        try:
            # Initialize
            entity = await self.initialize()
            self.create_download_structure()
            
            print(f"\n{'='*60}")
            print(f"📥 Starting download from: {entity.title}")
            print(f"{'='*60}\n")
            
            # Iterate through messages
            message_count = 0
            async for message in self.client.iter_messages(
                entity, 
                limit=MAX_MESSAGES,
                reverse=False,
                offset_id=RESUME_FROM_MESSAGE_ID or 0
            ):
                message_count += 1
                self.stats['total_messages'] = message_count
                
                # Download media if present
                media_path = await self.download_media(message)
                
                # Save metadata
                self.save_message_metadata(message, media_path)
                
                # Progress update every 10 messages
                if message_count % 10 == 0:
                    self.print_stats()
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
            
            # Final stats
            print(f"\n{'='*60}")
            print("✅ Download complete!")
            print(f"{'='*60}")
            self.print_stats()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Download interrupted by user")
            print(f"Last processed message ID: {message_count}")
            print("You can resume by setting RESUME_FROM_MESSAGE_ID in the config")
            self.print_stats()
        except Exception as e:
            print(f"\n❌ Error during download: {e}")
            raise
        finally:
            if self.client:
                await self.client.disconnect()
    
    def print_stats(self):
        """Print download statistics"""
        print(f"\n📊 Statistics:")
        print(f"   Total messages: {self.stats['total_messages']}")
        print(f"   Videos: {self.stats['videos_downloaded']}")
        print(f"   Photos: {self.stats['photos_downloaded']}")
        print(f"   Documents: {self.stats['documents_downloaded']}")
        print(f"   Audio: {self.stats['audio_downloaded']}")
        print(f"   Skipped: {self.stats['skipped']}")
        print(f"   Errors: {self.stats['errors']}\n")


async def main():
    """Entry point"""
    # Validate configuration
    if API_ID == 'YOUR_API_ID' or API_HASH == 'YOUR_API_HASH':
        print("❌ Error: Please set your API_ID and API_HASH in the configuration section")
        print("Get them from: https://my.telegram.org")
        return
    
    if CHANNEL_USERNAME == 'channelname':
        print("❌ Error: Please set CHANNEL_USERNAME in the configuration section")
        print("Use channel username (e.g., 'telegram') or invite link")
        return
    
    # Create and run downloader
    downloader = ChannelDownloader(
        API_ID, 
        API_HASH, 
        CHANNEL_USERNAME, 
        DOWNLOAD_FOLDER
    )
    
    await downloader.download_channel()


if __name__ == '__main__':
    # Run the async main function
    asyncio.run(main())
