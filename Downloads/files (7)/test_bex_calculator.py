"""
Comprehensive test suite for BEX Calculator
Tests various scenarios and edge cases
"""

import sys

# Test scenarios
TEST_SCENARIOS = [
    {
        "name": "Small Gain - Below Cap",
        "yesterday_close": 100.0,
        "today_close": 105.0,
        "position": 1000.0,
        "position_type": "Shares",
        "strategy": "Aggressive",
        "expected_return": 0.05,
        "expected_offset": 0.20,  # 4.0 * 0.05 = 0.20, capped at 0.20
        "expected_shares": 200.0
    },
    {
        "name": "Large Gain - Hits Cap",
        "yesterday_close": 100.0,
        "today_close": 120.0,
        "position": 1000.0,
        "position_type": "Shares",
        "strategy": "Aggressive",
        "expected_return": 0.20,
        "expected_offset": 0.20,  # 4.0 * 0.20 = 0.80, capped at 0.20
        "expected_shares": 200.0
    },
    {
        "name": "Conservative Strategy - Small Gain",
        "yesterday_close": 100.0,
        "today_close": 105.0,
        "position": 1000.0,
        "position_type": "Shares",
        "strategy": "Conservative",
        "expected_return": 0.05,
        "expected_offset": 0.08,  # 2.0 * 0.05 = 0.10, but capped at 0.08
        "expected_shares": 80.0
    },
    {
        "name": "Price Decline - No Action",
        "yesterday_close": 100.0,
        "today_close": 95.0,
        "position": 1000.0,
        "position_type": "Shares",
        "strategy": "Aggressive",
        "expected_return": -0.05,
        "expected_offset": 0.0,
        "expected_shares": 0.0
    },
    {
        "name": "Flat Price - No Action",
        "yesterday_close": 100.0,
        "today_close": 100.0,
        "position": 1000.0,
        "position_type": "Shares",
        "strategy": "Aggressive",
        "expected_return": 0.0,
        "expected_offset": 0.0,
        "expected_shares": 0.0
    },
    {
        "name": "Dollar Value Position",
        "yesterday_close": 100.0,
        "today_close": 110.0,
        "position": 100000.0,
        "position_type": "Dollar Value",
        "strategy": "Aggressive",
        "expected_return": 0.10,
        "expected_offset": 0.20,  # 4.0 * 0.10 = 0.40, capped at 0.20
        "expected_shares": None  # Will calculate
    },
    {
        "name": "Very Small Position",
        "yesterday_close": 50.0,
        "today_close": 51.0,
        "position": 10.0,
        "position_type": "Shares",
        "strategy": "Aggressive",
        "expected_return": 0.02,
        "expected_offset": 0.08,  # 4.0 * 0.02 = 0.08, below cap
        "expected_shares": 0.8
    },
    {
        "name": "Moderate Strategy - Medium Gain",
        "yesterday_close": 100.0,
        "today_close": 108.0,
        "position": 1000.0,
        "position_type": "Shares",
        "strategy": "Moderate",
        "expected_return": 0.08,
        "expected_offset": 0.125,  # 3.0 * 0.08 = 0.24, capped at 0.125
        "expected_shares": 125.0
    },
    {
        "name": "Realistic BE Scenario - High Volatility",
        "yesterday_close": 102.50,
        "today_close": 118.09,
        "position": 670.0,
        "position_type": "Shares",
        "strategy": "Aggressive",
        "expected_return": 0.1521,
        "expected_offset": 0.20,  # 4.0 * 0.1521 = 0.6084, capped at 0.20
        "expected_shares": 134.0
    },
    {
        "name": "Conservative - High Volatility",
        "yesterday_close": 102.50,
        "today_close": 118.09,
        "position": 670.0,
        "position_type": "Shares",
        "strategy": "Conservative",
        "expected_return": 0.1521,
        "expected_offset": 0.08,  # 2.0 * 0.1521 = 0.3042, capped at 0.08
        "expected_shares": 53.6
    },
]

# Strategy parameters
STRATEGIES = {
    "Aggressive": {"multiplier": 4.0, "cap": 0.20},
    "Conservative": {"multiplier": 2.0, "cap": 0.08},
    "Moderate": {"multiplier": 3.0, "cap": 0.125}
}

