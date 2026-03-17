# VPN Deployment Guide

## 🌐 Deployment Scenarios

This guide covers three common deployment scenarios:

1. **Home Network** - Server on home network, client on mobile device
2. **Cloud VPS** - Server on cloud provider (AWS, DigitalOcean, etc.)
3. **Corporate Network** - Enterprise deployment with multiple clients

---

## Scenario 1: Home Network Setup

### Network Diagram

```
Internet
   │
   ▼
┌──────────────┐
│ Home Router  │ (Public IP: dynamic)
│ 192.168.1.1  │
└──────┬───────┘
       │
   ┌───┴────┐
   │        │
┌──▼──┐  ┌──▼──────┐
│ PC  │  │ VPN     │ (192.168.1.50)
│     │  │ Server  │
└─────┘  └─────────┘
```

### Step-by-Step Setup

#### 1. Configure Port Forwarding

Access your router admin panel (usually `192.168.1.1`):

1. Navigate to **Port Forwarding** or **Virtual Server**
2. Add new rule:
   - **Service Name:** VPN
   - **External Port:** 8080
   - **Internal Port:** 8080
   - **Internal IP:** 192.168.1.50
   - **Protocol:** TCP

#### 2. Find Your Public IP

On the server machine:
```bash
# Linux/macOS
curl ifconfig.me

# Windows PowerShell
(Invoke-WebRequest -Uri "https://ifconfig.me/ip").Content
```

Note this IP address (e.g., `73.45.123.89`)

#### 3. Configure Dynamic DNS (Optional but Recommended)

Since home IPs change, use DDNS:

**Option A: No-IP (Free)**
1. Sign up at https://www.noip.com/
2. Create hostname (e.g., `myvpn.no-ip.org`)
3. Install DDNS updater on server:
   ```bash
   sudo apt install noip2  # Linux
   ```

**Option B: DuckDNS (Free)**
1. Sign up at https://www.duckdns.org/
2. Get your token
3. Update script:
   ```bash
   curl "https://www.duckdns.org/update?domains=myvpn&token=YOUR_TOKEN"
   ```

#### 4. Start Server

```bash
cd /path/to/vpn_project
python vpn_server_main.py
```

#### 5. Configure Client

Edit `config/client.conf`:
```ini
SERVER_HOST=your-public-ip-or-ddns-hostname
SERVER_PORT=8080
USERNAME=user1
PASSWORD=password123
```

Example:
```ini
SERVER_HOST=myvpn.no-ip.org
# or
SERVER_HOST=73.45.123.89
```

#### 6. Test Connection

From external network (not same WiFi):
```bash
sudo python vpn_client_main.py
```

---

## Scenario 2: Cloud VPS Deployment

### Provider Options

| Provider | Starting Price | Recommended Instance |
|----------|---------------|---------------------|
| DigitalOcean | $5/month | Basic Droplet |
| AWS | Free tier (12mo) | t2.micro |
| Linode | $5/month | Nanode |
| Vultr | $2.50/month | Cloud Compute |

### AWS EC2 Setup

#### 1. Launch Instance

1. Go to AWS Console → EC2
2. Click "Launch Instance"
3. Choose AMI: **Ubuntu Server 22.04 LTS**
4. Instance type: **t2.micro** (free tier eligible)
5. Configure details (default is fine)
6. Add storage: 8GB GP2
7. Configure security group:
   ```
   Type: SSH
   Protocol: TCP
   Port: 22
   Source: 0.0.0.0/0
   
   Type: Custom TCP
   Protocol: TCP
   Port: 8080
   Source: 0.0.0.0/0
   ```
8. Create key pair (download `.pem` file)
9. Launch instance

#### 2. Connect to Server

```bash
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@YOUR_SERVER_IP
```

#### 3. Install Python and Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install -y python3 python3-pip

# Install git
sudo apt install -y git

# Clone or upload your project
git clone <your-repo-url>
cd VPN_project

