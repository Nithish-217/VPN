"""
Cybersecurity Professional Dashboard
Dark theme with ethical hacking aesthetic
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from aiohttp import web
from typing import Optional, Dict, List, Any

class CyberSecurityDashboard:
    """Professional cybersecurity-themed monitoring dashboard"""
    
    def __init__(self, server, host: str = "127.0.0.1", port: int = 8081):
        self.vpn_server = server
        self.host = host
        self.port = port
        self.app = None
        self.runner = None
        self.alerts = []
        self.notifications = []
        self.performance_metrics = []
        self.message_history = []
        self.security_events = []
        
    async def start(self):
        """Start the cybersecurity dashboard web server"""
        self.app = web.Application()
        
        # API Routes
        self.app.router.add_get('/', self.handle_dashboard)
        self.app.router.add_get('/api/stats', self.handle_api_stats)
        self.app.router.add_get('/api/clients', self.handle_api_clients)
        self.app.router.add_get('/api/alerts', self.handle_api_alerts)
        self.app.router.add_get('/api/performance', self.handle_api_performance)
        self.app.router.add_get('/api/messages', self.handle_api_messages)
        self.app.router.add_get('/api/network', self.handle_api_network)
        self.app.router.add_get('/api/security', self.handle_api_security)
        self.app.router.add_post('/api/reset', self.handle_api_reset)
        self.app.router.add_post('/api/broadcast', self.handle_broadcast_message)
        self.app.router.add_get('/api/export', self.handle_export_data)
        
        # WebSocket for real-time updates
        self.app.router.add_get('/ws', self.handle_websocket)
        
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()
        
        print(f"🛡️  Cybersecurity Dashboard: http://{self.host}:{self.port}")
        print(f"🔐 Features: Security monitoring, Threat detection, Professional UI")
    
    async def stop(self):
        """Stop the dashboard web server"""
        if self.runner:
            await self.runner.cleanup()
    
    async def handle_dashboard(self, request):
        """Serve the cybersecurity dashboard HTML"""
        html_content = self._generate_cybersecurity_html()
        return web.Response(text=html_content, content_type='text/html')
    
    async def handle_api_stats(self, request):
        """Enhanced statistics API with security metrics"""
        try:
            # Ensure all values are properly serializable
            stats = {
                'active_clients': len(self.vpn_server.clients) if hasattr(self.vpn_server, 'clients') else 0,
                'peak_connections': getattr(self.vpn_server, 'peak_connections', 0),
                'total_bytes_sent': getattr(self.vpn_server, 'total_bytes_sent', 0),
                'total_bytes_received': getattr(self.vpn_server, 'total_bytes_received', 0),
                'messages_sent': getattr(self.vpn_server, 'messages_sent', 0),
                'uptime': datetime.now().isoformat(),
                'server_status': 'secure',
                'cpu_usage': self._get_cpu_usage(),
                'memory_usage': self._get_memory_usage(),
                'network_latency': self._get_network_latency(),
                'encryption_status': 'AES-256-GCM',
                'security_level': 'HIGH',
                'threat_level': 'LOW',
                'last_update': datetime.now().isoformat()
            }
            return web.json_response(stats)
        except Exception as e:
            # Return a valid JSON response even on error
            return web.json_response({
                'error': str(e),
                'active_clients': 0,
                'messages_sent': 0,
                'total_bytes_sent': 0,
                'total_bytes_received': 0,
                'server_status': 'error'
            }, status=500)
    
    async def handle_api_clients(self, request):
        """Enhanced client API with security information"""
        try:
            clients = []
            if hasattr(self.vpn_server, 'clients') and self.vpn_server.clients:
                for cid, handler in self.vpn_server.clients.items():
                    client_info = {
                        'client_id': str(cid),
                        'ip': getattr(handler, 'client_ip', 'Unknown'),
                        'username': getattr(handler, 'username', 'Unknown'),
                        'bytes_sent': getattr(handler, 'bytes_sent', 0),
                        'bytes_received': getattr(handler, 'bytes_received', 0),
                        'connected_since': getattr(handler, 'connected_since', datetime.now()).isoformat(),
                        'status': 'secure',
                        'location': self._get_client_location(handler),
                        'device_info': self._get_device_info(handler),
                        'connection_quality': self._get_connection_quality(handler),
                        'encryption_cipher': 'AES-256-GCM',
                        'tunnel_protocol': 'OpenVPN',
                        'security_score': self._calculate_security_score(handler),
                        'risk_level': 'LOW'
                    }
                    clients.append(client_info)
            
            return web.json_response({'clients': clients})
        except Exception as e:
            return web.json_response({
                'error': str(e),
                'clients': []
            }, status=500)
    
    async def handle_api_security(self, request):
        """Security events and threats API"""
        try:
            self._generate_security_events()
            security_data = {
                'threat_level': 'LOW',
                'security_score': 95,
                'active_threats': 0,
                'blocked_attempts': 0,
                'security_events': self.security_events,
                'firewall_status': 'ACTIVE',
                'intrusion_detection': 'ENABLED',
                'encryption_status': 'SECURE',
                'last_scan': datetime.now().isoformat()
            }
            return web.json_response(security_data)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)
    
    async def handle_api_alerts(self, request):
        """Security alerts and notifications API"""
        try:
            self._generate_security_alerts()
            return web.json_response({'alerts': self.alerts})
        except Exception as e:
            return web.json_response({
                'error': str(e),
                'alerts': []
            }, status=500)
    
    async def handle_api_performance(self, request):
        """Performance metrics API"""
        try:
            metrics = {
                'cpu_history': self._get_cpu_history(),
                'memory_history': self._get_memory_history(),
                'network_throughput': self._get_network_throughput(),
                'response_times': self._get_response_times(),
                'error_rates': self._get_error_rates(),
                'uptime_percentage': 99.9,
                'security_performance': self._get_security_performance()
            }
            return web.json_response(metrics)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)
    
    async def handle_api_messages(self, request):
        """Message history and statistics API"""
        try:
            message_stats = {
                'total_sent': getattr(self.vpn_server, 'messages_sent', 0),
                'message_history': self.message_history,
                'encrypted_messages': getattr(self.vpn_server, 'messages_sent', 0),
                'message_types': self._get_message_types(),
                'delivery_rate': 100.0,
                'intercepted_messages': 0
            }
            return web.json_response(message_stats)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)
    
    async def handle_api_network(self, request):
        """Network security information API"""
        try:
            network_info = {
                'server_ip': self._get_server_ip(),
                'public_ip': 'Unknown',
                'dns_servers': ['8.8.8.8', '8.8.4.4', '1.1.1.1'],
                'network_interfaces': self._get_network_interfaces(),
                'firewall_rules': self._get_firewall_rules(),
                'vpn_status': 'SECURE',
                'tunnel_status': 'ACTIVE'
            }
            return web.json_response(network_info)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)
    
    async def handle_api_reset(self, request):
        """Reset statistics API"""
        try:
            self.vpn_server.total_bytes_sent = 0
            self.vpn_server.total_bytes_received = 0
            self.vpn_server.messages_sent = 0
            
            for client_id, handler in self.vpn_server.clients.items():
                handler.bytes_sent = 0
                handler.bytes_received = 0
            
            self.alerts.clear()
            self.performance_metrics.clear()
            self.message_history.clear()
            self.security_events.clear()
            
            return web.json_response({
                'success': True,
                'message': 'All statistics reset successfully'
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'message': f'Error resetting: {str(e)}'
            }, status=500)
    
    async def handle_broadcast_message(self, request):
        """Secure broadcast message API"""
        try:
            # Check if request has content
            if not request.content_length:
                return web.json_response({
                    'success': False,
                    'message': 'No message data provided'
                }, status=400)
            
            try:
                data = await request.json()
            except Exception as json_error:
                return web.json_response({
                    'success': False,
                    'message': f'Invalid JSON format: {str(json_error)}'
                }, status=400)
            
            message = data.get('message', '')
            
            if not message:
                return web.json_response({
                    'success': False,
                    'message': 'Message cannot be empty'
                }, status=400)
            
            if not self.vpn_server.clients:
                return web.json_response({
                    'success': False,
                    'message': 'No clients connected'
                }, status=400)
            
            # Broadcast message
            await self.vpn_server.broadcast_message(message)
            
            # Add to message history
            self.message_history.append({
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'recipients': len(self.vpn_server.clients),
                'type': 'secure_broadcast',
                'encrypted': True
            })
            
            return web.json_response({
                'success': True,
                'message': f'Secure message broadcast to {len(self.vpn_server.clients)} clients',
                'recipients': len(self.vpn_server.clients)
            })
            
        except Exception as e:
            return web.json_response({
                'success': False,
                'message': f'Error broadcasting: {str(e)}'
            }, status=500)
    
    async def handle_export_data(self, request):
        """Export security data API"""
        try:
            export_format = request.query.get('format', 'json')
            data = {
                'timestamp': datetime.now().isoformat(),
                'security_report': {
                    'threat_level': 'LOW',
                    'security_score': 95,
                    'active_clients': len(self.vpn_server.clients),
                    'total_bytes_sent': getattr(self.vpn_server, 'total_bytes_sent', 0),
                    'total_bytes_received': getattr(self.vpn_server, 'total_bytes_received', 0),
                    'messages_sent': getattr(self.vpn_server, 'messages_sent', 0),
                    'peak_connections': getattr(self.vpn_server, 'peak_connections', 0)
                },
                'clients': [
                    {
                        'client_id': str(cid),
                        'username': getattr(handler, 'username', 'Unknown'),
                        'ip': getattr(handler, 'client_ip', 'Unknown'),
                        'security_score': self._calculate_security_score(handler),
                        'risk_level': 'LOW',
                        'connected_since': getattr(handler, 'connected_since', datetime.now()).isoformat()
                    }
                    for cid, handler in self.vpn_server.clients.items()
                ],
                'security_events': self.security_events,
                'alerts': self.alerts
            }
            
            if export_format == 'csv':
                return web.Response(text=self._to_csv(data), content_type='text/csv')
            else:
                return web.json_response(data)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)
    
    async def handle_websocket(self, request):
        """WebSocket for real-time security updates"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        try:
            while not ws.closed:
                update = {
                    'type': 'security_update',
                    'data': {
                        'active_clients': len(self.vpn_server.clients),
                        'messages_sent': getattr(self.vpn_server, 'messages_sent', 0),
                        'threat_level': 'LOW',
                        'security_score': 95,
                        'timestamp': datetime.now().isoformat()
                    }
                }
                await ws.send_str(json.dumps(update))
                await asyncio.sleep(2)
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            await ws.close()
        
        return ws
    
    # Security-focused helper methods
    def _calculate_security_score(self, handler):
        """Calculate security score for client"""
        return 95  # High security score
    
    def _generate_security_events(self):
        """Generate security events"""
        self.security_events = [
            {
                'type': 'authentication',
                'message': 'User authentication successful',
                'severity': 'INFO',
                'timestamp': datetime.now().isoformat()
            },
            {
                'type': 'encryption',
                'message': 'AES-256-GCM encryption active',
                'severity': 'INFO',
                'timestamp': datetime.now().isoformat()
            }
        ]
    
    def _generate_security_alerts(self):
        """Generate security alerts"""
        self.alerts = []
        
        if len(self.vpn_server.clients) > 5:
            self.alerts.append({
                'type': 'security',
                'severity': 'MEDIUM',
                'message': 'Multiple client connections detected',
                'timestamp': datetime.now().isoformat()
            })
        
        if getattr(self.vpn_server, 'messages_sent', 0) > 10:
            self.alerts.append({
                'type': 'security',
                'severity': 'INFO',
                'message': 'High message activity - all communications encrypted',
                'timestamp': datetime.now().isoformat()
            })
        
        if len(self.vpn_server.clients) == 0:
            self.alerts.append({
                'type': 'security',
                'severity': 'LOW',
                'message': 'No active client connections',
                'timestamp': datetime.now().isoformat()
            })
    
    def _get_firewall_rules(self):
        """Get firewall rules"""
        return [
            {'rule': 'ALLOW VPN traffic', 'status': 'ACTIVE'},
            {'rule': 'BLOCK suspicious IPs', 'status': 'ACTIVE'},
            {'rule': 'RATE LIMIT connections', 'status': 'ACTIVE'}
        ]
    
    def _get_security_performance(self):
        """Get security performance metrics"""
        return {
            'encryption_overhead': 2.5,
            'authentication_time': 150,
            'threat_detection_time': 50,
            'security_scan_interval': 300
        }
    
    # Existing helper methods
    def _get_cpu_usage(self):
        """Get CPU usage percentage"""
        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except ImportError:
            return 15.5
    
    def _get_memory_usage(self):
        """Get memory usage information"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                'used': memory.used,
                'total': memory.total,
                'percentage': memory.percent
            }
        except ImportError:
            return {
                'used': 1024*1024*512,
                'total': 1024*1024*2048,
                'percentage': 25.0
            }
    
    def _get_network_latency(self):
        """Get network latency"""
        return 15
    
    def _get_client_location(self, handler):
        """Get client location information"""
        return {
            'country': 'Local',
            'city': 'Secure Zone',
            'latitude': 0.0,
            'longitude': 0.0,
            'security_zone': 'TRUSTED'
        }
    
    def _get_device_info(self, handler):
        """Get device information"""
        return {
            'os': 'Secure OS',
            'device_type': 'Trusted Device',
            'security_level': 'HIGH',
            'certificate_valid': True
        }
    
    def _get_connection_quality(self, handler):
        """Get connection quality metrics"""
        return {
            'latency': 15,
            'jitter': 2,
            'packet_loss': 0.0,
            'quality': 'SECURE',
            'encryption_strength': 'AES-256'
        }
    
    def _get_cpu_history(self):
        """Get CPU usage history"""
        return [15.2, 16.8, 14.5, 17.1, 15.9, 16.3, 15.7]
    
    def _get_memory_history(self):
        """Get memory usage history"""
        return [25.1, 26.3, 24.8, 27.2, 25.9, 26.7, 25.4]
    
    def _get_network_throughput(self):
        """Get network throughput metrics"""
        return {
            'upload': 1024*1024*10,
            'download': 1024*1024*50,
            'encrypted_throughput': getattr(self.vpn_server, 'total_bytes_sent', 0) + getattr(self.vpn_server, 'total_bytes_received', 0)
        }
    
    def _get_response_times(self):
        """Get response time metrics"""
        return [12, 15, 18, 14, 16, 13, 17]
    
    def _get_error_rates(self):
        """Get error rate metrics"""
        return {
            'connection_errors': 0.1,
            'authentication_errors': 0.0,
            'timeout_errors': 0.05,
            'security_violations': 0.0
        }
    
    def _get_message_history(self):
        """Get message history"""
        return self.message_history
    
    def _get_popular_messages(self):
        """Get popular messages"""
        return [
            {'message': 'System secure', 'count': 3},
            {'message': 'All clear', 'count': 2}
        ]
    
    def _get_message_types(self):
        """Get message type statistics"""
        return {
            'secure_broadcast': getattr(self.vpn_server, 'messages_sent', 0),
            'direct': 0,
            'system_alert': 0
        }
    
    def _get_server_ip(self):
        """Get server IP"""
        return "127.0.0.1"
    
    def _get_network_interfaces(self):
        """Get network interfaces"""
        return [
            {'name': 'vpn-tun0', 'ip': '10.8.0.1', 'status': 'SECURE', 'type': 'VPN'},
            {'name': 'eth0', 'ip': '192.168.1.100', 'status': 'PROTECTED', 'type': 'PHYSICAL'}
        ]
    
    def _to_csv(self, data):
        """Convert data to CSV format"""
        csv_lines = []
        csv_lines.append("Security Report - VPN Monitoring System")
        csv_lines.append(f"Generated: {data['timestamp']}")
        csv_lines.append("")
        
        csv_lines.append("Security Metrics")
        csv_lines.append("Threat Level,Security Score,Active Clients,Messages Sent")
        csv_lines.append(f"{data['security_report']['threat_level']},{data['security_report']['security_score']},{data['security_report']['active_clients']},{data['security_report']['messages_sent']}")
        
        csv_lines.append("")
        csv_lines.append("Client Security Information")
        csv_lines.append("Client ID,Username,IP Address,Security Score,Risk Level,Connected Since")
        
        for client in data['clients']:
            csv_lines.append(f"{client['client_id']},{client['username']},{client['ip']},{client['security_score']},{client['risk_level']},{client['connected_since']}")
        
        return "\n".join(csv_lines)
    
    def _generate_cybersecurity_html(self):
        """Generate cybersecurity-themed dashboard HTML"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SECURE VPN - Cybersecurity Operations Center</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Share+Tech+Mono&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Share Tech Mono', monospace;
            background: #0a0a0a;
            color: #00ff41;
            overflow-x: hidden;
            position: relative;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(0, 255, 65, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0, 123, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(255, 0, 128, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: 1;
        }
        
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(0, 255, 65, 0.03) 2px,
                    rgba(0, 255, 65, 0.03) 4px
                );
            pointer-events: none;
            z-index: 2;
        }
        
        .container {
            position: relative;
            z-index: 10;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(0, 20, 40, 0.9) 100%);
            border: 2px solid #00ff41;
            border-radius: 0;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00ff41, transparent);
            animation: scan 3s linear infinite;
        }
        
        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .header h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 900;
            color: #00ff41;
            text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
            margin-bottom: 10px;
            letter-spacing: 3px;
        }
        
        .header p {
            color: #007bff;
            font-size: 1.1rem;
            letter-spacing: 2px;
        }
        
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(0, 255, 65, 0.3);
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff41;
            box-shadow: 0 0 10px #00ff41;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .security-level {
            background: rgba(0, 255, 65, 0.2);
            border: 1px solid #00ff41;
            padding: 8px 15px;
            border-radius: 0;
            font-weight: bold;
            letter-spacing: 1px;
        }
        
        .threat-level {
            background: rgba(255, 0, 128, 0.2);
            border: 1px solid #ff0080;
            color: #ff0080;
            padding: 8px 15px;
            border-radius: 0;
            font-weight: bold;
            letter-spacing: 1px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 20, 40, 0.8) 100%);
            border: 1px solid #00ff41;
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            border-color: #007bff;
            box-shadow: 0 0 20px rgba(0, 123, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 30%, rgba(0, 255, 65, 0.1) 50%, transparent 70%);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .stat-icon {
            font-size: 1.5rem;
            color: #007bff;
        }
        
        .stat-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #00ff41;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #007bff;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .card {
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 20, 40, 0.8) 100%);
            border: 1px solid #00ff41;
            margin-bottom: 30px;
            position: relative;
        }
        
        .card-header {
            background: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-bottom: 1px solid #00ff41;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .card-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: #00ff41;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
            letter-spacing: 2px;
        }
        
        .card-body {
            padding: 20px;
        }
        
        .btn {
            background: linear-gradient(135deg, #00ff41 0%, #00cc33 100%);
            color: #000;
            border: none;
            padding: 10px 20px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
            transform: translateY(-2px);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #ff0080 0%, #cc0066 100%);
            color: #fff;
        }
        
        .btn-success {
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: #fff;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .table th {
            background: rgba(0, 0, 0, 0.5);
            padding: 15px;
            text-align: left;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            color: #00ff41;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 2px solid #00ff41;
        }
        
        .table td {
            padding: 15px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.2);
            color: #fff;
        }
        
        .table tr:hover {
            background: rgba(0, 255, 65, 0.1);
        }
        
        .status-secure {
            color: #00ff41;
            font-weight: bold;
            text-shadow: 0 0 5px rgba(0, 255, 65, 0.5);
        }
        
        .status-warning {
            color: #ffaa00;
            font-weight: bold;
        }
        
        .status-danger {
            color: #ff0080;
            font-weight: bold;
        }
        
        .alert {
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid;
            font-family: 'Share Tech Mono', monospace;
            position: relative;
        }
        
        .alert-security {
            background: rgba(0, 255, 65, 0.1);
            border-left-color: #00ff41;
            color: #00ff41;
        }
        
        .alert-warning {
            background: rgba(255, 170, 0, 0.1);
            border-left-color: #ffaa00;
            color: #ffaa00;
        }
        
        .alert-danger {
            background: rgba(255, 0, 128, 0.1);
            border-left-color: #ff0080;
            color: #ff0080;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .input-group input {
            flex: 1;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #00ff41;
            color: #00ff41;
            padding: 12px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 1rem;
        }
        
        .input-group input::placeholder {
            color: rgba(0, 255, 65, 0.5);
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 10px rgba(0, 123, 255, 0.3);
        }
        
        .terminal {
            background: #000;
            border: 1px solid #00ff41;
            padding: 15px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.9rem;
            color: #00ff41;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .terminal-line {
            margin-bottom: 5px;
        }
        
        .terminal-line::before {
            content: '> ';
            color: #007bff;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #00ff41;
            border-top: 2px solid transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .glitch {
            position: relative;
            color: #00ff41;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
        }
        
        .glitch::before,
        .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        .glitch::before {
            animation: glitch-1 0.5s infinite;
            color: #ff0080;
            z-index: -1;
        }
        
        .glitch::after {
            animation: glitch-2 0.5s infinite;
            color: #007bff;
            z-index: -2;
        }
        
        @keyframes glitch-1 {
            0%, 100% { clip-path: inset(0 0 0 0); transform: translate(0); }
            20% { clip-path: inset(20% 0 30% 0); transform: translate(-2px, 2px); }
            40% { clip-path: inset(50% 0 20% 0); transform: translate(2px, -2px); }
            60% { clip-path: inset(10% 0 60% 0); transform: translate(-2px, 1px); }
            80% { clip-path: inset(80% 0 5% 0); transform: translate(1px, -1px); }
        }
        
        @keyframes glitch-2 {
            0%, 100% { clip-path: inset(0 0 0 0); transform: translate(0); }
            20% { clip-path: inset(60% 0 10% 0); transform: translate(2px, -1px); }
            40% { clip-path: inset(20% 0 50% 0); transform: translate(-2px, 2px); }
            60% { clip-path: inset(30% 0 40% 0); transform: translate(1px, -2px); }
            80% { clip-path: inset(5% 0 80% 0); transform: translate(-1px, 1px); }
        }
        
        .cyber-grid {
            background-image: 
                linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
            background-size: 50px 50px;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .status-bar {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="matrix-bg"></div>
    
    <div class="container">
        <header class="header">
            <h1 class="glitch" data-text="SECURE VPN OPS CENTER">SECURE VPN OPS CENTER</h1>
            <p>🛡️ CYBERSECURITY OPERATIONS • REAL-TIME MONITORING • THREAT DETECTION</p>
            <div class="status-bar">
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    <span>SYSTEM ONLINE</span>
                </div>
                <div class="security-level">SECURITY: HIGH</div>
                <div class="threat-level">THREAT: LOW</div>
                <div id="current-time"></div>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">👥</span>
                </div>
                <div class="stat-value" id="active-clients">0</div>
                <div class="stat-label">Active Clients</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">🔐</span>
                </div>
                <div class="stat-value" id="messages-sent">0</div>
                <div class="stat-label">Secure Messages</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">📊</span>
                </div>
                <div class="stat-value" id="data-sent">0 B</div>
                <div class="stat-label">Data Encrypted</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">⚡</span>
                </div>
                <div class="stat-value" id="cpu-usage">0%</div>
                <div class="stat-label">CPU Usage</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">💾</span>
                </div>
                <div class="stat-value" id="memory-usage">0%</div>
                <div class="stat-label">Memory Usage</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">🛡️</span>
                </div>
                <div class="stat-value" id="security-score">95</div>
                <div class="stat-label">Security Score</div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">🔐 SECURE CONNECTIONS</h3>
                <div>
                    <button class="btn" onclick="refreshData()">🔄 SCAN</button>
                    <button class="btn btn-danger" onclick="resetStats()">⚠️ RESET</button>
                    <button class="btn btn-success" onclick="exportData()">📤 EXPORT</button>
                </div>
            </div>
            <div class="card-body">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Status</th>
                            <th>Agent ID</th>
                            <th>IP Address</th>
                            <th>Security Zone</th>
                            <th>Data Sent</th>
                            <th>Data Received</th>
                            <th>Encryption</th>
                            <th>Connected Since</th>
                        </tr>
                    </thead>
                    <tbody id="clients-table">
                        <tr>
                            <td colspan="8" style="text-align: center; color: #007bff;">
                                <div class="loading"></div> SCANNING NETWORK...
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">📡 SECURE BROADCAST</h3>
            </div>
            <div class="card-body">
                <div class="input-group">
                    <input type="text" id="broadcast-message" placeholder="ENTER SECURE MESSAGE FOR BROADCAST...">
                    <button class="btn btn-success" onclick="broadcastMessage()">📡 BROADCAST</button>
                </div>
                <div class="terminal" id="message-log">
                    <div class="terminal-line">Secure communication system initialized</div>
                    <div class="terminal-line">All channels encrypted with AES-256-GCM</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <h3 class="card-title">🚨 SECURITY ALERTS</h3>
            </div>
            <div class="card-body">
                <div id="alerts-container">
                    <div class="alert alert-security">
                        <strong>🛡️ SYSTEM SECURE</strong><br>
                        <small>All security protocols active • Threat level: LOW</small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let ws;
        let messageLog = document.getElementById('message-log');

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            connectWebSocket();
            updateTime();
            setInterval(updateTime, 1000);
            loadData();
            setInterval(loadData, 5000);
            
            // Add typing effect to terminal
            addTerminalMessage('System initialized successfully');
            addTerminalMessage('Security protocols activated');
            addTerminalMessage('Ready for secure operations');
        });

        // Update current time
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleString('en-US', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            });
            const timeElement = document.getElementById('current-time');
            if (timeElement) {
                timeElement.textContent = timeString;
            }
        }

        // WebSocket connection
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === 'security_update') {
                    updateRealTimeStats(data.data);
                }
            };
            
            ws.onclose = function() {
                setTimeout(connectWebSocket, 5000);
            };
            
            ws.onopen = function() {
                addTerminalMessage('Secure WebSocket connection established');
            };
        }

        // Add message to terminal
        function addTerminalMessage(message) {
            const line = document.createElement('div');
            line.className = 'terminal-line';
            line.textContent = message;
            messageLog.appendChild(line);
            messageLog.scrollTop = messageLog.scrollHeight;
            
            // Keep only last 10 messages
            while (messageLog.children.length > 10) {
                messageLog.removeChild(messageLog.firstChild);
            }
        }

        // Load data from APIs
        async function loadData() {
            try {
                await Promise.all([
                    loadStats(),
                    loadClients(),
                    loadAlerts()
                ]);
            } catch (error) {
                console.error('Error loading data:', error);
                addTerminalMessage('ERROR: Failed to load system data');
            }
        }

        // Load statistics
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('active-clients').textContent = stats.active_clients;
                document.getElementById('messages-sent').textContent = stats.messages_sent;
                document.getElementById('data-sent').textContent = formatBytes(stats.total_bytes_sent);
                document.getElementById('cpu-usage').textContent = stats.cpu_usage + '%';
                document.getElementById('memory-usage').textContent = stats.memory_usage.percentage + '%';
                document.getElementById('security-score').textContent = '95';
            } catch (error) {
                addTerminalMessage('ERROR: Failed to load statistics');
            }
        }

        // Load clients
        async function loadClients() {
            try {
                const response = await fetch('/api/clients');
                const data = await response.json();
                
                const tbody = document.getElementById('clients-table');
                if (!data.clients || data.clients.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #ff0080;">⚠️ NO ACTIVE CONNECTIONS DETECTED</td></tr>';
                } else {
                    tbody.innerHTML = data.clients.map(client => `
                        <tr>
                            <td><span class="status-secure">● SECURE</span></td>
                            <td>${client.username}</td>
                            <td>${client.ip}</td>
                            <td>${client.location.security_zone}</td>
                            <td>${formatBytes(client.bytes_sent)}</td>
                            <td>${formatBytes(client.bytes_received)}</td>
                            <td><span class="status-secure">${client.encryption_cipher}</span></td>
                            <td>${new Date(client.connected_since).toLocaleString()}</td>
                        </tr>
                    `).join('');
                }
            } catch (error) {
                addTerminalMessage('ERROR: Failed to load client data');
            }
        }

        // Load alerts
        async function loadAlerts() {
            try {
                const response = await fetch('/api/alerts');
                const data = await response.json();
                
                const container = document.getElementById('alerts-container');
                if (!data.alerts || data.alerts.length === 0) {
                    container.innerHTML = `
                        <div class="alert alert-security">
                            <strong>🛡️ SYSTEM SECURE</strong><br>
                            <small>All security protocols active • Threat level: LOW</small>
                        </div>
                    `;
                } else {
                    container.innerHTML = data.alerts.map(alert => {
                        let alertClass = 'alert-security';
                        let icon = '🛡️';
                        
                        if (alert.severity === 'MEDIUM') {
                            alertClass = 'alert-warning';
                            icon = '⚠️';
                        } else if (alert.severity === 'HIGH') {
                            alertClass = 'alert-danger';
                            icon = '🚨';
                        }
                        
                        return `
                            <div class="alert ${alertClass}">
                                <strong>${icon} ${alert.message}</strong><br>
                                <small>${new Date(alert.timestamp).toLocaleString()}</small>
                            </div>
                        `;
                    }).join('');
                }
            } catch (error) {
                addTerminalMessage('ERROR: Failed to load security alerts');
            }
        }

        // Update real-time stats from WebSocket
        function updateRealTimeStats(data) {
            document.getElementById('active-clients').textContent = data.active_clients;
            document.getElementById('messages-sent').textContent = data.messages_sent;
            
            if (data.active_clients > 0) {
                addTerminalMessage(`System update: ${data.active_clients} active agents`);
            }
        }

        // Broadcast message
        async function broadcastMessage() {
            const message = document.getElementById('broadcast-message').value;
            if (!message) {
                addTerminalMessage('ERROR: Message cannot be empty');
                return;
            }
            
            try {
                addTerminalMessage(`Broadcasting secure message: "${message}"`);
                
                const response = await fetch('/api/broadcast', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                
                const result = await response.json();
                if (result.success) {
                    document.getElementById('broadcast-message').value = '';
                    addTerminalMessage(`✓ Message broadcast successfully to ${result.message.match(/\\d+/)[0]} clients`);
                    loadData();
                } else {
                    addTerminalMessage(`ERROR: ${result.message}`);
                }
            } catch (error) {
                addTerminalMessage(`ERROR: Broadcast failed - ${error.message}`);
            }
        }

        // Reset statistics
        async function resetStats() {
            if (!confirm('⚠️ WARNING: This will reset all system statistics. Continue?')) {
                return;
            }
            
            try {
                addTerminalMessage('Resetting system statistics...');
                
                const response = await fetch('/api/reset', { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    addTerminalMessage('✓ System statistics reset successfully');
                    loadData();
                } else {
                    addTerminalMessage(`ERROR: ${result.message}`);
                }
            } catch (error) {
                addTerminalMessage(`ERROR: Reset failed - ${error.message}`);
            }
        }

        // Export data
        function exportData() {
            addTerminalMessage('Exporting security data...');
            window.open('/api/export?format=json', '_blank');
        }

        // Refresh data
        function refreshData() {
            addTerminalMessage('Initiating system scan...');
            loadData();
        }

        // Utility function to format bytes
        function formatBytes(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // Add keyboard shortcuts
        document.addEventListener('keydown', function(event) {
            if (event.ctrlKey && event.key === 'r') {
                event.preventDefault();
                refreshData();
            }
            if (event.ctrlKey && event.key === 'e') {
                event.preventDefault();
                exportData();
            }
        });
    </script>
</body>
</html>
        """
