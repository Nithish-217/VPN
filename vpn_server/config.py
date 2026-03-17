"""
VPN Server Configuration
"""

class Config:
    """Server configuration settings"""
    
    # Network settings
    SERVER_HOST = "0.0.0.0"  # Listen on all interfaces
    SERVER_PORT = 8080
    
    # Authentication
    AUTH_ENABLED = True
    
    # Valid credentials (in production, use a database)
    VALID_CREDENTIALS = {
        "user1": "password123",
        "admin": "admin123"
    }
    
    # Encryption settings
    ENCRYPTION_METHOD = "AES-256-CFB"
    KEY_SIZE = 32  # 256 bits
    
    # Logging
    LOG_LEVEL = "INFO"
    
    # Connection limits
    MAX_CLIENTS = 10
    
    # Timeout settings
    CONNECTION_TIMEOUT = 30  # seconds
    KEEPALIVE_INTERVAL = 10  # seconds
