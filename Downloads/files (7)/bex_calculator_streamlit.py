import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="BEX Decay Calculator",
    page_icon="📊",
    layout="wide"
)

# Strategy presets
STRATEGIES = {
    "Aggressive": {
        "multiplier": 4.0,
        "cap": 0.20,
        "description": "High risk, maximum extraction (best long-term)",
        "best_for": "Long-term holders, trending markets"
    },
    "Conservative": {
        "multiplier": 2.0,
        "cap": 0.08,
        "description": "Low risk, proven returns (+6.53% in high vol)",
        "best_for": "High volatility markets, risk-averse"
    },
    "Moderate": {
        "multiplier": 3.0,
        "cap": 0.125,
        "description": "Balanced approach",
        "best_for": "Normal volatility conditions"
    }
}

# Title
st.title("📊 BEX Volatility Decay Calculator")
st.caption("End-of-day rebalancing tool for 2x leveraged positions")

# Strategy selection
st.subheader("1. Strategy Configuration")
col_strat1, col_strat2 = st.columns([1, 2])

with col_strat1:
    selected_strategy = st.selectbox(
        "Select Strategy Preset:",
        options=list(STRATEGIES.keys()),
        index=0  # Default to Aggressive
    )

with col_strat2:
    strategy = STRATEGIES[selected_strategy]
    st.info(f"**{selected_strategy} Strategy:** {strategy['description']}\n\n**Best for:** {strategy['best_for']}")

MULTIPLIER = strategy["multiplier"]
CAP = strategy["cap"]

# Market data inputs
st.subheader("2. Market Data")
col_mkt1, col_mkt2, col_mkt3 = st.columns(3)

with col_mkt1:
    yesterday_close = st.number_input(
        "Yesterday's Close ($)",
        min_value=0.0,
        value=102.50,
        step=0.01,
        format="%.2f",
        help="Previous day's closing price"
    )

with col_mkt2:
    today_close = st.number_input(
        "Today's Close ($)",
        min_value=0.0,
        value=118.09,
        step=0.01,
        format="%.2f",
        help="Current day's closing price"
    )

with col_mkt3:
    avg_price = st.number_input(
        "Average Entry Price ($)",
        min_value=0.0,
        value=0.0,
        step=0.01,
        format="%.2f",
        help="Optional: For P&L calculation"
    )

# Portfolio inputs
st.subheader("3. Portfolio Details")
col_port1, col_port2 = st.columns(2)

with col_port1:
    position_type = st.radio(
        "Position Type:",
        ["Shares", "Dollar Value"],
        horizontal=True
    )

with col_port2:
    position = st.number_input(
        f"Current Position ({'shares' if position_type == 'Shares' else '$'})",
        min_value=0.0,
        value=670.0,
        step=1.0 if position_type == "Shares" else 100.0,
        format="%.2f"
    )

