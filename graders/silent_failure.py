"""
Graders for Category 3: Silent Failure
These tasks all run without errors — the failure is in the output value.
"""


def grade_SF01(fn):
    cases = [
        (0, 0),
        (1, 1),
        (4, 2),
        (8, 2),
        (9, 3),
        (15, 3),
        (16, 4),
        # Large number where float precision silently breaks int(math.sqrt(n))
        (9999999999999999948, 3162277660168379),
    ]
    results = []
    for n, expected in cases:
        try:
            got = fn(n)
            passed = got == expected
            results.append({
                "input": f"n={n}",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"n={n}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_SF02(fn):
    cases = [
        (0, 0),
        (123, 6),
        (999, 27),
        (-123, 6),    # negative — should treat as positive digits
        (-999, 27),
        (100, 1),
        (10, 1),
    ]
    results = []
    for n, expected in cases:
        try:
            got = fn(n)
            passed = got == expected
            results.append({
                "input": f"n={n}",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"n={n}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_SF03(fn):
    cases = [
        (("abc", 1), "bcd"),
        (("xyz", 3), "abc"),       # wrap around — most common failure
        (("XYZ", 3), "ABC"),       # uppercase wrap
        (("Hello, World!", 13), "Uryyb, Jbeyq!"),  # ROT13, non-letters unchanged
        (("abc", 0), "abc"),       # zero shift
        (("abc", 26), "abc"),      # full rotation = same
        (("az", 1), "ba"),         # cross boundary
    ]
    results = []
    for (text, shift), expected in cases:
        try:
            got = fn(text, shift)
            passed = got == expected
            results.append({
                "input": f"text='{text}', shift={shift}",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"text='{text}', shift={shift}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_SF04(fn):
    cases = [
        ([1], [1.0]),
        ([1, 2], [1.0, 1.5]),              # integer division gives [1, 1]
        ([1, 2, 3], [1.0, 1.5, 2.0]),
        ([10, 20, 30], [10.0, 15.0, 20.0]),
        ([5, 5, 5, 5], [5.0, 5.0, 5.0, 5.0]),
        ([1, 3], [1.0, 2.0]),              # (1+3)/2 = 2.0, not 1
    ]
    results = []
    for numbers, expected in cases:
        try:
            got = fn(numbers[:])
            passed = got == expected
            results.append({
                "input": str(numbers),
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": str(numbers),
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


def grade_SF05(fn):
    # Rotate RIGHT: [1,2,3,4,5] by 2 → [4,5,1,2,3]
    cases = [
        (([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]),
        (([1, 2, 3, 4, 5], 1), [5, 1, 2, 3, 4]),
        (([1, 2, 3], 3), [1, 2, 3]),       # full rotation = same
        (([1, 2, 3], 0), [1, 2, 3]),       # zero rotation
        (([1, 2, 3, 4, 5], 7), [4, 5, 1, 2, 3]),  # k > len wraps
        (([1], 5), [1]),                   # single element
    ]
    results = []
    for (lst, k), expected in cases:
        try:
            got = fn(lst[:], k)
            passed = got == expected
            results.append({
                "input": f"lst={lst}, k={k}",
                "expected": expected,
                "got": got,
                "passed": passed,
            })
        except Exception as e:
            results.append({
                "input": f"lst={lst}, k={k}",
                "expected": expected,
                "got": f"ERROR: {e}",
                "passed": False,
            })
    return results


GRADERS = {
    "SF-01": grade_SF01,
    "SF-02": grade_SF02,
    "SF-03": grade_SF03,
    "SF-04": grade_SF04,
    "SF-05": grade_SF05,
}