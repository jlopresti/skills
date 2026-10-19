# Change preventers

This family concerns the shape of changes. Commit history can corroborate it. When history is absent, trace a concrete current requirement and label predictions about future edits as hypotheses.

## Divergent Change

[Catalog entry](https://refactoring.guru/smells/divergent-change).

One component must change for independent business or technical reasons. Identify the distinct reasons and the fields or operations each reason touches. [Extract Class](https://refactoring.guru/extract-class), or a module extraction, can separate responsibilities when the new boundary reduces shared knowledge.

A component participating in several commits is insufficient evidence. A cohesive domain rule can legitimately affect several of its operations. Do not split every operation into its own owner and create scattered edits instead.

## Shotgun Surgery

[Catalog entry](https://refactoring.guru/smells/shotgun-surgery).

One rule is represented in scattered places, so a single change requires coordinated edits. Cite those representations and explain why they must agree. [Move Method](https://refactoring.guru/move-method) is one candidate for putting the decision with its owner. Functions and modules can provide the same consolidation.

A cross-cutting feature can legitimately change presentation, persistence, and tests for different reasons. Many touched files alone do not show scattered ownership. Establish that the same decision is repeated, and account for dependency costs before centralizing it.

## Parallel Inheritance Hierarchies

[Catalog entry](https://refactoring.guru/smells/parallel-inheritance-hierarchies).

Adding a subtype requires matching subtypes in another hierarchy. Trace the pairing, registration, and selection rules to show the synchronization burden. Composition and [Move Method](https://refactoring.guru/move-method) may remove the duplicated variation axis.

Parallel structures can express intentionally separate capabilities, and a Visitor can deliberately trade one kind of extension for another. A shared naming pattern alone proves nothing. Retain the design if combining the hierarchies would entangle responsibilities or lose supported combinations.

## Tell the first two apart

Divergent Change concentrates independent reasons to change in one component. Shotgun Surgery scatters one reason to change across components. They can coexist. Demonstrate each relationship separately and check that a proposed split does not merely exchange one for the other.
