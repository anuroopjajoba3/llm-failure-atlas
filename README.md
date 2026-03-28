# LLM Failure Atlas

A curated benchmark of coding tasks designed to expose where frontier AI models fail in predictable, documentable ways.

## What This Is

Most engineers use LLMs as tools. This project uses them as subjects — finding the exact prompts and edge cases where Claude, GPT-4, and Gemini break down, and why.

Each task is:
- A self-contained coding challenge
- Designed with a known failure hypothesis
- Equipped with an automated grader
- Documented with observed model behavior

## Categories

| # | Category | What it tests |
|---|----------|---------------|
| 1 | **Boundary Conditions** | Off-by-one errors, edge cases, zero inputs |
| 2 | **Ambiguous Requirements** | Prompts with two valid interpretations |
| 3 | **Silent Failure** | Code that runs but produces wrong output |
| 4 | **Context Window Traps** | Critical info buried in long prompts |
| 5 | **Overconfidence** | Tasks where the model is confidently wrong |

## Results So Far (Claude claude-opus-4-6)

| Task | Name | Score | Known Failure |
|------|------|-------|---------------|
| BC-01 | Fence Post Problem | TBD | Returns n instead of n+1, fails on n=0 |
| BC-02 | Inclusive Range | TBD | Uses range(a,b), fails on a==b and a>b |
| BC-03 | Last Page Number | TBD | Misses ceiling division when n%k==0 |
| BC-04 | Overlapping Substring | TBD | Uses str.count() which skips overlaps |
| BC-05 | Circular Buffer Index | TBD | Fails on k=0, single element, full loop |

## Setup

```bash
git clone https://github.com/anuroopjajoba3/llm-failure-atlas
cd llm-failure-atlas
pip install anthropic
export ANTHROPIC_API_KEY=your_key
python runner.py
```

## Project Structure

```
llm_failure_atlas/
├── tasks/
│   └── boundary_conditions.py   # Task prompts + failure hypotheses
├── graders/
│   └── boundary_conditions.py   # Automated test cases per task
├── results/                      # JSON output from each run
├── runner.py                     # Main runner — calls API, grades, saves
└── README.md
```

## Why I Built This

I'm building this to develop intuition for how frontier models fail — not just where they succeed. The goal is to find gaps the model itself doesn't see, document the failure patterns, and eventually use this benchmark to compare models systematically.

Built by Anuroop Jajoba | [github.com/anuroopjajoba3](https://github.com/anuroopjajoba3)