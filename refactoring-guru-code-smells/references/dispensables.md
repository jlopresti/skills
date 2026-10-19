# Dispensables

Treat removal as a candidate response after establishing what the element contributes and who depends on it.

## Comments

[Catalog entry](https://refactoring.guru/smells/comments).

Comments repeatedly decode names, expressions, or tangled steps that could state their own intent. Locate the obscured behavior before proposing a rename, [Extract Variable](https://refactoring.guru/extract-variable), or extraction.

Keep rationale, external constraints, algorithm explanations, public documentation, and license notices when they carry information the code cannot express. Comment presence is insufficient evidence. A stale factual comment can warrant a correction independently of structural refactoring.

## Duplicate Code

[Catalog entry](https://refactoring.guru/smells/duplicate-code).

Several locations implement the same rule and need synchronized edits. Compare semantics, dependencies, and failure behavior. [Extract Method](https://refactoring.guru/extract-method) can consolidate a stable shared decision.

Similar syntax can implement independent policies that will evolve separately. Generated files, vendor code, and intentionally independent test expectations have different owners. A shared helper that needs unrelated flags may be more expensive than the duplication.

## Data Class

[Catalog entry](https://refactoring.guru/smells/data-class).

Clients repeatedly enforce invariants or manipulate a data container through broad access. Cite those rules and their duplication before considering [Move Method](https://refactoring.guru/move-method) or a narrower operation.

DTOs, immutable records, schema objects, and functional programs can deliberately separate data and behavior. An empty method set is insufficient evidence. Assess ownership of invariants and dependency direction, without requiring methods on every record.

## Dead Code

[Catalog entry](https://refactoring.guru/smells/dead-code).

An element appears unreachable or lacks consumers. Establish the supported entrypoints and search exports, configuration, reflection, dependency injection, plugin registration, generated references, migrations, and external contracts. A static search or uncovered test run alone establishes only a suspect.

An extension hook or public library API can have no local calls and still be live. With deletion authorized, remove only what the evidence covers and verify relevant build and runtime entrypoints. Retain uncertainty when external use cannot be established.

## Lazy Class

[Catalog entry](https://refactoring.guru/smells/lazy-class).

A component adds a place to navigate and maintain while hiding little behavior or policy. Trace what callers gain before considering [Inline Class](https://refactoring.guru/inline-class).

A small adapter, semantic type, compatibility boundary, or access-control wrapper may justify its cost. Count the knowledge it hides, not its methods or lines.

## Speculative Generality

[Catalog entry](https://refactoring.guru/smells/speculative-generality).

Extension points, parameters, or hierarchies support variation with no demonstrated consumer or supported requirement. Show the cost of that unused flexibility. [Collapse Hierarchy](https://refactoring.guru/collapse-hierarchy) is one candidate when the hierarchy adds no meaningful distinction.

Framework consumers, published compatibility contracts, and test access can justify apparently unused flexibility. Apply the Dead Code entrypoint checks before removal. A single implementation alone does not invalidate a dependency boundary.
