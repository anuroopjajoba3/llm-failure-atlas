"""
Category 2: Ambiguous Requirements
Prompts with two or more valid interpretations.
The model picks one without acknowledging the ambiguity — that's the failure.
The grader tests the interpretation the model DIDN'T pick.
"""

TASKS = [
    {
        "id": "AR-01",
        "name": "Remove Duplicates",
        "category": "ambiguous_requirements",
        "prompt": (
            "Write a Python function called `remove_duplicates(lst)` that removes "
            "duplicate elements from a list. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Two valid interpretations: (1) keep first occurrence, (2) keep last occurrence. "
            "Models almost always keep first. Also ambiguous: does order matter? "
            "Most models return sorted or set-converted result losing original order."
        ),
        "correct_interpretation": "Keep first occurrence, preserve original order.",
    },
    {
        "id": "AR-02",
        "name": "Capitalize Words",
        "category": "ambiguous_requirements",
        "prompt": (
            "Write a Python function called `capitalize_words(s)` that capitalizes "
            "the words in a string. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Three valid interpretations: (1) title case every word, "
            "(2) capitalize only first word, (3) uppercase everything. "
            "Also ambiguous: what happens to already-capitalized letters mid-word? "
            "'hELLO' → 'Hello' or 'HELLO' or 'HEllo'? Models never ask."
        ),
        "correct_interpretation": "Title case — first letter of each word uppercase, rest lowercase.",
    },
    {
        "id": "AR-03",
        "name": "Find Middle Element",
        "category": "ambiguous_requirements",
        "prompt": (
            "Write a Python function called `find_middle(lst)` that returns "
            "the middle element of a list. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Ambiguous for even-length lists: return one middle, both middles, or average? "
            "For [1,2,3,4]: is middle 2, 3, [2,3], or 2.5? "
            "Models silently pick one without flagging the ambiguity. "
            "Also fails on empty list — most models crash."
        ),
        "correct_interpretation": "For odd length return middle element. For even length return the lower middle.",
    },
    {
        "id": "AR-04",
        "name": "Truncate String",
        "category": "ambiguous_requirements",
        "prompt": (
            "Write a Python function called `truncate(s, n)` that truncates a string "
            "to n characters. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Ambiguous: does n include the ellipsis or not? "
            "truncate('hello world', 7) → 'hell...' (4 chars + 3 dots = 7) "
            "or 'hello w...' (7 chars + 3 dots = 10)? "
            "Also: what if string is already shorter than n? Add ellipsis or return as-is? "
            "Models add ellipsis even when not needed."
        ),
        "correct_interpretation": "n is the max total length including ellipsis. If string fits, return as-is.",
    },
    {
        "id": "AR-05",
        "name": "Flatten List",
        "category": "ambiguous_requirements",
        "prompt": (
            "Write a Python function called `flatten(lst)` that flattens a nested list. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Ambiguous depth: flatten one level or all levels? "
            "[1, [2, [3, 4]]] → [1, 2, [3, 4]] (one level) or [1, 2, 3, 4] (full)? "
            "Models almost always do full flatten without asking. "
            "Also fails silently on mixed types: [1, 'hello', [2, 3]] — "
            "iterating over string characters is a common bug."
        ),
        "correct_interpretation": "Fully flatten all levels of nesting.",
    },
]