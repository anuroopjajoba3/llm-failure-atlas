"""
Graders for Category 4: Context Window Traps
Tests whether the model correctly applied buried constraints,
late updates, unit conversions, and redefined variables.
"""


def grade_CT01(fn):
    # Key test: on-sale items should NOT get the discount
    cases = [
        # (price, is_on_sale, code), expected
        ((100, False, "SAVE20"), 80.0),    # not on sale + code = 20% off
        ((100, True, "SAVE20"), 100.0),    # ON SALE + code = no discount (buried rule)
        ((100, False, None), 100.0),       # no code = no discount
        ((100, True, None), 100.0),        # on sale + no code = unchanged
        ((50, False, "SAVE20"), 40.0),     # not on sale + code = 20% off
        ((200, True, "SAVE20"), 200.0),    # on sale = price unchanged regardless of code
    ]
    results = []
    for (price, is_on_sale, code), expected in cases:
        try:
            got = fn(price, is_on_sale, code)
            passed = got == expected
            results.append({
                "input": f"price={price}, is_on_sale={is_on_sale}, code={code}",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"price={price}, is_on_sale={is_on_sale}, code={code}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_CT02(fn):
    # Correct: DESCENDING order (the update at the end of the prompt)
    cases = [
        ([3, 1, 2], [3, 2, 1]),
        ([1, 2, 3], [3, 2, 1]),
        ([5, 5, 5], [5, 5, 5]),
        ([], []),
        ([1], [1]),
        ([3.5, 1.2, 2.8], [3.5, 2.8, 1.2]),
    ]
    results = []
    for lst, expected in cases:
        try:
            got = fn(lst[:])
            passed = got == expected
            results.append({
                "input": str(lst),
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": str(lst),
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_CT03(fn):
    # Correct: threshold is 500km, input is in meters → threshold = 500,000 meters
    cases = [
        (600000, True),    # 600km > 500km → long distance
        (499000, False),   # 499km < 500km → not long distance
        (500000, False),   # exactly 500km → not long distance (must EXCEED)
        (500001, True),    # just over 500km → long distance
        (1000000, True),   # 1000km → long distance
        (100, False),      # 0.1km → definitely not long distance
        (600, False),      # 0.6km → correctly NOT long distance (fixed grader bug)
    ]
    results = []
    for meters, expected in cases:
        try:
            got = fn(meters)
            passed = got == expected
            results.append({
                "input": f"meters={meters} ({meters/1000}km)",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"meters={meters}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_CT04(fn):
    # Tests all categories including the buried exceptions
    cases = [
        (("electronics", 100), 15.0),   # 15%
        (("clothing", 100), 10.0),      # 10%
        (("food", 100), 0.0),           # 0% — buried in middle, common failure
        (("home goods", 100), 10.0),    # 10%
        (("books", 100), 5.0),          # 5% — also commonly missed
        (("luxury", 100), 25.0),        # 25%
        (("toys", 100), 10.0),          # 10%
        (("sporting goods", 100), 10.0), # 10%
    ]
    results = []
    for (category, price), expected in cases:
        try:
            got = fn(category, price)
            passed = abs(got - expected) < 0.01  # float comparison
            results.append({
                "input": f"category='{category}', price={price}",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"category='{category}', price={price}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_CT05(fn):
    # n = retry attempts so far, failed = did last attempt fail
    # should_retry = True only if failed AND n < 3
    cases = [
        ((0, True), True),    # 0 attempts, failed → retry
        ((1, True), True),    # 1 attempt, failed → retry
        ((2, True), True),    # 2 attempts, failed → retry (still under 3)
        ((3, True), False),   # 3 attempts, failed → no more retries
        ((0, False), False),  # 0 attempts, succeeded → no retry needed
        ((1, False), False),  # 1 attempt, succeeded → no retry needed
        ((10, True), False),  # 10 attempts → definitely stop
    ]
    results = []
    for (n, failed), expected in cases:
        try:
            got = fn(n, failed)
            passed = got == expected
            results.append({
                "input": f"n={n}, failed={failed}",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"n={n}, failed={failed}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


GRADERS = {
    "CT-01": grade_CT01,
    "CT-02": grade_CT02,
    "CT-03": grade_CT03,
    "CT-04": grade_CT04,
    "CT-05": grade_CT05,
}