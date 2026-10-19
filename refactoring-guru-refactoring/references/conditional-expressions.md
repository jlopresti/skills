# Conditional expressions

Names follow [Refactoring Guru's conditional family](https://refactoring.guru/refactoring/techniques/simplifying-conditional-expressions). Selection checks are local guidance.

| Technique | Selection cue |
| --- | --- |
| [Decompose Conditional](https://refactoring.guru/decompose-conditional) | Conditions mix domain concepts. |
| [Consolidate Conditional Expression](https://refactoring.guru/consolidate-conditional-expression) | Conditions share an outcome. |
| [Consolidate Duplicate Conditional Fragments](https://refactoring.guru/consolidate-duplicate-conditional-fragments) | Branches share an operation. |
| [Remove Control Flag](https://refactoring.guru/remove-control-flag) | Direct control flow expresses intent. |
| [Replace Nested Conditional with Guard Clauses](https://refactoring.guru/replace-nested-conditional-with-guard-clauses) | Exceptional paths obscure normal flow. |
| [Replace Conditional with Polymorphism](https://refactoring.guru/replace-conditional-with-polymorphism) | Repeated dispatch has independent variants. |
| [Introduce Null Object](https://refactoring.guru/introduce-null-object) | Absence has an agreed neutral behavior. |
| [Introduce Assertion](https://refactoring.guru/introduce-assertion) | An internal invariant is already guaranteed. |

## Selection checks

Preserve short-circuit order, error precedence, and resource cleanup. Moving a shared fragment before a branch can move its side effects.

A closed match or small lookup table can remain simpler than polymorphism. A Null Object must not convert missing required data into success.

Assertions document internal invariants. Runtime input validation must remain active in production. Adding a rejection for previously accepted input is a behavior change.
