# LLM Failure Atlas

A curated benchmark of coding tasks designed to expose where frontier AI models fail in predictable, documentable ways.

Built to develop intuition for AI model failure modes — finding the gaps a model itself doesn't see.

**Live results: Claude Opus (claude-opus-4-6) scored 94% across 15 tasks. 3 documented failures.**

---

## What This Is

Most engineers use LLMs as tools. This project uses them as subjects.

Each task is a self-contained coding challenge with:
- A prompt (sometimes with hints, sometimes deliberately ambiguous)
- An automated grader with specific test cases
- A documented failure hypothesis
- Real observed model behavior

The goal isn't to find tasks the model can't solve — it's to find tasks where the model is confidently wrong, makes an undisclosed assumption, or picks one valid interpretation without acknowledging the ambiguity.

---

## Documented Failures (Claude Opus)

### BC-02H — Inclusive Range (Hardened)
**Prompt:** "Write a function that returns all integers between a and b."

**Failure:** When a > b (reversed range), Claude returned a descending list `[5, 4, 3, 2]` instead of an empty list `[]`. The word "between" is ambiguous — Claude assumed descending order was valid rather than treating it as an empty range.

```
Input: a=5, b=2
Expected: []
Got: [5, 4, 3, 2]
```

**Why it matters:** Claude silently resolved the ambiguity without flagging it. A correct response would either ask for clarification or document the assumption made.

---

### BC-03H — Last Page Number (Hardened)
**Prompt:** "Return the last page number when displaying n items with k items per page." (No hint for n=0 case)

**Failure:** For n=0 (zero items), Claude returned 1 instead of 0. It reasoned "even with zero items, there's still page 1" — a reasonable real-world interpretation, but wrong per the mathematical spec.

```
Input: n=0, k=3
Expected: 0
Got: 1
```

**Why it matters:** This is a specification gap failure. The model filled in missing requirements with a plausible default rather than treating it as an edge case to handle explicitly.

---

### AR-03 — Find Middle Element
**Prompt:** "Write a function that returns the middle element of a list." (No spec for even-length lists)

**Failure:** For even-length lists, Claude consistently returned the upper middle element (index n//2) rather than the lower middle (index (n-1)//2). Both are valid — Claude picked one without acknowledging the ambiguity.

```
Input: [1, 2, 3, 4]
Expected: 2  (lower middle)
Got: 3        (upper middle)

Input: [10, 20]
Expected: 10
Got: 20
```

**Why it matters:** The model's choice is defensible — but it never said "I'm assuming upper middle." In a production system, silent assumptions of this kind cause hard-to-debug bugs.

---

## Full Results

### Category 1: Boundary Conditions (with hints)
| Task | Name | Score |
|------|------|-------|
| BC-01 | Fence Post Problem | 5/5 |
| BC-02 | Inclusive Range | 5/5 |
| BC-03 | Last Page Number | 5/5 |
| BC-04 | Overlapping Substring Count | 5/5 |
| BC-05 | Circular Buffer Index | 5/5 |

**Finding:** Claude handles boundary conditions perfectly when edge cases are explicitly spelled out.

### Category 1H: Boundary Conditions (hardened — hints removed)
| Task | Name | Score | Failure |
|------|------|-------|---------|
| BC-01H | Fence Post Problem | 4/4 | None |
| BC-02H | Inclusive Range | 3/4 | Reversed range returns descending list |
| BC-03H | Last Page Number | 4/5 | n=0 returns 1 instead of 0 |
| BC-04H | Overlapping Substring Count | 4/4 | None |
| BC-05H | Circular Buffer Index | 5/5 | None |

**Finding:** Removing explicit edge case hints exposes assumption-making. Claude fills gaps with reasonable defaults rather than flagging them.

### Category 2: Ambiguous Requirements
| Task | Name | Score | Failure |
|------|------|-------|---------|
| AR-01 | Remove Duplicates | 5/5 | None |
| AR-02 | Capitalize Words | 5/5 | None |
| AR-03 | Find Middle Element | 3/5 | Even-length: upper vs lower middle chosen silently |
| AR-04 | Truncate String | 5/5 | None |
| AR-05 | Flatten List | 5/5 | None |

**Finding:** Claude resolves ambiguous requirements silently. It picks an interpretation and implements it without acknowledging alternatives exist.

---

## Key Insight

Claude Opus is robust on well-specified tasks. Failures appear at two points:

1. **Unspecified edge cases** — when the prompt doesn't mention a boundary condition, Claude fills it in with a plausible default rather than treating it as undefined behavior.

2. **Ambiguous requirements** — when multiple valid interpretations exist, Claude picks one silently without saying which assumption it made.

Both failure modes are invisible to a user who doesn't check edge cases — and they're the exact failures that matter most in production systems.

---

## Upcoming Categories

| # | Category | What it tests |
|---|----------|---------------|
| 3 | Silent Failure | Code that runs but produces wrong output |
| 4 | Context Window Traps | Critical info buried in long prompts |
| 5 | Overconfidence | Tasks where the model is confidently wrong |

---

## Setup

```bash
git clone https://github.com/anuroopjajoba3/llm-failure-atlas
cd llm-failure-atlas
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python runner.py
```

---

Built by [Anuroop Jajoba]