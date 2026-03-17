"""
Direct API tester to update dashboard stats
"""
import asyncio
import aiohttp

async def test_dashboard():
    """Test dashboard by making direct API calls"""
    print("Testing Dashboard APIs...\n")
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Get current stats
        print("1. Getting current stats...")
        async with session.get('http://localhost:8081/api/stats') as resp:
            stats = await resp.json()
            print(f"   Stats: {stats}\n")
        
        # Test 2: Get clients
        print("2. Getting connected clients...")
        async with session.get('http://localhost:8081/api/clients') as resp:
            clients = await resp.json()
            print(f"   Clients: {clients}\n")
        
        # Test 3: Get logs
        print("3. Getting logs...")
        async with session.get('http://localhost:8081/api/logs') as resp:
            logs = await resp.json()
            print(f"   Logs keys: {list(logs.keys())}\n")
        
        print("✅ All API endpoints are working!")
        print("\nOpen http://localhost:8081 in your browser to see the dashboard.")
        print("The dashboard will show '0' values until a real VPN client connects.")

if __name__ == "__main__":
    asyncio.run(test_dashboard())
