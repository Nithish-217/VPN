"""
VPN Server - Main Entry Point
Handles client connections, authentication, and traffic forwarding
"""

import asyncio
import logging
from vpn_server.server import VPNServer
from vpn_server.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VPNServer')


async def main():
    """Start the VPN server"""
    config = Config()
    
    server = VPNServer(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        auth_enabled=config.AUTH_ENABLED
    )
    
    logger.info(f"Starting VPN Server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
