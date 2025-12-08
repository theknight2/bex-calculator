import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="BEX Calculator",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Styles - All in one block
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Base styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #FFFFFF;
    }
    
    /* Typography */
    h1 {
        font-family: 'Inter', sans-serif;
        font-size: 56px;
        font-weight: 300;
        letter-spacing: -0.02em;
        color: #000000;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 400;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        color: #666666;
        margin-bottom: 0.5rem;
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #666666;
    }
    
    /* Input labels */
    .stNumberInput label {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #666666;
    }
    
    /* Number inputs */
    .stNumberInput input {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 500;
        border: 1px solid #E0E0E0;
        border-radius: 4px;
        padding: 12px 16px;
    }
    
    .stNumberInput input:focus {
        border-color: #000000;
    }
    
    /* Output container */
    .output-container {
        background: #000000;
        color: #FFFFFF;
        padding: 3rem;
        border-radius: 4px;
        margin: 2rem 0;
    }
    
    .output-title {
        font-family: 'Inter', sans-serif;
        font-size: 48px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 1rem;
    }
    
    .output-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        color: #CCCCCC;
        margin-bottom: 0.5rem;
    }
    
    .output-reason {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 300;
        color: #999999;
        margin-top: 1.5rem;
    }
    
    /* Strategy cards */
    .strategy-card {
        border: 1px solid #E0E0E0;
        border-radius: 4px;
        padding: 2.5rem;
        background: #FFFFFF;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .strategy-card:hover {
        border-color: #000000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .strategy-card.selected {
        background: #000000;
        color: #FFFFFF;
        border-color: #000000;
    }
    
    .strategy-title {
        font-family: 'Inter', sans-serif;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .strategy-desc {
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        color: #666666;
        line-height: 1.6;
    }
    
    .strategy-card.selected .strategy-title,
    .strategy-card.selected .strategy-desc {
        color: #FFFFFF;
    }
    
    /* Table styles */
    .data-table {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        width: 100%;
        border-collapse: collapse;
        margin-top: 2rem;
    }
    
    .data-table th {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #666666;
        text-align: left;
        padding: 0.75rem 0;
        border-bottom: 2px solid #000000;
    }
    
    .data-table td {
        padding: 0.75rem 0;
        border-bottom: 1px solid #F0F0F0;
        color: #000000;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 1px solid #E0E0E0;
        margin: 3rem 0;
    }
    
    /* Spacing */
    .section-spacing {
        margin: 3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Constants
MULTIPLIER = 9.0
MAX_REBALANCE = 0.50

STRATEGIES = {
    "Conservative": {
        "position": 10.0,
        "expected_return": 7.0,
        "max_drawdown": -8.0
    },
    "Aggressive": {
        "position": 15.0,
        "expected_return": 86.0,
        "max_drawdown": -57.0
    }
}

# Default values
BE_YESTERDAY_DEFAULT = 102.50
BE_TODAY_DEFAULT = 118.09
BEX_PRICE_DEFAULT = 14.91
BEX_SHARES_DEFAULT = 670
PORTFOLIO_DEFAULT = 100000.0

# Session state initialization
if 'strategy' not in st.session_state:
    st.session_state.strategy = 'Conservative'

# Header
st.markdown('<h1>BEX Calculator</h1>', unsafe_allow_html=True)
st.markdown('<h2>Weekly Rebalancing Strategy</h2>', unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# Strategy Selection
st.markdown('<h3>Strategy Selection</h3>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.session_state.strategy == "Conservative":
        st.markdown("""
        <div class="strategy-card selected">
            <div class="strategy-title">CONSERVATIVE</div>
            <div class="strategy-desc">10% position • +7% expected<br>Max drawdown: -8%</div>
            <div style="margin-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #999999;">RESEARCH-BACKED<br>1,659 DAYS VALIDATED</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="strategy-card">
            <div class="strategy-title">CONSERVATIVE</div>
            <div class="strategy-desc">10% position • +7% expected<br>Max drawdown: -8%</div>
            <div style="margin-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #999999;">RESEARCH-BACKED<br>1,659 DAYS VALIDATED</div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("SELECT CONSERVATIVE", key="strat_conservative", use_container_width=True):
        st.session_state.strategy = "Conservative"
        st.rerun()

with col2:
    if st.session_state.strategy == "Aggressive":
        st.markdown("""
        <div class="strategy-card selected">
            <div class="strategy-title">AGGRESSIVE</div>
            <div class="strategy-desc">15% position • +86% expected<br>Max drawdown: -57%</div>
            <div style="margin-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #999999;">RESEARCH-BACKED<br>1,659 DAYS VALIDATED</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="strategy-card">
            <div class="strategy-title">AGGRESSIVE</div>
            <div class="strategy-desc">15% position • +86% expected<br>Max drawdown: -57%</div>
            <div style="margin-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #999999;">RESEARCH-BACKED<br>1,659 DAYS VALIDATED</div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("SELECT AGGRESSIVE", key="strat_aggressive", use_container_width=True):
        st.session_state.strategy = "Aggressive"
        st.rerun()

st.markdown('<hr>', unsafe_allow_html=True)

# Market Data Inputs
st.markdown('<h3>Market Data</h3>', unsafe_allow_html=True)
col_mkt1, col_mkt2, col_mkt3 = st.columns(3)

with col_mkt1:
    be_yesterday = st.number_input(
        "BE YESTERDAY CLOSE",
        min_value=0.01,
        value=BE_YESTERDAY_DEFAULT,
        step=0.01,
        format="%.2f"
    )

with col_mkt2:
    be_today = st.number_input(
        "BE TODAY CLOSE",
        min_value=0.01,
        value=BE_TODAY_DEFAULT,
        step=0.01,
        format="%.2f"
    )

with col_mkt3:
    bex_price = st.number_input(
        "BEX CURRENT PRICE",
        min_value=0.01,
        value=BEX_PRICE_DEFAULT,
        step=0.01,
        format="%.2f"
    )

st.markdown('<hr>', unsafe_allow_html=True)

# Position Inputs
st.markdown('<h3>Position Details</h3>', unsafe_allow_html=True)
col_pos1, col_pos2 = st.columns(2)

with col_pos1:
    bex_shares = st.number_input(
        "BEX SHARES HELD",
        min_value=0.0,
        value=BEX_SHARES_DEFAULT,
        step=1.0,
        format="%.0f"
    )

with col_pos2:
    portfolio_value = st.number_input(
        "PORTFOLIO VALUE",
        min_value=0.01,
        value=PORTFOLIO_DEFAULT,
        step=1000.0,
        format="%.2f"
    )

st.markdown('<hr>', unsafe_allow_html=True)

# Calculation Logic
be_return = (be_today - be_yesterday) / be_yesterday if be_yesterday > 0 else 0

if be_return <= 0:
    action = "HOLD"
    shares_to_sell = 0
    cash_to_extract = 0
else:
    raw_rebal = be_return * MULTIPLIER
    rebal_pct = min(raw_rebal, MAX_REBALANCE)
    shares_to_sell = bex_shares * rebal_pct
    cash_to_extract = shares_to_sell * bex_price
    action = "SELL"

# Calculate new position
new_shares = bex_shares - shares_to_sell
new_position_value = new_shares * bex_price
new_allocation = (new_position_value / portfolio_value * 100) if portfolio_value > 0 else 0

# Output Container
st.markdown('<hr>', unsafe_allow_html=True)

if action == "SELL":
    output_html = f"""
    <div class="output-container">
        <div class="output-title">SELL {int(shares_to_sell)} SHARES</div>
        <div class="output-subtitle">Extract ${cash_to_extract:,.2f}</div>
        <div class="output-subtitle">Retain {int(new_shares)} shares ({new_allocation:.1f}%)</div>
        <div class="output-reason">BE rose {be_return * 100:.2f}% today</div>
    </div>
    """
else:
    output_html = f"""
    <div class="output-container">
        <div class="output-title">HOLD POSITION</div>
        <div class="output-reason">BE declined or flat ({be_return * 100:.2f}%)</div>
    </div>
    """
st.markdown(output_html, unsafe_allow_html=True)

# Details Table (if SELL)
if action == "SELL":
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<h3>Position Details</h3>', unsafe_allow_html=True)
    
    current_value = bex_shares * bex_price
    current_allocation = (current_value / portfolio_value * 100) if portfolio_value > 0 else 0
    cash_after = portfolio_value - current_value + cash_to_extract
    new_allocation_after = (new_position_value / portfolio_value * 100) if portfolio_value > 0 else 0
    
    details_data = {
        "METRIC": ["BEX Shares", "Position Value", "Cash Balance", "BEX Allocation"],
        "CURRENT": [f"{bex_shares:.0f}", f"${current_value:,.2f}", f"${portfolio_value - current_value:,.2f}", f"{current_allocation:.2f}%"],
        "AFTER": [f"{new_shares:.0f}", f"${new_position_value:,.2f}", f"${cash_after:,.2f}", f"{new_allocation:.2f}%"]
    }
    
    df = pd.DataFrame(details_data)
    st.markdown("""
    <table class="data-table">
        <tr>
            <th>METRIC</th>
            <th>CURRENT</th>
            <th>AFTER</th>
        </tr>
    """, unsafe_allow_html=True)
    for i in range(len(df)):
        st.markdown(f"""
        <tr>
            <td>{df.iloc[i]['METRIC']}</td>
            <td>{df.iloc[i]['CURRENT']}</td>
            <td>{df.iloc[i]['AFTER']}</td>
        </tr>
        """, unsafe_allow_html=True)
    st.markdown("</table>", unsafe_allow_html=True)

# Expanders
with st.expander("STRATEGY METHODOLOGY"):
    st.markdown("""
    ### Weekly Rebalancing Strategy
    
    **Core Principle**
    
    BEX internally rebalances daily to maintain 2x leverage, creating volatility decay. We counter this by selling after BE gains, extracting profits before decay occurs.
    
    **Formula**
    
    Shares to Sell = Current Shares × min(BE Return × 9.0, 50%)
    
    **Position Sizing**
    
    Conservative: 10% of portfolio (Kelly Criterion optimal)
    Aggressive: 15% of portfolio (Higher growth, higher risk)
    
    **Expected Performance**
    
    Conservative: +7% over 6.5 years vs -85% buy-and-hold
    Aggressive: +86% over 6.5 years vs -85% buy-and-hold
    
    Based on 1,659 days of historical data validation.
    """)

with st.expander("WEEKLY EXECUTION WORKFLOW"):
    st.markdown("""
    ### Weekly Execution (Friday 4:00 PM ET)
    
    1. Note BE closing prices (this Friday vs last Friday)
    2. Note current BEX price
    3. Enter values in calculator
    4. Execute recommendation (SELL or HOLD)
    5. Record transaction in tracking spreadsheet
    
    **If SELL:**
    Place market or limit order for specified shares at BEX price.
    
    **If HOLD:**
    No action required. Review again next Friday.
    
    **Tracking:**
    Date | BE Return | Shares Sold | Cash Extracted | Remaining Position
    """)
