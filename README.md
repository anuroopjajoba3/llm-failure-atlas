# LLM Failure Atlas

A curated benchmark of coding tasks designed to expose where frontier AI models fail in predictable, documentable ways.

**Final results: Claude Opus (claude-opus-4-6) — 95% across 30 tasks. 7 documented failures. 5 distinct failure patterns.**

---

## What This Is

Most engineers use LLMs as tools. This project uses them as subjects.

Each task is a self-contained coding challenge with a prompt, an automated grader, a failure hypothesis, and real observed model behavior. The goal isn't to find tasks the model can't solve — it's to find tasks where the model is confidently wrong, makes an undisclosed assumption, or picks one interpretation without acknowledging the ambiguity.

This is the kind of work [Mechanize](https://mechanize.work) describes as their core job: finding where frontier coding models fail in interesting ways.

---

## The 7 Failures

### 1. BC-02H — Reversed Range (Specification Gap)
**Prompt:** "Return all integers between a and b." (No spec for reversed range)

```
Input: a=5, b=2
Expected: []
Got: [5, 4, 3, 2]
```
Claude assumed "between" allowed descending order rather than treating it as an empty range.

---

### 2. BC-03H — Zero Items Edge Case (Specification Gap)
**Prompt:** "Return the last page number when displaying n items with k items per page." (No hint for n=0)

```
Input: n=0, k=3
Expected: 0
Got: 1
```
Claude reasoned "even with zero items, there's still page 1" — a plausible default that violates the mathematical spec.

---

### 3. AR-03 — Middle Element of Even List (Ambiguous Requirements)
**Prompt:** "Return the middle element of a list." (No spec for even-length lists)

```
Input: [1, 2, 3, 4]  →  Expected: 2 (lower middle)  |  Got: 3 (upper middle)
Input: [10, 20]      →  Expected: 10                 |  Got: 20
```
Both interpretations are valid. Claude picks upper middle every time without flagging the ambiguity.

---

### 4. SF-01 — Large Integer Square Root (Silent Failure)
**Prompt:** "Return the integer square root of n."

```
Input: n=9999999999999999948
Expected: 3162277660168379
Got: 3162277660
```
Claude used `int(math.sqrt(n))` — correct for small numbers, silently wrong for large integers due to float64 precision limits. No error raised. The correct implementation is `math.isqrt(n)`.

---

### 5. CT-04 — Buried Tax Exceptions (Context Window Trap)
**Prompt:** Long list of tax rates with food (0%) and luxury (25%) buried among many 10% categories.

```
Input: category='food',    price=100  →  Expected: 0.0   |  Got: 10.0
Input: category='luxury',  price=100  →  Expected: 25.0  |  Got: 10.0
```
Claude correctly handles the prominent exceptions (electronics=15%, books=5%) but misses exceptions buried in longer lists. Interestingly, which exceptions get missed varies between runs — the model's attention on buried items isn't deterministic.

---

### 6. OC-04 — None Value in Dictionary (Overconfidence)
**Prompt:** "Safely get a value from a dictionary, returning 0 if the key doesn't exist."

```
Input: d={'a': None}, key='a'
Expected: 0
Got: None
```
Claude used `d.get(key, 0)` — the obvious solution. But `dict.get()` only returns the default for *missing* keys, not for keys that exist with `None` as their value. No error, just a silently wrong return.

---

### 7. OC-05 — Punctuation in Word Count (Overconfidence)
**Prompt:** "Return the number of unique words in a string."

```
Input: 'hello, hello.'
Expected: 1
Got: 2
```
Claude split on spaces — `'hello,'` and `'hello.'` are counted as two distinct words. The naive `text.split()` approach is confidently wrong on punctuation without any signal that something went wrong.

---

## Full Results

| Category | Task | Score |
|----------|------|-------|
| **Boundary Conditions** | BC-01 Fence Post Problem | 5/5 |
| | BC-02 Inclusive Range | 5/5 |
| | BC-03 Last Page Number | 5/5 |
| | BC-04 Overlapping Substring Count | 5/5 |
| | BC-05 Circular Buffer Index | 5/5 |
| **Boundary Conditions (Hardened)** | BC-01H Fence Post Problem | 4/4 |
| | BC-02H Inclusive Range | **3/4** ⚠️ |
| | BC-03H Last Page Number | **4/5** ⚠️ |
| | BC-04H Overlapping Substring Count | 4/4 |
| | BC-05H Circular Buffer Index | 5/5 |
| **Ambiguous Requirements** | AR-01 Remove Duplicates | 5/5 |
| | AR-02 Capitalize Words | 5/5 |
| | AR-03 Find Middle Element | **3/5** ⚠️ |
| | AR-04 Truncate String | 5/5 |
| | AR-05 Flatten List | 5/5 |
| **Silent Failure** | SF-01 Integer Square Root | **7/8** ⚠️ |
| | SF-02 Sum of Digits | 7/7 |
| | SF-03 Caesar Cipher | 7/7 |
| | SF-04 Running Average | 6/6 |
| | SF-05 Rotate List | 6/6 |
| **Context Window Traps** | CT-01 Hidden Constraint | 6/6 |
| | CT-02 Contradicting Update | 6/6 |
| | CT-03 Unit Mismatch | 7/7 |
| | CT-04 Buried Exception | **6/8** ⚠️ |
| | CT-05 Redefined Variable | 7/7 |
| **Overconfidence** | OC-01 Floating Point Equality | 6/6 |
| | OC-02 Mutable Default Argument | 4/4 |
| | OC-03 Most Frequent Element | 6/6 |
| | OC-04 Safe Dictionary Access | **5/6** ⚠️ |
| | OC-05 Count Unique Words | **6/7** ⚠️ |

**Overall: 95% across 30 tasks**

---

## Key Insights

**1. Specification gaps → plausible defaults, not flags**
When the prompt doesn't specify an edge case, Claude fills it with a reasonable assumption rather than flagging undefined behavior. BC-02H and BC-03H both show this — Claude never says "this case isn't specified."

**2. Ambiguity → silent choice**
When multiple valid interpretations exist, Claude picks one and implements it confidently. AR-03 (middle element of even list) fails every run — Claude always picks upper middle without acknowledging lower middle exists.

**3. Float precision → silent wrong answers**
`int(math.sqrt(large_n))` produces wrong results with no error signal. This is the most dangerous failure type in this benchmark — the function looks correct, runs without errors, and fails only at the edges of float64 representation.

**4. Attention weights surprises, not position**
CT-04 shows Claude's attention isn't simply "first wins" or "last wins." It correctly handles surprising exceptions (books=5%) but misses values that blend into surrounding context (food=0% sometimes, luxury=25% sometimes). Which exceptions get missed varies between runs.

**5. Overconfident standard library usage**
`d.get(key, 0)` and `text.split()` are the right tools for the obvious interpretation of a problem, but wrong for edge cases the prompt didn't explicitly rule out. Claude implements the obvious solution without considering None values or punctuation.

**What Claude Opus gets right that we expected it to miss:**
- Alphabet wrapping in Caesar cipher (xyz+3 → abc, not {|})
- Overlapping substring counting (doesn't use str.count())
- Float division in running averages (uses / not //)
- Right-direction list rotation
- Mutable default argument trap (correctly used None guard)
- Hidden constraints buried in long prompts
- Contradicting requirement updates

---

## Benchmark Design Note

Building reliable benchmarks is itself a hard problem. CT-03 contained a grader bug — the test case `meters=600 → True` was incorrect (0.6km is not long distance). Claude was right. The grader was wrong. This is a meta-lesson: the benchmark designer makes the same class of mistakes as the model.

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
│   ├── context_window_traps.py
│   └── overconfidence.py
├── graders/
│   ├── boundary_conditions.py
│   ├── category2.py
│   ├── silent_failure.py
│   ├── context_window_traps.py
│   └── overconfidence.py
├── results/
├── runner.py
└── README.md
```

---

Built by [Anuroop Jajoba]