# Calculate button
if st.button("🚀 Calculate Rebalancing Action", type="primary", use_container_width=True):
    
    if yesterday_close > 0 and today_close > 0 and position > 0:
        # Calculate daily return
        daily_return = (today_close - yesterday_close) / yesterday_close
        
        # Calculate offset
        if daily_return > 0:
            raw_offset = MULTIPLIER * daily_return
            offset_percent = min(CAP, raw_offset)
            cap_hit = raw_offset > CAP
            
            # Calculate shares/dollars to sell
            if position_type == "Shares":
                shares_to_sell = position * offset_percent
                dollar_value = shares_to_sell * today_close
                new_position = position - shares_to_sell
                position_unit = "shares"
                total_value = position * today_close
                new_value = new_position * today_close
            else:
                dollar_value = position * offset_percent
                shares_to_sell = dollar_value / today_close
                new_position = position - dollar_value
                position_unit = "$"
                total_value = position
                new_value = new_position
            
            # Calculate P&L if avg price provided
            if avg_price > 0:
                if position_type == "Shares":
                    unrealized_pnl = position * (today_close - avg_price)
                else:
                    shares_held = position / avg_price
                    unrealized_pnl = shares_held * (today_close - avg_price)
            else:
                unrealized_pnl = None
            
            # Display action recommendation
            st.divider()
            
            # Action box with proper formatting (no HTML)
            action_col1, action_col2 = st.columns([2, 1])
            
            with action_col1:
                st.markdown("### ⚠️ Action Required")
                if cap_hit:
                    st.warning(f"**SELL BEX SHARES** - Cap limit reached")
                else:
                    st.success(f"**SELL BEX SHARES** - Rebalancing recommended")
                
                reason_text = f"BE up {daily_return * 100:.2f}% → Rebalance {offset_percent * 100:.1f}% of position"
                if cap_hit:
                    reason_text += f" (capped at {CAP * 100:.0f}%)"
                st.markdown(f"**Reason:** {reason_text}")
            
            with action_col2:
                st.metric(
                    "Daily Return",
                    f"{daily_return * 100:.2f}%",
                    delta=f"{daily_return * 100:.2f}%"
                )
            
            # Main metrics
            st.divider()
            st.markdown("### 📈 Rebalancing Summary")
            
            col_met1, col_met2, col_met3, col_met4 = st.columns(4)
            
            with col_met1:
                st.metric(
                    "Shares to Sell",
                    f"{shares_to_sell:,.0f}",
                    delta=f"-{offset_percent * 100:.1f}% of position",
                    delta_color="inverse"
                )
            
            with col_met2:
                st.metric(
                    "Cash to Extract",
                    f"${dollar_value:,.2f}",
                    delta="Profit taking",
                    delta_color="normal"
                )
            
            with col_met3:
                st.metric(
                    "New Position",
                    f"{new_position:,.0f} {position_unit}",
                    delta=f"${new_value:,.2f}",
                    delta_color="normal"
                )
            
            with col_met4:
                new_allocation_pct = (new_value / total_value * 100) if total_value > 0 else 0
                st.metric(
                    "New Allocation",
                    f"{new_allocation_pct:.1f}%",
                    delta=f"-{offset_percent * 100:.1f}%",
                    delta_color="inverse"
                )
            
            # Additional details
            st.divider()
            st.markdown("### 📊 Calculation Details")
            
            detail_col1, detail_col2, detail_col3 = st.columns(3)
            
            with detail_col1:
                st.metric(
                    "Raw Offset",
                    f"{raw_offset * 100:.2f}%",
                    delta="Before cap" if cap_hit else None
                )
            
            with detail_col2:
                st.metric(
                    "Applied Offset",
                    f"{offset_percent * 100:.2f}%",
                    delta="CAP HIT" if cap_hit else None,
                    delta_color="off" if cap_hit else "normal"
                )
            
            with detail_col3:
                st.metric(
                    "Multiplier",
                    f"{MULTIPLIER:.1f}x",
                    delta=f"Cap: {CAP * 100:.0f}%"
                )
            
            # P&L if available
            if unrealized_pnl is not None:
                st.divider()
                pnl_col1, pnl_col2 = st.columns(2)
                
                with pnl_col1:
                    st.metric(
                        "Unrealized P&L (Total)",
                        f"${unrealized_pnl:,.2f}",
                        delta=f"{((today_close - avg_price) / avg_price * 100):.2f}%" if avg_price > 0 else None
                    )
                
                with pnl_col2:
                    pnl_on_sold = shares_to_sell * (today_close - avg_price) if avg_price > 0 else 0
                    st.metric(
                        "P&L on Sold Shares",
                        f"${pnl_on_sold:,.2f}",
                        delta=None
                    )
            
            # Calculation formula
            st.divider()
            with st.expander("📐 View Calculation Formula"):
                st.code(f"""
Daily Return = (Today - Yesterday) / Yesterday
             = ({today_close:.2f} - {yesterday_close:.2f}) / {yesterday_close:.2f}
             = {daily_return:.4f} ({daily_return * 100:.2f}%)

Raw Offset = Multiplier × Daily Return
           = {MULTIPLIER:.1f} × {daily_return:.4f}
           = {raw_offset:.4f} ({raw_offset * 100:.2f}%)

Applied Offset = min(Cap, Raw Offset)
               = min({CAP:.2f}, {raw_offset:.4f})
               = {offset_percent:.4f} ({offset_percent * 100:.2f}%)

Shares to Sell = Position × Applied Offset
               = {position:.0f} × {offset_percent:.4f}
               = {shares_to_sell:.0f} shares

Cash Extracted = Shares to Sell × Today's Price
               = {shares_to_sell:.0f} × {today_close:.2f}
               = ${dollar_value:,.2f}
                """)
            
        else:
            # No action needed
            st.divider()
            st.info("✅ No offset needed - price declined or flat")
            st.caption(f"Daily Return: {daily_return * 100:.2f}%")
            st.caption("Offset only applies when position closes higher than previous day")
    
    else:
        st.error("❌ Please enter valid values for all required fields")

# Methodology section
st.divider()
with st.expander("📚 How This Works"):
    st.markdown("""
    **The Problem:** Leveraged ETFs/ETNs rebalance daily at 4 PM, creating a "buy high, sell low" pattern that causes volatility decay.
    
    **The Solution:** Manually counter-rebalance by selling a percentage when the position rises.
    
    **Formula:** Offset % = min(Cap, Multiplier × Daily Return)
    
    **Current Parameters:**
    - Multiplier: {:.1f}x
    - Cap: {:.0f}%
    - Strategy: {}
    
    **Execution:**
    1. Only applies when position closes higher than previous day
    2. Execute at end of day (after 4 PM close)
    3. Reduces exposure before volatility reverses
    4. Extracts cash while minimizing decay
    
    **Important:** This strategy defends against volatility decay but may cap upside in sustained bull markets.
    """.format(MULTIPLIER, CAP * 100, selected_strategy))

# Footer
st.divider()
st.caption(f"Current parameters: Multiplier = {MULTIPLIER:.1f}x, Cap = {CAP * 100:.0f}% | Strategy: {selected_strategy} | Backtested on 1,636 trading days")
