"""
Category 1: Boundary Conditions (Hardened)
Same tasks as before but with explicit hints removed.
Claude scored 5/5 on the easy versions — these are designed to actually make it fail.
"""

TASKS = [
    {
        "id": "BC-01H",
        "name": "Fence Post Problem (Hardened)",
        "category": "boundary_conditions_hardened",
        "prompt": (
            "Write a Python function called `fence_posts(n)` that returns the number "
            "of fence posts needed to build a fence with n sections. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Without the n=0 hint, models often return 0 or raise an error for n=0. "
            "Some return n instead of n+1 for very small n."
        ),
    },
    {
        "id": "BC-02H",
        "name": "Inclusive Range (Hardened)",
        "category": "boundary_conditions_hardened",
        "prompt": (
            "Write a Python function called `inclusive_range(a, b)` that returns a list "
            "of all integers between a and b. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "'Between' is ambiguous — models often exclude endpoints. "
            "Without 'inclusive on both ends', models use range(a+1, b) or range(a, b). "
            "Reversed range (a > b) almost always crashes or returns wrong result."
        ),
    },
    {
        "id": "BC-03H",
        "name": "Last Page Number (Hardened)",
        "category": "boundary_conditions_hardened",
        "prompt": (
            "Write a Python function called `last_page(n, k)` that returns the last page number "
            "when displaying n items with k items per page. Pages are numbered starting from 1. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Without the n=0 hint, models skip the zero case. "
            "Without the ceiling division hint, models use n // k and fail when n % k != 0."
        ),
    },
    {
        "id": "BC-04H",
        "name": "Overlapping Substring Count (Hardened)",
        "category": "boundary_conditions_hardened",
        "prompt": (
            "Write a Python function called `count_overlapping(pattern, string)` that counts "
            "how many times pattern appears in string. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Without 'overlapping' explicitly stated, models use str.count() which skips overlaps. "
            "This is the most reliable failure in Category 1 — str.count() is the obvious solution."
        ),
    },
    {
        "id": "BC-05H",
        "name": "Circular Buffer Index (Hardened)",
        "category": "boundary_conditions_hardened",
        "prompt": (
            "Write a Python function called `circular_index(n, i, k)` where n is the buffer size, "
            "i is the current index, and k is the number of steps forward. "
            "Return the resulting index. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Without examples, models sometimes forget to apply modulo. "
            "n=1 single element buffer with large k causes ZeroDivisionError in some models "
            "if they don't handle n=1 specially — but Claude usually gets (i+k)%n right. "
            "The real failure is k=0 returning wrong type or n=0 causing ZeroDivisionError."
        ),
    },
]