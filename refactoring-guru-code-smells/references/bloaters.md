# Bloaters

These cues locate candidates. A demonstrated finding also needs the evidence and maintenance consequence required by `SKILL.md`.

## Long Method

[Catalog entry](https://refactoring.guru/smells/long-method).

A function mixes steps with different purposes or keeps unrelated state alive across them. Trace a concrete change that requires understanding those other steps. A possible response is [Extract Method](https://refactoring.guru/extract-method) at a boundary with a meaningful name and few dependencies.

A cohesive algorithm, linear orchestration, or declarative table may remain readable in one function. Splitting it into fragments that share many locals can increase the reader's work. Judge responsibilities and state, without a line-count cutoff.

## Large Class

[Catalog entry](https://refactoring.guru/smells/large-class).

Distinct groups of fields and operations support different responsibilities. Show which clients or changes use each group and where the shared container creates interference. [Extract Class](https://refactoring.guru/extract-class) is a candidate when a cohesive responsibility has an independent boundary.

Many operations over one invariant can belong together. Generated bindings and declarative schemas can also be large without creating a useful extraction. A module in a functional design needs a module boundary when justified, not an imposed class hierarchy.

## Primitive Obsession

[Catalog entry](https://refactoring.guru/smells/primitive-obsession).

Raw strings, numbers, or positional data carry domain meaning that callers repeatedly validate or interpret. Locate the repeated rules or values that callers can confuse. [Replace Data Value with Object](https://refactoring.guru/replace-data-value-with-object) suggests a domain representation that owns the rules. A record, tagged union, or validated type may fit the language better.

Boundary serialization and simple scalar arithmetic legitimately use basic values. Introduce a domain representation when it protects a real invariant or removes repeated interpretation.

## Long Parameter List

[Catalog entry](https://refactoring.guru/smells/long-parameter-list).

Callers must coordinate related arguments, remember ordering, or supply values that select unrelated modes. Inspect actual calls for ambiguity and repeated construction. [Introduce Parameter Object](https://refactoring.guru/introduce-parameter-object) fits a cohesive concept with a name and rules.

Explicit dependencies can be clearer than a bag of options or a whole object that adds coupling. Named arguments and an independent mathematical operation may make the signature appropriate. Parameter count alone is insufficient.

## Data Clumps

[Catalog entry](https://refactoring.guru/smells/data-clumps).

The same related values travel together through several locations. Show their shared meaning and coordinated validation or change. [Introduce Parameter Object](https://refactoring.guru/introduce-parameter-object) is a candidate for that concept.

Repeated adjacent values do not necessarily share a lifecycle or invariant. Passing a whole entity can expose more data or dependencies than the callee needs. Prefer the smallest representation that preserves the actual relationship.
