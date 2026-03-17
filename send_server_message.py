#!/usr/bin/env python3
"""
Server Message Sender
Send messages from VPN server to connected clients
"""

import asyncio
import sys
from vpn_server.enhanced_server import VPNServer
from vpn_server.config import Config

async def send_message_menu():
    """Interactive message sending menu"""
    config = Config()
    
    # Create server instance (we won't start it, just use messaging)
    server = VPNServer(
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        auth_enabled=config.AUTH_ENABLED
    )
    
    print("=" * 60)
    print("🔔 VPN SERVER MESSAGE SENDER")
    print("=" * 60)
    print(f"Server: {config.SERVER_HOST}:{config.SERVER_PORT}")
    print()
    
    while True:
        print("Options:")
        print("1. Send message to specific client")
        print("2. Broadcast message to all clients")
        print("3. List connected clients")
        print("4. Exit")
        print()
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            await send_to_client(server)
        elif choice == "2":
            await broadcast_to_all(server)
        elif choice == "3":
            list_clients(server)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
        print()

async def send_to_client(server):
    """Send message to specific client"""
    if not server.clients:
        print("❌ No clients connected!")
        return
    
    print("\nConnected Clients:")
    for i, client_id in enumerate(server.clients.keys(), 1):
        handler = server.clients[client_id]
        print(f"{i}. {client_id} ({handler.client_ip}) - User: {handler.username}")
    
    try:
        client_num = int(input("\nEnter client number: ")) - 1
        client_ids = list(server.clients.keys())
        
        if 0 <= client_num < len(client_ids):
            client_id = client_ids[client_num]
            message = input("Enter message: ").strip()
            
            if message:
                success = await server.send_message_to_client(client_id, message)
                if success:
                    print(f"✅ Message sent to {client_id}")
                else:
                    print(f"❌ Failed to send message")
            else:
                print("❌ Message cannot be empty")
        else:
            print("❌ Invalid client number")
    except ValueError:
        print("❌ Invalid input")

async def broadcast_to_all(server):
    """Broadcast message to all clients"""
    if not server.clients:
        print("❌ No clients connected!")
        return
    
    message = input("Enter broadcast message: ").strip()
    
    if message:
        count = await server.broadcast_message(message)
        print(f"✅ Message sent to {count} clients")
    else:
        print("❌ Message cannot be empty")

def list_clients(server):
    """List all connected clients"""
    if not server.clients:
        print("❌ No clients connected!")
        return
    
    print(f"\nConnected Clients ({len(server.clients)}):")
    print("-" * 40)
    for client_id, handler in server.clients.items():
        duration = str(asyncio.get_event_loop().time() - handler.connected_since.timestamp())
        print(f"📱 {client_id}")
        print(f"   IP: {handler.client_ip}")
        print(f"   User: {handler.username}")
        print(f"   Connected: {duration}")
        print(f"   Data: ↑{handler.bytes_sent} ↓{handler.bytes_received}")
        print()

if __name__ == "__main__":
    try:
        asyncio.run(send_message_menu())
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
