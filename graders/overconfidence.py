"""
Graders for Category 5: Overconfidence
The model's confident answer is wrong in specific edge cases.
"""
import math


def grade_OC01(fn):
    # Float equality must use tolerance, not ==
    cases = [
        ((0.1 + 0.2, 0.3), True),      # classic float trap — == returns False
        ((1.0, 1.0), True),             # exact match
        ((0.0, 0.0), True),             # zero
        ((1.0, 1.0000001), False),      # genuinely different
        ((1.0 / 3.0, 0.3333333333333333), True),  # float representation
        ((0.1 + 0.1 + 0.1, 0.3), True), # another classic trap
    ]
    results = []
    for (a, b), expected in cases:
        try:
            got = fn(a, b)
            passed = got == expected
            results.append({
                "input": f"a={a}, b={b}",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"a={a}, b={b}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_OC02(fn):
    # Mutable default argument — each call must be independent
    # We test by calling the function multiple times and checking isolation
    results = []

    # Reset between tests by calling with explicit list
    cases = [
        # Each tested independently by passing explicit lst
        {"desc": "single item explicit list", "args": (1, []), "expected": [1]},
        {"desc": "multiple items explicit list", "args": (2, [1]), "expected": [1, 2]},
        {"desc": "empty explicit list", "args": (5, []), "expected": [5]},
    ]

    for case in cases:
        try:
            got = fn(*case["args"])
            passed = got == case["expected"]
            results.append({
                "input": str(case["args"]),
                "expected": case["expected"],
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": str(case["args"]),
                "expected": case["expected"],
                "got": f"ERROR: {e}",
                "passed": False,
            })

    # The real test — call twice with no explicit list, second call must not accumulate
    try:
        fn(1)  # first call — populates default list
        got2 = fn(2)  # second call — should return [2] not [1, 2]
        passed = got2 == [2]
        results.append({
            "input": "fn(1) then fn(2) with no explicit lst",
            "expected": [2],
            "got": got2,
            "passed": passed,
        })
    except Exception as e:
        results.append({
            "input": "fn(1) then fn(2) with no explicit lst",
            "expected": [2],
            "got": f"ERROR: {e}",
            "passed": False,
        })

    return results


def grade_OC03(fn):
    # Tie-breaking: when elements are equally frequent, return the one that appears first
    cases = [
        ([1, 2, 3, 1], 1),            # clear winner
        ([1, 2, 1, 2], 1),            # tie — first element wins (1 appears first)
        ([3, 3, 2, 2, 1], 3),         # tie between 3 and 2 — 3 appears first
        (["a", "b", "a"], "a"),       # strings
        ([1], 1),                      # single element
        ([], None),                    # empty list
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


def grade_OC04(fn):
    # Safe dict access — key missing → 0, key exists with None → 0, key exists with value → value
    cases = [
        ({"a": 1}, "a", 1),           # key exists with value
        ({"a": 1}, "b", 0),           # key missing → 0
        ({"a": None}, "a", 0),        # key exists with None → should return 0 (common failure)
        ({}, "x", 0),                  # empty dict
        ({"a": 0}, "a", 0),           # key exists with 0 → return 0
        ({"a": False}, "a", False),   # key exists with False → return False (not 0)
    ]
    results = []
    for d, key, expected in cases:
        try:
            got = fn(d, key)
            passed = got == expected
            results.append({
                "input": f"d={d}, key='{key}'",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"d={d}, key='{key}'",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_OC05(fn):
    # Unique words — must handle punctuation and case
    cases = [
        ("hello world", 2),                    # basic
        ("hello hello", 1),                    # duplicate — case insensitive
        ("Hello hello", 1),                    # mixed case same word
        ("hello, hello.", 1),                  # punctuation — naive split gives 2
        ("the cat sat on the mat", 5),         # repeated 'the' and unique words
        ("", 0),                               # empty string
        ("one", 1),                            # single word
    ]
    results = []
    for text, expected in cases:
        try:
            got = fn(text)
            passed = got == expected
            results.append({
                "input": repr(text),
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": repr(text),
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


GRADERS = {
    "OC-01": grade_OC01,
    "OC-02": grade_OC02,
    "OC-03": grade_OC03,
    "OC-04": grade_OC04,
    "OC-05": grade_OC05,
}