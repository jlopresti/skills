# Composing methods

Canonical names follow [Refactoring Guru's method composition family](https://refactoring.guru/refactoring/techniques/composing-methods). Selection checks below are local engineering guidance.

| Technique | Selection cue |
| --- | --- |
| [Extract Method](https://refactoring.guru/extract-method) | A fragment has a coherent name. |
| [Inline Method](https://refactoring.guru/inline-method) | A wrapper hides no useful decision. |
| [Extract Variable](https://refactoring.guru/extract-variable) | An expression needs a name. |
| [Inline Temp](https://refactoring.guru/inline-temp) | A name obscures a trivial expression. |
| [Replace Temp with Query](https://refactoring.guru/replace-temp-with-query) | A reusable calculation is pure. |
| [Split Temporary Variable](https://refactoring.guru/split-temporary-variable) | One local represents different concepts. |
| [Remove Assignments to Parameters](https://refactoring.guru/remove-assignments-to-parameters) | Reassignment obscures the original input. |
| [Replace Method with Method Object](https://refactoring.guru/replace-method-with-method-object) | Entangled locals prevent smaller extractions. |
| [Substitute Algorithm](https://refactoring.guru/substitute-algorithm) | A simpler algorithm preserves the contract. |

## Selection checks

Keep evaluation count, effects, and captured state equivalent when moving expressions. A query must not silently replace a snapshot with repeated reads. Parameter reassignment differs from mutation of the argument's contents. Method objects add lifecycle and mutable state. Prefer a local extraction when it suffices.

For algorithm substitution, compare boundary values, ordering, precision, errors, and mutation. A performance benefit requires separate measurement.
