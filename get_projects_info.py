import sqlite3
import json

def get_all_project_info():
    """
    Retrieve all information about projects, shareholders, and dividends from the database.
    Returns a dictionary with all the information.
    """
    conn = sqlite3.connect('solar_crowdfunding.db')
    c = conn.cursor()
    
    # Get all projects
    c.execute('''
        SELECT * FROM projects
    ''')
    projects = []
    for row in c.fetchall():
        project = {
            "project_id": row[0],
            "name": row[1],
            "description": row[2],
            "location": row[3],
            "total_power_kw": row[4],
            "total_shares": row[5],
            "share_price_xrp": row[6],
            "wallet_address": row[7],
            "status": row[8],
            "created_at": row[9]
        }
        
        # Get shareholders for this project
        c.execute('''
            SELECT id, holder_wallet_address, shares_amount, purchase_date
            FROM shareholders
            WHERE project_id = ?
        ''', (row[0],))
        shareholders = []
        for sh_row in c.fetchall():
            shareholders.append({
                "shareholder_id": sh_row[0],
                "wallet_address": sh_row[1],
                "shares_amount": sh_row[2],
                "purchase_date": sh_row[3]
            })
        project["shareholders"] = shareholders
        
        # Get dividends for this project
        c.execute('''
            SELECT id, amount_xrp, distribution_date, status
            FROM dividends
            WHERE project_id = ?
        ''', (row[0],))
        dividends = []
        for div_row in c.fetchall():
            dividends.append({
                "dividend_id": div_row[0],
                "amount_xrp": div_row[1],
                "distribution_date": div_row[2],
                "status": div_row[3]
            })
        project["dividends"] = dividends
        
        projects.append(project)
    
    conn.close()
    return projects

if __name__ == "__main__":
    # Get all information
    all_info = get_all_project_info()
    
    # Print the information in a readable format
    print("\nAll Project Information:")
    print(json.dumps(all_info, indent=2))
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total Projects: {len(all_info)}")
    total_shares = sum(project["total_shares"] for project in all_info)
    total_invested = sum(project["total_shares"] * project["share_price_xrp"] for project in all_info)
    total_dividends = sum(sum(div["amount_xrp"] for div in project["dividends"]) for project in all_info)
    print(f"Total Shares Across All Projects: {total_shares}")
    print(f"Total Invested (XRP): {total_invested}")
    print(f"Total Dividends Distributed (XRP): {total_dividends}")
    
    # Print details for each project
    for project in all_info:
        print(f"\nProject: {project['name']}")
        print(f"Status: {project['status']}")
        print(f"Shareholders: {len(project['shareholders'])}")
        print(f"Dividend Distributions: {len(project['dividends'])}")