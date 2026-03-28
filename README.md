# LLM Failure Atlas

A curated benchmark of coding tasks designed to expose where frontier AI models fail in predictable, documentable ways.

Built to develop intuition for AI model failure modes — finding the gaps a model itself doesn't see.

**Live results: Claude Opus (claude-opus-4-6) scored 95% across 25 tasks. 5 documented failures.**

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

**Failure:** When a > b, Claude returned a descending list `[5, 4, 3, 2]` instead of `[]`. The word "between" is ambiguous — Claude assumed descending order was valid rather than treating it as an empty range.

```
Input: a=5, b=2
Expected: []
Got: [5, 4, 3, 2]
```

**Why it matters:** Claude silently resolved the ambiguity without flagging it.

---

### BC-03H — Last Page Number (Hardened)
**Prompt:** "Return the last page number when displaying n items with k items per page." (No hint for n=0)

**Failure:** For n=0, Claude returned 1 instead of 0 — reasoning "even with zero items, there's still page 1."

```
Input: n=0, k=3
Expected: 0
Got: 1
```

**Why it matters:** Specification gap filled with a plausible default rather than flagging undefined behavior.

---

### AR-03 — Find Middle Element
**Prompt:** "Write a function that returns the middle element of a list." (No spec for even-length lists)

**Failure:** For even-length lists, Claude consistently returns the upper middle (index n//2) rather than lower middle (index (n-1)//2). Both are valid — Claude picks one silently.

```
Input: [1, 2, 3, 4]  →  Expected: 2  |  Got: 3
Input: [10, 20]      →  Expected: 10 |  Got: 20
```

**Why it matters:** Silent assumption in production causes hard-to-debug bugs.

---

### SF-01 — Integer Square Root (Silent Failure)
**Prompt:** "Write a function that returns the integer square root of n."

**Failure:** Claude used `int(math.sqrt(n))` which silently returns wrong answers for very large integers due to floating point precision limits.

```
Input: n=9999999999999999948
Expected: 3162277660168379
Got: 3162277660
```

**Why it matters:** No exception, no warning, no signal. The correct implementation is `math.isqrt(n)`.

---

### CT-04 — Buried Exception (Context Window Trap)
**Prompt:** Long list of tax rates for different product categories, with luxury goods (25%) listed near the end among many 10% categories.

**Failure:** Claude correctly identified the surprising exceptions (food=0%, books=5%) but missed luxury goods (25%), defaulting it to the standard 10% rate.

```
Input: category='luxury', price=100
Expected: 25.0
Got: 10.0
```

**Why it matters:** Claude's attention isn't simply "first wins" or "last wins." It weights *surprising* exceptions more carefully but can miss high-percentage exceptions that blend into a list of similar values. Luxury at 25% looks plausible as a standard rate; food at 0% is unusual enough to stick.

---

## Full Results

### Category 1: Boundary Conditions (with hints)
| Task | Score |
|------|-------|
| BC-01 Fence Post Problem | 5/5 |
| BC-02 Inclusive Range | 5/5 |
| BC-03 Last Page Number | 5/5 |
| BC-04 Overlapping Substring Count | 5/5 |
| BC-05 Circular Buffer Index | 5/5 |

### Category 1H: Boundary Conditions (hardened)
| Task | Score | Failure |
|------|-------|---------|
| BC-01H Fence Post Problem | 4/4 | None |
| BC-02H Inclusive Range | 3/4 | Reversed range returns descending list |
| BC-03H Last Page Number | 4/5 | n=0 returns 1 instead of 0 |
| BC-04H Overlapping Substring Count | 4/4 | None |
| BC-05H Circular Buffer Index | 5/5 | None |

### Category 2: Ambiguous Requirements
| Task | Score | Failure |
|------|-------|---------|
| AR-01 Remove Duplicates | 5/5 | None |
| AR-02 Capitalize Words | 5/5 | None |
| AR-03 Find Middle Element | 3/5 | Even-length: upper vs lower middle chosen silently |
| AR-04 Truncate String | 5/5 | None |
| AR-05 Flatten List | 5/5 | None |

### Category 3: Silent Failure
| Task | Score | Failure |
|------|-------|---------|
| SF-01 Integer Square Root | 7/8 | Float precision silently wrong on large integers |
| SF-02 Sum of Digits | 7/7 | None |
| SF-03 Caesar Cipher | 7/7 | None |
| SF-04 Running Average | 6/6 | None |
| SF-05 Rotate List | 6/6 | None |

### Category 4: Context Window Traps
| Task | Score | Failure |
|------|-------|---------|
| CT-01 Hidden Constraint | 6/6 | None |
| CT-02 Contradicting Update | 6/6 | None |
| CT-03 Unit Mismatch | 7/7 | None (grader bug fixed) |
| CT-04 Buried Exception | 7/8 | Luxury goods (25%) missed, defaulted to 10% |
| CT-05 Redefined Variable | 7/7 | None |

---

## Key Insights

**Pattern 1: Specification gaps → plausible defaults**
When the prompt doesn't specify an edge case, Claude fills it with a reasonable assumption (BC-02H, BC-03H).

**Pattern 2: Ambiguity → silent choice**
Multiple valid interpretations exist, Claude picks one without flagging the alternatives (AR-03).

**Pattern 3: Float precision → silent wrong answer**
`int(math.sqrt(large_n))` produces wrong results with no error signal. Use `math.isqrt()` (SF-01).

**Pattern 4: Attention weights surprises more than high values**
In CT-04, Claude correctly caught food=0% and books=5% (unusual values) but missed luxury=25% (high but plausible-sounding). The model's attention isn't position-based — it's weighted by how surprising a value is relative to context.

**Benchmark design note:** CT-03 revealed a grader bug — the test case `meters=600 → True` was incorrect (0.6km is not long distance). Claude was right. Building reliable benchmarks is itself a hard problem.

---

## Upcoming
| # | Category |
|---|----------|
| 5 | Overconfidence — tasks where the model is confidently wrong |

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

## Project Structure

```
llm-failure-atlas/
├── tasks/
│   ├── boundary_conditions.py
│   ├── boundary_conditions_hardened.py
│   ├── ambiguous_requirements.py
│   ├── silent_failure.py
│   └── context_window_traps.py
├── graders/
│   ├── boundary_conditions.py
│   ├── category2.py
│   ├── silent_failure.py
│   └── context_window_traps.py
├── results/
├── runner.py
└── README.md
```

---

Built by [Anuroop Jajoba]