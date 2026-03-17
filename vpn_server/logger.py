"""
Connection Logger Module
Comprehensive logging for VPN connections
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger('VPNServer.ConnectionLogger')


class ConnectionLogger:
    """Advanced connection logging system"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Log files
        self.connections_log = self.log_dir / "connections.jsonl"
        self.auth_log = self.log_dir / "auth.jsonl"
        self.traffic_log = self.log_dir / "traffic.jsonl"
        
        logger.info(f"Connection logger initialized - Logs: {self.log_dir}")
    
    def log_connect(self, client_id: str, remote_ip: str, username: str, vpn_ip: str):
        """Log new connection"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'connect',
            'client_id': client_id,
            'remote_ip': remote_ip,
            'username': username,
            'vpn_ip': vpn_ip
        }
        
        self._write_log(self.connections_log, log_entry)
        logger.info(f"CONNECT: {username}@{remote_ip} -> VPN:{vpn_ip}")
    
    def log_disconnect(self, client_id: str, remote_ip: str):
        """Log disconnection"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'disconnect',
            'client_id': client_id,
            'remote_ip': remote_ip
        }
        
        self._write_log(self.connections_log, log_entry)
        logger.info(f"DISCONNECT: {client_id}@{remote_ip}")
    
    def log_auth_success(self, client_id: str, remote_ip: str, username: str):
        """Log successful authentication"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'auth_success',
            'client_id': client_id,
            'remote_ip': remote_ip,
            'username': username
        }
        
        self._write_log(self.auth_log, log_entry)
    
    def log_auth_failure(self, client_id: str, remote_ip: str, username: str):
        """Log failed authentication"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'auth_failure',
            'client_id': client_id,
            'remote_ip': remote_ip,
            'username': username,
            'severity': 'WARNING'
        }
        
        self._write_log(self.auth_log, log_entry)
        logger.warning(f"AUTH FAILED: {username}@{remote_ip}")
    
    def log_traffic(self, client_id: str, username: str, bytes_sent: int, bytes_received: int):
        """Log traffic statistics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'traffic',
            'client_id': client_id,
            'username': username,
            'bytes_sent': bytes_sent,
            'bytes_received': bytes_received
        }
        
        self._write_log(self.traffic_log, log_entry)
    
    def _write_log(self, filepath: Path, entry: dict):
        """Write log entry to JSONL file"""
        try:
            with open(filepath, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Error writing log: {e}")
    
    def get_recent_connections(self, limit: int = 100):
        """Get recent connection logs"""
        return self._read_recent_logs(self.connections_log, limit)
    
    def get_auth_attempts(self, limit: int = 100):
        """Get recent authentication attempts"""
        return self._read_recent_logs(self.auth_log, limit)
    
    def get_traffic_stats(self, limit: int = 100):
        """Get recent traffic statistics"""
        return self._read_recent_logs(self.traffic_log, limit)
    
    def _read_recent_logs(self, filepath: Path, limit: int):
        """Read recent log entries"""
        if not filepath.exists():
            return []
        
        entries = []
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    entries.append(json.loads(line.strip()))
        except Exception as e:
            logger.error(f"Error reading logs: {e}")
        
        return entries
    
    def generate_report(self) -> dict:
        """Generate comprehensive report"""
        connections = self.get_recent_connections(1000)
        auth_attempts = self.get_auth_attempts(1000)
        traffic = self.get_traffic_stats(1000)
        
        # Calculate statistics
        total_connections = len([c for c in connections if c['event'] == 'connect'])
        total_disconnections = len([c for c in connections if c['event'] == 'disconnect'])
        successful_auths = len([a for a in auth_attempts if a['event'] == 'auth_success'])
        failed_auths = len([a for a in auth_attempts if a['event'] == 'auth_failure'])
        
        total_bytes_sent = sum(t.get('bytes_sent', 0) for t in traffic)
        total_bytes_received = sum(t.get('bytes_received', 0) for t in traffic)
        
        return {
            'summary': {
                'total_connections': total_connections,
                'active_sessions': total_connections - total_disconnections,
                'successful_authentications': successful_auths,
                'failed_authentications': failed_auths,
                'total_data_sent_mb': round(total_bytes_sent / (1024 * 1024), 2),
                'total_data_received_mb': round(total_bytes_received / (1024 * 1024), 2)
            },
            'recent_connections': connections[-10:],
            'security_alerts': [a for a in auth_attempts if a['event'] == 'auth_failure'][-5:]
        }
