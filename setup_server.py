"""
Setup script for VPN Server
"""

import os
import sys

def setup_server():
    """Setup VPN Server environment"""
    print("=" * 60)
    print("VPN Server Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher required")
        return False
    
    print(f"✓ Python version: {sys.version}")
    
    # Create necessary directories
    directories = [
        'vpn_server',
        'vpn_client',
        'logs',
        'config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create server configuration
    config_content = """# VPN Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
AUTH_ENABLED=True
MAX_CLIENTS=10
LOG_LEVEL=INFO
"""
    
    with open('config/server.conf', 'w') as f:
        f.write(config_content)
    print("✓ Created server configuration")
    
    # Create credentials file
    credentials_content = """# User Credentials
# Format: username:password
user1:password123
admin:admin123
testuser:test123
"""
    
    with open('config/credentials.txt', 'w') as f:
        f.write(credentials_content)
    print("✓ Created credentials file")
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nTo start the server:")
    print("  python vpn_server_main.py")
    print("\nConfigure firewall to allow incoming connections on port 8080")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    setup_server()
