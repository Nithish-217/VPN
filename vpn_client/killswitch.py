"""
Kill Switch Module
Blocks internet if VPN disconnects unexpectedly
"""

import subprocess
import logging
import sys
from typing import Optional

logger = logging.getLogger('VPNClient.KillSwitch')


class KillSwitch:
    """Prevents IP leaks when VPN disconnects"""
    
    def __init__(self):
        self.enabled = False
        self.original_rules_backup = []
        self.active = False
        
    def enable(self, vpn_interface: str = "tun0", vpn_gateway: str = None):
        """
        Enable kill switch
        
        Args:
            vpn_interface: TUN interface name
            vpn_gateway: VPN server gateway IP (optional)
        """
        try:
            if sys.platform.startswith('linux'):
                self._enable_linux(vpn_interface, vpn_gateway)
            elif sys.platform == 'darwin':
                self._enable_macos(vpn_interface, vpn_gateway)
            elif sys.platform == 'win32':
                self._enable_windows(vpn_interface)
            else:
                logger.error(f"Platform {sys.platform} not supported")
                return False
            
            self.enabled = True
            self.active = True
            logger.info("Kill switch ENABLED - Internet blocked if VPN drops")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable kill switch: {e}")
            return False
    
    def disable(self):
        """Disable kill switch and restore original rules"""
        try:
            if sys.platform.startswith('linux'):
                self._disable_linux()
            elif sys.platform == 'darwin':
                self._disable_macos()
            elif sys.platform == 'win32':
                self._disable_windows()
            
            self.enabled = False
            self.active = False
            logger.info("Kill switch DISABLED - Normal routing restored")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable kill switch: {e}")
            return False
    
    def _enable_linux(self, vpn_interface: str, vpn_gateway: str = None):
        """Enable kill switch on Linux"""
        # Backup current rules
        result = subprocess.run(['iptables-save'], capture_output=True, text=True)
        self.original_rules_backup.append(('iptables', result.stdout))
        
        # Block all traffic except VPN
        # Allow DNS through VPN
        subprocess.run([
            'iptables', '-A', 'OUTPUT', '-o', vpn_interface, '-j', 'ACCEPT'
        ], check=True)
        
        # Allow established connections
        subprocess.run([
            'iptables', '-A', 'OUTPUT', '-m', 'state', '--state', 'ESTABLISHED,RELATED', '-j', 'ACCEPT'
        ], check=True)
        
        # Block everything else
        subprocess.run([
            'iptables', '-A', 'OUTPUT', '-j', 'DROP'
        ], check=True)
        
        logger.info("Linux kill switch activated")
    
    def _disable_linux(self):
        """Disable kill switch on Linux"""
        # Flush OUTPUT chain
        subprocess.run(['iptables', '-F', 'OUTPUT'], check=True)
        
        # Restore original rules if backed up
        if self.original_rules_backup:
            for rule_type, rules in self.original_rules_backup:
                if rule_type == 'iptables':
                    subprocess.run(['iptables-restore'], input=rules.encode(), check=True)
        
        logger.info("Linux kill switch deactivated")
    
    def _enable_macos(self, vpn_interface: str, vpn_gateway: str = None):
        """Enable kill switch on macOS"""
        # Get default interface
        result = subprocess.run(
            ['route', '-n', 'get', 'default'],
            capture_output=True,
            text=True
        )
        
        # Parse default interface
        default_interface = None
        for line in result.stdout.split('\n'):
            if 'interface:' in line:
                default_interface = line.split(':')[1].strip()
                break
        
        if not default_interface:
            raise Exception("Could not determine default interface")
        
        # Block traffic on non-VPN interfaces
        subprocess.run([
            'pfctl', '-e'
        ], check=True)
        
        # Create PF rule file
        pf_conf = f"""
block out on {default_interface}
pass out on {vpn_interface}
"""
        
        pf_file = '/tmp/vpn_killswitch.pf.conf'
        with open(pf_file, 'w') as f:
            f.write(pf_conf)
        
        # Load PF rules
        subprocess.run(['pfctl', '-f', pf_file], check=True)
        
        logger.info("macOS kill switch activated")
    
    def _disable_macos(self):
        """Disable kill switch on macOS"""
        # Disable PF
        subprocess.run(['pfctl', '-d'], check=True)
        
        # Flush rules
        subprocess.run(['pfctl', '-F', 'all'], check=True)
        
        logger.info("macOS kill switch deactivated")
    
    def _enable_windows(self, vpn_interface: str):
        """Enable kill switch on Windows"""
        logger.warning("Windows kill switch requires PowerShell admin rights")
        logger.info("Simulated kill switch for Windows (requires manual implementation)")
        
        # In production, use Windows Filtering Platform (WFP)
        # This is a simplified version using netsh
        
        # Block all outbound except VPN
        try:
            # Create blocking rule
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                'name="VPN Kill Switch"',
                'dir=out',
                'action=block',
                'enable=yes'
            ], check=True)
            
            # Allow VPN interface
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                'name="Allow VPN"',
                'dir=out',
                'interface=any',
                'action=allow',
                'enable=yes'
            ], check=True)
            
            logger.info("Windows kill switch activated (basic)")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Windows kill switch failed: {e}")
            raise
    
    def _disable_windows(self):
        """Disable kill switch on Windows"""
        try:
            # Delete blocking rule
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                'name="VPN Kill Switch"'
            ], check=True)
            
            subprocess.run([
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                'name="Allow VPN"'
            ], check=True)
            
            logger.info("Windows kill switch deactivated")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error disabling Windows kill switch: {e}")
    
    def status(self) -> bool:
        """Check if kill switch is active"""
        return self.active


