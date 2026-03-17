# Quick Start Guide

## 🚀 Get VPN Running in 5 Minutes

### Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

### Step 2: Setup Server (1 minute)

```bash
python setup_server.py
```

### Step 3: Setup Client (1 minute)

```bash
python setup_client.py
```

### Step 4: Configure (1 minute)

**On Server Machine:**
- Edit `config/server.conf` if needed
- Note your server's public IP address

**On Client Machine:**
- Edit `config/client.conf`
- Change `SERVER_HOST` to your server's IP

Example:
```ini
SERVER_HOST=your.server.ip.address
USERNAME=user1
PASSWORD=password123
```

### Step 5: Run! (30 seconds)

**Terminal 1 - Start Server:**
```bash
python vpn_server_main.py
```

**Terminal 2 - Start Client (as Admin/Sudo):**
```bash
# Linux/macOS
sudo python vpn_client_main.py

# Windows (PowerShell as Administrator)
python vpn_client_main.py
```

## ✅ Verify Connection

You should see:

**Server logs:**
```
INFO - VPN Server started on 0.0.0.0:8080
INFO - New connection from ('192.168.1.100', 54321)
INFO - User user1 authenticated successfully
INFO - Key exchange completed for ('192.168.1.100', 54321)
```

**Client logs:**
```
INFO - Connecting to 192.168.1.50:8080
INFO - Connected to server
INFO - Authentication successful
INFO - Key exchange completed
INFO - TUN interface tun0 created
```

## 🔍 Test the Tunnel

With client connected, try:

```bash
# Check your routing
ip route show

# Or on Windows
route print

# Your default route should point through the VPN tunnel
```

## 🛑 Stop VPN

Press `Ctrl+C` in both terminal windows.

---

**Next Steps:** See README.md for detailed documentation.
