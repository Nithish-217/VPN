"""
VPN Client Configuration
"""

class Config:
    """Client configuration settings"""
    
    # Server connection
    SERVER_HOST = "127.0.0.1"  # Local server for testing
    SERVER_PORT = 8080
    
    # Authentication credentials
    USERNAME = "user1"
    PASSWORD = "password123"
    
    # TUN interface settings
    TUN_INTERFACE = "tun0"
    TUN_IP = "10.8.0.2"  # Client IP in VPN network
    SERVER_TUN_IP = "10.8.0.1"  # Server IP in VPN network
    NETMASK = "255.255.255.0"
    
    # Encryption settings
    ENCRYPTION_METHOD = "AES-256-CFB"
    KEY_SIZE = 32  # 256 bits
    
    # Routing
    ROUTE_ALL_TRAFFIC = True
    
    # DNS settings
    DNS_SERVER = "8.8.8.8"
    
    # Logging
    LOG_LEVEL = "INFO"
    
    # Connection settings
    RECONNECT_ATTEMPTS = 3
    CONNECTION_TIMEOUT = 30  # seconds
