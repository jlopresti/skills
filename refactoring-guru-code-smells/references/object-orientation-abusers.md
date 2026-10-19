# Object-orientation abusers

Use this family where the design has the relevant relationships. The catalog's object-oriented framing does not require converting functional code to classes.

## Alternative Classes with Different Interfaces

[Catalog entry](https://refactoring.guru/smells/alternative-classes-with-different-interfaces).

Components provide the same capability through incompatible names or calling conventions. Locate duplicated client adaptation and verify that the semantics match before suggesting [Rename Method](https://refactoring.guru/rename-method) or a shared contract.

Similar names or output shapes can hide different guarantees, error behavior, or ownership. Separate third-party APIs may justify a local adapter. A common interface earns its place through real interchangeable use.

## Refused Bequest

[Catalog entry](https://refactoring.guru/smells/refused-bequest).

A subtype disables inherited operations, rejects valid parent inputs, or exposes inherited state that makes no sense for it. Check the documented parent contract and polymorphic callers. [Replace Inheritance with Delegation](https://refactoring.guru/replace-inheritance-with-delegation) can preserve reuse without claiming substitutability.

Unused inherited methods alone do not prove a broken relationship. An explicitly optional operation in a framework contract may be valid. If a subtype violates an actual contract, report that behavioral defect separately from the smell.

## Switch Statements

[Catalog entry](https://refactoring.guru/smells/switch-statements).

Several branches on the same type or mode encode the same evolving decision across locations. Demonstrate which places a new variant must change and how their behavior can diverge. [Extract Method](https://refactoring.guru/extract-method) can first isolate the decision. A dispatch table or polymorphism may help after the change axis is clear.

A localized factory selection, simple branch, parser, reducer, or exhaustive match over a closed union can be the appropriate representation. A switch token establishes no finding. Compare the cost of the alternative with the edits it would remove.

## Temporary Field

[Catalog entry](https://refactoring.guru/smells/temporary-field).

Object fields exist only for one operation and leave the object partially meaningful at other times. Trace writers, readers, reset behavior, and permitted call order. A local value or [Extract Class](https://refactoring.guru/extract-class) for the operation can reduce the state readers must track.

Optional domain attributes, intentional caches, and explicitly modeled lifecycle states can be valid. Identify the unexplained lifecycle burden. Do not replace meaningful absence with a null object that changes behavior.
