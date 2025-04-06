import sqlite3

def clear_tables():
    """Clear all data from the database tables"""
    conn = sqlite3.connect('solar_crowdfunding.db')
    c = conn.cursor()
    
    # Clear tables in the correct order to respect foreign key constraints
    c.execute('DELETE FROM dividends')
    c.execute('DELETE FROM shareholders')
    #c.execute('DELETE FROM projects')
    
    conn.commit()
    conn.close()
    print("All tables have been cleared successfully!")

if __name__ == "__main__":
    clear_tables() 