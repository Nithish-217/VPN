"""
Simple Data Sender for Testing VPN
Sends test messages through the encrypted VPN tunnel
"""

import asyncio
import logging
import struct
from vpn_client.crypto import CryptoManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DataSender')


async def send_test_data():
    """Connect to VPN server and send test data"""
    
    # Connect to VPN server
    logger.info("Connecting to VPN server at 127.0.0.1:8080...")
    reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
    logger.info("✓ TCP connection established")
    
    try:
        # Step 1: Authenticate (using correct protocol: length-prefixed colon-separated credentials)
        credentials = "user1:password123"
        credentials_bytes = credentials.encode('utf-8')
        
        writer.write(struct.pack('!I', len(credentials_bytes)))
        writer.write(credentials_bytes)
        await writer.drain()
        
        response = await reader.read(1)
        if response and response[0] == 1:
            logger.info("✓ Authentication successful")
        else:
            logger.error(f"✗ Authentication failed - Response: {response}")
            return
        
        # Step 2: Key exchange
        from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
        private_key = X25519PrivateKey.generate()
        public_key = private_key.public_key().public_bytes_raw()
        
        # Receive server's public key FIRST (server sends it after authentication)
        key_length_data = await reader.read(2)
        key_length = struct.unpack('!H', key_length_data)[0]
        server_public_key = await reader.read(key_length)
        logger.info(f"Received server public key: {len(server_public_key)} bytes")
        
        # Send client's public key with length prefix
        writer.write(struct.pack('!H', len(public_key)))
        writer.write(public_key)
        await writer.drain()
        
        # Create crypto manager
        crypto = CryptoManager()
        
        # Generate shared secret from server's public key
        crypto.generate_shared_secret(server_public_key)
        logger.info("✓ Encryption established")
        
        # Step 3: Configure tunnel (send client IP)
        client_ip = "10.0.0.2"  # Simulated client IP
        writer.write(struct.pack('!B', len(client_ip)))
        writer.write(client_ip.encode('utf-8'))
        await writer.drain()
        logger.info(f"✓ Tunnel configured with IP: {client_ip}")
        
        # Small delay to let server process tunnel config
        await asyncio.sleep(0.1)
        
        # Step 4: Send test messages as simulated IP packets
        test_messages = [
            b"Hello VPN Server! This is test message #1",
        ]
        
        for i, message in enumerate(test_messages, 1):
            logger.info(f"\n📤 Sending message {i}:")
            logger.info(f"   Content: {message.decode()}")
            logger.info(f"   Size: {len(message)} bytes")
            
            # Create a simple fake IP-like packet (prepend dummy IP header)
            # Real IP header is 20 bytes minimum
            fake_ip_header = bytes([
                0x45,  # Version (4) + IHL (5)
                0x00,  # DSCP + ECN
                0x00, len(message) + 20,  # Total length (header + data)
                0x00, 0x00,  # Identification
                0x00, 0x00,  # Flags + Fragment offset
                0x40,  # TTL (64)
                0x06,  # Protocol (TCP)
                0x00, 0x00,  # Header checksum (placeholder)
                127, 0, 0, 1,  # Source IP
                127, 0, 0, 1,  # Destination IP
            ])
            
            # Combine header + payload
            packet = fake_ip_header + message
            logger.info(f"   Packet size with header: {len(packet)} bytes")
            
            # Encrypt the packet
            encrypted = crypto.encrypt(packet)
            logger.info(f"   Encrypted size: {len(encrypted)} bytes")
            
            # Send with length prefix
            length = len(encrypted)
            writer.write(struct.pack('!I', length))
            writer.write(encrypted)
            await writer.drain()
            
            logger.info(f"   ✓ Sent {len(encrypted)} encrypted bytes")
            
            # Wait longer between messages to let server process
            await asyncio.sleep(2)
        
        logger.info("\n✅ All test messages sent!")
        logger.info("Check the server terminal to see what it received")
        
        # Keep connection open briefly to see server response
        await asyncio.sleep(2)
        
    except Exception as e:
        logger.error(f"\n❌ ERROR during transmission: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        writer.close()
        await writer.wait_closed()
        logger.info("Disconnected from VPN server")


if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(send_test_data())
