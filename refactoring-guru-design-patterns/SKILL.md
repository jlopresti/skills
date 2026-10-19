---
name: refactoring-guru-design-patterns
description: Explain, compare, or select Refactoring Guru design patterns, and implement them when the user requests code changes. Use when a request names a design pattern or asks which pattern fits concrete code, rather than for a general code-smell audit.
---

# Choose design patterns by the problem they solve

Use a pattern to address concrete change pressure. A direct function, a data structure, or no pattern can be the best result.

## Match the requested work

- For an explanation, explain the pattern's intent, its moving parts, and when its costs outweigh its benefits. Use an original example in the user's language or programming language. An explanation does not authorize repository edits.
- For a comparison or recommendation, inspect the relevant code and callers when available. Separate observed facts from assumptions when only a description is available.
- For requested implementation, follow the repository's conventions and the user's authorized scope. A request to fix or implement authorizes the necessary code changes. Preserve observable behavior when the request is a refactoring.

## Establish the decision

Before introducing an abstraction, identify the concrete force it addresses. Cite a symbol, repeated change, dependency problem, lifetime invariant, or explicit requirement. Hypothetical future extensions alone do not justify a pattern.

Compare the candidate with the simplest viable design and the nearest competing pattern. Explain which edits or invariants become easier to manage and what indirection, state, or lifecycle costs the pattern adds. If the simpler design meets the requirement, recommend it and state why.

Use native language and framework features where they express the same intent. Functions, closures, generators, tagged unions, immutable values, and existing dependency injection can avoid new classes. Follow an established class hierarchy only when the problem earns it. Similar class diagrams do not make two patterns interchangeable.

## Load the relevant selection notes

Read only the family needed for the current decision. For a comparison across families, read the relevant families.

- For object creation, construction steps, copying, or single-instance lifetime, read [creational patterns](references/creational.md). This includes the distinction between Factory Method and an ordinary factory function.
- For incompatible interfaces, independent dimensions, trees, wrappers, subsystem access, or shared object data, read [structural patterns](references/structural.md).
- For requests, traversal, collaboration, notifications, state transitions, algorithm variation, or operations over object types, read [behavioral patterns](references/behavioral.md). This includes State versus Strategy.

## Apply and verify the decision

For code changes, map the chosen roles to existing symbols before adding new ones. Keep dependencies, ownership, and initialization explicit. Preserve callers, error behavior, side effects, and ordering unless the requested behavior changes them.

Run the relevant checks and exercise the behavior affected by the change. Verification must cover the force that motivated the pattern, such as a new algorithm variant, a legal state transition, wrapper order, or substitutable product family. Report checks that could not run and the resulting uncertainty.

Scale the reply to the request. A recommendation names the observed force, the chosen design or no pattern, the simpler alternative, and the main cost. An implementation report also names the changed behavior and verification evidence. Use canonical pattern names for lookup and explain them in the user's language.

## Sources

This independent guide uses the public [Refactoring Guru design-pattern catalog](https://refactoring.guru/design-patterns/catalog). The references contain original selection notes, with a source link for each of the catalog's 22 patterns. Simpler alternatives are engineering judgments. Read the linked source when deeper explanation or exact attribution is needed. Create original examples instead of copying the site's prose, code, or diagrams.
