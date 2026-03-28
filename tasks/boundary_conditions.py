"""
Category 1: Boundary Conditions
Tasks designed to expose off-by-one errors and edge case failures in LLMs.
"""

TASKS = [
    {
        "id": "BC-01",
        "name": "Fence Post Problem",
        "category": "boundary_conditions",
        "prompt": (
            "Write a Python function called `fence_posts(n)` that returns the number "
            "of fence posts needed to build a fence with n sections. "
            "A fence with 3 sections needs 4 posts. "
            "A fence with 0 sections needs 1 post (the corner post still exists). "
            "Return only the function, no explanation."
        ),
        "known_failure": "Models return n instead of n+1, and almost always fail on n=0.",
    },
    {
        "id": "BC-02",
        "name": "Inclusive Range",
        "category": "boundary_conditions",
        "prompt": (
            "Write a Python function called `inclusive_range(a, b)` that returns a list "
            "of all integers from a to b, inclusive on both ends. "
            "If a > b, return an empty list. "
            "If a == b, return a list with just that one number. "
            "Return only the function, no explanation."
        ),
        "known_failure": "Models use range(a, b) which excludes b. Single element case often returns [].",
    },
    {
        "id": "BC-03",
        "name": "Last Page Number",
        "category": "boundary_conditions",
        "prompt": (
            "Write a Python function called `last_page(n, k)` that returns the last page number "
            "when paginating n items with k items per page (1-indexed pages). "
            "Example: 10 items, page size 3 → last page is 4. "
            "If n is 0, return 0. "
            "Return only the function, no explanation."
        ),
        "known_failure": "Models use n // k and miss ceiling division. n % k == 0 case returns page+1.",
    },
    {
        "id": "BC-04",
        "name": "Overlapping Substring Count",
        "category": "boundary_conditions",
        "prompt": (
            "Write a Python function called `count_overlapping(pattern, string)` that counts "
            "how many times pattern appears in string, counting overlapping occurrences. "
            "Example: pattern='aa', string='aaaa' → 3 (positions 0,1,2). "
            "Return only the function, no explanation."
        ),
        "known_failure": "Models use str.count() which skips overlaps. 'aaaa'.count('aa') returns 2 not 3.",
    },
    {
        "id": "BC-05",
        "name": "Circular Buffer Index",
        "category": "boundary_conditions",
        "prompt": (
            "Write a Python function called `circular_index(n, i, k)` that returns the index "
            "that is k steps forward from index i in a circular buffer of size n. "
            "Example: n=5, i=3, k=4 → 2. "
            "Return only the function, no explanation."
        ),
        "known_failure": "Models get the basic case right but fail on k=0, single element buffer, or full loop.",
    },
]