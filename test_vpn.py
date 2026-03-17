"""
Test script to verify VPN components
"""

import sys
import asyncio


def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import cryptography
        print("✓ cryptography module")
    except ImportError as e:
        print(f"✗ cryptography module: {e}")
        return False
    
    try:
        import asyncio
        print("✓ asyncio module")
    except ImportError as e:
        print(f"✗ asyncio module: {e}")
        return False
    
    return True


async def test_crypto():
    """Test encryption/decryption"""
    print("\nTesting crypto operations...")
    
    try:
        from vpn_client.crypto import CryptoManager
        
        # Create two crypto instances (client and server)
        client_crypto = CryptoManager()
        server_crypto = CryptoManager()
        
        # Exchange keys
        client_public = client_crypto.get_public_key()
        server_public = server_crypto.get_public_key()
        
        # Generate shared secrets
        client_crypto.generate_shared_secret(server_public)
        server_crypto.generate_shared_secret(client_public)
        
        # Test encryption/decryption
        test_message = b"Hello, VPN World!"
        
        # Encrypt with client
        encrypted = client_crypto.encrypt(test_message)
        print(f"✓ Encrypted message (length: {len(encrypted)})")
        
        # Decrypt with server
        decrypted = server_crypto.decrypt(encrypted)
        print(f"✓ Decrypted message: {decrypted.decode()}")
        
        if decrypted == test_message:
            print("✓ Encryption/Decryption test PASSED")
            return True
        else:
            print("✗ Encryption/Decryption test FAILED")
            return False
            
    except Exception as e:
        print(f"✗ Crypto test failed: {e}")
        return False


async def test_auth():
    """Test authentication"""
    print("\nTesting authentication...")
    
    try:
        from vpn_server.auth import Authenticator
        
        auth = Authenticator()
        
        # Test valid credentials
        result = await auth.verify("user1", "password123")
        if result:
            print("✓ Valid credentials accepted")
        else:
            print("✗ Valid credentials rejected")
            return False
        
        # Test invalid credentials
        result = await auth.verify("user1", "wrongpassword")
        if not result:
            print("✓ Invalid credentials rejected")
        else:
            print("✗ Invalid credentials accepted")
            return False
        
        print("✓ Authentication test PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Authentication test failed: {e}")
        return False


def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from vpn_server.config import Config as ServerConfig
        from vpn_client.config import Config as ClientConfig
        
        print(f"✓ Server config loaded (port: {ServerConfig.SERVER_PORT})")
        print(f"✓ Client config loaded (server: {ClientConfig.SERVER_HOST})")
        
        print("✓ Configuration test PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("VPN System Tests")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("\n✗ Import tests failed. Install dependencies:")
        print("  pip install -r requirements.txt")
        return
    
    # Test configuration
    if not test_config():
        print("\n✗ Configuration test failed")
        return
    
    # Test crypto
    crypto_passed = await test_crypto()
    
    # Test auth
    auth_passed = await test_auth()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Crypto: {'PASSED ✓' if crypto_passed else 'FAILED ✗'}")
    print(f"Auth: {'PASSED ✓' if auth_passed else 'FAILED ✗'}")
    print("=" * 60)
    
    if crypto_passed and auth_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    # Handle Windows event loop
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
