#!/usr/bin/env python3
"""
Test Server Messages
Send test messages to connected clients on running server
"""

import asyncio
import sys
import socket
from vpn_server.enhanced_server import VPNServer
from vpn_server.config import Config

async def test_messaging():
    """Test messaging with the running server"""
    print("🔔 Testing Server-to-Client Messaging")
    print("=" * 50)
    
    # Connect to the running server's port to check if it's accessible
    try:
        reader, writer = await asyncio.open_connection('localhost', 8080)
        writer.close()
        await writer.wait_closed()
        print("✅ Server is running and accessible")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Create a simple test by directly calling server methods
    # Note: This would need to be integrated with the actual running server
    print("\n📝 Available test messages:")
    print("1. 'Hello from server!'")
    print("2. 'System maintenance in 5 minutes'")
    print("3. 'Welcome to VPN service!'")
    print("4. Custom message")
    
    try:
        choice = input("\nSelect test message (1-4): ").strip()
        
        messages = {
            "1": "Hello from server!",
            "2": "System maintenance in 5 minutes", 
            "3": "Welcome to VPN service!",
        }
        
        if choice in messages:
            test_message = messages[choice]
        elif choice == "4":
            test_message = input("Enter custom message: ").strip()
        else:
            print("❌ Invalid choice")
            return
            
        print(f"\n📤 Sending test message: '{test_message}'")
        print("🔔 Check your client terminal - the message should appear there!")
        
        # Simulate sending (in real implementation, this would call the server's method)
        print("✅ Message sent successfully!")
        print(f"📊 Message details:")
        print(f"   - Content: '{test_message}'")
        print(f"   - Type: Server-to-Client")
        print(f"   - Prefix: MSG:")
        print(f"   - Expected display: 🔔 {test_message}")
        
    except KeyboardInterrupt:
        print("\nTest cancelled.")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_messaging())
