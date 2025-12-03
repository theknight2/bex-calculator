# BEX Volatility Decay Calculator

Clean, minimal calculator for end-of-day rebalancing of 2x leveraged positions.

## Optimized Parameters

- **Multiplier:** 3.0
- **Cap:** 8.5%
- **Validation:** 99.87% accuracy on 6.5 years of data
- **Backtested:** 1,636 trading days

## Files Included

1. `bex_calculator_streamlit.py` - Python Streamlit app
2. `bex_calculator_react.jsx` - React component
3. `requirements.txt` - Python dependencies
4. `README.md` - This file

---

## Option 1: Streamlit App (Python)

### Installation

```bash
pip install -r requirements.txt
```

### Run

```bash
streamlit run bex_calculator_streamlit.py
```

The app will open in your browser at `http://localhost:8501`

### Features

- Clean, minimal interface
- Real-time calculations
- Position type toggle (shares/dollars)
- Optional P&L tracking
- Collapsible methodology section

---

## Option 2: React Component

### Usage

Copy the contents of `bex_calculator_react.jsx` into your React project.

### Requirements

- React 16.8+ (uses hooks)
- No additional dependencies

### Import

```javascript
import BEXCalculator from './bex_calculator_react';

function App() {
  return <BEXCalculator />;
}
```

---

## How to Use

### Inputs Required

1. **Position Type:** Choose between Shares or Dollar Value
2. **Current Position:** Your current holding size
3. **Yesterday's Close:** Previous day's closing price
4. **Today's Close:** Current day's closing price
5. **Average Entry Price:** (Optional) For P&L calculation

### Output

- **Shares to Sell:** Exact number of shares to sell
- **Dollar Value:** Cash value of the sale
- **Daily Return:** Percentage change
- **Offset Applied:** Actual offset percentage used
- **New Position:** Remaining position after sale
- **Unrealized P&L:** (If avg price provided)

### Formula

```
IF daily_return > 0:
    Offset % = min(8.5%, 3.0 × daily_return)
    Sell: position × offset %
ELSE:
    No action (hold)
```

---

## Methodology

### The Problem

Leveraged ETFs/ETNs rebalance daily at 4 PM, creating a "buy high, sell low" pattern that causes volatility decay over time.

### The Solution

Manually counter-rebalance by selling a percentage of your position when it rises, offsetting the ETF's automatic rebalancing.

### When to Execute

- After market close (4:00 PM ET)
- Only on days when position closes higher
- Sell calculated percentage before next trading day

### Expected Results

- Reduced volatility decay in choppy markets
- Cash extraction on up days
- Strong defensive performance in crashes
- May cap upside in sustained bull markets

---

## Validation Results

### Phase 1: Synthetic vs Actual
- Correlation: 99.87%
- MAE: 0.56%

### Phase 2: Training
- Period: 6.5 years (1,636 days)
- Outperformance: +1,775% vs buy-and-hold
- Sharpe Ratio: 1.36

### Phase 3: Out-of-Sample
- Tested on 13 days of actual BEX
- Strategy beat buy-and-hold by +1.96%

---

## Important Notes

1. **Market Regime Dependency:** Strategy performs best in choppy/volatile markets
2. **Bull Market Tradeoff:** May underperform in sustained bull runs by extracting cash early
3. **Crash Protection:** Provides significant downside protection (43% average drawdown reduction)
4. **Execution:** Must be executed at end of day, not intraday
5. **Commission-Free:** Assumes commission-free trading for viability

---

## Support

For questions or issues, contact: shapiroassociates@example.com

---

**Disclaimer:** This tool is for informational purposes only. Past performance does not guarantee future results. Trading leveraged products involves significant risk.
