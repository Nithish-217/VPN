"""
Simple VPN Dashboard - Error Free Version
Minimal dashboard that just works without complications
"""

import asyncio
import json
from aiohttp import web
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from vpn_server.enhanced_server import VPNServer


class SimpleDashboard:
    """Simple, error-free monitoring dashboard"""
    
    def __init__(self, server: 'VPNServer', host: str = "127.0.0.1", port: int = 8081):
        self.vpn_server = server
        self.host = host
        self.port = port
        self.app = None
        self.runner = None
        
    async def start(self):
        """Start the simple dashboard web server"""
        self.app = web.Application()
        self.app.router.add_get('/', self.handle_dashboard)
        self.app.router.add_get('/api/stats', self.handle_api_stats)
        self.app.router.add_get('/api/clients', self.handle_api_clients)
        self.app.router.add_post('/api/reset', self.handle_api_reset)
        
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()
        
        print(f"Simple Dashboard: http://{self.host}:{self.port}")
    
    async def stop(self):
        """Stop the dashboard web server"""
        if self.runner:
            await self.runner.cleanup()
    
    async def handle_dashboard(self, request):
        """Serve the simple dashboard HTML"""
        html_content = self._generate_simple_html()
        return web.Response(text=html_content, content_type='text/html')
    
    async def handle_api_stats(self, request):
        """API endpoint for statistics"""
        try:
            stats = {
                'active_clients': len(self.vpn_server.clients),
                'peak_connections': getattr(self.vpn_server, 'peak_connections', 0),
                'total_bytes_sent': getattr(self.vpn_server, 'total_bytes_sent', 0),
                'total_bytes_received': getattr(self.vpn_server, 'total_bytes_received', 0),
                'messages_sent': getattr(self.vpn_server, 'messages_sent', 0),
                'uptime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return web.json_response(stats)
        except Exception as e:
            return web.json_response({'error': str(e)})
    
    async def handle_api_clients(self, request):
        """API endpoint for client list"""
        try:
            clients = []
            for cid, handler in self.vpn_server.clients.items():
                client_info = {
                    'client_id': str(cid),
                    'ip': getattr(handler, 'client_ip', 'Unknown'),
                    'username': getattr(handler, 'username', 'Unknown'),
                    'bytes_sent': getattr(handler, 'bytes_sent', 0),
                    'bytes_received': getattr(handler, 'bytes_received', 0),
                    'connected_since': getattr(handler, 'connected_since', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
                }
                clients.append(client_info)
            return web.json_response({'clients': clients})
        except Exception as e:
            return web.json_response({'error': str(e)})
    
    async def handle_api_reset(self, request):
        """Reset traffic statistics without disconnecting clients"""
        try:
            # Reset traffic stats
            self.vpn_server.total_bytes_sent = 0
            self.vpn_server.total_bytes_received = 0
            self.vpn_server.messages_sent = 0
            
            # Reset client stats but keep them connected
            for client_id, handler in self.vpn_server.clients.items():
                handler.bytes_sent = 0
                handler.bytes_received = 0
            
            return web.json_response({
                'success': True,
                'message': 'Statistics reset successfully (clients remain connected)'
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'message': f'Error resetting stats: {str(e)}'
            }, status=500)
    
    def _generate_simple_html(self):
        """Generate simple, error-free HTML"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>VPN Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stat-value { font-size: 2em; font-weight: bold; color: #3498db; }
        .stat-label { color: #7f8c8d; margin-top: 5px; }
        .clients { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #ecf0f1; }
        .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #3498db; color: white; }
        .btn-danger { background: #e74c3c; color: white; }
        .status-online { color: #27ae60; }
        .status-offline { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 VPN Monitoring Dashboard</h1>
            <p>Simple • Reliable • Real-time</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="active-clients">0</div>
                <div class="stat-label">Active Clients</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="peak-connections">0</div>
                <div class="stat-label">Peak Connections</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="data-sent">0 B</div>
                <div class="stat-label">Data Sent</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="data-received">0 B</div>
                <div class="stat-label">Data Received</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="messages-sent">0</div>
                <div class="stat-label">Messages Sent</div>
            </div>
        </div>
        
        <div class="clients">
            <h2>Connected Clients</h2>
            <button class="btn btn-primary" onclick="loadData()">Refresh</button>
            <button class="btn btn-danger" onclick="resetData()">Reset Stats</button>
            
            <table id="clients-table">
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Username</th>
                        <th>IP Address</th>
                        <th>Data Sent</th>
                        <th>Data Received</th>
                        <th>Connected Since</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td colspan="6" style="text-align: center;">Loading...</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function formatBytes(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        async function loadData() {
            try {
                // Load stats
                const statsResponse = await fetch('/api/stats');
                const stats = await statsResponse.json();
                
                document.getElementById('active-clients').textContent = stats.active_clients || 0;
                document.getElementById('peak-connections').textContent = stats.peak_connections || 0;
                document.getElementById('data-sent').textContent = formatBytes(stats.total_bytes_sent || 0);
                document.getElementById('data-received').textContent = formatBytes(stats.total_bytes_received || 0);
                document.getElementById('messages-sent').textContent = stats.messages_sent || 0;
                
                // Load clients
                const clientsResponse = await fetch('/api/clients');
                const clientsData = await clientsResponse.json();
                
                const clientsTable = document.getElementById('clients-table').getElementsByTagName('tbody')[0];
                if (!clientsData.clients || clientsData.clients.length === 0) {
                    clientsTable.innerHTML = '<tr><td colspan="6" style="text-align: center;">No active connections</td></tr>';
                } else {
                    clientsTable.innerHTML = clientsData.clients.map(client => 
                        '<tr>' +
                        '<td><span class="status-online">● Online</span></td>' +
                        '<td>' + (client.username || 'N/A') + '</td>' +
                        '<td>' + (client.ip || 'N/A') + '</td>' +
                        '<td>' + formatBytes(client.bytes_sent || 0) + '</td>' +
                        '<td>' + formatBytes(client.bytes_received || 0) + '</td>' +
                        '<td>' + (client.connected_since || 'N/A') + '</td>' +
                        '</tr>'
                    ).join('');
                }
            } catch (error) {
                console.error('Error loading data:', error);
                document.getElementById('clients-table').getElementsByTagName('tbody')[0].innerHTML = 
                    '<tr><td colspan="6" style="text-align: center;">Error loading data</td></tr>';
            }
        }

        async function resetData() {
            if (confirm('Reset all statistics?')) {
                try {
                    // Reset traffic stats without disconnecting clients
                    const response = await fetch('/api/reset', { method: 'POST' });
                    const result = await response.json();
                    alert(result.message || 'Stats reset successfully');
                    loadData();
                } catch (error) {
                    alert('Error resetting stats: ' + error.message);
                }
            }
        }

        // Auto-refresh every 3 seconds
        setInterval(loadData, 3000);
        
        // Initial load
        loadData();
    </script>
</body>
</html>
        """
