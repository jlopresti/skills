# Strategy

## Choose independent algorithms for one task

The canonical [Strategy pattern](https://refactoring.guru/design-patterns/strategy) separates interchangeable algorithms from the context that uses them. The client chooses the algorithm. A callable can express the strategy role when one operation varies. An object is useful when an algorithm owns configuration, dependencies, or resources. These roles do not require an inheritance hierarchy.

Choose Strategy when actual changes show that algorithms evolve independently, or callers need to supply different implementations of one operation. Identify the affected callers and the change that motivates the separation. A shorter conditional alone is weak evidence.

Original counterexample. A shipping service has two stable formulas, one caller, and no independent dependencies. Keep its two branches together. A rate table may suffice if only constants vary. The miniature example below shows mechanics. It earns extraction only when real change pressure justifies separate algorithms.

## Keep selection and execution contracts explicit

The original example uses built-in positive integer grams, built-in service strings, and an ordinary event list. It returns integer cents. Both implementations accept the same public arguments. Each rate accepts grams, returns cents, and leaves caller data unchanged. Shared validation precedes selection. Unknown services raise `ValueError`, without an event. One successful quote appends one event after calculation. Existing events retain their order.

The public `quote_shipping` function owns service selection. `_quote_with` owns calculation and the shared success event. The core accepts a callable and never inspects its identity. Moving selection into every strategy would spread service names across algorithms. A registry centralizes selection but still changes when a service name is added.

Selection can itself be observable. Preserve the number and timing of comparisons or lookups unless the input contract makes them pure. In a batch, choosing once can remove comparisons that previously happened for every element. A string subclass can define effectful equality or raise on a later comparison. A dictionary also introduces hashing requirements. Keep the original comparison route when those behaviors are supported or uncertain. Separating algorithms does not require caching the selection.

In a real integration, establish the common currency, rounding rule, accepted inputs, failure semantics, cancellation, and permitted mutations before substituting algorithms. The same function signature does not establish substitutability. A provider that returns dollars, writes an invoice, or catches errors differently violates this example's contract.

## Before

```python
def quote_shipping(weight_grams: int, service: str, events: list[str]) -> int:
	if weight_grams <= 0:
		raise ValueError("weight must be positive")
	if service == "economy":
		cents = 400 + ((weight_grams + 499) // 500) * 90
	elif service == "express":
		cents = 800 + ((weight_grams + 249) // 250) * 130
	else:
		raise ValueError("unknown service")
	events.append(f"quote:{service}:{cents}")
	return cents
```

## After

```python
from collections.abc import Callable

Rate = Callable[[int], int]


def _economy(weight_grams: int) -> int:
	return 400 + ((weight_grams + 499) // 500) * 90


def _express(weight_grams: int) -> int:
	return 800 + ((weight_grams + 249) // 250) * 130


_RATES: dict[str, Rate] = {"economy": _economy, "express": _express}


def _quote_with(
	weight_grams: int, service: str, rate: Rate, events: list[str]
) -> int:
	cents = rate(weight_grams)
	events.append(f"quote:{service}:{cents}")
	return cents


def quote_shipping(weight_grams: int, service: str, events: list[str]) -> int:
	if weight_grams <= 0:
		raise ValueError("weight must be positive")
	rate = _RATES.get(service)
	if rate is None:
		raise ValueError("unknown service")
	return _quote_with(weight_grams, service, rate, events)
```

## Extract without changing behavior

1. Record each branch's result, exceptions, effects, and evaluation order. Include conflicting invalid inputs to expose validation precedence.
2. Extract one algorithm with explicit inputs. Keep shared effects in their existing order, outside the algorithm.
3. Compare observable outcomes before extracting the next algorithm. Preserve integer arithmetic and rounding thresholds.
4. Pass the selected implementation into the context. Remove the replaced algorithm branches after callers use the same route.

Keep stateless callables reusable. If an object owns a connection or mutable cache, assign its lifetime and cleanup explicitly. Sharing one mutable strategy between requests can introduce behavior that the branches never had.

## Distinguish selection from lifecycle

Choosing economy or express selects a calculation. It does not change which order operations are legal. In [State](https://refactoring.guru/design-patterns/state), a lifecycle transition changes later behavior and may constrain legal operations. An order moving from draft to dispatched needs explicit transition rules. Treating every lifecycle flag as a strategy hides those rules.

## Verify observable outcomes

Compare both public functions for weights 1, 249, 250, 251, 499, 500, and 501 with both services. Compare cents and the complete event list, starting with a pre-existing event. Repeat calls on one list to check accumulation order.

Check zero and negative weights, unknown service, and zero weight with unknown service. The last case must report `weight must be positive` first. Errors leave events unchanged. For the new core, inject a callable that records its invocation, then returns 777. Confirm one invocation precedes the success event. Inject a raising callable and confirm the exception propagates without a success event.

The canonical idea and State distinction are attributed above. Contracts, selection guidance, counterexample, extraction sequence, and Python examples are original engineering guidance. Sources checked on 2026-10-19. This page is sufficient for the example without network access.
