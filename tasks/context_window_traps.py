"""
Category 4: Context Window Traps
Critical information is buried in long prompts.
Models anchor on early instructions, ignore updates, or miss buried constraints.
"""

TASKS = [
    {
        "id": "CT-01",
        "name": "Hidden Constraint",
        "category": "context_window_traps",
        "prompt": (
            "You are building a discount system for an e-commerce platform. "
            "The platform sells a wide variety of products including electronics, clothing, food, and home goods. "
            "Customers can apply discount codes at checkout to receive a percentage off their purchase. "
            "The discount system was designed to be flexible and support multiple code types. "
            "Note: discount codes cannot be applied to items that are already on sale. "
            "If an item is on sale, the discount code should be ignored and the original sale price returned as-is. "
            "The standard discount code gives 20% off the listed price. "
            "Write a Python function called `apply_discount(price, is_on_sale, code)` that returns the final price. "
            "If a code is provided and the item is not on sale, apply 20% off. "
            "If the item is on sale, ignore the code and return the price unchanged. "
            "If no code is provided, return the price unchanged. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Claude may apply the discount regardless of is_on_sale, ignoring the buried constraint. "
            "The constraint is stated once in the middle of a long paragraph and models often anchor "
            "on the function signature and final instructions instead."
        ),
    },
    {
        "id": "CT-02",
        "name": "Contradicting Update",
        "category": "context_window_traps",
        "prompt": (
            "Write a function to sort a list of numbers in ascending order. "
            "The function will be used in a leaderboard system where lower scores are better. "
            "Ascending order means smallest values appear first, which aligns with our ranking system. "
            "The function should handle duplicates correctly and preserve them in the output. "
            "It should also handle empty lists gracefully by returning an empty list. "
            "The function should work with both integers and floating point numbers. "
            "After further discussion with the client, the requirements have changed. "
            "The leaderboard was redesigned and now higher scores are better. "
            "Please sort in descending order instead, so the highest value appears first. "
            "Write a Python function called `sort_list(lst)` that sorts the list. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models anchor on the first instruction (ascending) and ignore the update buried near the end (descending). "
            "The result looks correct for ascending order but fails the descending grader."
        ),
    },
    {
        "id": "CT-03",
        "name": "Unit Mismatch",
        "category": "context_window_traps",
        "prompt": (
            "You are building a logistics system for a delivery company. "
            "All internal distance measurements in this system are stored and processed in kilometers. "
            "The database stores every route distance in kilometers. "
            "Reports, dashboards, and APIs all use kilometers as the standard unit. "
            "The delivery system classifies routes as long distance if they exceed 500 kilometers. "
            "However, the GPS devices used by drivers report distances in meters. "
            "The function you are writing receives raw GPS data from the driver's device. "
            "Write a Python function called `is_long_distance(meters)` that takes a distance "
            "in meters as input and returns True if the route is long distance, False otherwise. "
            "Remember that the threshold of 500 is defined in kilometers. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models use 500 as the raw threshold against the meters input, ignoring the unit conversion. "
            "is_long_distance(600000) should return True (600km > 500km) but models return True for "
            "anything over 500 meters, making almost every delivery 'long distance'."
        ),
    },
    {
        "id": "CT-04",
        "name": "Buried Exception",
        "category": "context_window_traps",
        "prompt": (
            "Build a tax calculation function for a retail system. "
            "The standard tax rate is 10% applied to all purchases. "
            "Electronics have a higher tax rate of 15% due to import duties. "
            "Clothing is taxed at the standard rate of 10%. "
            "Raw food items and groceries are completely tax-exempt — they have a 0% tax rate. "
            "Home goods and furniture are taxed at the standard 10% rate. "
            "Sporting goods follow the standard 10% rate as well. "
            "Books and educational materials are taxed at 5% as a reduced rate. "
            "Luxury goods including jewelry and watches are taxed at 25%. "
            "Toys and games follow the standard 10% rate. "
            "Automotive parts are taxed at 10%. "
            "Write a Python function called `calculate_tax(category, price)` that returns "
            "the tax amount (not the total price) for a given product category and price. "
            "Use lowercase category names. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models correctly handle electronics (15%) and luxury (25%) since they stand out. "
            "But food (0%) is buried in the middle and gets missed — models return 10% for food. "
            "Books (5%) is also commonly missed. The buried exceptions are the failure points."
        ),
    },
    {
        "id": "CT-05",
        "name": "Redefined Variable",
        "category": "context_window_traps",
        "prompt": (
            "You are building a retry system for a distributed API client. "
            "In this system, n represents the total number of active users currently connected. "
            "The system monitors n to decide when to scale infrastructure. "
            "When n exceeds 10000, the system triggers auto-scaling. "
            "Each API call is tracked and logged with the user count at time of call. "
            "For the retry logic specifically, the variable n takes on a different meaning. "
            "In the context of retries, n represents the current number of retry attempts made so far. "
            "The retry system should allow a maximum of 3 attempts before giving up. "
            "Write a Python function called `should_retry(n, failed)` where n is the number of "
            "retry attempts made so far, and failed is a boolean indicating if the last attempt failed. "
            "Return True if another retry should be attempted, False otherwise. "
            "A retry should happen only if the attempt failed AND fewer than 3 attempts have been made. "
            "Return only the function, no explanation."
        ),
        "known_failure": (
            "Models confuse the two definitions of n. The first definition (active users, threshold 10000) "
            "can bleed into the retry logic, causing models to use 10000 as the max retry count "
            "or to add unnecessary scaling checks. The redefinition in the middle of the prompt is the trap."
        ),
    },
]