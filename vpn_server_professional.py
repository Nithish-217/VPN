"""
Professional VPN Server with Advanced Dashboard
Clean, organized structure with extensive features
"""

import asyncio
import logging
import threading
import sys
from vpn_server.enhanced_server import VPNServer
from vpn_server.professional_dashboard import ProfessionalDashboard
from vpn_server.config import Config

# Configure logging with reduced noise
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VPNServer')

# Reduce aiohttp access log noise
logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

def message_input_loop(server):
    """Professional message input interface"""
    while True:
        try:
            print("\n" + "="*80)
            print("🚀 PROFESSIONAL VPN SERVER - MESSAGE CONTROL CENTER")
            print("="*80)
            print("📝 Enter your message (spaces fully supported) or 'quit' to exit:")
            print("💡 Examples: 'Hello world!', 'System maintenance in 5 minutes'")
            print("-"*80)
            
            # Use sys.stdin.readline for better input handling
            message = sys.stdin.readline().strip()
            
            if message.lower() == 'quit':
                print("\n👋 Shutting down message input system...")
                break
                
            if message and server.clients:
                # Schedule the async function to run in the server's event loop
                asyncio.run_coroutine_threadsafe(
                    server.broadcast_message(message), 
                    server_loop
                )
                print(f"\n✅ MESSAGE DELIVERED: '{message}'")
                print(f"📊 Recipients: {len(server.clients)} clients")
                print(f"🌐 Check dashboard: http://localhost:8081")
                print(f"📈 Messages Sent counter updated!")
            elif not server.clients:
                print("❌ No clients connected - waiting for connections...")
            else:
                print("❌ Message cannot be empty - please try again")
                
        except KeyboardInterrupt:
            print("\n👋 Message input interrupted by user...")
            break
        except Exception as e:
            print(f"❌ Error in message input: {e}")
            print("🔄 Continuing message input system...")

async def main():
    """Start the professional VPN server with advanced dashboard"""
    global server_loop
    
    config = Config()
    
    print("🚀 Starting Professional VPN Server Suite")
    print("="*50)
    
    # Create VPN server
    server = VPNServer(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        auth_enabled=config.AUTH_ENABLED
    )
    
    # Create professional dashboard
    dashboard = ProfessionalDashboard(server, host="0.0.0.0", port=8081)
    
    logger.info(f"🔧 VPN Server: {config.SERVER_HOST}:{config.SERVER_PORT}")
    logger.info(f"📊 Advanced Dashboard: http://localhost:8081")
    logger.info(f"🔐 Authentication: {'Enabled' if config.AUTH_ENABLED else 'Disabled'}")
    
    try:
        # Start both servers
        server_task = asyncio.create_task(server.start())
        dashboard_task = asyncio.create_task(dashboard.start())
        
        # Store event loop for message sending
        server_loop = asyncio.get_event_loop()
        
        # Start message input thread
        message_thread = threading.Thread(
            target=message_input_loop, 
            args=(server,),
            daemon=True
        )
        message_thread.start()
        
        logger.info("="*60)
        logger.info("🎉 PROFESSIONAL VPN SERVER SUITE RUNNING")
        logger.info("="*60)
        logger.info(f"📡 VPN Server: {config.SERVER_HOST}:{config.SERVER_PORT}")
        logger.info(f"📊 Dashboard: http://localhost:8081")
        logger.info(f"🔐 Authentication: {'Enabled' if config.AUTH_ENABLED else 'Disabled'}")
        logger.info(f"👥 Max Clients: {config.MAX_CLIENTS if hasattr(config, 'MAX_CLIENTS') else 'Unlimited'}")
        logger.info(f"💬 Message System: Active")
        logger.info(f"📈 Real-time Monitoring: Active")
        logger.info("="*60)
        logger.info("🎯 Features Available:")
        logger.info("   • Real-time client monitoring")
        logger.info("   • Advanced message broadcasting")
        logger.info("   • Performance metrics")
        logger.info("   • Network statistics")
        logger.info("   • Client management")
        logger.info("   • Data export functionality")
        logger.info("   • WebSocket real-time updates")
        logger.info("="*60)
        
        # Wait for both tasks
        await asyncio.gather(server_task, dashboard_task)
        
    except KeyboardInterrupt:
        logger.info("🛑 Server shutdown requested by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
    finally:
        logger.info("🔄 Shutting down server components...")
        if 'server_task' in locals():
            server_task.cancel()
        if 'dashboard_task' in locals():
            dashboard_task.cancel()
        logger.info("✅ Professional VPN Server stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
