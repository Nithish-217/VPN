"""
Setup script for VPN Client
"""

import os
import sys
import platform

def setup_client():
    """Setup VPN Client environment"""
    print("=" * 60)
    print("VPN Client Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher required")
        return False
    
    print(f"✓ Python version: {sys.version}")
    print(f"✓ Platform: {platform.system()}")
    
    # Create necessary directories
    directories = [
        'vpn_client',
        'logs',
        'config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create client configuration
    config_content = """# VPN Client Configuration
SERVER_HOST=192.168.1.50
SERVER_PORT=8080
USERNAME=user1
PASSWORD=password123
TUN_INTERFACE=tun0
TUN_IP=10.8.0.2
SERVER_TUN_IP=10.8.0.1
NETMASK=255.255.255.0
ROUTE_ALL_TRAFFIC=True
DNS_SERVER=8.8.8.8
"""
    
    with open('config/client.conf', 'w') as f:
        f.write(config_content)
    print("✓ Created client configuration")
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nIMPORTANT: Edit config/client.conf to set your VPN server address")
    print("\nTo start the client:")
    
    if platform.system() == "Windows":
        print("  Run as Administrator:")
        print("  python vpn_client_main.py")
    else:
        print("  Run with sudo:")
        print("  sudo python vpn_client_main.py")
    
    print("\nNote: TUN interface creation requires administrator privileges")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    setup_client()
