from flask import Flask, request, jsonify
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.models.requests import AccountInfo
from xrpl.transaction import autofill_and_sign, submit_and_wait
from xrpl.core.keypairs import generate_seed
import uuid
import json
from datetime import datetime
import sqlite3
import os
import requests
import time

app = Flask(__name__)

# Global client variable; will be initialized from config
client = None

def ensure_client():
    """Ensure XRPL client is initialized"""
    global client
    if client is None:
        client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
    return client

def wait_for_wallet_funding(client, wallet_address, max_attempts=10):
    """Wait for a wallet to be funded and return True if active"""
    for attempt in range(max_attempts):
        try:
            acct_info = AccountInfo(
                account=wallet_address,
                ledger_index="validated"
            )
            response = client.request(acct_info)
            balance = int(response.result['account_data']['Balance']) / 1000000
            print(f"Wallet {wallet_address} active with {balance} XRP")
            return True
        except Exception as e:
            print(f"Waiting for wallet funding (attempt {attempt+1}/{max_attempts})...")
            time.sleep(2)
    print("Wallet funding confirmation timeout.")
    return False

def create_funded_wallet(max_retries=3):
    """Create and fund a new wallet using the testnet faucet with retries"""
    ensure_client()
    wallet = Wallet.create()
    print(f"Created new wallet: {wallet.classic_address}")
    faucet_url = "https://faucet.altnet.rippletest.net/accounts"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(faucet_url, json={"destination": wallet.classic_address}, timeout=10)
            if response.status_code == 200:
                if wait_for_wallet_funding(client, wallet.classic_address):
                    return wallet
                else:
                    raise Exception("Wallet funding confirmation timeout")
            else:
                print(f"Faucet call failed with status {response.status_code} on attempt {attempt+1}/{max_retries}")
        except Exception as e:
            print(f"Faucet attempt {attempt+1} failed: {e}")
        time.sleep(5)
    raise Exception("Failed to fund wallet after multiple attempts")

