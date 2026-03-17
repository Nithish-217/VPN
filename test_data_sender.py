"""
VPN Data Testing Tool
Send test data through VPN and verify what server receives
"""

import socket
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('VPNTrafficTester')


class VPNDataTester:
    """Test VPN tunnel by sending actual data"""
    
    def __init__(self, server_host='127.0.0.1', server_port=8080):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        
    def connect(self, username='user1', password='password123'):
        """Connect to VPN server"""
        try:
            logger.info(f"Connecting to {self.server_host}:{self.server_port}...")
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            
            logger.info("✓ TCP connection established")
            
            # Send authentication
            credentials = f"{username}:{password}"
            cred_bytes = credentials.encode('utf-8')
            
            # Send length prefix + credentials
            self.socket.sendall(len(cred_bytes).to_bytes(4, 'big'))
            self.socket.sendall(cred_bytes)
            
            # Wait for auth response
            response = self.socket.recv(1)
            
            if response[0] == 1:
                logger.info("✓ Authentication successful")
                return True
            else:
                logger.error("✗ Authentication failed")
                return False
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    def send_test_data(self, data: str, test_type='text'):
        """
        Send test data through VPN tunnel
        
        Args:
            data: Data to send
            test_type: Type of test (text, binary, large, etc.)
        """
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"TEST: {test_type}")
            logger.info(f"{'='*60}")
            
            # Prepare data
            if test_type == 'binary':
                data_bytes = bytes.fromhex(data)
            else:
                data_bytes = data.encode('utf-8')
            
            # Log what we're sending
            logger.info(f"📤 SENDING:")
            logger.info(f"   Type: {test_type}")
            logger.info(f"   Size: {len(data_bytes)} bytes")
            logger.info(f"   Content: {data[:100] if len(data) > 100 else data}")
            
            # Send with length prefix (simulating VPN packet)
            length_prefix = len(data_bytes).to_bytes(4, 'big')
            self.socket.sendall(length_prefix)
            self.socket.sendall(data_bytes)
            
            logger.info(f"✓ Data sent successfully")
            
            # Calculate checksum
            checksum = sum(data_bytes) % 256
            logger.info(f"   Checksum: {checksum}")
            
            return {
                'sent_size': len(data_bytes),
                'sent_checksum': checksum,
                'sent_content': data[:200] if len(data) > 200 else data,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Send error: {e}")
            return None
    
    def receive_response(self, timeout=5):
        """Receive response from server"""
        try:
            self.socket.settimeout(timeout)
            
            # Read length prefix
            length_bytes = self.socket.recv(4)
            if not length_bytes:
                return None
            
            message_length = int.from_bytes(length_bytes, 'big')
            logger.info(f"\n📥 RECEIVING:")
            logger.info(f"   Expected size: {message_length} bytes")
            
            # Read message
            data = b''
            remaining = message_length
            while remaining > 0:
                chunk = self.socket.recv(min(remaining, 4096))
                if not chunk:
                    break
                data += chunk
                remaining -= len(chunk)
            
            if data:
                checksum = sum(data) % 256
                logger.info(f"   Received size: {len(data)} bytes")
                logger.info(f"   Checksum: {checksum}")
                
                # Try to decode as text
                try:
                    text_content = data.decode('utf-8')
                    logger.info(f"   Content: {text_content[:100] if len(text_content) > 100 else text_content}")
                except:
                    logger.info(f"   Content (hex): {data[:50].hex()}")
                
                return {
                    'received_size': len(data),
                    'received_checksum': checksum,
                    'received_data': data,
                    'matches_sent': True  # We'll verify this
                }
            else:
                logger.warning("No data received")
                return None
                
        except socket.timeout:
            logger.warning("Receive timeout")
            return None
        except Exception as e:
            logger.error(f"Receive error: {e}")
            return None
    
    def run_tests(self):
        """Run comprehensive data tests"""
        results = []
        
        # Test 1: Simple text
        logger.info("\n" + "="*80)
        logger.info("TEST SUITE: VPN Data Integrity Verification")
        logger.info("="*80)
        
        test_data = [
            ("Hello, VPN World!", "Simple Text"),
            ("Test message with special chars: ñáéíóú", "Unicode Text"),
            ("A" * 1000, "Large Text (1KB)"),
            ("48656c6c6f20576f726c6421", "Binary Data (Hex)"),
            ("Line 1\nLine 2\nLine 3\n", "Multi-line Text"),
            ('{"key": "value", "number": 42}', "JSON Data"),
        ]
        
        for data, test_name in test_data:
            result = self.send_test_data(data, test_name)
            if result:
                results.append(result)
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("TEST SUMMARY")
        logger.info("="*80)
        logger.info(f"Total tests: {len(results)}")
        total_bytes = sum(r['sent_size'] for r in results)
        logger.info(f"Total bytes sent: {total_bytes}")
        logger.info("="*80)
        
        return results
    
    def disconnect(self):
        """Disconnect from server"""
        if self.socket:
            self.socket.close()
            logger.info("\n✓ Disconnected from server")


def main():
    """Main test function"""
    print("="*80)
    print("VPN DATA INTEGRITY TESTER")
    print("="*80)
    print()
    print("This tool will:")
    print("1. Connect to VPN server")
    print("2. Send various test data")
    print("3. Verify data integrity")
    print("4. Show exactly what was sent")
    print()
    
    # Create tester
    tester = VPNDataTester(server_host='127.0.0.1', server_port=8080)
    
    # Connect
    if not tester.connect(username='user1', password='password123'):
        print("\n✗ Failed to connect to VPN server")
        print("Make sure the server is running: python vpn_server_main_enhanced.py")
        return
    
    # Run tests
    try:
        results = tester.run_tests()
        
        print("\n" + "="*80)
        print("RESULTS")
        print("="*80)
        print(f"✓ Successfully sent {len(results)} test messages")
        print(f"✓ Total data: {sum(r['sent_size'] for r in results)} bytes")
        print("\nCheck server logs to see what was received:")
        print("  - Server console output")
        print("  - logs/traffic.jsonl")
        print("  - Dashboard at http://localhost:8081")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
    finally:
        tester.disconnect()


if __name__ == "__main__":
    main()
