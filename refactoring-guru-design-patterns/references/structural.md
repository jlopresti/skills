# Structural pattern decisions

These original selection notes follow the seven structural entries in the [Refactoring Guru catalog](https://refactoring.guru/design-patterns/catalog). Select by intent rather than wrapper shape.

| Pattern and source | Concrete reason to consider it | Simpler option or reason to reject it |
| --- | --- | --- |
| [Adapter](https://refactoring.guru/design-patterns/adapter) | A useful dependency has an interface incompatible with the contract clients already need. Translate at that boundary. | Change an owned interface or use a conversion function when possible. Do not hide incompatible semantics, units, errors, or ownership behind matching method names. |
| [Bridge](https://refactoring.guru/design-patterns/bridge) | Two independently changing dimensions would otherwise multiply subclasses, such as presentation variants and platform implementations. | Use one implementation or one injected dependency when only one dimension varies. Bridge adds a second abstraction to maintain, so identify both independent changes. |
| [Composite](https://refactoring.guru/design-patterns/composite) | Clients perform a coherent operation on both individual items and nested groups in a genuine tree. | Use a recursive data type and a traversal function when the structure is data. Keep leaf and group operations distinct when a uniform contract would invent meaningless methods. |
| [Decorator](https://refactoring.guru/design-patterns/decorator) | Optional behaviors must compose around the same contract without a subclass for every combination. | Use a function wrapper or existing middleware support when sufficient. For one stable combination, direct code can be clearer. Specify wrapper order and preserve the component's contract. |
| [Facade](https://refactoring.guru/design-patterns/facade) | Callers repeat subsystem coordination or depend on more subsystem detail than their task requires. Expose a coherent task-level operation. | Extract a function or module first. A facade that mirrors every dependency method adds delegation without reducing caller knowledge. Keep unrelated tasks out of one central object. |
| [Flyweight](https://refactoring.guru/design-patterns/flyweight) | Measured memory pressure comes from many objects repeating immutable intrinsic data, while per-use context can remain external. | Use ordinary values or existing interning first. Reject the extra lookup and state separation when duplication is cheap. Shared data must stay immutable and its retention must remain bounded. |
| [Proxy](https://refactoring.guru/design-patterns/proxy) | A substitute must control access, initialization, or another service concern while preserving the service contract. | Use an explicit function or existing client support when sufficient. Hidden I/O, cache staleness, and altered failure timing can surprise callers. Preserve relevant lifecycle and error semantics. |

## Separate wrappers by intent

Adapter translates a client's contract. Decorator composes additional behavior around a component contract. Proxy controls access to a service through its contract. Facade offers a smaller task-level view of a subsystem.

One object may serve more than one intent, but a similar delegation structure alone does not justify several pattern names. Name the intent that explains the dependency boundary to the next maintainer.