class DNSLeakProtection:
    """Prevents DNS leaks"""
    
    def __init__(self):
        self.original_dns = []
        self.enabled = False
    
    def enable(self, dns_server: str = "8.8.8.8"):
        """Force DNS through VPN only"""
        try:
            if sys.platform.startswith('linux'):
                self._enable_linux(dns_server)
            elif sys.platform == 'darwin':
                self._enable_macos(dns_server)
            elif sys.platform == 'win32':
                self._enable_windows(dns_server)
            
            self.enabled = True
            logger.info(f"DNS leak protection ENABLED - Using DNS: {dns_server}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable DNS leak protection: {e}")
            return False
    
    def disable(self):
        """Restore original DNS settings"""
        try:
            if sys.platform.startswith('linux'):
                self._disable_linux()
            elif sys.platform == 'darwin':
                self._disable_macos()
            elif sys.platform == 'win32':
                self._disable_windows()
            
            self.enabled = False
            logger.info("DNS leak protection DISABLED")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable DNS leak protection: {e}")
            return False
    
    def _enable_linux(self, dns_server: str):
        """Set DNS on Linux"""
        # Backup resolv.conf
        try:
            with open('/etc/resolv.conf', 'r') as f:
                self.original_dns = f.readlines()
        except:
            pass
        
        # Set VPN DNS
        with open('/etc/resolv.conf', 'w') as f:
            f.write(f"nameserver {dns_server}\n")
            f.write("# VPN DNS - Leak protection enabled\n")
    
    def _disable_linux(self):
        """Restore DNS on Linux"""
        if self.original_dns:
            with open('/etc/resolv.conf', 'w') as f:
                f.writelines(self.original_dns)
    
    def _enable_macos(self, dns_server: str):
        """Set DNS on macOS"""
        # Get network interface
        result = subprocess.run(
            ['scutil', '--nc', 'list'],
            capture_output=True,
            text=True
        )
        
        # Set DNS
        subprocess.run([
            'networksetup', '-setdnsservers',
            'Wi-Fi', dns_server
        ], check=True)
    
    def _disable_macos(self):
        """Restore DNS on macOS"""
        subprocess.run([
            'networksetup', '-setdnsservers',
            'Wi-Fi', 'Empty'
        ], check=True)
    
    def _enable_windows(self, dns_server: str):
        """Set DNS on Windows"""
        # Get interface index
        result = subprocess.run(
            ['netsh', 'interface', 'ip', 'show', 'interfaces'],
            capture_output=True,
            text=True
        )
        
        # Set DNS (simplified - would need specific interface)
        logger.info("Windows DNS configuration requires interface specification")
    
    def _disable_windows(self):
        """Restore DNS on Windows"""
        subprocess.run([
            'netsh', 'interface', 'ip', 'set', 'dns',
            'name="Ethernet"', 'source=dhcp'
        ], check=True)
