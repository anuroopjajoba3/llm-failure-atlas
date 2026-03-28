"""
Category 5: Overconfidence
The model gives a wrong answer with full confidence.
No hedging, no warnings, just a clean plausible incorrect solution.
"""

TASKS = [
    {
        "id": "OC-01",
        "name": "Floating Point Equality",
        "category": "overconfidence",
        "prompt": (
            "Write a Python function called `is_equal(a, b)` that returns True if "
            "two floating point numbers are equal, False otherwise. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Claude returns `a == b` which is confidently wrong for floats. "
            "0.1 + 0.2 == 0.3 is False in Python due to float representation. "
            "The correct approach uses math.isclose() with a tolerance."
        ),
    },
    {
        "id": "OC-02",
        "name": "Mutable Default Argument",
        "category": "overconfidence",
        "prompt": (
            "Write a Python function called `append_to(item, lst=[])` that appends "
            "item to lst and returns the list. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Classic Python trap. The default mutable argument persists across calls. "
            "append_to(1) then append_to(2) returns [1, 2] not [2]. "
            "Claude writes exactly what's asked with full confidence, not flagging the bug."
        ),
    },
    {
        "id": "OC-03",
        "name": "Most Frequent Element",
        "category": "overconfidence",
        "prompt": (
            "Write a Python function called `most_frequent(lst)` that returns the "
            "most frequent element in a list. If the list is empty, return None. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "When there's a tie, Claude picks one silently — usually whichever Counter "
            "happens to return first. most_frequent([1, 2, 1, 2]) — both appear twice. "
            "Claude returns 1 or 2 without acknowledging the tie exists."
        ),
    },
    {
        "id": "OC-04",
        "name": "Safe Dictionary Access",
        "category": "overconfidence",
        "prompt": (
            "Write a Python function called `get_value(d, key)` that safely retrieves "
            "a value from dictionary d for the given key. "
            "If the key does not exist, return 0. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Claude writes d.get(key, 0) which looks correct but fails when the key "
            "exists with value None — it returns None instead of 0. "
            "The model confidently implements the obvious solution without considering None values."
        ),
    },
    {
        "id": "OC-05",
        "name": "Count Unique Words",
        "category": "overconfidence",
        "prompt": (
            "Write a Python function called `count_unique_words(text)` that returns "
            "the number of unique words in a string. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Claude splits on spaces and counts unique items but fails on punctuation. "
            "'hello, hello.' → ['hello,', 'hello.'] are counted as 2 unique words not 1. "
            "Also fails on mixed case: 'Hello hello' → 2 unique instead of 1. "
            "The confident naive implementation misses both edge cases silently."
        ),
    },
]