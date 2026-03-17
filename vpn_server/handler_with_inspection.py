"""
Enhanced Handler with Data Inspection
Shows exactly what data the server receives
"""

import asyncio
import logging
import struct
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from .crypto import CryptoManager
from .auth import Authenticator

if TYPE_CHECKING:
    from .enhanced_server import VPNServer

logger = logging.getLogger('VPNServer.ClientHandler')


class ClientHandler:
    """Handles a single client connection with enhanced tracking and data inspection"""
    
    def __init__(self, 
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter,
                 client_id: str,
                 authenticator: Optional[Authenticator],
                 server: 'VPNServer',
                 connection_logger=None):
        self.reader = reader
        self.writer = writer
        self.client_id = client_id
        self.authenticator = authenticator
        self.server = server
        self.connection_logger = connection_logger
        self.crypto = None
        self.authenticated = False
        self.client_ip = None
        self.username = None
        self.running = False
        self.connected_since = datetime.now()
        self.bytes_sent = 0
        self.bytes_received = 0
        self.packet_count = 0
        
    async def handle_connection(self):
        """Main connection handler"""
        self.running = True
        
        try:
            # Step 1: Authentication
            if not await self._authenticate():
                logger.warning(f"Authentication failed for {self.client_id}")
                return
            
            # Step 2: Key Exchange
            await self._key_exchange()
            
            # Step 3: Configure tunnel
            await self._configure_tunnel()
            
            logger.info(f"Client {self.client_id} connected successfully")
            
            # Step 4: Handle traffic WITH DATA INSPECTION
            await self._handle_traffic_with_inspection()
            
        except Exception as e:
            logger.error(f"Error in connection handler: {e}")
            raise
        finally:
            self.running = False
    
    async def _authenticate(self) -> bool:
        """Authenticate the client"""
        if not self.authenticator:
            logger.info("Authentication disabled")
            self.authenticated = True
            return True
        
        try:
            # Receive credentials
            cred_length_data = await self.reader.read(4)
            if not cred_length_data:
                return False
            
            cred_length = struct.unpack('!I', cred_length_data)[0]
            credentials_data = await self.reader.read(cred_length)
            
            # Parse credentials
            credentials = credentials_data.decode('utf-8')
            username, password = credentials.split(':', 1)
            
            # Verify credentials
            if await self.authenticator.verify(username, password):
                self.authenticated = True
                self.username = username
                logger.info(f"Client {self.client_id} authenticated as {username}")
                
                # Log successful authentication
                if self.connection_logger:
                    self.connection_logger.log_auth_success(
                        self.client_id, 
                        self.writer.get_extra_info('peername')[0],
                        username
                    )
                
                # Send success
                self.writer.write(struct.pack('!B', 1))
                await self.writer.drain()
                return True
            else:
                # Send failure
                self.writer.write(struct.pack('!B', 0))
                await self.writer.drain()
                
                # Log failed authentication
                if self.connection_logger:
                    self.connection_logger.log_auth_failure(
                        self.client_id,
                        self.writer.get_extra_info('peername')[0],
                        username
                    )
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    async def _key_exchange(self):
        """Perform Diffie-Hellman key exchange"""
        try:
            # Generate keys
            self.crypto = CryptoManager()
            
            # Send our public key
            public_key = self.crypto.get_public_key()
            self.writer.write(struct.pack('!H', len(public_key)))
            self.writer.write(public_key)
            await self.writer.drain()
            
            # Receive client's public key
            key_length_data = await self.reader.read(2)
            key_length = struct.unpack('!H', key_length_data)[0]
            client_public_key = await self.reader.read(key_length)
            
            # Generate shared secret
            self.crypto.generate_shared_secret(client_public_key)
            
            logger.info(f"Key exchange completed for {self.client_id}")
            
        except Exception as e:
            logger.error(f"Key exchange error: {e}")
            raise
    
    async def _configure_tunnel(self):
        """Configure tunnel parameters"""
        try:
            # Receive client tunnel IP
            ip_length_data = await self.reader.read(1)
            ip_length = struct.unpack('!B', ip_length_data)[0]
            ip_data = await self.reader.read(ip_length)
            self.client_ip = ip_data.decode('utf-8')
            
            # Log connection
            if self.connection_logger:
                self.connection_logger.log_connect(
                    self.client_id,
                    self.writer.get_extra_info('peername')[0],
                    self.username,
                    self.client_ip
                )
            
            logger.info(f"Tunnel configured - Client IP: {self.client_ip}")
            
        except Exception as e:
            logger.error(f"Tunnel configuration error: {e}")
            raise
    
    async def _handle_traffic_with_inspection(self):
        """Handle traffic and INSPECT every packet"""
        logger.info("="*80)
        logger.info("DATA INSPECTION MODE ACTIVE")
        logger.info("="*80)
        
        while self.running:
            try:
                # Read packet length
                length_data = await asyncio.wait_for(
                    self.reader.read(4),
                    timeout=60.0
                )
                
                if not length_data:
                    logger.info(f"Client {self.client_id} disconnected")
                    break
                
                packet_length = struct.unpack('!I', length_data)[0]
                
                # Read encrypted packet
                encrypted_packet = await self.reader.read(packet_length)
                
                if not encrypted_packet:
                    break
                
                # Update statistics
                self.bytes_received += len(encrypted_packet)
                if self.server:
                    self.server.update_traffic_stats(bytes_received=len(encrypted_packet))
                
                # Decrypt packet
                original_packet = self.crypto.decrypt(encrypted_packet)
                
                # INCREASED PACKET COUNT
                self.packet_count += 1
                
                # INSPECT THE PACKET
                logger.info("\n" + "="*80)
                logger.info(f"📦 PACKET #{self.packet_count} RECEIVED")
                logger.info("="*80)
                logger.info(f"   Encrypted size: {len(encrypted_packet)} bytes")
                logger.info(f"   Decrypted size: {len(original_packet)} bytes")
                logger.info(f"   Timestamp: {datetime.now().isoformat()}")
                
                # Try to interpret as text
                try:
                    text_data = original_packet.decode('utf-8')
                    logger.info(f"   Type: TEXT/UTF-8")
                    logger.info(f"   Content:")
                    logger.info(f"   ┌─{'─' * 76}─┐")
                    for line in text_data.split('\n'):
                        logger.info(f"   │ {line[:76]:<76} │")
                    logger.info(f"   └─{'─' * 76}─┘")
                except UnicodeDecodeError:
                    # Not text, show as hex
                    logger.info(f"   Type: BINARY")
                    logger.info(f"   Hex dump (first 100 bytes):")
                    hex_lines = [hex(original_packet[i:i+16]).replace('0x', '').zfill(2) 
                                for i in range(min(100, len(original_packet)))]
                    logger.info(f"   {' '.join(hex_lines)}")
                
                # Calculate checksums
                sent_checksum = sum(original_packet) % 256
                logger.info(f"   Checksum: {sent_checksum}")
                logger.info(f"   Byte values: {list(original_packet[:20])}")
                logger.info("="*80)
                
                # Forward packet to internet (in real VPN, this would go to actual internet)
                await self._forward_packet(original_packet)
                
            except asyncio.TimeoutError:
                # Send keepalive
                continue
            except Exception as e:
                logger.error(f"Traffic handling error: {e}")
                break
    
    async def _forward_packet(self, packet: bytes):
        """Forward decrypted packet to internet"""
        try:
            # Parse IP header to get destination
            if len(packet) < 20:
                return
            
            # Get destination IP from IP header
            dest_ip = ".".join(str(b) for b in packet[16:20])
            
            # For testing purposes, we'll just log it
            logger.debug(f"Would forward packet to {dest_ip} (length: {len(packet)})")
            
            # In production, you would:
            # 1. Create raw socket
            # 2. Send packet to destination
            # 3. Handle response
            
        except Exception as e:
            logger.error(f"Packet forwarding error: {e}")
    
    async def send_to_client(self, data: bytes):
        """Send encrypted data to client"""
        try:
            if not self.crypto:
                return
            
            # Encrypt data
            encrypted = self.crypto.encrypt(data)
            
            # Update statistics
            self.bytes_sent += len(encrypted)
            if self.server:
                self.server.update_traffic_stats(bytes_sent=len(encrypted))
            
            # Send length prefix + data
            self.writer.write(struct.pack('!I', len(encrypted)))
            self.writer.write(encrypted)
            await self.writer.drain()
            
        except Exception as e:
            logger.error(f"Error sending to client: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect the client"""
        self.running = False
        
        # Log final statistics for this client
        logger.info("\n" + "="*80)
        logger.info(f"📊 CLIENT {self.client_id} DISCONNECTED")
        logger.info("="*80)
        logger.info(f"   Username: {self.username}")
        logger.info(f"   Total packets received: {self.packet_count}")
        logger.info(f"   Total bytes received: {self.bytes_received:,}")
        logger.info(f"   Total bytes sent: {self.bytes_sent:,}")
        logger.info(f"   Connection duration: {datetime.now() - self.connected_since}")
        logger.info("="*80)
        
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except:
            pass
        
        logger.info(f"Client {self.client_id} disconnected")
