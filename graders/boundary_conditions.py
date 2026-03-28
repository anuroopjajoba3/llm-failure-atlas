"""
Graders for Category 1: Boundary Conditions
Each grader runs the model's extracted function against test cases
and returns a result dict with pass/fail per test case.
"""


def grade_BC01(fn):
    cases = [
        (3, 4),
        (1, 2),
        (0, 1),   # most models fail here
        (100, 101),
        (10, 11),
    ]
    results = []
    for n, expected in cases:
        try:
            got = fn(n)
            results.append({
                "input": f"n={n}",
                "expected": expected,
                "got": got,
                "passed": got == expected,
            })
        except Exception as e:
            results.append({
                "input": f"n={n}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_BC02(fn):
    cases = [
        ((2, 5), [2, 3, 4, 5]),
        ((5, 5), [5]),         # single element — models return []
        ((5, 2), []),          # reversed — models crash or return wrong
        ((0, 0), [0]),
        ((-2, 2), [-2, -1, 0, 1, 2]),
    ]
    results = []
    for (a, b), expected in cases:
        try:
            got = fn(a, b)
            results.append({
                "input": f"a={a}, b={b}",
                "expected": expected,
                "got": got,
                "passed": got == expected,
            })
        except Exception as e:
            results.append({
                "input": f"a={a}, b={b}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_BC03(fn):
    cases = [
        ((10, 3), 4),
        ((9, 3), 3),    # exactly divisible — models return 4
        ((1, 10), 1),   # fewer items than page size
        ((0, 3), 0),    # zero items
        ((7, 7), 1),    # exactly one page
    ]
    results = []
    for (n, k), expected in cases:
        try:
            got = fn(n, k)
            results.append({
                "input": f"n={n}, k={k}",
                "expected": expected,
                "got": got,
                "passed": got == expected,
            })
        except Exception as e:
            results.append({
                "input": f"n={n}, k={k}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_BC04(fn):
    cases = [
        (("aa", "aaaa"), 3),
        (("ab", "ababab"), 3),
        (("aa", "aaa"), 2),
        (("xyz", "abcdef"), 0),
        (("a", "aaaa"), 4),    # single char — easy but confirms baseline
    ]
    results = []
    for (pattern, string), expected in cases:
        try:
            got = fn(pattern, string)
            results.append({
                "input": f"pattern='{pattern}', string='{string}'",
                "expected": expected,
                "got": got,
                "passed": got == expected,
            })
        except Exception as e:
            results.append({
                "input": f"pattern='{pattern}', string='{string}'",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_BC05(fn):
    cases = [
        ((5, 3, 4), 2),
        ((5, 0, 5), 0),    # full loop back to start
        ((5, 4, 1), 0),    # wrap from last index
        ((5, 0, 0), 0),    # zero steps
        ((1, 0, 100), 0),  # single element buffer
    ]
    results = []
    for (n, i, k), expected in cases:
        try:
            got = fn(n, i, k)
            results.append({
                "input": f"n={n}, i={i}, k={k}",
                "expected": expected,
                "got": got,
                "passed": got == expected,
            })
        except Exception as e:
            results.append({
                "input": f"n={n}, i={i}, k={k}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


GRADERS = {
    "BC-01": grade_BC01,
    "BC-02": grade_BC02,
    "BC-03": grade_BC03,
    "BC-04": grade_BC04,
    "BC-05": grade_BC05,
}