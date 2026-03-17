"""
Cybersecurity VPN Server - Professional Ethical Hacking Interface
Dark theme with security operations center aesthetic
"""

import asyncio
import logging
import threading
import sys
from vpn_server.enhanced_server import VPNServer
from vpn_server.cybersecurity_dashboard import CyberSecurityDashboard
from vpn_server.config import Config

# Configure logging with security theme
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SECURE_VPN')

# Reduce aiohttp access log noise
logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

def message_input_loop(server):
    """Cybersecurity-themed message input interface"""
    while True:
        try:
            print("\n" + "="*80)
            print("🛡️  CYBERSECURITY VPN OPERATIONS CENTER")
            print("="*80)
            print("🔐 SECURE MESSAGE TRANSMISSION SYSTEM")
            print("💬 Enter encrypted message (spaces fully supported) or 'quit' to exit:")
            print("🎯 Examples: 'All systems secure', 'Threat level low', 'Mission accomplished'")
            print("-"*80)
            
            # Use sys.stdin.readline for better input handling
            message = sys.stdin.readline().strip()
            
            if message.lower() == 'quit':
                print("\n🔒 Shutting down secure communications...")
                break
                
            if message and server.clients:
                # Schedule the async function to run in the server's event loop
                asyncio.run_coroutine_threadsafe(
                    server.broadcast_message(message), 
                    server_loop
                )
                print(f"\n✅ SECURE TRANSMISSION: '{message}'")
                print(f"🎯 Recipients: {len(server.clients)} secure agents")
                print(f"🌐 Cybersecurity Dashboard: http://localhost:8081")
                print(f"📊 Encrypted messages counter updated!")
                print(f"🔒 All transmissions secured with AES-256-GCM")
            elif not server.clients:
                print("❌ No secure agents connected - awaiting connections...")
            else:
                print("❌ Message cannot be empty - please transmit valid data")
                
        except KeyboardInterrupt:
            print("\n🔒 Secure communications terminated by operator...")
            break
        except Exception as e:
            print(f"❌ Security breach in message system: {e}")
            print("🔄 Reinitializing secure message system...")

async def main():
    """Start the cybersecurity VPN server with security dashboard"""
    global server_loop
    
    config = Config()
    
    print("🛡️  INITIALIZING CYBERSECURITY VPN SUITE")
    print("="*60)
    
    # Create VPN server
    server = VPNServer(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        auth_enabled=config.AUTH_ENABLED
    )
    
    # Create cybersecurity dashboard
    dashboard = CyberSecurityDashboard(server, host="0.0.0.0", port=8081)
    
    logger.info(f"🔐 Secure VPN Server: {config.SERVER_HOST}:{config.SERVER_PORT}")
    logger.info(f"🛡️  Cybersecurity Dashboard: http://localhost:8081")
    logger.info(f"🔒 Authentication: {'Enabled' if config.AUTH_ENABLED else 'Disabled'}")
    
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
        
        logger.info("="*70)
        logger.info("🛡️  CYBERSECURITY VPN OPERATIONS CENTER ACTIVE")
        logger.info("="*70)
        logger.info(f"🔐 Secure VPN Server: {config.SERVER_HOST}:{config.SERVER_PORT}")
        logger.info(f"🛡️  Security Dashboard: http://localhost:8081")
        logger.info(f"🔒 Authentication: {'Enabled' if config.AUTH_ENABLED else 'Disabled'}")
        logger.info(f"👥 Max Agents: {config.MAX_CLIENTS if hasattr(config, 'MAX_CLIENTS') else 'Unlimited'}")
        logger.info(f"📡 Secure Communications: Active")
        logger.info(f"🔍 Real-time Monitoring: Active")
        logger.info("="*70)
        logger.info("🎯 Security Features Available:")
        logger.info("   • Real-time threat monitoring")
        logger.info("   • Secure message broadcasting")
        logger.info("   • Advanced security metrics")
        logger.info("   • Network surveillance")
        logger.info("   • Agent management system")
        logger.info("   • Security data export")
        logger.info("   • WebSocket secure updates")
        logger.info("   • AES-256-GCM encryption")
        logger.info("="*70)
        
        # Wait for both tasks
        await asyncio.gather(server_task, dashboard_task)
        
    except KeyboardInterrupt:
        logger.info("🛡️  Security shutdown initiated by operator")
    except Exception as e:
        logger.error(f"❌ Security system error: {e}")
    finally:
        logger.info("🔄 Deactivating security systems...")
        if 'server_task' in locals():
            server_task.cancel()
        if 'dashboard_task' in locals():
            dashboard_task.cancel()
        logger.info("✅ Cybersecurity VPN Suite secured and stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛡️  Security operations terminated. Stay safe!")
    except Exception as e:
        print(f"❌ Critical security failure: {e}")
