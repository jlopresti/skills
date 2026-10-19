# Long Method

Use this page when one function makes a maintenance change require reasoning about several responsibilities or unrelated live variables. Treat length as a search cue. A line count establishes neither a finding nor a useful extraction.

## Diagnose the maintenance cost

Keep an audit or review analysis-only unless the user authorizes changes. Trace the function's callers and observable behavior before recommending a split. Record exact repository file and line evidence for the candidate regions. Name a concrete change, the unrelated code it forces a maintainer to understand, and the resulting risk. Separate a demonstrated cost from a hypothesis that needs history or a real change request.

Look for independent rules with different reasons to change. Track which local values each region reads, changes, and leaves for later regions. A variable with a long lifetime is a concern when unrelated work can accidentally change its meaning. A cohesive algorithm can legitimately carry shared state throughout its body.

In the original example below, fee policy and customer receipt wording occupy the same function. A request to change membership allowances concerns arithmetic. A request to translate a receipt concerns presentation. Show those actual requirements before reporting a finding in a repository. The compact example illustrates their boundary rather than a length violation.

## Choose a useful boundary

A useful extraction has a domain purpose and a small, explicit result. Here `_late_charge` owns the fee rule and returns the two values the receipt needs. Its arithmetic locals stop there. `_return_receipt` owns wording. `close_rental` retains validation and the order of mutations and emission.

Prefer this boundary when those rules change independently. Keep the code together when extraction merely creates step-numbered wrappers or requires many mutable locals to travel between helpers. Preserve exception timing, validation order, callback order, and the state visible to callbacks. An extraction that repairs an existing partial write changes behavior and needs separate authorization.

A concrete counterexample is a fixed-layout telemetry frame decoder. Its explicit offset checks, checksum accumulation, and field reads can belong in one longer function because all implement one binary format invariant. If a field-layout change remains local and the offsets are readable together, a collection of tiny readers can obscure that invariant. Retain the cohesive function unless a separate maintenance cost supports a split.

## Before

The data is a plain rental dictionary with `status`, `start_day`, `due_day`, `daily_fee_cents`, `member`, `id`, and `item`. Days and monetary amounts are integers. A member receives a 100-cent allowance against the overdue fee. `emit` receives the receipt after the same dictionary has been updated. Both blocks are independent Python examples with the public signature `close_rental(rental, returned_day, emit)`.

```python
def close_rental(rental, returned_day, emit):
	if rental["status"] != "out":
		raise ValueError("rental is not out")
	if returned_day < rental["start_day"]:
		raise ValueError("return precedes rental")
	overdue_days = max(0, returned_day - rental["due_day"])
	fee_cents = overdue_days * rental["daily_fee_cents"]
	if rental["member"]:
		fee_cents = max(0, fee_cents - 100)
	lines = [
		f"Return {rental['id']}",
		f"Item: {rental['item']}",
		f"Overdue days: {overdue_days}",
	]
	lines.append(f"Fee: {fee_cents // 100}.{fee_cents % 100:02d}")
	if rental["member"]:
		lines.append("Membership allowance applied")
	receipt = "\n".join(lines)
	rental["status"] = "returned"
	rental["returned_day"] = returned_day
	rental["fee_cents"] = fee_cents
	emit(receipt)
	return receipt
```

## After

```python
def _late_charge(rental, returned_day):
	overdue_days = max(0, returned_day - rental["due_day"])
	fee_cents = overdue_days * rental["daily_fee_cents"]
	if rental["member"]:
		fee_cents = max(0, fee_cents - 100)
	return overdue_days, fee_cents


def _return_receipt(rental, overdue_days, fee_cents):
	lines = [
		f"Return {rental['id']}",
		f"Item: {rental['item']}",
		f"Overdue days: {overdue_days}",
	]
	lines.append(f"Fee: {fee_cents // 100}.{fee_cents % 100:02d}")
	if rental["member"]:
		lines.append("Membership allowance applied")
	return "\n".join(lines)


def close_rental(rental, returned_day, emit):
	if rental["status"] != "out":
		raise ValueError("rental is not out")
	if returned_day < rental["start_day"]:
		raise ValueError("return precedes rental")
	overdue_days, fee_cents = _late_charge(rental, returned_day)
	receipt = _return_receipt(rental, overdue_days, fee_cents)
	rental["status"] = "returned"
	rental["returned_day"] = returned_day
	rental["fee_cents"] = fee_cents
	emit(receipt)
	return receipt
```

## Check observable behavior

Run both versions against independent copies of the same rental. Compare the exact returned receipt, final dictionary, emission count, and dictionary snapshot observed by `emit`. Cover early, due-day, and late returns. For members, cover an allowance that removes the fee and one that leaves a positive fee.

Compare exception types and messages for a closed rental, a return before the start day, and missing required keys. Both versions must leave the rental unchanged and emit nothing in these cases. If `emit` raises, both must propagate its exception after the dictionary updates. A second call must reject the already-returned rental without another emission. These checks establish the example's contract, not compatibility with arbitrary mapping subclasses or every surrounding application.

## Sources and scope

The [Long Method catalog page](https://refactoring.guru/smells/long-method) suggests extraction and identifies local-variable dependencies as an obstacle. [Extract Method](https://refactoring.guru/extract-method) describes passing required inputs and returning modified values still needed by the caller. Both pages were checked on 2026-10-19. The diagnostic criteria, contraindications, telemetry counterexample, rental examples, and checks above are original guidance. They supplement the catalog rather than reproduce its text or examples.
