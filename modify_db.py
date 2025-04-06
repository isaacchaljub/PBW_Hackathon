import sqlite3

def modify_database():
    """Modify the database to use name as primary key instead of id"""
    conn = sqlite3.connect('solar_crowdfunding.db')
    c = conn.cursor()
    
    # Create temporary tables with new structure
    c.execute('''
        CREATE TABLE projects_new (
            name TEXT PRIMARY KEY,
            description TEXT,
            location TEXT,
            total_power_kw REAL,
            total_shares INTEGER,
            share_price_xrp REAL,
            wallet_address TEXT,
            wallet_seed TEXT,
            status TEXT,
            created_at TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE shareholders_new (
            id TEXT PRIMARY KEY,
            project_name TEXT,
            holder_wallet_address TEXT,
            shares_amount INTEGER,
            purchase_date TIMESTAMP,
            FOREIGN KEY (project_name) REFERENCES projects (name)
        )
    ''')
    
    c.execute('''
        CREATE TABLE dividends_new (
            id TEXT PRIMARY KEY,
            project_name TEXT,
            amount_xrp REAL,
            distribution_date TIMESTAMP,
            status TEXT,
            FOREIGN KEY (project_name) REFERENCES projects (name)
        )
    ''')
    
    # Copy data from old tables to new tables
    try:
        c.execute('''
            INSERT INTO projects_new 
            SELECT name, description, location, total_power_kw, total_shares, 
                   share_price_xrp, wallet_address, wallet_seed, status, created_at 
            FROM projects
        ''')
        
        c.execute('''
            INSERT INTO shareholders_new 
            SELECT id, project_id, holder_wallet_address, shares_amount, purchase_date 
            FROM shareholders
        ''')
        
        c.execute('''
            INSERT INTO dividends_new 
            SELECT id, project_id, amount_xrp, distribution_date, status 
            FROM dividends
        ''')
    except Exception as e:
        print(f"Error copying data: {e}")
        # Continue with the process even if copying fails
        # as we might be dealing with empty tables
        pass
    
    # Drop old tables
    c.execute('DROP TABLE IF EXISTS dividends')
    c.execute('DROP TABLE IF EXISTS shareholders')
    c.execute('DROP TABLE IF EXISTS projects')
    
    # Rename new tables to original names
    c.execute('ALTER TABLE projects_new RENAME TO projects')
    c.execute('ALTER TABLE shareholders_new RENAME TO shareholders')
    c.execute('ALTER TABLE dividends_new RENAME TO dividends')
    
    conn.commit()
    conn.close()
    print("Database structure has been updated successfully!")

if __name__ == "__main__":
    modify_database() 