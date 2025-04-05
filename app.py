import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests

# Base URL for your Flask backend (adjust port if necessary)
BASE_URL = "http://localhost:5001"

# Set the page configuration (only one call needed)
st.set_page_config(
    page_title="Solar Farm Crowdfunding with XRP Blockchain",
    page_icon="🌞",
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

# Sidebar Navigation: Define groups for static content and API interactions.
section_groups = {
    "Home & About": ["Home", "About the Project"],
    "How It Works": ["How It Works"],
    "Calculator & Features": ["Contribution Calculator", "Key Features & Benefits"],
    "Impact & Involvement": ["Impact", "Get Involved"],
    "API Demo": ["Create Project", "Get Project Details", "Buy Shares", "Distribute Dividends"],
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
                <h1>🌞 Solar Farm Crowdfunding with XRP Blockchain 🌞</h1>
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
        # Add an interactive funding progress chart (static demo data)
        st.markdown("### Funding Progress Over Time")
        dates = pd.date_range(start="2025-01-01", periods=30)
        funds = np.cumsum(np.random.randint(10, 100, size=30))
        progress_data = pd.DataFrame({"Date": dates, "Funds Raised (XRP)": funds})
        fig = px.line(progress_data, x="Date", y="Funds Raised (XRP)", title="Cumulative Funds Raised")
        st.plotly_chart(fig, use_container_width=True)
        # Reactive slider for simulation
        st.markdown("#### Simulate Future Funding")
        additional_funds = st.slider("Projected additional XRP contribution:", 0, 1000, 200)
        future_total = funds[-1] + additional_funds
        st.write(f"Projected Total Funds Raised: **{future_total} XRP**")

    if "About the Project" in selected_sections:
        st.header("🌍 About the Project")
        st.markdown(
            """
            Join our mission to create a solar farm funded by blockchain-powered contributions. 
            Contributors receive tokenized rewards, ensuring accountability and transparency.
            """
        )
        st.markdown(
            """
            **Ownership Model**  
            By contributing, you gain ownership in the solar farm through SUNWATT tokens, representing your share in the renewable energy generated.

            **Energy Generation**  
            As the solar farm generates energy, real-time tracking displays performance on our dashboard, ensuring transparency and accountability.
            """
        )

    if "How It Works" in selected_sections:
        st.header("📖 How It Works")
        st.markdown(
            """
            **Step 1: Join the Community**  
            - **Sign Up:** Become a member of our renewable energy cooperative.  
            - **Invest:** Make your initial contribution to get started.  
            - **Receive Tokens:** Earn SUNWATT tokens representing your share in the solar farm.

            **Step 2: Contribute to the Solar Farm**  
            - **Fund Installation:** Contribute XRP to help fund the solar farm.  
            - **Tokenization:** Your contribution is converted into SUNWATT tokens on the XRP Blockchain.  
            - **Efficient Transactions:** Enjoy fast and low-cost transactions.

            **Step 3: Track Energy Generation**  
            - **Real-Time Monitoring:** Check the dashboard to see the solar farm's energy production.  
            - **Transparent Data:** All data is recorded on the blockchain for accountability.  
            - **Token Value Growth:** Watch your token value increase as more clean energy is generated.

            **Step 4: Save on Your Bills**  
            - **Energy Savings:** Use the energy generated to reduce your electricity bills.  
            - **Earn Rewards:** Benefit from dividends or additional token rewards as the project scales.  
            - **Join the Revolution:** Be part of a movement toward greener, more affordable energy.
            """
        )
        with st.expander("More Details"):
            st.markdown("Additional FAQs or technical details can be provided here.")

    if "Contribution Calculator" in selected_sections:
        st.header("💸 Contribution Calculator")
        st.markdown("Discover how many SUNWATT tokens you can earn with your contribution.")
        xrp_amount = st.number_input("Enter your contribution amount in XRP:", min_value=0.0, step=0.1)
        tokens = xrp_amount * 10  # Example conversion rate
        st.write(f"With {xrp_amount} XRP, you'll receive approximately **{tokens:.2f} SUNWATT tokens**.")

    if "Key Features & Benefits" in selected_sections:
        st.header("✨ Key Features & Benefits")
        st.markdown(
            """
            - **XRP Blockchain:** Fast and low-cost transactions.
            - **Tokenized Energy:** Trackable rewards with SUNWATT tokens.
            - **Escrow Mechanism:** Ensures milestone-based accountability.
            - **Community Governance:** Contributors have voting power for future decisions.
            """
        )
        st.markdown(
            """
            **Environmental Impact:**  
            - Contribute to reducing carbon emissions by funding solar energy projects.  
            - Increase the adoption of renewable energy in communities worldwide.
            """
        )

    if "Impact" in selected_sections:
        st.header("🌟 Impact")
        col1, col2, col3 = st.columns(3)
        col1.metric("CO2 Saved", "12,500 kg")
        col2.metric("Energy Generated", "50,000 kWh")
        col3.metric("Contributors", "200+")
        st.markdown(
            """
            Our solar farm project empowers communities to embrace renewable energy while delivering tangible environmental and economic benefits.
            """
        )

    if "Get Involved" in selected_sections:
        st.header("🔗 Get Involved")
        st.markdown(
            """
            Ready to make a difference? Join our community and take part in shaping the future of renewable energy.
            - **Own Solar Farm Shares:** Receive SUNWATT tokens and be part of the renewable energy revolution.
            - **Track Progress:** Use our real-time dashboard to follow project milestones and energy generation.
            """
        )
        if st.button("Contribute Now"):
            st.write("Thank you for your contribution! Your support makes a difference.")

    if "Contact" in selected_sections:
        st.header("📧 Contact Us")
        st.markdown(
            """
            Have questions or want to reach out? Contact us at **support@solarfarm.com**.
            """
        )

# ---------------------- API Demo Section ----------------------
if selected_group == "API Demo":
    st.header("API Demo: Interact with the Solar Crowdfunding Backend")
    st.markdown("""
    Use the controls below to create a project, buy shares, get project details, and distribute dividends.
    """)
    
    # Create Project
    st.subheader("1. Create a Solar Project")
    if st.button("Create Demo Project"):
        project_data = {
            "name": "Desert Sun Power Plant",
            "description": "20MW solar plant in Arizona desert",
            "location": "Phoenix, AZ",
            "total_power_kw": 20000,
            "total_shares": 1000,
            "share_price_xrp": 0.000001  # very low for testing
        }
        response = requests.post(f"{BASE_URL}/create_project", json=project_data)
        st.write("Response Code:", response.status_code)
        st.json(response.json())
        if response.status_code == 200:
            project_id = response.json().get("project_id")
            st.success(f"Project created with ID: {project_id}")
            st.session_state["project_id"] = project_id

    # Get Project Details
    st.subheader("2. Get Project Details")
    project_id_input = st.text_input("Enter Project ID", value=st.session_state.get("project_id", ""))
    if st.button("Get Project Details") and project_id_input:
        response = requests.get(f"{BASE_URL}/project/{project_id_input}")
        st.write("Response Code:", response.status_code)
        st.json(response.json())

    # Buy Shares
    st.subheader("3. Buy Shares")
    project_id_buy = st.text_input("Project ID for Buying Shares", value=st.session_state.get("project_id", ""))
    shares_amount = st.number_input("Enter number of shares to buy:", min_value=1, step=1)
    if st.button("Buy Shares") and project_id_buy:
        buy_data = {
            "project_id": project_id_buy,
            "shares_amount": shares_amount
        }
        response = requests.post(f"{BASE_URL}/buy_shares", json=buy_data)
        st.write("Response Code:", response.status_code)
        st.json(response.json())

    # Distribute Dividends
    st.subheader("4. Distribute Dividends")
    project_id_div = st.text_input("Project ID for Dividend Distribution", value=st.session_state.get("project_id", ""))
    dividend_amount = st.number_input("Enter total dividend amount in XRP:", value=0.000001, format="%.6f")
    if st.button("Distribute Dividends") and project_id_div:
        dividend_data = {
            "project_id": project_id_div,
            "total_dividend_xrp": dividend_amount
        }
        response = requests.post(f"{BASE_URL}/distribute_dividends", json=dividend_data)
        st.write("Response Code:", response.status_code)
        st.json(response.json())

# ---------------------- Sidebar Footer ----------------------
st.sidebar.markdown("---")
st.sidebar.markdown("©️ 2025 Solar Farm Crowdfunding. All Rights Reserved.")