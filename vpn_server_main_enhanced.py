"""
Enhanced VPN Server with Monitoring Dashboard
"""

import asyncio
import logging
import threading
from vpn_server.enhanced_server import VPNServer
from vpn_server.simple_dashboard import SimpleDashboard
from vpn_server.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VPNServer')

# Reduce aiohttp access log noise
logging.getLogger('aiohttp.access').setLevel(logging.WARNING)


def message_input_loop(server):
    """Run input loop in separate thread for sending messages"""
    while True:
        try:
            # Use a cleaner prompt that doesn't get mixed with logs
            import sys
            print("\n" + "="*60)
            print("📝 MESSAGE INPUT MODE")
            print("Type your message and press ENTER (or 'quit' to exit):")
            print("="*60)
            
            # Use sys.stdin.readline for better input handling
            message = sys.stdin.readline().strip()
            
            if message.lower() == 'quit':
                print("👋 Exiting message input mode...")
                break
                
            if message and server.clients:
                # Schedule the async function to run in the server's event loop
                asyncio.run_coroutine_threadsafe(
                    server.broadcast_message(message), 
                    server_loop
                )
                print(f"\n✅ MESSAGE SENT: '{message}' to {len(server.clients)} clients")
                print(f"📊 Check dashboard - Messages Sent should increase!")
            elif not server.clients:
                print("❌ No clients connected to receive messages")
            else:
                print("❌ Message cannot be empty")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting message input mode...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            # Continue the loop even if there's an error


async def main():
    """Start the enhanced VPN server with monitoring"""
    global server_loop
    
    config = Config()
    
    # Create VPN server
    server = VPNServer(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        auth_enabled=config.AUTH_ENABLED
    )
    
    # Create simple dashboard
    dashboard = SimpleDashboard(server, host="0.0.0.0", port=8081)
    
    logger.info(f"Starting Enhanced VPN Server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    logger.info("Monitoring Dashboard will be available at http://localhost:8081")
    
    try:
        # Start both servers
        server_task = asyncio.create_task(server.start())
        dashboard_task = asyncio.create_task(dashboard.start())
        
        # Store event loop for message sending
        server_loop = asyncio.get_event_loop()
        
        # Start message input thread
        message_thread = threading.Thread(target=message_input_loop, args=(server,))
        message_thread.daemon = True
        message_thread.start()
        
        # Wait for server to start
        await asyncio.sleep(2)
        logger.info("=" * 60)
        logger.info("✅ VPN SERVER RUNNING")
        logger.info("=" * 60)
        logger.info(f"📡 VPN Address: {config.SERVER_HOST}:{config.SERVER_PORT}")
        logger.info(f"📊 Dashboard: http://localhost:8081")
        logger.info(f"🔐 Authentication: {'Enabled' if config.AUTH_ENABLED else 'Disabled'}")
        logger.info(f"👥 Max Clients: Unlimited (concurrent)")
        logger.info("💬 Type messages in console to send to clients")
        logger.info("=" * 60)
        
        # Keep running
        await server_task
        
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        await dashboard.stop()
        await server.stop()


# Global variable to store event loop
server_loop = None


if __name__ == "__main__":
    asyncio.run(main())
