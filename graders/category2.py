"""
Graders for:
- Category 1 Hardened (BC-01H through BC-05H)
- Category 2: Ambiguous Requirements (AR-01 through AR-05)
"""

# ─────────────────────────────────────────────
# HARDENED BOUNDARY CONDITIONS
# ─────────────────────────────────────────────

def grade_BC01H(fn):
    cases = [
        (3, 4),
        (1, 2),
        (0, 1),    # no hint given — does model handle this?
        (100, 101),
    ]
    results = []
    for n, expected in cases:
        try:
            got = fn(n)
            results.append({"input": f"n={n}", "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": f"n={n}", "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


def grade_BC02H(fn):
    # "between a and b" — does model include endpoints?
    cases = [
        ((2, 5), [2, 3, 4, 5]),   # inclusive both ends (correct interpretation)
        ((5, 5), [5]),             # a == b
        ((5, 2), []),              # reversed
        ((-1, 1), [-1, 0, 1]),
    ]
    results = []
    for (a, b), expected in cases:
        try:
            got = fn(a, b)
            results.append({"input": f"a={a}, b={b}", "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": f"a={a}, b={b}", "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


def grade_BC03H(fn):
    cases = [
        ((10, 3), 4),
        ((9, 3), 3),
        ((0, 3), 0),    # no hint — does model handle n=0?
        ((1, 10), 1),
        ((7, 7), 1),
    ]
    results = []
    for (n, k), expected in cases:
        try:
            got = fn(n, k)
            results.append({"input": f"n={n}, k={k}", "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": f"n={n}, k={k}", "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


def grade_BC04H(fn):
    # Without "overlapping" in prompt — does model use str.count()?
    cases = [
        (("aa", "aaaa"), 3),      # str.count() returns 2 — EXPECTED FAILURE
        (("ab", "ababab"), 3),
        (("aa", "aaa"), 2),       # str.count() returns 1 — EXPECTED FAILURE
        (("xyz", "abcdef"), 0),
    ]
    results = []
    for (pattern, string), expected in cases:
        try:
            got = fn(pattern, string)
            results.append({"input": f"pattern='{pattern}', string='{string}'", "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": f"pattern='{pattern}', string='{string}'", "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


def grade_BC05H(fn):
    cases = [
        ((5, 3, 4), 2),
        ((5, 0, 5), 0),
        ((5, 4, 1), 0),
        ((5, 0, 0), 0),
        ((1, 0, 100), 0),
    ]
    results = []
    for (n, i, k), expected in cases:
        try:
            got = fn(n, i, k)
            results.append({"input": f"n={n}, i={i}, k={k}", "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": f"n={n}, i={i}, k={k}", "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


# ─────────────────────────────────────────────
# AMBIGUOUS REQUIREMENTS
# ─────────────────────────────────────────────

def grade_AR01(fn):
    # Correct: keep first occurrence, preserve order
    cases = [
        ([1, 2, 3, 2, 1], [1, 2, 3]),
        ([1, 1, 1], [1]),
        ([], []),
        (['a', 'b', 'a', 'c'], ['a', 'b', 'c']),
        ([3, 1, 2, 1, 3], [3, 1, 2]),   # order preserved, not sorted
    ]
    results = []
    for lst, expected in cases:
        try:
            got = fn(lst[:])   # pass copy so fn can't mutate original
            results.append({"input": str(lst), "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": str(lst), "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


def grade_AR02(fn):
    # Correct: title case, first letter upper rest lower
    cases = [
        ("hello world", "Hello World"),
        ("HELLO WORLD", "Hello World"),   # models often leave as HELLO WORLD
        ("hello", "Hello"),
        ("", ""),
        ("it's a test", "It's A Test"),
    ]
    results = []
    for s, expected in cases:
        try:
            got = fn(s)
            results.append({"input": repr(s), "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": repr(s), "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


def grade_AR03(fn):
    # Correct: odd → middle, even → lower middle
    cases = [
        ([1, 2, 3], 2),
        ([1, 2, 3, 4], 2),      # even: lower middle — models often return 3
        ([1], 1),
        ([1, 2, 3, 4, 5], 3),
        ([10, 20], 10),         # even 2-element: lower middle
    ]
    results = []
    for lst, expected in cases:
        try:
            got = fn(lst[:])
            results.append({"input": str(lst), "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": str(lst), "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


def grade_AR04(fn):
    # Correct: n = max total length including ellipsis; no ellipsis if fits
    cases = [
        (("hello world", 7), "hell..."),   # 4 + 3 = 7
        (("hello", 10), "hello"),          # fits — no ellipsis
        (("hello world", 11), "hello world"),  # exact fit — no ellipsis
        (("hi", 5), "hi"),                 # short string — no ellipsis
        (("hello world", 5), "he..."),     # 2 + 3 = 5
    ]
    results = []
    for (s, n), expected in cases:
        try:
            got = fn(s, n)
            results.append({"input": f"s='{s}', n={n}", "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": f"s='{s}', n={n}", "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


def grade_AR05(fn):
    # Correct: full flatten all levels
    cases = [
        ([1, [2, 3]], [1, 2, 3]),
        ([1, [2, [3, 4]]], [1, 2, 3, 4]),
        ([], []),
        ([1, 2, 3], [1, 2, 3]),            # already flat
        ([[1, 2], [3, [4, 5]]], [1, 2, 3, 4, 5]),
    ]
    results = []
    for lst, expected in cases:
        try:
            got = fn(lst)
            results.append({"input": str(lst), "expected": expected, "got": got, "passed": got == expected})
        except Exception as e:
            results.append({"input": str(lst), "expected": expected, "got": f"ERROR: {e}", "passed": False})
    return results


GRADERS = {
    "BC-01H": grade_BC01H,
    "BC-02H": grade_BC02H,
    "BC-03H": grade_BC03H,
    "BC-04H": grade_BC04H,
    "BC-05H": grade_BC05H,
    "AR-01": grade_AR01,
    "AR-02": grade_AR02,
    "AR-03": grade_AR03,
    "AR-04": grade_AR04,
    "AR-05": grade_AR05,
}