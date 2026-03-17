"""
VPN Server Implementation
Handles multiple client connections and traffic forwarding
"""

import asyncio
import logging
from typing import Dict, Optional
from .handler import ClientHandler
from .auth import Authenticator

logger = logging.getLogger('VPNServer')


class VPNServer:
    """Main VPN Server class"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8080, auth_enabled: bool = True):
        self.host = host
        self.port = port
        self.auth_enabled = auth_enabled
        self.server = None
        self.clients: Dict[str, ClientHandler] = {}
        self.authenticator = Authenticator()
        self.running = False
        
        # Traffic statistics
        self.total_bytes_sent = 0
        self.total_bytes_received = 0
        
    async def start(self):
        """Start the VPN server"""
        self.running = True
        
        # Create TCP server
        self.server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port
        )
        
        logger.info(f"VPN Server started on {self.host}:{self.port}")
        
        # Serve forever
        async with self.server:
            await self.server.serve_forever()
    
    async def stop(self):
        """Stop the VPN server"""
        self.running = False
        
        # Disconnect all clients
        for client_id, handler in list(self.clients.items()):
            await handler.disconnect()
        
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        logger.info("VPN Server stopped")
    
    def update_traffic_stats(self, bytes_sent: int = 0, bytes_received: int = 0):
        """Update traffic statistics"""
        self.total_bytes_sent += bytes_sent
        self.total_bytes_received += bytes_received
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connection"""
        client_addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {client_addr}")
        
        # Create client handler
        client_id = str(client_addr)
        handler = ClientHandler(
            reader=reader,
            writer=writer,
            client_id=client_id,
            authenticator=self.authenticator if self.auth_enabled else None,
            server=self
        )
        
        # Store client
        self.clients[client_id] = handler
        
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
            
            logger.info(f"Client {client_id} disconnected")
    
    def get_client(self, client_id: str) -> Optional[ClientHandler]:
        """Get a client handler by ID"""
        return self.clients.get(client_id)
    
    def get_client_count(self) -> int:
        """Get number of connected clients"""
        return len(self.clients)
