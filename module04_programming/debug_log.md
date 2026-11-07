# Week 8 Debug Log
# Author: Minh Nguyen (AI-assisted debugging session)

This log covers the initial AI-assisted debugging run and my guided follow-up
review. AI executed the original commands and code edits. In the follow-up, I
gave my own diagnoses and proposed fixes, and confirmed that I explained the
code aloud and can explain both corrections. This follow-up occurred after the
initial implementation; it was not an original attempt completed without AI.

## Bug 1

Error type: `KeyError: 'amount'`.

File + line: `week8_buggy.py`, original line 12 in `get_total()`, called from
original line 21. The failing statement is `total += rec['amount']`.

What the error means: The lookup requests a dictionary key that does not exist.
The traceback points to `rec['amount']`, so that spelling needs to match the key
actually stored in the record.

What I told the duck (follow-up explanation, with AI clarification):

1. `def get_total(records):` defines my function and names its input `records`.
2. `total = 0` starts the running total at zero each time I call the function.
3. `for rec in records:` takes one dictionary from the list at a time.
4. `total += rec['amount']` reads the exact key `amount` and adds its value.
   If that key is missing, the lookup fails before the addition happens.
5. `return total` sends the accumulated value back after the loop finishes.
   The error prevents this line from running.

What I tried: In the initial AI-assisted run, the unchanged script was run and
the traceback was read from the bottom. The diagnosis was recorded before adding
`print(f'DEBUG: rec = {rec}')` before the lookup. The output showed
`DEBUG: rec = {'id': 1, 'name': 'Taylor', 'amout': 1200}`.

During the follow-up, my first guess was to rename `rec` to `record`. AI
explained that `rec` is just the loop variable's name, so renaming it consistently
would not fix the missing key. After comparing `amout` with `amount`, I identified
`amount` as the correct spelling for the dictionary key.

How I fixed it: In the initial implementation, AI renamed the first record's
`amout` key to `amount`, removed the temporary DEBUG print, and reran the script.
It printed
`Total: $5150.00 across 3 records`, so the accumulator finished and execution
advanced to the next error.

## Bug 2

Error type: `TypeError: '>' not supported between instances of 'int' and 'str'`.

File + line: `week8_buggy.py`, original line 16 in `is_over_limit()`, called from
original line 23. The failing statement is `return amount > '1000'`.

What the error means: Python cannot compare an integer and a string using `>`.
The traceback identifies the two incompatible types.

What I told the duck (follow-up explanation): The left side,
`amount`, is the integer 5150 returned by `get_total()`. The right side, `'1000'`,
is text because it is surrounded by quotes. My rule needs to compare numbers,
so the threshold should be the integer `1000`.

How I fixed it: In the initial implementation, AI removed the quotes around
`1000` while keeping the `>` operator. Both operands are now numeric, and exactly
1000 still does not exceed
the limit. Rerunning the script produced the expected two-line output.

During the follow-up, I explained, "amount is int, '1000' is text" and proposed,
"i would change '1000' to 1000" before AI explained the fix in that discussion.
For `is_over_limit(1000)`, I answered False. My initial reason referred to 1200;
AI clarified that exactly 1000 equals the limit, so strict `>` returns False,
whereas 1200 would return True.

Verified implementation detail: The executable statements are under
`if __name__ == "__main__":` so importing the functions does not print the
demonstration. Ruff formatted the finished script. The traceback line numbers
above refer to the original script, before formatting and the main guard.

## After Fixing Both Bugs

Final output from `.venv/bin/python week8_buggy.py`:

```text
Total: $5150.00 across 3 records
True
```

Did pytest pass? Yes. All 26 repository tests passed, including the five new
tests in `tests/test_week8.py`. The larger total includes tests from earlier labs.
Ruff formatting and lint checks also passed.

The five new tests check summation, amounts above and below the limit, the exact
1000 boundary, and the complete formatted summary.

Instruction inconsistency: The supplied script's header says "three bugs", but
the lab identifies two bugs and asks for an "After Fixing Both Bugs" section.
Both observed runtime errors were fixed; the supplied `format_summary()` already
produces the required text, so no third functional bug was invented.

## AI Literacy Reflection

Did I use AI? Yes. AI performed the initial implementation, testing, and
documentation, then guided my follow-up review with questions and explanations.

Exact prompt I used for the initial work, with the attached lab instructions:

> heres what for this lab, handle it, if theres soemthign wrong get back to me, if not keep going

Exact prompt I used to begin the guided follow-up:

> ok now act as me and you are going thru the bug, I ask you questions so you can help me do whatever the requirments are, then update the log

What AI explained: `total = 0` initializes the sum; it is not part of the loop
syntax. `rec` is an arbitrary loop variable name, while the string key `amount`
must match the dictionary exactly. AI confirmed my explanation of the integer
and string mismatch and clarified why equality at 1000 makes strict `>` False.

What I changed myself: During the follow-up, I revised my initial diagnosis about
`rec`, identified the correct dictionary key as `amount`, and proposed changing
`'1000'` to numeric `1000`. These were my answers during the review; AI made the
repository edits, removed the DEBUG print, and added the main guard and tests.
I did not manually edit the code during this follow-up.

Can I explain every fixed line? Yes. I confirmed this during the follow-up and
identified both fixes. The dictionary key must be `amount`, and numeric `1000`
makes the comparison valid while preserving the strict `>` rule.

Did I explain the code aloud? Yes. I confirmed that I completed the out-loud
walkthrough during the follow-up.

## What I learned

I learned that renaming a loop variable does not fix a misspelled dictionary key;
the key itself must match the lookup. Quotes make `'1000'` text, so the comparison
needs numeric `1000`. Testing exactly at the limit checks that `>` excludes
equality, unlike `>=`.
