#!/usr/bin/env python3
"""
Test Fixed Cybersecurity Dashboard
Verify all JSON API endpoints are working correctly
"""

import requests
import json
import time

def test_dashboard_apis():
    """Test all dashboard API endpoints"""
    print("🛡️  Testing Fixed Cybersecurity Dashboard APIs")
    print("=" * 50)
    
    base_url = "http://localhost:8081"
    
    # Test endpoints
    endpoints = [
        ("/api/stats", "Statistics"),
        ("/api/clients", "Client Information"),
        ("/api/alerts", "Security Alerts"),
        ("/api/security", "Security Status"),
        ("/api/performance", "Performance Metrics"),
        ("/api/network", "Network Information"),
        ("/api/messages", "Message History")
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        try:
            print(f"\n🔍 Testing {name}...")
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    results[endpoint] = {
                        'status': 'SUCCESS',
                        'status_code': response.status_code,
                        'data_keys': list(data.keys()) if isinstance(data, dict) else 'non-dict response'
                    }
                    print(f"✅ {name}: SUCCESS")
                    print(f"   Status: {response.status_code}")
                    print(f"   Data keys: {results[endpoint]['data_keys']}")
                except json.JSONDecodeError as e:
                    results[endpoint] = {
                        'status': 'JSON_ERROR',
                        'status_code': response.status_code,
                        'error': str(e)
                    }
                    print(f"❌ {name}: JSON ERROR - {e}")
            else:
                results[endpoint] = {
                    'status': 'HTTP_ERROR',
                    'status_code': response.status_code,
                    'error': response.text
                }
                print(f"❌ {name}: HTTP ERROR {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results[endpoint] = {
                'status': 'CONNECTION_ERROR',
                'error': str(e)
            }
            print(f"❌ {name}: CONNECTION ERROR - {e}")
    
    # Test broadcast message
    print(f"\n📡 Testing Broadcast Message...")
    try:
        broadcast_data = {"message": "Test secure message from API test"}
        response = requests.post(
            f"{base_url}/api/broadcast",
            json=broadcast_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Broadcast: SUCCESS")
            print(f"   Response: {result.get('message', 'No message')}")
        else:
            print(f"❌ Broadcast: HTTP ERROR {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Broadcast: ERROR - {e}")
    
    # Summary
    print(f"\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    success_count = sum(1 for r in results.values() if r['status'] == 'SUCCESS')
    total_count = len(results)
    
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print(f"\n🎉 ALL TESTS PASSED! Dashboard is working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Check the details above.")
    
    print(f"\n🌐 Dashboard URL: {base_url}")
    print(f"🔐 Features: Real-time monitoring, Security alerts, Message broadcasting")
    
    return success_count == total_count

if __name__ == "__main__":
    success = test_dashboard_apis()
    if success:
        print(f"\n🛡️  Cybersecurity Dashboard is FULLY OPERATIONAL!")
    else:
        print(f"\n🔧 Dashboard needs attention - see test results above.")
