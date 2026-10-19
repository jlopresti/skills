# Moving features

Canonical names follow [Refactoring Guru's responsibility family](https://refactoring.guru/refactoring/techniques/moving-features-between-objects). Selection checks below are local engineering guidance.

| Technique | Selection cue |
| --- | --- |
| [Move Method](https://refactoring.guru/move-method) | Another owner holds its decisions. |
| [Move Field](https://refactoring.guru/move-field) | Another owner maintains its invariant. |
| [Extract Class](https://refactoring.guru/extract-class) | Distinct responsibilities have distinct dependencies. |
| [Inline Class](https://refactoring.guru/inline-class) | A boundary contributes no responsibility. |
| [Hide Delegate](https://refactoring.guru/hide-delegate) | Callers depend on internal navigation. |
| [Remove Middle Man](https://refactoring.guru/remove-middle-man) | Forwarding adds maintenance without isolation. |
| [Introduce Foreign Method](https://refactoring.guru/introduce-foreign-method) | One missing library operation needs adaptation. |
| [Introduce Local Extension](https://refactoring.guru/introduce-local-extension) | Several missing library operations need one boundary. |

## Selection checks

Choose ownership by invariant and change pressure, not the number of reads. Keep transaction, synchronization, and lifecycle boundaries intact.

Hide Delegate and Remove Middle Man are alternatives. Preserve a facade that owns policy, security, or compatibility. Remove forwarding only when that responsibility is absent.

Prefer language-supported extension functions or a wrapper around external types. Check serialization and runtime entrypoints before moving fields or deleting old methods.
