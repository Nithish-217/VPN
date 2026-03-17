"""
TUN Interface Manager
Creates and manages virtual network interface
"""

import os
import sys
import logging
import subprocess
from typing import Optional

logger = logging.getLogger('VPNClient.TUNInterface')


class TUNInterface:
    """Manages TUN/TAP virtual network interface"""
    
    def __init__(self, name: str = "tun0"):
        self.name = name
        self.ip_address = "10.8.0.2"
        self.netmask = "255.255.255.0"
        self.mtu = 1500
        self.fd: Optional[int] = None
        self.file = None
    
    async def create(self):
        """Create and configure TUN interface"""
        try:
            if sys.platform.startswith('linux'):
                await self._create_linux()
            elif sys.platform == 'darwin':
                await self._create_macos()
            elif sys.platform == 'win32':
                await self._create_windows()
            else:
                raise NotImplementedError(f"Platform {sys.platform} not supported")
            
            logger.info(f"TUN interface {self.name} created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create TUN interface: {e}")
            raise
    
    async def _create_linux(self):
        """Create TUN interface on Linux"""
        try:
            # Open TUN device
            TUNSETIFF = 0x400454ca
            IFF_TUN = 0x0001
            IFF_NO_PI = 0x1000
            
            import fcntl
            import struct
            
            self.file = open('/dev/net/tun', 'r+b')
            self.fd = self.file.fileno()
            
            # Prepare ifreq structure
            ifreq = struct.pack('16sH', self.name.encode(), IFF_TUN | IFF_NO_PI)
            
            # Create interface
            fcntl.ioctl(self.file, TUNSETIFF, ifreq)
            
            # Configure interface
            await self._configure_linux()
            
        except Exception as e:
            logger.error(f"Linux TUN creation error: {e}")
            raise
    
    async def _configure_linux(self):
        """Configure TUN interface on Linux"""
        try:
            # Bring up interface
            subprocess.run(['ip', 'link', 'set', 'dev', self.name, 'up'], check=True)
            
            # Set IP address
            subprocess.run([
                'ip', 'addr', 'add',
                f'{self.ip_address}/{self.netmask}',
                'dev', self.name
            ], check=True)
            
            # Set MTU
            subprocess.run([
                'ip', 'link', 'set', self.name, 'mtu', str(self.mtu)
            ], check=True)
            
            logger.info(f"Linux TUN configured: {self.name} - {self.ip_address}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Configuration error: {e}")
            raise
    
    async def _create_macos(self):
        """Create TUN interface on macOS"""
        try:
            # macOS uses utun devices
            utun_name = f"utun0"
            
            # Open TUN device
            self.file = open(f'/dev/{utun_name}', 'r+b')
            self.fd = self.file.fileno()
            
            # Configure interface
            subprocess.run(['ifconfig', utun_name, self.ip_address, self.netmask, 'up'], check=True)
            
            self.name = utun_name
            logger.info(f"macOS TUN created: {self.name}")
            
        except Exception as e:
            logger.error(f"macOS TUN creation error: {e}")
            raise
    
    async def _create_windows(self):
        """Create TUN interface on Windows"""
        try:
            # Windows requires Wintun driver
            # This is a simplified implementation
            logger.warning("Windows TUN implementation requires Wintun driver")
            logger.info("Using simulated TUN for demonstration")
            
            # In production, you would:
            # 1. Load Wintun DLL
            # 2. Create adapter using wintun.CreateAdapter()
            # 3. Configure IP using netsh or PowerShell
            
            # For now, we'll simulate it
            self.fd = -1  # Simulated file descriptor
            
            logger.info(f"Windows TUN simulated: {self.name}")
            
        except Exception as e:
            logger.error(f"Windows TUN creation error: {e}")
            raise
    
    async def read_packet(self) -> Optional[bytes]:
        """Read packet from TUN interface"""
        if not self.file:
            return None
        
        try:
            if sys.platform.startswith('linux'):
                # Read packet length first (4 bytes)
                packet_len_bytes = self.file.read(4)
                if not packet_len_bytes:
                    return None
                
                packet_len = int.from_bytes(packet_len_bytes, byteorder='big')
                
                # Read packet
                packet = self.file.read(packet_len)
                return packet
            
            elif sys.platform == 'darwin':
                # macOS reads directly
                packet = self.file.read(self.mtu)
                return packet
            
            elif sys.platform == 'win32':
                # Windows simulation
                await asyncio.sleep(0.1)  # Simulate waiting for packet
                return None
            
        except Exception as e:
            logger.error(f"Error reading packet: {e}")
            return None
    
    async def write_packet(self, packet: bytes):
        """Write packet to TUN interface"""
        if not self.file:
            return
        
        try:
            if sys.platform.startswith('linux'):
                # Write packet length first
                self.file.write(len(packet).to_bytes(4, byteorder='big'))
                self.file.write(packet)
                self.file.flush()
            
            elif sys.platform == 'darwin':
                self.file.write(packet)
                self.file.flush()
            
            elif sys.platform == 'win32':
                # Windows simulation
                pass
            
        except Exception as e:
            logger.error(f"Error writing packet: {e}")
    
    async def close(self):
        """Close TUN interface"""
        try:
            if self.file:
                self.file.close()
                self.file = None
            
            if sys.platform.startswith('linux'):
                # Remove interface
                try:
                    subprocess.run(['ip', 'link', 'delete', self.name], check=False)
                except:
                    pass
            
            logger.info(f"TUN interface {self.name} closed")
            
        except Exception as e:
            logger.error(f"Error closing TUN: {e}")
