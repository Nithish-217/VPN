"""
Authentication Module for Client
Handles credential management
"""

import logging

logger = logging.getLogger('VPNClient.Authenticator')


class Authenticator:
    """Handles client authentication"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    def get_credentials(self) -> tuple:
        """Get credentials as tuple"""
        return (self.username, self.password)
    
    def validate_credentials(self) -> bool:
        """Validate credentials format"""
        if not self.username or len(self.username) < 3:
            logger.error("Invalid username")
            return False
        
        if not self.password or len(self.password) < 6:
            logger.error("Invalid password")
            return False
        
        return True