# Install dependencies
pip3 install -r requirements.txt
```

#### 4. Configure Server

```bash
python3 setup_server.py
```

Edit `config/server.conf`:
```ini
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
AUTH_ENABLED=True
```

#### 5. Run as Systemd Service

Create service file:
```bash
sudo nano /etc/systemd/system/vpn-server.service
```

Content:
```ini
[Unit]
Description=VPN Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/VPN_project
ExecStart=/usr/bin/python3 /home/ubuntu/VPN_project/vpn_server_main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vpn-server
sudo systemctl start vpn-server
sudo systemctl status vpn-server
```

#### 6. Configure Firewall (UFW)

```bash
sudo ufw allow 22/tcp
sudo ufw allow 8080/tcp
sudo ufw enable
sudo ufw status
```

#### 7. Configure Client

Edit `config/client.conf` on your device:
```ini
SERVER_HOST=YOUR_SERVER_PUBLIC_IP
SERVER_PORT=8080
USERNAME=user1
PASSWORD=password123
```

Find your server's public IP:
```bash
# On server
curl ifconfig.me
```

---

## Scenario 3: Corporate Network Deployment

### Architecture

```
                    Internet
                        │
                        ▼
                ┌───────────────┐
                │ Firewall      │
                │ (Port 8080)   │
                └───────┬───────┘
                        │
                ┌───────▼───────┐
                │ Load Balancer │ (optional)
                └───────┬───────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
   │ VPN     │    │ VPN     │    │ VPN     │
   │ Server 1│    │ Server 2│    │ Server 3│
   └─────────┘    └─────────┘    └─────────┘
```

### High Availability Setup

#### 1. Multiple Server Instances

Deploy on multiple machines:

**Server 1 (Primary):**
```ini
# config/server.conf
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
```

**Server 2 (Secondary):**
```ini
SERVER_HOST=0.0.0.0
SERVER_PORT=8081
```

**Server 3 (Tertiary):**
```ini
SERVER_HOST=0.0.0.0
SERVER_PORT=8082
```

#### 2. Load Balancer Configuration (HAProxy)

Install HAProxy:
```bash
sudo apt install haproxy
```

Configure `/etc/haproxy/haproxy.cfg`:
```
frontend vpn_frontend
    bind *:8080
    mode tcp
    default_backend vpn_servers

backend vpn_servers
    mode tcp
    balance roundrobin
    server vpn1 192.168.1.50:8080 check
    server vpn2 192.168.1.51:8080 check
    server vpn3 192.168.1.52:8080 check
```

Start HAProxy:
```bash
sudo systemctl start haproxy
sudo systemctl enable haproxy
```

#### 3. Centralized Authentication

Use LDAP/Active Directory:

Modify `vpn_server/auth.py`:
```python
import ldap

class Authenticator:
    def __init__(self):
        self.ldap_server = "ldap://ad.company.com"
        self.base_dn = "dc=company,dc=com"
    
    async def verify(self, username, password):
        try:
            conn = ldap.initialize(self.ldap_server)
            search_filter = f"(uid={username})"
            result = conn.search_s(self.base_dn, ldap.SUBTREE, search_filter)
            
            if result:
                user_dn = result[0][0]
                conn.simple_bind_s(user_dn, password)
                return True
            return False
        except:
            return False
