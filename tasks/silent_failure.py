"""
Category 3: Silent Failure
Code that runs without errors but produces wrong output.
The model thinks it's done. The grader catches what the model doesn't.
"""

TASKS = [
    {
        "id": "SF-01",
        "name": "Integer Square Root",
        "category": "silent_failure",
        "prompt": (
            "Write a Python function called `int_sqrt(n)` that returns the integer square root of n. "
            "The integer square root is the largest integer whose square is less than or equal to n. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models use int(math.sqrt(n)) which silently fails on large integers due to floating point precision. "
            "For very large n, the result is off by 1 with no error raised."
        ),
    },
    {
        "id": "SF-02",
        "name": "Sum of Digits",
        "category": "silent_failure",
        "prompt": (
            "Write a Python function called `digit_sum(n)` that returns the sum of the digits of n. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models handle positive integers correctly but fail silently on negatives. "
            "digit_sum(-123) often returns the same as digit_sum(123), or includes the minus sign causing wrong results. "
            "No crash, just a quietly wrong answer."
        ),
    },
    {
        "id": "SF-03",
        "name": "Caesar Cipher",
        "category": "silent_failure",
        "prompt": (
            "Write a Python function called `caesar(text, shift)` that encrypts text using a Caesar cipher. "
            "Shift each letter by the given amount. Preserve case. Leave non-letter characters unchanged. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models forget to wrap around the alphabet. caesar('xyz', 3) should return 'abc' "
            "but often returns '{|}'. Works fine for most inputs — only fails silently at the wrap boundary."
        ),
    },
    {
        "id": "SF-04",
        "name": "Running Average",
        "category": "silent_failure",
        "prompt": (
            "Write a Python function called `running_avg(numbers)` that returns a list where each element "
            "is the average of all numbers seen so far. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models use integer division // instead of /. running_avg([1, 2]) returns [1, 1] instead of [1.0, 1.5]. "
            "The list has the right length and looks plausible — the values are just quietly wrong."
        ),
    },
    {
        "id": "SF-05",
        "name": "Rotate List",
        "category": "silent_failure",
        "prompt": (
            "Write a Python function called `rotate(lst, k)` that rotates a list k positions to the right. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models rotate in the wrong direction, or off by one. "
            "rotate([1,2,3,4,5], 2) should return [4,5,1,2,3] but models often return [3,4,5,1,2]. "
            "The result looks like a valid rotation — just wrong direction or wrong amount."
        ),
    },
]