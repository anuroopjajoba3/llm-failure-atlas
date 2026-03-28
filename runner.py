"""
LLM Failure Atlas — Main Runner v5 (Final)
All 5 categories: BC, BCH, AR, SF, CT, OC

Usage:
    python runner.py

Requirements:
    pip install anthropic
    export ANTHROPIC_API_KEY=your_key
"""

import os
import re
import json
from datetime import datetime
from anthropic import Anthropic

from tasks.boundary_conditions import TASKS as BC_TASKS
from tasks.boundary_conditions_hardened import TASKS as BCH_TASKS
from tasks.ambiguous_requirements import TASKS as AR_TASKS
from tasks.silent_failure import TASKS as SF_TASKS
from tasks.context_window_traps import TASKS as CT_TASKS
from tasks.overconfidence import TASKS as OC_TASKS
from graders.boundary_conditions import GRADERS as BC_GRADERS
from graders.category2 import GRADERS as CAT2_GRADERS
from graders.silent_failure import GRADERS as SF_GRADERS
from graders.context_window_traps import GRADERS as CT_GRADERS
from graders.overconfidence import GRADERS as OC_GRADERS

client = Anthropic()
MODEL = "claude-opus-4-6"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

ALL_TASKS = BC_TASKS + BCH_TASKS + AR_TASKS + SF_TASKS + CT_TASKS + OC_TASKS
ALL_GRADERS = {**BC_GRADERS, **CAT2_GRADERS, **SF_GRADERS, **CT_GRADERS, **OC_GRADERS}


def ask_claude(prompt: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def extract_function(response: str, fn_name: str):
    code = re.sub(r"```(?:python)?", "", response).replace("```", "").strip()
    fn_match = re.search(rf"(def {fn_name}\(.*?(?=\ndef |\Z))", code, re.DOTALL)
    if fn_match:
        code = fn_match.group(1).strip()
    namespace = {}
    try:
        exec(code, namespace)
        return namespace.get(fn_name)
    except Exception:
        return None


def extract_fn_name(prompt: str) -> str:
    match = re.search(r"`(\w+)\(", prompt)
    return match.group(1) if match else "solution"


def run_task(task: dict) -> dict:
    task_id = task["id"]
    fn_name = extract_fn_name(task["prompt"])

    print(f"\n{'='*55}")
    print(f"  {task_id}: {task['name']}")
    print(f"{'='*55}")

    raw_response = ask_claude(task["prompt"])
    fn = extract_function(raw_response, fn_name)

    if fn is None:
        print("  Could not extract function")
        return {
            "task_id": task_id,
            "task_name": task["name"],
            "category": task["category"],
            "known_failure": task["known_failure"],
            "raw_response": raw_response,
            "extraction_failed": True,
            "test_results": [],
            "score": 0,
            "passed": 0,
            "total": 0,
        }

    grader = ALL_GRADERS.get(task_id)
    test_results = grader(fn)

    passed = sum(1 for r in test_results if r["passed"])
    total = len(test_results)
    score = passed / total if total > 0 else 0

    print(f"  Score: {passed}/{total} ({score*100:.0f}%)")
    for r in test_results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"    [{status}] {r['input']} -> expected {r['expected']}, got {r['got']}")

    return {
        "task_id": task_id,
        "task_name": task["name"],
        "category": task["category"],
        "known_failure": task["known_failure"],
        "raw_response": raw_response,
        "extraction_failed": False,
        "test_results": test_results,
        "score": score,
        "passed": passed,
        "total": total,
    }


def run_all():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_results = []

    for task in ALL_TASKS:
        result = run_task(task)
        all_results.append(result)

    output_path = os.path.join(RESULTS_DIR, f"run_{MODEL}_{timestamp}.json")
    with open(output_path, "w") as f:
        json.dump({
            "model": MODEL,
            "timestamp": timestamp,
            "total_tasks": len(all_results),
            "overall_score": sum(r.get("score", 0) for r in all_results) / len(all_results),
            "results": all_results,
        }, f, indent=2)

    print(f"\n\n{'='*55}")
    print(f"  FINAL SUMMARY -- {MODEL}")
    print(f"{'='*55}")

    categories = {}
    for r in all_results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    for cat, results in categories.items():
        print(f"\n  [{cat.upper().replace('_', ' ')}]")
        for r in results:
            pct = f"{r.get('score', 0)*100:.0f}%"
            print(f"    {r['task_id']} {r['task_name']}: {r.get('passed',0)}/{r.get('total',0)} ({pct})")

    overall = sum(r.get("score", 0) for r in all_results) / len(all_results)
    print(f"\n  Overall: {overall*100:.0f}% across {len(all_results)} tasks")
    print(f"  Results saved -> {output_path}")


if __name__ == "__main__":
    run_all()