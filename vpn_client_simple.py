"""
Simple VPN Client for Testing (No Kill Switch)
Works on Windows without admin rights
"""

import asyncio
import logging
import sys
from vpn_client.client import VPNClient
from vpn_client.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VPNClient')


async def main():
    """Start the VPN client (without kill switch for testing)"""
    config = Config()
    
    # Create client WITHOUT kill switch for easier Windows testing
    client = VPNClient(
        server_host=config.SERVER_HOST,
        server_port=config.SERVER_PORT,
        username=config.USERNAME,
        password=config.PASSWORD,
        tun_interface=config.TUN_INTERFACE,
        enable_killswitch=False,      # Disabled for testing
        enable_dns_protection=False   # Disabled for testing
    )
    
    logger.info(f"Connecting to VPN Server at {config.SERVER_HOST}:{config.SERVER_PORT}")
    
    try:
        await client.connect()
        
        # Keep running until user interrupts
        logger.info("✓ Connected! Press Ctrl+C to disconnect...")
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Client shutting down...")
        await client.disconnect()
    except Exception as e:
        logger.error(f"Client error: {e}")
        await client.disconnect()
        sys.exit(1)


if __name__ == "__main__":
    # Check if running on Windows
    if sys.platform == 'win32':
        # Windows-specific event loop policy
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
