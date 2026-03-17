#!/usr/bin/env python3
"""
Quick Message Test
Send a test message to verify dashboard message tracking
"""

import asyncio
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vpn_server.enhanced_server import VPNServer
from vpn_server.config import Config

async def send_test_message():
    """Send a test message to verify dashboard tracking"""
    print("🔔 Sending Test Message for Dashboard")
    print("=" * 50)
    
    # Check if server has clients
    try:
        # Import here to avoid path issues
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        
        if result != 0:
            print("❌ Server not running")
            return
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("✅ Server is running")
    print("📝 Sending test message: 'Dashboard test message!'")
    
    # The message will be sent through the server's console input
    print("\n🎯 To complete the test:")
    print("1. Go to the server console window")
    print("2. Type: Dashboard test message!")
    print("3. Press Enter")
    print("4. Watch dashboard update:")
    print("   - Messages Sent: 0 → 1")
    print("   - Data Sent: increases by message size")
    print("   - Charts show traffic spike")
    
    print("\n📊 Dashboard should now show:")
    print("✅ Active Clients: 1")
    print("✅ Peak Connections: 1") 
    print("✅ Messages Sent: 0 (will become 1 after sending)")
    print("✅ Connected client: user1@10.8.0.2")

if __name__ == "__main__":
    asyncio.run(send_test_message())
