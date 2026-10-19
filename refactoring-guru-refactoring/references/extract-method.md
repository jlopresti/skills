# Extract Method

Move a coherent operation into a named function while preserving what callers can observe. The canonical technique comes from [Refactoring Guru](https://refactoring.guru/extract-method), checked on 2026-10-19. The decision checks and Python examples below are original engineering guidance.

## Establish a useful boundary

Extract when the new name explains a domain operation and hides decisions the caller does not need to follow. Find the inputs, outputs, and effects before moving code. A long body alone does not establish that boundary. Keep a cohesive sequence together when extraction would expose most of its locals as parameters.

Classify each value used by the fragment:

| Relationship to the fragment | Consequence for extraction |
| --- | --- |
| Created and consumed inside | Keep it local to the new function. |
| Created outside and read inside | Pass the current value, or keep an existing explicit dependency. |
| Reassigned inside and read afterward | Return the new value and assign it in the caller. |
| Referenced mutable object changed inside | Preserve object identity and mutation timing. Copying can change the contract. |
| One-shot input, resource, or callback | Preserve consumption, ownership, invocation count, and failure timing. |

Return several genuinely related results as a tuple or the language's small record when necessary. If many unrelated results must cross the boundary, reconsider the fragment. A closure can keep dependencies explicit to a local scope, but a helper that mutates hidden captured state can make the original problem harder to see.

## Before

The public function receives an iterable of line mappings, an opening balance in cents, and an output callback. A callback failure propagates after the iterable has been consumed. Missing mapping keys fail at their original read.

```python
def write_balance(lines, opening_cents, publish):
	balance_cents = opening_cents
	for line in lines:
		balance_cents += line["cents"] * line["count"]
	publish({"balance_cents": balance_cents})
	return balance_cents
```

## After

The calculation receives the opening value and returns the updated balance. The caller owns publication. Both blocks are standalone Python.

```python
def _accumulate_balance(lines, opening_cents):
	balance_cents = opening_cents
	for line in lines:
		balance_cents += line["cents"] * line["count"]
	return balance_cents


def write_balance(lines, opening_cents, publish):
	balance_cents = _accumulate_balance(lines, opening_cents)
	publish({"balance_cents": balance_cents})
	return balance_cents
```

## Move the fragment safely

1. Establish current outputs, mutations, errors, and externally visible effects for the affected paths.
2. Choose the fragment and account for its crossing values using the table. Keep the public signature stable unless its migration is authorized.
3. Move the fragment without also changing its conditions or algorithm. Replace it with a call and assign every result needed afterward.
4. Check the public operation before deleting duplicate code or changing surrounding control flow. Review dynamic callers if any public name moves.

In this example, omitting the caller's balance assignment loses the accumulated amount. Iterating again to reconstruct that amount fails for a generator and can repeat effects. Moving publication into the loop emits several partial results instead of one final result.

Keep evaluation at its original point. Replacing a captured value with a later query can observe changed state. Moving an `await`, a cleanup boundary, or a potentially failing read can change which effects happen before failure. Preserve asynchronous behavior and resource lifetime when the original operation has them.

## Check the public contract

For the example, opening balance 100 with lines of 30 cents times two and 5 cents times three returns 175. It publishes one mapping containing 175. An empty iterable returns and publishes the opening balance. Check a generator that records each yield, a missing key after one valid line, and a publication callback that raises. Confirm the same results, error type, consumption, and prior effects in both versions.

For code that collects existing objects, also check that returned elements remain the original objects and that caller-visible mutations occur at the same point. Assert these public properties rather than a helper's name or the number of functions.

## When to keep or reverse the change

An expression with one use and an already clear name may need no extraction. A parser whose local state expresses one protocol can be clearer as one function. If a helper only repeats a call without hiding a useful concept, inlining can remove unnecessary navigation. Choose the boundary that makes the caller's job easier to understand.
