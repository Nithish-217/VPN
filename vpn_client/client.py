"""
VPN Client Implementation
Creates TUN interface, connects to server, handles encrypted tunnel
"""

import asyncio
import logging
import struct
from typing import Optional
from .tun_interface import TUNInterface
from .crypto import CryptoManager
from .auth import Authenticator
from .killswitch import KillSwitch, DNSLeakProtection

logger = logging.getLogger('VPNClient')


class VPNClient:
    """Main VPN Client class"""
    
    def __init__(self, 
                 server_host: str,
                 server_port: int,
                 username: str,
                 password: str,
                 tun_interface: str = "tun0",
                 enable_killswitch: bool = True,
                 enable_dns_protection: bool = True):
        self.server_host = server_host
        self.server_port = server_port
        self.username = username
        self.password = password
        self.tun_interface_name = tun_interface
        self.enable_killswitch = enable_killswitch
        self.enable_dns_protection = enable_dns_protection
        
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.tun: Optional[TUNInterface] = None
        self.crypto: Optional[CryptoManager] = None
        self.killswitch: Optional[KillSwitch] = None
        self.dns_protection: Optional[DNSLeakProtection] = None
        self.running = False
        self.connected = False
    
    async def connect(self):
        """Connect to VPN server and start tunnel"""
        try:
            # Step 1: Connect to server
            logger.info(f"Connecting to {self.server_host}:{self.server_port}")
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.server_host, self.server_port),
                timeout=30.0
            )
            logger.info("Connected to server")
            
            # Step 2: Authenticate
            if not await self._authenticate():
                raise Exception("Authentication failed")
            logger.info("Authentication successful")
            
            # Step 3: Key exchange
            await self._key_exchange()
            logger.info("Key exchange completed")
            
            # Step 4: Create TUN interface
            self.tun = TUNInterface(self.tun_interface_name)
            await self.tun.create()
            logger.info(f"TUN interface {self.tun_interface_name} created")
            
            # Step 5: Enable kill switch and DNS protection
            if self.enable_killswitch:
                self.killswitch = KillSwitch()
                self.killswitch.enable(self.tun_interface_name)
            
            if self.enable_dns_protection:
                self.dns_protection = DNSLeakProtection()
                self.dns_protection.enable()
            
            # Step 6: Configure tunnel
            await self._configure_tunnel()
            
            # Mark as connected
            self.connected = True
            self.running = True
            
            # Step 6: Start traffic handling
            await self._handle_traffic()
            
        except Exception as e:
            logger.error(f"Connection error: {e}")
            await self.disconnect()
            raise
    
    async def disconnect(self):
        """Disconnect from VPN server and cleanup"""
        self.running = False
        self.connected = False
        
        # Disable kill switch and DNS protection
        if self.killswitch:
            self.killswitch.disable()
        
        if self.dns_protection:
            self.dns_protection.disable()
        
        # Close TUN interface
        if self.tun:
            await self.tun.close()
        
        # Close connection
        if self.writer:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except:
                pass
        
        logger.info("Disconnected from VPN server")
    
    async def _authenticate(self) -> bool:
        """Authenticate with the server"""
        try:
            # Send credentials
            credentials = f"{self.username}:{self.password}"
            credentials_bytes = credentials.encode('utf-8')
            
            # Send length + credentials
            self.writer.write(struct.pack('!I', len(credentials_bytes)))
            self.writer.write(credentials_bytes)
            await self.writer.drain()
            
            # Wait for response
            response = await self.reader.read(1)
            
            if response and response[0] == 1:
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    async def _key_exchange(self):
        """Perform Diffie-Hellman key exchange"""
        try:
            # Initialize crypto
            self.crypto = CryptoManager()
            
            # Send our public key
            public_key = self.crypto.get_public_key()
            self.writer.write(struct.pack('!H', len(public_key)))
            self.writer.write(public_key)
            await self.writer.drain()
            
            # Receive server's public key
            key_length_data = await self.reader.read(2)
            key_length = struct.unpack('!H', key_length_data)[0]
            server_public_key = await self.reader.read(key_length)
            
            # Generate shared secret
            self.crypto.generate_shared_secret(server_public_key)
            
        except Exception as e:
            logger.error(f"Key exchange error: {e}")
            raise
    
    async def _configure_tunnel(self):
        """Send tunnel configuration to server"""
        try:
            # Send client tunnel IP
            client_ip = self.tun.ip_address.encode('utf-8')
            self.writer.write(struct.pack('!B', len(client_ip)))
            self.writer.write(client_ip)
            await self.writer.drain()
            
        except Exception as e:
            logger.error(f"Tunnel configuration error: {e}")
            raise
    
    async def _handle_traffic(self):
        """Handle bidirectional traffic between TUN and server"""
        try:
            # Create tasks for both directions
            read_from_tun_task = asyncio.create_task(self._read_from_tun())
            read_from_server_task = asyncio.create_task(self._read_from_server())
            
            # Wait for either task to complete
            done, pending = await asyncio.wait(
                [read_from_tun_task, read_from_server_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
        except Exception as e:
            logger.error(f"Traffic handling error: {e}")
            raise
    
    async def _read_from_tun(self):
        """Read packets from TUN interface and send to server"""
        while self.running and self.tun:
            try:
                # Read packet from TUN
                packet = await self.tun.read_packet()
                
                if not packet:
                    continue
                
                # Encrypt packet
                encrypted = self.crypto.encrypt(packet)
                
                # Send to server (length prefix + data)
                self.writer.write(struct.pack('!I', len(encrypted)))
                self.writer.write(encrypted)
                await self.writer.drain()
                
            except Exception as e:
                logger.error(f"Error reading from TUN: {e}")
                break
    
    async def _read_from_server(self):
        """Receive packets from server and write to TUN"""
        while self.running:
            try:
                # Check for special message format first
                peek_data = await self.reader.read(4)
                
                if not peek_data:
                    logger.info("Server disconnected")
                    break
                
                # Check if it's a message (MSG: prefix)
                if peek_data.startswith(b'MSG:'):
                    # Read the rest of the message
                    remaining_data = await self.reader.read(1024)  # Max message length
                    full_message = peek_data + remaining_data
                    message_text = full_message[4:].decode('utf-8').strip()
                    logger.info(f"🔔 SERVER MESSAGE: {message_text}")
                    print(f"\n🔔 SERVER MESSAGE: {message_text}")
                    continue
                
                # Regular VPN packet processing
                length_data = peek_data
                packet_length = struct.unpack('!I', length_data)[0]
                
                # Read encrypted packet
                encrypted_packet = await self.reader.read(packet_length)
                
                if not encrypted_packet:
                    break
                
                # Decrypt packet
                packet = self.crypto.decrypt(encrypted_packet)
                
                # Write to TUN interface
                if self.tun:
                    await self.tun.write_packet(packet)
                
            except Exception as e:
                logger.error(f"Error reading from server: {e}")
                break
