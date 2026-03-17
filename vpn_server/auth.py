"""
Authentication Module
Handles user credential verification
"""

import logging
from typing import Optional, Dict

logger = logging.getLogger('VPNServer.Authenticator')


class Authenticator:
    """Handles authentication for VPN clients"""
    
    def __init__(self):
        # Import locally to avoid circular dependency
        from vpn_server.config import Config
        self.credentials = Config.VALID_CREDENTIALS
    
    async def verify(self, username: str, password: str) -> bool:
        """
        Verify username and password
        
        Args:
            username: Client username
            password: Client password
            
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # Check if user exists
            if username not in self.credentials:
                logger.warning(f"Unknown user: {username}")
                return False
            
            # Verify password
            stored_password = self.credentials[username]
            
            if password == stored_password:
                logger.info(f"User {username} authenticated successfully")
                return True
            else:
                logger.warning(f"Invalid password for user {username}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    def add_user(self, username: str, password: str):
        """Add a new user (for runtime management)"""
        self.credentials[username] = password
        logger.info(f"User {username} added")
    
    def remove_user(self, username: str):
        """Remove a user"""
        if username in self.credentials:
            del self.credentials[username]
            logger.info(f"User {username} removed")
