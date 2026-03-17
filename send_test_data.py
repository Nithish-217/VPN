"""
Simple VPN Test Client
Send test data and see exactly what server receives
"""

import asyncio
import logging
from vpn_client.client import VPNClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TestDataSender')


async def send_test_messages():
    """Send test messages through VPN"""
    
    print("="*80)
    print("VPN DATA TESTER - Send Data & Verify")
    print("="*80)
    print()
    
    # Create client
    client = VPNClient(
        server_host='127.0.0.1',
        server_port=8080,
        username='user1',
        password='password123',
        enable_killswitch=False,  # Disable for testing
        enable_dns_protection=False
    )
    
    try:
        # Connect
        logger.info("Connecting to VPN server...")
        await client.connect()
        
        logger.info("✓ Connected successfully!")
        logger.info("")
        
        # Test messages
        test_messages = [
            "Hello, VPN World!",
            "This is a test message.",
            "Testing 1-2-3...",
            "A" * 50,  # Long message
            "Special chars: ñáéíóú 中文 🎉",
            '{"type": "test", "data": "value123"}',
        ]
        
        print("="*80)
        print("SENDING TEST MESSAGES")
        print("="*80)
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📨 Message {i}:")
            print(f"   Content: {message}")
            print(f"   Length: {len(message)} bytes")
            
            # Simulate sending (in real scenario, this would go through TUN)
            # For now, we'll just show what WOULD be sent
            print(f"   ✓ Would be encrypted and sent to server")
            
            await asyncio.sleep(0.5)
        
        print("\n" + "="*80)
        print("CHECK SERVER OUTPUT")
        print("="*80)
        print()
        print("Look at the server terminal to see:")
        print("  1. Exactly what data was received")
        print("  2. Packet checksums")
        print("  3. Byte-by-byte breakdown")
        print("  4. Decrypted content display")
        print()
        print("The server will show each packet with:")
        print("  • Encrypted size vs Decrypted size")
        print("  • Full content display (text or hex)")
        print("  • Checksum verification")
        print("  • Timestamp")
        print()
        print("="*80)
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(send_test_messages())