def check_wallet_balance(wallet_address):
    """Return the XRP balance of a wallet (in XRP)"""
    try:
        ensure_client()
        acct_info = AccountInfo(
            account=wallet_address,
            ledger_index="validated"
        )
        response = client.request(acct_info)
        balance_xrp = int(response.result['account_data']['Balance']) / 1000000
        return balance_xrp
    except Exception as e:
        print(f"Error checking wallet balance: {e}")
        return 0

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('solar_crowdfunding.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
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
        CREATE TABLE IF NOT EXISTS shareholders (
            id TEXT PRIMARY KEY,
            project_id TEXT,
            holder_wallet_address TEXT,
            shares_amount INTEGER,
            purchase_date TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS dividends (
            id TEXT PRIMARY KEY,
            project_id TEXT,
            amount_xrp REAL,
            distribution_date TIMESTAMP,
            status TEXT,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

@app.route("/create_project", methods=["POST"])
def create_project():
    """Create a new solar plant project and its dedicated wallet"""
    try:
        data = request.get_json(force=True)
        project_id = str(uuid.uuid4())
        # For testing, enforce a low share price so that faucet-funded wallets have enough funds.
        if data.get('share_price_xrp', 0) > 1:
            return jsonify({"error": "Share price too high for testing. Please use 1 XRP or less per share."}), 400
        
        project_wallet = create_funded_wallet()
        print(f"Created project wallet: {project_wallet.classic_address}")
        balance = check_wallet_balance(project_wallet.classic_address)
        print(f"Project wallet balance: {balance} XRP")
        
        conn = sqlite3.connect('solar_crowdfunding.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO projects (
                id, name, description, location, total_power_kw,
                total_shares, share_price_xrp, wallet_address,
                wallet_seed, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            data['name'],
            data['description'],
            data['location'],
            data['total_power_kw'],
            data['total_shares'],
            data['share_price_xrp'],
            project_wallet.classic_address,
            project_wallet.seed,
            'FUNDING',
            datetime.now()
        ))
        conn.commit()
        conn.close()
        
        return jsonify({
            "project_id": project_id,
            "wallet_address": project_wallet.classic_address,
            "share_price_xrp": data['share_price_xrp'],
            "total_shares": data['total_shares'],
            "wallet_balance": balance
        }), 200
        
    except Exception as e:
        print(f"Error in create_project: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/buy_shares", methods=["POST"])
def buy_shares():
    """Purchase shares in a project using XRP from a newly created buyer wallet"""
    try:
        data = request.get_json(force=True)
        project_id = data['project_id']
        shares_amount = int(data['shares_amount'])
        
        conn = sqlite3.connect('solar_crowdfunding.db')
        c = conn.cursor()
        c.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = c.fetchone()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Calculate total XRP needed based on share price.
        xrp_amount = shares_amount * project[6]  # share_price_xrp from db
        drops_amount = int(xrp_amount * 1000000)  # XRP -> drops conversion
        
        buyer_wallet = create_funded_wallet()
        print(f"Created buyer wallet: {buyer_wallet.classic_address}")
        buyer_balance = check_wallet_balance(buyer_wallet.classic_address)
        if buyer_balance < xrp_amount:
            return jsonify({
                "error": f"Insufficient funds. Need {xrp_amount} XRP but wallet only has {buyer_balance} XRP",
                "buyer_address": buyer_wallet.classic_address,
                "buyer_seed": buyer_wallet.seed
            }), 400
        
        payment = Payment(
            account=buyer_wallet.classic_address,
            destination=project[7],  # project wallet address
            amount=str(drops_amount)
        )
        # NOTE: Corrected parameter order: client first, then buyer_wallet.
        payment_prepared = autofill_and_sign(payment, client, buyer_wallet)
        payment_result = submit_and_wait(payment_prepared, client)
        if payment_result.result.get('meta', {}).get('TransactionResult') != 'tesSUCCESS':
            raise Exception(f"Transaction failed: {payment_result.result}")
        
        c.execute('''
            INSERT INTO shareholders (
                id, project_id, holder_wallet_address,
                shares_amount, purchase_date
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()),
            project_id,
            buyer_wallet.classic_address,
            shares_amount,
            datetime.now()
        ))
        conn.commit()
        conn.close()
        
        buyer_final_balance = check_wallet_balance(buyer_wallet.classic_address)
        project_final_balance = check_wallet_balance(project[7])
        
        return jsonify({
            "buyer_address": buyer_wallet.classic_address,
            "buyer_seed": buyer_wallet.seed,
            "shares_amount": shares_amount,
            "xrp_paid": xrp_amount,
            "buyer_balance": buyer_final_balance,
            "project_balance": project_final_balance,
            "payment_result": payment_result.result
        }), 200
        
    except Exception as e:
        print(f"Error in buy_shares: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/distribute_dividends", methods=["POST"])
def distribute_dividends():
    """Distribute dividends from the project wallet to its shareholders"""
    try:
        data = request.get_json(force=True)
        project_id = data['project_id']
        total_dividend_xrp = float(data['total_dividend_xrp'])
        
        conn = sqlite3.connect('solar_crowdfunding.db')
        c = conn.cursor()
        c.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = c.fetchone()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        project_balance = check_wallet_balance(project[7])
        if project_balance < total_dividend_xrp:
            return jsonify({
                "error": f"Insufficient funds in project wallet. Need {total_dividend_xrp} XRP but wallet only has {project_balance} XRP"
            }), 400
        
        c.execute('SELECT * FROM shareholders WHERE project_id = ?', (project_id,))
        holders = c.fetchall()
        if not holders:
            return jsonify({"error": "No shareholders found for this project"}), 400
        
        total_shares = sum(holder[3] for holder in holders)
        dividend_id = str(uuid.uuid4())
        c.execute('''
            INSERT INTO dividends (
                id, project_id, amount_xrp,
                distribution_date, status
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            dividend_id,
            project_id,
            total_dividend_xrp,
            datetime.now(),
            'PROCESSING'
        ))
        
        # Recover project wallet from stored seed
        project_wallet = Wallet.from_seed(project[8])
        distributions = []
        for holder in holders:
            holder_share = (holder[3] / total_shares) * total_dividend_xrp
            drops = str(int(holder_share * 1000000))
            payment = Payment(
                account=project_wallet.classic_address,
                destination=holder[2],  # holder_wallet_address
                amount=drops
            )
            # Correct parameter order: client first, then project_wallet.
            payment_prepared = autofill_and_sign(payment, client, project_wallet)
            result = submit_and_wait(payment_prepared, client)
            if result.result.get('meta', {}).get('TransactionResult') != 'tesSUCCESS':
                raise Exception(f"Dividend payment failed: {result.result}")
            distributions.append({
                "holder_address": holder[2],
                "amount_xrp": holder_share,
                "result": result.result
            })
        
        c.execute('UPDATE dividends SET status = ? WHERE id = ?', ('COMPLETED', dividend_id))
        conn.commit()
        conn.close()
        
        final_balance = check_wallet_balance(project[7])
        return jsonify({
            "dividend_id": dividend_id,
            "distributions": distributions,
            "project_final_balance": final_balance
        }), 200
        
    except Exception as e:
        print(f"Error in distribute_dividends: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/project/<project_id>", methods=["GET"])
def get_project(project_id):
    """Retrieve project details including shareholders and dividend history"""
    try:
        conn = sqlite3.connect('solar_crowdfunding.db')
        c = conn.cursor()
        c.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = c.fetchone()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        project_balance = check_wallet_balance(project[7])
        c.execute('SELECT * FROM shareholders WHERE project_id = ?', (project_id,))
        holders = c.fetchall()
        c.execute('SELECT * FROM dividends WHERE project_id = ?', (project_id,))
        dividends = c.fetchall()
        conn.close()
        
        return jsonify({
            "project": {
                "id": project[0],
                "name": project[1],
                "description": project[2],
                "location": project[3],
                "total_power_kw": project[4],
                "total_shares": project[5],
                "share_price_xrp": project[6],
                "wallet_address": project[7],
                "status": project[9],
                "created_at": project[10],
                "current_balance_xrp": project_balance
            },
            "shareholders": [{
                "holder_address": holder[2],
                "shares_amount": holder[3],
                "purchase_date": holder[4]
            } for holder in holders],
            "dividends": [{
                "id": div[0],
                "amount_xrp": div[2],
                "distribution_date": div[3],
                "status": div[4]
            } for div in dividends]
        }), 200
        
    except Exception as e:
        print(f"Error in get_project: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/get_all_project_info", methods=["GET"])
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
        projects.append(project)

    conn.close()
    return projects

if __name__ == "__main__":
    ensure_client()
    app.run(debug=True)