```

#### 4. Monitoring and Logging

**Centralized Logging (ELK Stack):**

Install Filebeat on each server:
```bash
sudo apt install filebeat
```

Configure `/etc/filebeat/filebeat.yml`:
```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/vpn/*.log

output.logstash:
  hosts: ["logstash.company.com:5044"]
```

**Monitoring with Prometheus:**

Install exporter:
```bash
sudo apt install prometheus-node-exporter
```

Scrape metrics on Prometheus server:
```yaml
scrape_configs:
  - job_name: 'vpn_servers'
    static_configs:
      - targets: ['vpn1:8080', 'vpn2:8080', 'vpn3:8080']
```

---

## 🔒 Security Hardening

### For All Deployments

#### 1. Firewall Rules

**Linux (iptables):**
```bash
# Allow VPN port
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# NAT rules
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i tun0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o tun0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

**Windows (PowerShell):**
```powershell
# Allow VPN port
New-NetFirewallRule -DisplayName "VPN Server" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow

# Enable IP forwarding
Set-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters -Name IpEnableRouter -Value 1
```

#### 2. Fail2Ban (Brute Force Protection)

Install:
```bash
sudo apt install fail2ban
```

Create filter `/etc/fail2ban/filter.d/vpn-auth.conf`:
```ini
[Definition]
failregex = .*Authentication failed.*
ignoreregex =
```

Create jail `/etc/fail2ban/jail.local`:
```ini
[vpn-auth]
enabled = true
port = 8080
filter = vpn-auth
logpath = /var/log/vpn/*.log
maxretry = 5
bantime = 3600
```

Start:
```bash
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

#### 3. SSL/TLS Wrapper (Optional)

Add TLS layer with stunnel:

Install:
```bash
sudo apt install stunnel4
```

Configure `/etc/stunnel/stunnel.conf`:
```ini
[vpn-tls]
accept = 443
connect = 8080
cert = /etc/ssl/certs/vpn.crt
key = /etc/ssl/private/vpn.key
```

Generate certificate:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/vpn.key \
  -out /etc/ssl/certs/vpn.crt
```

Start:
```bash
sudo systemctl start stunnel4
```

---

## 📊 Performance Tuning

### Server Optimization

#### 1. System Limits

Edit `/etc/security/limits.conf`:
```
* soft nofile 65536
* hard nofile 65536
root soft nofile 65536
root hard nofile 65536
```

#### 2. Kernel Parameters

Edit `/etc/sysctl.conf`:
```
net.core.somaxconn = 65536
net.ipv4.tcp_max_syn_backlog = 65536
net.core.netdev_max_backlog = 65536
net.ipv4.ip_local_port_range = 1024 65535
```

Apply:
```bash
sudo sysctl -p
```

#### 3. TCP Optimization

For high-latency networks:
```bash
sudo sysctl -w net.ipv4.tcp_window_scaling=1
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
```

---

## 🧪 Testing and Verification

### Connection Tests

#### 1. Port Reachability

From client machine:
```bash
# Test TCP connection
telnet SERVER_IP 8080

# Or using netcat
nc -zv SERVER_IP 8080

# Or using nmap
nmap -p 8080 SERVER_IP
```

Expected output:
```
Connected to SERVER_IP.
```

#### 2. Speed Test

With VPN connected:
```bash
# Download test
curl -o /dev/null http://speedtest.wdc01.softlayer.com/downloads/test10.zip

# Upload test (requires iperf3)
iperf3 -c SERVER_IP -p 8080
```

#### 3. Leak Test

Check for DNS leaks:
```bash
# Visit these sites while VPN is active
# https://dnsleaktest.com
# https://ipleak.net
```

Your visible IP should be the VPN server's IP, not your real IP.

---

## 🛠️ Maintenance

### Regular Tasks

#### Daily
- Check logs for errors
- Monitor disk space
- Verify service is running

#### Weekly
- Review authentication logs
- Check for failed login attempts
- Update system packages

#### Monthly
- Rotate credentials
- Review firewall rules
- Backup configuration
- Test failover (if HA setup)

### Log Rotation

Create `/etc/logrotate.d/vpn`:
```
/var/log/vpn/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 root root
    postrotate
        systemctl reload rsyslog
    endscript
}
```

---

## 📱 Mobile Client Setup

### Android

1. Install Termux from F-Droid
2. Install Python in Termux:
   ```bash
   pkg install python
   ```
3. Transfer VPN client files
4. Install dependencies:
   ```bash
   pip install cryptography
   ```
5. Run client (requires root for TUN):
   ```bash
   python vpn_client_main.py
   ```

### iOS

Requires jailbreak or use alternative apps like:
- OpenVPN Connect
- WireGuard

(Our current implementation doesn't support iOS directly)

---

## 🎯 Troubleshooting by Scenario

### Home Network Issues

**Problem:** Can't connect from outside
- Check port forwarding is enabled
- Verify public IP hasn't changed
- Ensure firewall allows port 8080
- Try disabling router's SPI firewall temporarily

**Problem:** Slow speeds
- Check upload bandwidth at home
- Reduce encryption overhead (if needed)
- Use Ethernet instead of WiFi for server

### Cloud VPS Issues

**Problem:** Connection timeout
- Check security group rules
- Verify instance is running
- Check public IP is correct
- Test SSH connectivity first

**Problem:** High latency
- Choose region closest to you
- Consider CDN or edge locations
- Optimize TCP settings

### Corporate Issues

**Problem:** Load balancer not distributing
- Check health checks are passing
- Verify backend servers are healthy
- Review HAProxy stats page

**Problem:** Authentication failures
- Test LDAP connectivity
- Verify service account permissions
- Check firewall between VPN and AD

---

## 📞 Support Resources

### Documentation
- Official Python docs: https://docs.python.org/3/
- Cryptography library: https://cryptography.io/
- asyncio reference: https://docs.python.org/3/library/asyncio.html

### Community
- Stack Overflow: Tag `vpn`, `python`, `encryption`
- Reddit: r/networking, r/selfhosted
- GitHub Issues for this project

### Monitoring Tools
- Grafana dashboards
- Prometheus metrics
- ELK stack for logs

---

**End of Deployment Guide**
