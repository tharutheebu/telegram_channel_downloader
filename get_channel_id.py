#!/usr/bin/env python3
"""
Find Telegram Channel IDs
Lists all channels you're a member of with their IDs
"""

import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel

# Your API credentials
API_ID = '23811293'
API_HASH = '5d43e3bbb7fe7e63a697af4e088ea04e'


async def list_channels():
    """List all channels you're a member of"""
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start()
    
    print("\n" + "="*70)
    print("📋 YOUR TELEGRAM CHANNELS")
    print("="*70 + "\n")
    
    # Get all dialogs (chats/channels)
    dialogs = await client.get_dialogs()
    
    channels = []
    for dialog in dialogs:
        # Filter only channels
        if isinstance(dialog.entity, Channel):
            channels.append(dialog)
    
    if not channels:
        print("❌ No channels found. Make sure you've joined some channels!")
        return
    
    print(f"Found {len(channels)} channels:\n")
    
    for i, dialog in enumerate(channels, 1):
        entity = dialog.entity
        
        # Get channel info
        channel_id = entity.id
        channel_title = entity.title
        username = entity.username if entity.username else "No username (Private)"
        is_private = not entity.username
        member_count = getattr(entity, 'participants_count', 'Unknown')
        
        print(f"{i}. {channel_title}")
        print(f"   ID: {channel_id}")
        print(f"   Username: @{username}" if not is_private else f"   Username: {username}")
        print(f"   Type: {'Private Channel' if is_private else 'Public Channel'}")
        print(f"   Members: {member_count}")
        print(f"   {'─'*66}\n")
    
    print("\n💡 To use a channel in the downloader script:")
    print("   - For public channels: Use '@username' or the ID")
    print("   - For private channels: Use the ID number")
    print("\n   Example in script:")
    print("   CHANNEL_USERNAME = -1001234567890  # Use the ID directly (no quotes!)")
    print("   or")
    print("   CHANNEL_USERNAME = 1234567890  # Without the -100 prefix also works")
    
    await client.disconnect()


async def main():
    if API_ID == 'YOUR_API_ID' or API_HASH == 'YOUR_API_HASH':
        print("❌ Error: Please set your API_ID and API_HASH first!")
        return
    
    await list_channels()


if __name__ == '__main__':
    asyncio.run(main())
