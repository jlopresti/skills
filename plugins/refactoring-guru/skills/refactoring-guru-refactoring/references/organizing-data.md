# Organizing data

Names follow [Refactoring Guru's data family](https://refactoring.guru/refactoring/techniques/organizing-data). Selection checks are local guidance.

| Technique | Selection cue |
| --- | --- |
| [Self Encapsulate Field](https://refactoring.guru/self-encapsulate-field) | Internal access needs one policy. |
| [Replace Data Value with Object](https://refactoring.guru/replace-data-value-with-object) | A value carries domain rules. |
| [Change Value to Reference](https://refactoring.guru/change-value-to-reference) | Shared identity is required. |
| [Change Reference to Value](https://refactoring.guru/change-reference-to-value) | Structural equality suffices. |
| [Replace Array with Object](https://refactoring.guru/replace-array-with-object) | Positions represent named fields. |
| [Duplicate Observed Data](https://refactoring.guru/duplicate-observed-data) | Presentation requires synchronized state. |
| [Change Unidirectional Association to Bidirectional](https://refactoring.guru/change-unidirectional-association-to-bidirectional) | Both navigation directions are needed. |
| [Change Bidirectional Association to Unidirectional](https://refactoring.guru/change-bidirectional-association-to-unidirectional) | One direction is unnecessary. |
| [Encapsulate Field](https://refactoring.guru/encapsulate-field) | Writes require an invariant. |
| [Encapsulate Collection](https://refactoring.guru/encapsulate-collection) | Aliases bypass collection policy. |
| [Replace Magic Number with Symbolic Constant](https://refactoring.guru/replace-magic-number-with-symbolic-constant) | A domain constant lacks meaning. |
| [Replace Type Code with Class](https://refactoring.guru/replace-type-code-with-class) | A coded value has rules. |
| [Replace Type Code with Subclasses](https://refactoring.guru/replace-type-code-with-subclasses) | Stable variants own distinct behavior. |
| [Replace Type Code with State/Strategy](https://refactoring.guru/replace-type-code-with-state-strategy) | Runtime variants own distinct behavior. |
| [Replace Subclass with Fields](https://refactoring.guru/replace-subclass-with-fields) | Variants differ only by data. |

## Selection checks

Preserve identity, equality, mutability, wire formats, and aliasing. Synchronization creates an additional invariant. Prefer derived state when possible. Enums, records, and tagged unions may suffice for coded values.
