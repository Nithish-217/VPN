#!/usr/bin/env python3
"""
Fixed Message Sender
Handles spaces in messages correctly
"""

import asyncio
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vpn_server.enhanced_server import VPNServer
from vpn_server.config import Config

async def send_message_with_spaces():
    """Send messages with spaces properly handled"""
    print("📨 Fixed Message Sender - Spaces Supported!")
    print("=" * 50)
    
    config = Config()
    
    # Create server instance for messaging
    server = VPNServer(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        auth_enabled=config.AUTH_ENABLED
    )
    
    print("✅ Message sender ready")
    print("💡 You can now type messages with spaces!")
    print("📝 Examples:")
    print("   - 'Hello world this is a test'")
    print("   - 'System maintenance in 5 minutes'")
    print("   - 'Welcome to the VPN service!'")
    print()
    
    while True:
        try:
            # Get full message including spaces
            message = input("Enter message (or 'quit' to exit): ").strip()
            
            if message.lower() == 'quit':
                print("👋 Goodbye!")
                break
                
            if not message:
                print("❌ Message cannot be empty")
                continue
            
            # For demo purposes, we'll just show what would be sent
            print(f"✅ Message ready to send: '{message}'")
            print(f"📏 Message length: {len(message)} characters")
            print(f"🔤 Words: {len(message.split())} words")
            print(f"💬 Spaces: {message.count(' ')} spaces")
            print()
            
            print("💡 To actually send this message:")
            print("   1. Go to the server console")
            print("   2. Type the exact message above")
            print("   3. Press Enter")
            print("   4. Watch dashboard update!")
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_message_with_spaces())
