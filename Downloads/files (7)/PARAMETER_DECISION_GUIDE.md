# BEX CALCULATOR PARAMETERS - DECISION GUIDE

## CURRENT SITUATION

**BE's Current Volatility: 113-140% (VERY HIGH)**
- Classification: High Volatility Regime (>70%)
- This matters because optimal parameters CHANGE by volatility

---

## TWO OPTIONS FOR ANDREW

### **OPTION A: Static Aggressive (4.0x / 20%)**

**Parameters:**
```python
MULTIPLIER = 4.0
CAP = 0.20  # 20%
```

**Performance:**
- Full period (6.5 years): -14.23% (BEST overall)
- High volatility periods: -14.23% (underperforms)
- Normal volatility: Positive returns
- Low volatility: +56% returns
- Recent 13-day test: +20.48% (outperformed)

**When to use:**
- You believe BE will trend upward
- You want maximum cash extraction long-term
- You're willing to accept short-term underperformance in high vol
- You want simplicity (no regime monitoring)

**Pros:**
✅ Best long-term performance
✅ Maximum extraction in bull markets
✅ Simple - set and forget
✅ Validated on 6.5 years of data

**Cons:**
❌ Underperforms RIGHT NOW (high vol regime)
❌ More aggressive = higher risk
❌ Suboptimal in current conditions

---

### **OPTION B: Adaptive Conservative (2.0x / 8% for current high vol)**

**Parameters for Current High Volatility:**
```python
MULTIPLIER = 2.0
CAP = 0.08  # 8%
```

**Performance:**
- High volatility periods: +6.53% (POSITIVE RETURNS!)
- Normal volatility: +27.20% (excellent)
- Low volatility: +47.30% (good)
- Full period: -26.14% (worse than aggressive)

**When to use:**
- BE is currently in high volatility (it is - 113%)
- You want positive returns RIGHT NOW
- You're willing to monitor and adjust parameters
- You prefer conservative approach in chaos

**Pros:**
✅ Makes POSITIVE returns in current high vol (+6.53%)
✅ Better risk-adjusted returns
✅ Lower drawdowns (-30% vs -19%)
✅ Optimal for TODAY's conditions

**Cons:**
❌ Requires monitoring volatility
❌ Need to change parameters when regime shifts
❌ Worse long-term performance
❌ Misses gains in bull runs

---

## PERFORMANCE COMPARISON - HIGH VOLATILITY (CURRENT)

**BE Volatility: 113% (HIGH)**

| Strategy | Return | Sharpe | Max DD | Cap Hit % |
|----------|--------|--------|--------|-----------|
| **2.0x / 8% (Conservative)** | **+6.53%** | 0.20 | -30% | 48% |
| 4.0x / 20% (Aggressive) | -14.23% | -0.45 | -19% | 31% |
| **Difference** | **+20.76%** | | | |

**In current conditions, conservative is 20.76% better!**

---

## HOW TO SWITCH BETWEEN OPTIONS

### **Option A (Static Aggressive) - DEFAULT:**
Calculator already set to 4.0 / 20%
- No action needed
- Best for long-term

### **Option B (Adaptive Conservative) - FOR CURRENT HIGH VOL:**
In the Streamlit file, uncomment these lines:
```python
# MULTIPLIER = 2.0
# CAP = 0.08  # 8%
```

And comment out:
```python
# MULTIPLIER = 4.0
# CAP = 0.20
```

---

## MONITORING VOLATILITY

**To know when to switch back to aggressive:**

**Check BE's 20-day realized volatility:**
- If vol drops below 70%: Switch to 4.0 / 20%
- If vol stays above 70%: Keep 2.0 / 8%

**How to calculate:**
```
20-day realized vol = stdev(daily_returns) × sqrt(252) × 100
```

**Or use a platform:**
- TradingView: Add "Historical Volatility" indicator
- Think or Swim: Use `.HV20` study
- Yahoo Finance: Check implied volatility as proxy

---

## MY RECOMMENDATION

### **For Andrew Right Now:**

**Use OPTION B: Conservative 2.0 / 8%**

**Why:**
1. ✅ BE is currently in HIGH volatility (113%)
2. ✅ Makes POSITIVE returns (+6.53%) vs negative (-14.23%)
3. ✅ 20.76% performance advantage in current regime
4. ✅ Lower risk, better Sharpe ratio
5. ✅ Market is choppy, conservative wins

**When BE volatility drops below 70%:**
- Switch to aggressive 4.0 / 20%
- Capture maximum gains in trending market

---

## REAL EXAMPLES WITH BOTH PARAMETERS

**Scenario: BE moves +5% today, you have 1000 BEX shares**

### **With Conservative (2.0 / 8%):**
```
Offset = min(8%, 2.0 × 5%) = 8% (capped)
Sell: 80 shares
Extract: $80 × price = cash
Keep: 920 shares
```

### **With Aggressive (4.0 / 20%):**
```
Offset = min(20%, 4.0 × 5%) = 20% (capped)
Sell: 200 shares
Extract: $200 × price = cash
Keep: 800 shares
```

**Aggressive extracts 2.5x more per event.**
**But in high volatility, this can backfire.**

---

## UPDATED FILES

**Streamlit Calculator:**
- File: bex_calculator_streamlit.py
- Default: Set to 4.0 / 20% (Option A)
- To switch: Uncomment conservative lines (Option B)

**React Calculator:**
- File: bex_calculator_react.jsx
- Update: Will update to match chosen option

---

## BOTTOM LINE

**Two valid approaches:**

**Conservative (2.0 / 8%):**
- Best for RIGHT NOW
- Makes money in current high vol
- Requires monitoring

**Aggressive (4.0 / 20%):**
- Best for LONG TERM
- Maximum extraction over time
- Set and forget

**Which should Andrew use?**

If Andrew can monitor volatility → Use conservative now, switch to aggressive later
If Andrew wants set-and-forget → Use aggressive and accept current underperformance

**My vote: Conservative for current market (113% vol), then aggressive when it calms.**
