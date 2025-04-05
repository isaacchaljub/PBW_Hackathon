import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_response(response):
    """Pretty print API response"""
    print("\nResponse:", response.status_code)
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

def wait_for_server(max_attempts=5):
    """Wait until the Flask server is ready"""
    for attempt in range(max_attempts):
        try:
            response = requests.post(f"{BASE_URL}/create_project", json={
                "name": "Health Check Project",
                "description": "Test",
                "location": "Test",
                "total_power_kw": 1000,
                "total_shares": 1000,
                "share_price_xrp": 0.000001
            })
            if response.status_code != 500:
                return True
        except requests.exceptions.ConnectionError:
            pass
        print(f"Waiting for server (attempt {attempt+1}/{max_attempts})...")
        time.sleep(2)
    return False

def demo_workflow():
    """Demonstrate the complete solar crowdfunding workflow"""
    if not wait_for_server():
        print("❌ Server not responding. Make sure to run solar_crowdfunding.py first!")
        return False

    print("\n🌟 1. Creating a Solar Plant Project...")
    project_data = {
        "name": "Desert Sun Power Plant",
        "description": "20MW solar plant in Arizona desert",
        "location": "Phoenix, AZ",
        "total_power_kw": 20000,
        "total_shares": 1000,
        "share_price_xrp": 0.000001  # extremely low for testing
    }
    response = requests.post(f"{BASE_URL}/create_project", json=project_data)
    print_response(response)
    if response.status_code == 200:
        project_id = response.json()["project_id"]
        print(f"\n✅ Project created! ID: {project_id}")
        
        print("\n⏳ Waiting for project wallet funding...")
        time.sleep(10)
        
        print("\n🌟 2. Buying Shares...")
        buy_data = {
            "project_id": project_id,
            "shares_amount": 2  # Buying 2 shares
        }
        response = requests.post(f"{BASE_URL}/buy_shares", json=buy_data)
        print_response(response)
        if response.status_code == 200:
            print("\n✅ Shares purchased!")
            
            print("\n⏳ Waiting for share purchase to settle...")
            time.sleep(10)
            
            print("\n🌟 3. Checking Project Details...")
            response = requests.get(f"{BASE_URL}/project/{project_id}")
            print_response(response)
            
            print("\n🌟 4. Distributing Dividends...")
            dividend_data = {
                "project_id": project_id,
                "total_dividend_xrp": 0.000001
            }
            response = requests.post(f"{BASE_URL}/distribute_dividends", json=dividend_data)
            print_response(response)
            if response.status_code == 200:
                print("\n✅ Dividends distributed!")
                print("\n⏳ Waiting for dividend distribution to settle...")
                time.sleep(10)
                
                print("\n🌟 5. Final Project State...")
                response = requests.get(f"{BASE_URL}/project/{project_id}")
                print_response(response)
                return True
    return False

if __name__ == "__main__":
    print("🚀 Starting Solar Crowdfunding Demo...")
    success = demo_workflow()
    if success:
        print("\n✨ Demo completed successfully!")
    else:
        print("\n❌ Demo failed!")