def calculate_offset(yesterday_close, today_close, position, position_type, strategy_name):
    """Calculate the rebalancing offset"""
    if yesterday_close <= 0 or today_close <= 0 or position <= 0:
        return None, None, None, None
    
    daily_return = (today_close - yesterday_close) / yesterday_close
    
    if daily_return <= 0:
        return daily_return, 0.0, 0.0, 0.0
    
    strategy = STRATEGIES[strategy_name]
    multiplier = strategy["multiplier"]
    cap = strategy["cap"]
    
    raw_offset = multiplier * daily_return
    offset_percent = min(cap, raw_offset)
    
    if position_type == "Shares":
        shares_to_sell = position * offset_percent
        dollar_value = shares_to_sell * today_close
        new_position = position - shares_to_sell
    else:
        dollar_value = position * offset_percent
        shares_to_sell = dollar_value / today_close
        new_position = position - dollar_value
    
    return daily_return, offset_percent, shares_to_sell, dollar_value

def run_tests():
    """Run all test scenarios"""
    results = []
    passed = 0
    failed = 0
    
    print("=" * 80)
    print("BEX CALCULATOR TEST SUITE")
    print("=" * 80)
    print()
    
    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        print(f"Test {i}: {scenario['name']}")
        print("-" * 80)
        
        daily_return, offset_percent, shares_to_sell, dollar_value = calculate_offset(
            scenario["yesterday_close"],
            scenario["today_close"],
            scenario["position"],
            scenario["position_type"],
            scenario["strategy"]
        )
        
        # Check results
        return_match = abs(daily_return - scenario["expected_return"]) < 0.0001
        offset_match = abs(offset_percent - scenario["expected_offset"]) < 0.0001
        
        if scenario["expected_shares"] is not None:
            shares_match = abs(shares_to_sell - scenario["expected_shares"]) < 0.1
        else:
            shares_match = True  # Skip check for dollar value positions
        
        test_passed = return_match and offset_match and shares_match
        
        # Print details
        print(f"  Strategy: {scenario['strategy']}")
        print(f"  Input: ${scenario['yesterday_close']:.2f} → ${scenario['today_close']:.2f}")
        print(f"  Position: {scenario['position']:.0f} {scenario['position_type']}")
        print(f"  Daily Return: {daily_return * 100:.2f}% (expected: {scenario['expected_return'] * 100:.2f}%) {'✓' if return_match else '✗'}")
        print(f"  Offset Applied: {offset_percent * 100:.2f}% (expected: {scenario['expected_offset'] * 100:.2f}%) {'✓' if offset_match else '✗'}")
        expected_shares_str = f"{scenario['expected_shares']:.1f}" if scenario['expected_shares'] is not None else "N/A"
        print(f"  Shares to Sell: {shares_to_sell:.1f} (expected: {expected_shares_str}) {'✓' if shares_match else '✗'}")
        print(f"  Cash Extracted: ${dollar_value:,.2f}")
        
        if test_passed:
            print(f"  Status: ✓ PASSED")
            passed += 1
        else:
            print(f"  Status: ✗ FAILED")
            failed += 1
        
        print()
        
        results.append({
            "test": scenario["name"],
            "passed": test_passed,
            "daily_return": daily_return,
            "offset_percent": offset_percent,
            "shares_to_sell": shares_to_sell,
            "dollar_value": dollar_value,
            "details": {
                "yesterday": scenario["yesterday_close"],
                "today": scenario["today_close"],
                "position": scenario["position"],
                "position_type": scenario["position_type"],
                "strategy": scenario["strategy"]
            }
        })
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(TEST_SCENARIOS)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Success Rate: {(passed / len(TEST_SCENARIOS) * 100):.1f}%")
    print("=" * 80)
    
    return results, passed, failed

if __name__ == "__main__":
    results, passed, failed = run_tests()
    
    # Write results to file
    output_file = "test_results_bex_calculator.txt"
    with open(output_file, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("BEX CALCULATOR TEST RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"Test {i}: {result['test']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Status: {'PASSED ✓' if result['passed'] else 'FAILED ✗'}\n")
            f.write(f"Strategy: {result['details']['strategy']}\n")
            f.write(f"Price: ${result['details']['yesterday']:.2f} → ${result['details']['today']:.2f}\n")
            f.write(f"Position: {result['details']['position']:.0f} {result['details']['position_type']}\n")
            f.write(f"Daily Return: {result['daily_return'] * 100:.2f}%\n")
            f.write(f"Offset Applied: {result['offset_percent'] * 100:.2f}%\n")
            f.write(f"Shares to Sell: {result['shares_to_sell']:.1f}\n")
            f.write(f"Cash Extracted: ${result['dollar_value']:,.2f}\n")
            f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total Tests: {len(results)}\n")
        f.write(f"Passed: {passed}\n")
        f.write(f"Failed: {failed}\n")
        f.write(f"Success Rate: {(passed / len(results) * 100):.1f}%\n")
    
    print(f"\nResults saved to: {output_file}")
    
    sys.exit(0 if failed == 0 else 1)

