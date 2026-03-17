# VPN Project - Quick Start Commands

## 🚀 Running the VPN Server with Dashboard

### Option 1: Enhanced Server (Recommended)
```powershell
python vpn_server_main_enhanced.py
```
- Starts VPN Server on `0.0.0.0:8080`
- Starts Monitoring Dashboard on `http://localhost:8081`
- Features: Real-time charts, traffic monitoring, security alerts

### Option 2: Basic Server
```powershell
python vpn_server_main.py
```
- Starts VPN Server on `0.0.0.0:8080`
- No dashboard included

---

## 💻 Running the VPN Client

### Option 1: Full Client
```powershell
python vpn_client_main.py
```

### Option 2: Simple Client
```powershell
python vpn_client_simple.py
```

---

## 📊 Accessing the Dashboard

Once the server is running, open your browser to:
**http://localhost:8081**

### Dashboard Features:
- ✅ Real-time traffic charts (updates every 2 seconds)
- ✅ Live connection history
- ✅ Active clients list
- ✅ Security alerts
- ✅ Bandwidth statistics
- ✅ Reset to Defaults button

---

## 🔧 Common Issues

### Port Already in Use Error
If you get "OSError 10048" or port binding errors:
```powershell
# Kill all Python processes
Stop-Process -Name python -Force

# Then restart the server
python vpn_server_main_enhanced.py
```

### Dashboard Not Loading
1. Make sure server is running
2. Check if port 8081 is accessible
3. Hard refresh browser: `Ctrl + Shift + R`

---

## 🎯 Complete Workflow

1. **Start Server** (Terminal 1):
   ```powershell
   python vpn_server_main_enhanced.py
   ```

2. **Start Client** (Terminal 2):
   ```powershell
   python vpn_client_main.py
   ```

3. **Open Dashboard** (Browser):
   ```
   http://localhost:8081
   ```

---

## 📋 Default Configuration

- **VPN Server**: `0.0.0.0:8080`
- **Dashboard**: `http://localhost:8081`
- **Max Clients**: Unlimited (concurrent)
- **Authentication**: Enabled
- **Default Credentials**:
  - Username: `user1`, Password: `password123`
  - Username: `admin`, Password: `admin123`

---

## 📨 Sending Messages from Server to Client

### Option 1: Direct Server Console (Recommended)
```powershell
# Server is already running with built-in messaging
# Just type messages directly in the server terminal!
```
1. Start server: `python vpn_server_main_enhanced.py`
2. Start client: `python vpn_client_main.py`
3. **Type any message in server terminal and press Enter**
4. Message instantly appears on client with 🔔 prefix

### Option 2: Interactive Message Sender
```powershell
python send_server_message.py
```

### Option 3: Automated Test
```powershell
python send_test_message.py
```

### Message Features:
- ✅ **Real-time delivery** - Messages appear instantly
- ✅ **Broadcast to all clients** - One message reaches everyone
- ✅ **Visual notification** - 🔔 bell icon prefix
- ✅ **Server console integration** - Type directly in server window

### Example Test:
1. **Server Console**: Type "Hello everyone!" and press Enter
2. **Client Console**: Shows "🔔 SERVER MESSAGE: Hello everyone!"
3. **Dashboard**: Shows increased traffic activity

---

## � Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.
