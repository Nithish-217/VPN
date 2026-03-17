"""
Enhanced VPN Server with Advanced Features
- Multi-client support
- Comprehensive logging
- Traffic monitoring
- DNS leak protection
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Optional
from .handler import ClientHandler
from .auth import Authenticator
from .logger import ConnectionLogger

logger = logging.getLogger('VPNServer')


class VPNServer:
    """Enhanced VPN Server with advanced features"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080, auth_enabled: bool = True):
        self.host = host
        self.port = port
        self.auth_enabled = auth_enabled
        self.server = None
        self.clients: Dict[str, ClientHandler] = {}
        self.authenticator = Authenticator()
        self.connection_logger = ConnectionLogger()
        self.running = False
        
        # Traffic statistics
        self.total_bytes_sent = 0
        self.total_bytes_received = 0
        self.peak_connections = 0
        self.messages_sent = 0  # Track messages separately
        
    async def start(self):
        """Start the VPN server"""
        self.running = True
        
        # Create TCP server
        self.server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port
        )
        
        logger.info(f"Enhanced VPN Server started on {self.host}:{self.port}")
        logger.info(f"Max clients: Unlimited (concurrent)")
        
        # Serve forever
        async with self.server:
            await self.server.serve_forever()
    
    async def stop(self):
        """Stop the VPN server gracefully"""
        self.running = False
        
        logger.info(f"Stopping server... Disconnecting {len(self.clients)} clients")
        
        # Disconnect all clients
        for client_id, handler in list(self.clients.items()):
            await handler.disconnect()
        
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        # Log final statistics
        self._log_final_statistics()
        
        logger.info("VPN Server stopped")
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connection"""
        client_addr = writer.get_extra_info('peername')
        client_ip = client_addr[0] if client_addr else "unknown"
        
        logger.info(f"New connection from {client_ip}")
        
        # Check if we're at capacity (optional limit)
        if len(self.clients) >= 100:  # Hard limit for safety
            logger.warning(f"Maximum clients reached. Rejecting {client_ip}")
            writer.close()
            return
        
        # Create client handler with enhanced logging
        client_id = str(client_addr)
        handler = ClientHandler(
            reader=reader,
            writer=writer,
            client_id=client_id,
            authenticator=self.authenticator if self.auth_enabled else None,
            server=self,
            connection_logger=self.connection_logger
        )
        
        # Store client
        self.clients[client_id] = handler
        
        # Update peak connections
        if len(self.clients) > self.peak_connections:
            self.peak_connections = len(self.clients)
        
        try:
            # Start handling client
            await handler.handle_connection()
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
        finally:
            # Remove client
            if client_id in self.clients:
                del self.clients[client_id]
            
            # Close writer
            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass
            
            # Log disconnection
            self.connection_logger.log_disconnect(client_id, client_ip)
            
            logger.info(f"Client {client_id} disconnected. Active clients: {len(self.clients)}")
    
    def update_traffic_stats(self, bytes_sent: int = 0, bytes_received: int = 0):
        """Update global traffic statistics"""
        self.total_bytes_sent += bytes_sent
        self.total_bytes_received += bytes_received
    
    def get_statistics(self) -> dict:
        """Get current server statistics"""
        return {
            'active_clients': len(self.clients),
            'peak_connections': self.peak_connections,
            'total_bytes_sent': self.total_bytes_sent,
            'total_bytes_received': self.total_bytes_received,
            'messages_sent': self.messages_sent,  # Add message count
            'uptime': str(datetime.now()),
            'clients': [
                {
                    'client_id': cid,
                    'ip': handler.client_ip,
                    'username': handler.username,
                    'bytes_sent': handler.bytes_sent,
                    'bytes_received': handler.bytes_received,
                    'connected_since': handler.connected_since.isoformat() if hasattr(handler.connected_since, 'isoformat') else str(handler.connected_since)
                }
                for cid, handler in self.clients.items()
            ]
        }
    
    def _log_final_statistics(self):
        """Log final statistics before shutdown"""
        logger.info("=" * 60)
        logger.info("FINAL SERVER STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Peak concurrent connections: {self.peak_connections}")
        logger.info(f"Total data sent: {self._format_bytes(self.total_bytes_sent)}")
        logger.info(f"Total data received: {self._format_bytes(self.total_bytes_received)}")
        logger.info("=" * 60)
    
    def _format_bytes(self, bytes_count: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.2f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.2f} PB"
    
    def get_client(self, client_id: str) -> Optional[ClientHandler]:
        """Get a client handler by ID"""
        return self.clients.get(client_id)
    
    def get_client_count(self) -> int:
        """Get number of connected clients"""
        return len(self.clients)
    
    def disconnect_client(self, client_id: str):
        """Forcefully disconnect a specific client"""
        if client_id in self.clients:
            asyncio.create_task(self.clients[client_id].disconnect())
            logger.info(f"Forcefully disconnected client {client_id}")
    
    async def send_message_to_client(self, client_id: str, message: str) -> bool:
        """Send a message to a specific client"""
        if client_id not in self.clients:
            logger.warning(f"Client {client_id} not found")
            return False
        
        try:
            handler = self.clients[client_id]
            # Send message with special prefix to distinguish from VPN data
            message_data = f"MSG:{message}".encode('utf-8')
            message_length = len(message_data)
            
            handler.writer.write(message_data)
            await handler.writer.drain()
            
            # Update statistics
            self.total_bytes_sent += message_length
            self.messages_sent += 1
            handler.bytes_sent += message_length
            
            logger.info(f"Message sent to client {client_id}: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message to client {client_id}: {e}")
            return False
    
    async def broadcast_message(self, message: str) -> int:
        """Send a message to all connected clients"""
        success_count = 0
        for client_id in list(self.clients.keys()):
            if await self.send_message_to_client(client_id, message):
                success_count += 1
        logger.info(f"Broadcast message sent to {success_count}/{len(self.clients)} clients")
        return success_count
