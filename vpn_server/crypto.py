"""
Cryptographic Manager
Handles encryption/decryption using AES-256 and key exchange
"""

import os
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger('VPNServer.CryptoManager')


class CryptoManager:
    """Manages encryption for VPN tunnel"""
    
    def __init__(self):
        # Generate Diffie-Hellman keys for key exchange
        self.private_key = X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        
        # Shared secret (will be set after key exchange)
        self.shared_secret = None
        
        # Encryption settings
        self.key_size = 32  # 256 bits
        self.nonce_size = 16
        
        logger.info("CryptoManager initialized")
    
    def get_public_key(self) -> bytes:
        """Get public key for key exchange in raw bytes format"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
    
    def generate_shared_secret(self, peer_public_key_bytes: bytes):
        """Generate shared secret using Diffie-Hellman"""
        try:
            # Load peer's public key
            peer_public_key = X25519PublicKey.from_public_bytes(
                peer_public_key_bytes
            )
            
            # Perform key exchange
            self.shared_secret = self.private_key.exchange(peer_public_key)
            
            logger.info("Shared secret generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating shared secret: {e}")
            raise
    
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt data using AES-256-CFB
        
        Args:
            plaintext: Data to encrypt
            
        Returns:
            Encrypted data with nonce prepended
        """
        if not self.shared_secret:
            raise ValueError("Shared secret not established")
        
        try:
            # Generate random nonce
            nonce = os.urandom(self.nonce_size)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.shared_secret),
                modes.CFB(nonce),
                backend=default_backend()
            )
            
            # Encrypt
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            
            # Return nonce + ciphertext
            return nonce + ciphertext
            
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data using AES-256-CFB
        
        Args:
            encrypted_data: Encrypted data with nonce prepended
            
        Returns:
            Decrypted plaintext
        """
        if not self.shared_secret:
            raise ValueError("Shared secret not established")
        
        try:
            # Extract nonce and ciphertext
            nonce = encrypted_data[:self.nonce_size]
            ciphertext = encrypted_data[self.nonce_size:]
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.shared_secret),
                modes.CFB(nonce),
                backend=default_backend()
            )
            
            # Decrypt
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            return plaintext
            
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise
