import requests
import json
import time
import sqlite3
import random

BASE_URL = "http://localhost:5000"

def print_response(response):
    """Pretty print API response."""
    print("\nResponse:", response.status_code)
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

def create_projects():
    """
    Create 3 projects with a share price of 0.0001 XRP.
    Returns a list of created project details.
    """
    projects = []
    project_details = [
        {
            "name": "Desert Sun Power Plant",
            "description": "20MW solar plant in Arizona desert",
            "location": "Phoenix, AZ",
            "total_power_kw": 20000,
            "total_shares": 1000,
            "share_price_xrp": 0.5
        },
        {
            "name": "Ocean Breeze Solar Farm",
            "description": "15MW solar plant near the coast",
            "location": "San Diego, CA",
            "total_power_kw": 15000,
            "total_shares": 800,
            "share_price_xrp": 0.4
        },
        {
            "name": "Mountain Peak Solar",
            "description": "10MW solar plant in the mountains",
            "location": "Denver, CO",
            "total_power_kw": 10000,
            "total_shares": 600,
            "share_price_xrp": 0.3
        }
    ]
    for pd in project_details:
        print(f"\nCreating project: {pd['name']}")
        response = requests.post(f"{BASE_URL}/create_project", json=pd)
        print_response(response)
        if response.status_code == 200:
            projects.append(response.json())
        time.sleep(5)  # Wait a bit between project creations
    return projects

def invest_by_investor(project_id, investor_id, shares_amount):
    """
    Simulate an investment in a project by a specific investor.
    
    Parameters:
      - project_id: The project to invest in.
      - investor_id: A unique identifier for the investor (or their name).
      - shares_amount: Number of shares to buy.
      
    Returns a dictionary with the investment details (including the buyer wallet address).
    
    Note: Although the API endpoint /buy_shares doesn't process an investor_id,
          we pass it along so that you can map the returned buyer wallet address to the investor.
    """
    payload = {
       "project_id": project_id,
       "shares_amount": shares_amount,
       "investor_id": investor_id  # extra field to track investor locally
    }
    print(f"\nInvestor {investor_id} investing in project {project_id}")
    response = requests.post(f"{BASE_URL}/buy_shares", json=payload)
    print_response(response)
    if response.status_code == 200:
        investment = response.json()
        investment["investor_id"] = investor_id  # attach investor ID locally
        return investment
    return None

def distribute_dividends_for_project(project_id, dividend_rate=0.1):
    """
    Distribute dividends for a given project.
    
    The function retrieves project info to calculate total invested funds (total shares bought * share price)
    and then computes the dividend as a percentage (dividend_rate). It calls the endpoint to distribute
    the dividends, which returns the individual distribution amounts per investor (via their wallet address).
    
    Returns the JSON response from the dividend distribution endpoint.
    """
    # Retrieve project info first
    project_info = get_project_info(project_id)
    share_price = project_info.get("project", {}).get("share_price_xrp", 0)
    total_shares = sum(sh.get("shares_amount", 0) for sh in project_info.get("shareholders", []))
    total_invested = total_shares * share_price
    total_dividend = total_invested * dividend_rate
    print(f"\nProject {project_id} total invested: {total_invested} XRP")
    print(f"Distributing dividends at {dividend_rate*100}% => Total dividend: {total_dividend} XRP")
    dividend_payload = {
         "project_id": project_id,
         "total_dividend_xrp": total_dividend
    }
    response = requests.post(f"{BASE_URL}/distribute_dividends", json=dividend_payload)
    print_response(response)
    return response.json()

def get_project_info(project_id):
    """
    Retrieve detailed information for a project, including its shareholders and dividend history.
    Returns the JSON response.
    """
    print(f"\nRetrieving info for project {project_id}")
    response = requests.get(f"{BASE_URL}/project/{project_id}")
    print_response(response)
    return response.json()

# --- Main demonstration functions that can be called separately ---

def demo_create_projects():
    projects = create_projects()
    print("\nCreated Projects:")
    print(json.dumps(projects, indent=2))
    return projects

def demo_investments(projects):
    """
    For each project, simulate investments by specific investors.
    We'll simulate 12 investors in total (4 per project).
    Returns a mapping of project_id to a list of investment details.
    """
    all_investments = {}
    # Predefine a list of 12 investor IDs
    investor_ids = [f"INV{i+1}" for i in range(12)]
    for i, project in enumerate(projects):
        project_id = project["project_id"]
        print(f"\n--- Investments for Project {project_id} ---")
        investments = []
        # Assign 4 investors per project
        for investor_id in investor_ids[i*4:(i*4)+4]:
            inv_response = invest_by_investor(project_id, investor_id, shares_amount=random.randint(50,200))
            time.sleep(3)
            if inv_response:
                investments.append(inv_response)
            time.sleep(2)
        all_investments[project_id] = investments
    print("\nAll Investments:")
    print(json.dumps(all_investments, indent=2))
    return all_investments

def demo_distribute_dividends(projects):
    """
    For each project, distribute dividends.
    This function uses a 10% dividend rate based on the total invested amount.
    Returns a mapping of project_id to the dividend distribution results.
    """
    all_dividends = {}
    for project in projects:
        project_id = project["project_id"]
        print(f"\n--- Distributing Dividends for Project {project_id} ---")
        div_result = distribute_dividends_for_project(project_id, dividend_rate=0.1)
        all_dividends[project_id] = div_result
        time.sleep(5)
    print("\nDividend Distribution Results:")
    print(json.dumps(all_dividends, indent=2))
    return all_dividends

def demo_get_all_info(projects):
    """
    Retrieve and print the final info for each project.
    """
    for project in projects:
        project_id = project["project_id"]
        info = get_project_info(project_id)
        print(f"\nFinal info for project {project_id}:")
        print(json.dumps(info, indent=2))
    return

# --- If running as a script, you can choose which functions to call ---
if __name__ == "__main__":
    # Uncomment the function(s) you want to run separately.
    
    # 1. Create projects:
    # projects = demo_create_projects()

    # 1. Create projects:
    projects = []
    conn = sqlite3.connect('solar_crowdfunding.db')
    c = conn.cursor()
    c.execute('SELECT id, name, description, location, total_power_kw, total_shares, share_price_xrp, wallet_address FROM projects')
    rows = c.fetchall()
    for row in rows:
        projects.append({
            "project_id": row[0],
            "name": row[1], 
            "description": row[2],
            "location": row[3],
            "total_power_kw": row[4],
            "total_shares": row[5],
            "share_price_xrp": row[6],
            "wallet_address": row[7]
        })
    conn.close()
    
    # 2. Invest in each project (by investor):
    investments = demo_investments(projects)
    
    # 3. Distribute dividends for each project:
    dividends = demo_distribute_dividends(projects)
    
    # 4. Retrieve final info for each project:
    demo_get_all_info(projects)
