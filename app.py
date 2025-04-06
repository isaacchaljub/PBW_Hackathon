import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import os

# Base URL for your Flask backend (adjust port if necessary)
BASE_URL = "http://localhost:5001"

# Set the page configuration
st.set_page_config(
    page_title="Solar Farm Crowdfunding with XRP Blockchain",
    page_icon="",
    layout="wide"
)

# Custom CSS for background and UI styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #ffffff, #e6f7ff);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header {
        background-color: #F7DC6F;
        padding: 30px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .button-custom {
        background-color: #1E90FF;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        margin: 5px;
    }
    .button-custom:hover {
        background-color: #1C86EE;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
section_groups = {
    "Home & About": ["Home", "About the Project"],
    "How It Works": ["How It Works"],
    "API Demo": ["API Demo"],
    "Contact": ["Contact"]
}

selected_group = st.sidebar.radio("Go to:", list(section_groups.keys()))
selected_sections = section_groups[selected_group]

# ---------------------- Static Content Sections ----------------------
if selected_group in ["Home & About", "How It Works", "Calculator & Features", "Impact & Involvement", "Contact"]:
    
    if "Home" in selected_sections:
        st.markdown(
            """
            <div class="header">
                <h1>Solar Farm Crowdfunding with XRP Blockchain</h1>
                <p>Empowering communities through renewable energy and blockchain technology.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 30px;">
                <a href="#contribute" style="text-decoration: none;">
                    <button class="button-custom">Contribute Now</button>
                </a>
                <a href="#learn-more" style="text-decoration: none;">
                    <button class="button-custom" style="background-color: #32CD32;">Learn More</button>
                </a>
            </div> 
            """,
            unsafe_allow_html=True
        )

        # Funding chart
        st.markdown("### Funding Progress Over Time")
        dates = pd.date_range(start="2025-01-01", periods=30)
        funds = np.cumsum(np.random.randint(10, 100, size=30))
        progress_data = pd.DataFrame({"Date": dates, "Funds Raised (XRP)": funds})
        fig = px.line(progress_data, x="Date", y="Funds Raised (XRP)", title="Cumulative Funds Raised")
        st.plotly_chart(fig, use_container_width=True)

        # Project carousel
        st.markdown("### Featured Projects")

        # Specify the path to your local images directory
        image_directory = "images"  # Replace with your image directory path

        # Get the list of image files in the directory
        image_files = [f for f in os.listdir(image_directory) if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]

        # Create a 1x3 grid using columns
        col1, col2, col3 = st.columns(3)

        # Ensure we don't try to access more than 3 images
        for idx, image_file in enumerate(image_files[:3]):
            image_path = os.path.join(image_directory, image_file)
            if idx == 0:
                col1.image(image_path, caption="Desert Sun Solar Plant", width=300)
            elif idx == 1:
                col2.image(image_path, caption="Mountain Peak Project", width=300)
            elif idx == 2:
                col3.image(image_path, caption="Ocean Breez Project", width=300)


        # Simulate funding
        st.markdown("#### Simulate Future Funding")
        additional_funds = st.slider("Projected additional XRP contribution:", 0, 1000, 200)
        future_total = funds[-1] + additional_funds
        st.write(f"Projected Total Funds Raised: *{future_total} XRP*")
    
    if "About the Project" in selected_sections:
        st.header("About the Project")
        st.markdown(
            """
            Join our mission to create a solar farm funded by blockchain-powered contributions. 
            Contributors receive tokenized rewards, ensuring accountability and transparency.
            """
        )
        st.markdown(
            """
            *Ownership Model*  
            By contributing, you gain ownership in the solar farm through SUNWATT tokens, representing your share in the renewable energy generated.

            *Energy Generation*  
            As the solar farm generates energy, real-time tracking displays performance on our dashboard, ensuring transparency and accountability.
            """
        )
    
    if "How It Works" in selected_sections:
        st.header("How It Works")
        
        with st.expander("Step 1: Join the Community"):
            col1, col2 = st.columns([2, 1]) 

            with col1:
                st.markdown(
                    """
                    - *Sign Up:* Become a member of our renewable energy cooperative.  
                    - *Invest:* Make your initial contribution to get started.  
                    - *Receive Tokens:* Earn SUNWATT tokens representing your share in the solar farm.
                    """
                )

            with col2:
                st.image("images/Project_1.jpg", width=1000) 

            
        
        with st.expander("Step 2: Contribute to the Solar Farm"):
            col1, col2 = st.columns([2, 1]) 

            with col1:
                st.markdown(
                    """
                    - *Fund Installation:* Contribute XRP to help fund the solar farm.  
                    - *Tokenization:* Your contribution is converted into SUNWATT tokens on the XRP Blockchain.  
                    - *Efficient Transactions:* Enjoy fast and low-cost transactions.
                    """
                )
            with col2:
                st.image("images/Project_2.jpg", width=1000) 

        with st.expander("Step 3: Track Energy Generation"):
            col1, col2 = st.columns([2, 1]) 

            with col1:
                st.markdown(
                    """
                    - *Real-Time Monitoring:* Check the dashboard to see the solar farm's energy production.  
                    - *Transparent Data:* All data is recorded on the blockchain for accountability.  
                    - *Token Value Growth:* Watch your token value increase as more clean energy is generated.
                    """
                )
            with col2:
                st.image("images/Project_3.jpg", width=1000) 
        
        with st.expander("Step 4: Earn Passive Income"):
            col1, col2 = st.columns([2, 1]) 
            with col1:
                st.markdown(
                    """
                    - *Passive Revenue Stream:* Earn a consistent, passive income by holding your shares in the solar project.
                    - *Token Appreciation:* Benefit from the increasing value of your SUNWATT tokens as the project scales.  
                
                    """
                )
            with col2:
                st.image("images/Project_4.jpg", width=1000) 
    
    
    if "Contact" in selected_sections:
        st.header("Contact Us")
        st.markdown("Have questions or want to reach out? Contact us at *support@solarfarm.com*.")

# ---------------------- API Demo Section ----------------------
if selected_group == "API Demo":
    st.header("API Demo: Interact with the Solar Crowdfunding Backend")
    st.markdown("Use the carousel below to navigate through the API demo sections.")
    
    demo_tabs = st.tabs(["Create Project", "Get Project Details", "Buy Shares", "Distribute Dividends"])
    
    with demo_tabs[0]:
        st.subheader("1. Create a Solar Project")

        project_name = st.text_input("Project Name")
        project_description = st.text_area("Project Description")
        location = st.text_input("Location")
        power = st.number_input("Power plant capacity (kW)", min_value=50, max_value=None, value="min")
        investment = st.number_input("Project Investment ($)", min_value=100000, max_value=None, value="min")
        number_of_shares = st.number_input("Number of Shares", min_value=10000,value="min")
        xrp_price = st.number_input("XRP/USD", value=2.08, disabled=True )
        xrp_amount  = st.number_input("XRP amount", value=(investment//xrp_price)+1, disabled=True)
        share_price_xrp =  st.number_input("Share Price XRP", value=(xrp_amount / number_of_shares), disabled=True)

        if st.button("Create Project"):
            project_data = {
                "name": project_name,
                "description": project_description,
                "location": location,
                "total_power_kw": power,
                "total_shares": number_of_shares,
                "share_price_xrp": share_price_xrp
            }
            response = requests.post(f"{BASE_URL}/create_project", json=project_data)
            st.write("Response Code:", response.status_code)
            st.json(response.json())
            if response.status_code == 200:
                project_id = response.json().get("project_id")
                st.success(f"Project created with ID: {project_id}")
                st.session_state["project_id"] = project_id
    
    with demo_tabs[1]:
        st.subheader("2. Get Project Details")
        # Input for Project ID
    project_id_input = st.text_input("Enter Project ID", value=st.session_state.get("project_id", ""), key="get_project")
    
    # Button to fetch project details
    if st.button("Get Project Details", key="get_project_button") and project_id_input:
        response = requests.get(f"{BASE_URL}/project/{project_id_input}")
        
        # Display the response code
        st.write("Response Code:", response.status_code)
        
        # Only proceed if the response is successful
        if response.status_code == 200:
            project_data = response.json() 
            
            # Display Project Information
            st.markdown("### Project Information")
            st.markdown(f"**Project Name:** {project_data['project']['name']}")
            st.markdown(f"**Location:** {project_data['project']['location']}")
            st.markdown(f"**Description:** {project_data['project']['description']}")
            st.markdown(f"**Created At:** {project_data['project']['created_at']}")
            st.markdown(f"**Current Balance (XRP):** {project_data['project']['current_balance_xrp']}")
            st.markdown(f"**Status:** {project_data['project']['status']}")
            st.markdown(f"**Share Price (XRP):** {project_data['project']['share_price_xrp']}")
            st.markdown(f"**Total Power (kW):** {project_data['project']['total_power_kw']}")
            st.markdown(f"**Total Shares:** {project_data['project']['total_shares']}")
            st.markdown(f"**Wallet Address:** {project_data['project']['wallet_address']}")
            
            # Display Dividends
            st.markdown("### Dividends")
            if project_data["dividends"]:
                for dividend in project_data["dividends"]:
                    st.markdown(f"**Amount (XRP):** {dividend['amount_xrp']}")
                    st.markdown(f"**Distribution Date:** {dividend['distribution_date']}")
                    st.markdown(f"**ID:** {dividend['id']}")
                    st.markdown(f"**Status:** {dividend['status']}")
                    st.markdown("---")
            else:
                st.markdown("No dividends available.")
            
            # Display Shareholders
            st.markdown("### Shareholders")
            if project_data["shareholders"]:
                for shareholder in project_data["shareholders"]:
                    st.markdown(f"**Holder Address:** {shareholder['holder_address']}")
                    st.markdown(f"**Purchase Date:** {shareholder['purchase_date']}")
                    st.markdown(f"**Shares Amount:** {shareholder['shares_amount']}")
                    st.markdown("---")
            else:
                st.markdown("No shareholders available.")
        else:
            st.markdown(f"Failed to fetch project details. Status Code: {response.status_code}")

    with demo_tabs[2]:
        st.subheader("3. Buy Shares")
        project_id_buy = st.text_input("Project ID for Buying Shares", value=st.session_state.get("project_id", ""), key="buy_project")
        shares_amount = st.number_input("Enter number of shares to buy:", min_value=1, step=1, key="shares_amount")
        if st.button("Buy Shares", key="buy_shares_button") and project_id_buy:
            buy_data = {
                "project_id": project_id_buy,
                "shares_amount": shares_amount
            }
            response = requests.post(f"{BASE_URL}/buy_shares", json=buy_data)
            st.write("Response Code:", response.status_code)
            st.json(response.json())

    with demo_tabs[3]:
        st.subheader("4. Distribute Dividends")
        project_id_div = st.text_input("Project ID for Dividend Distribution", value=st.session_state.get("project_id", ""), key="dividend_project")
        dividend_amount = st.number_input("Enter total dividend amount in XRP:", value=0.000001, format="%.6f", key="dividend_amount")
        if st.button("Distribute Dividends", key="dividends_button") and project_id_div:
            dividend_data = {
                "project_id": project_id_div,
                "total_dividend_xrp": dividend_amount
            }
            response = requests.post(f"{BASE_URL}/distribute_dividends", json=dividend_data)
            st.write("Response Code:", response.status_code)
            st.json(response.json())

# ---------------------- Sidebar Footer ----------------------
st.sidebar.markdown("---")
st.sidebar.markdown("© 2025 Solar Farm Crowdfunding. All Rights Reserved.")
