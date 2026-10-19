# Creational pattern decisions

These original selection notes follow the five creational entries in the [Refactoring Guru catalog](https://refactoring.guru/design-patterns/catalog). They compare the creation problem with a smaller design.

| Pattern and source | Concrete reason to consider it | Simpler option or reason to reject it |
| --- | --- | --- |
| [Factory Method](https://refactoring.guru/design-patterns/factory-method) | An existing creator workflow needs subclasses to choose the concrete product it uses through a common contract. | Use a named factory function or an injected callable when creation merely needs centralization or configuration. New creator subclasses need a real extension requirement. |
| [Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory) | Several product kinds must vary together as a compatible family, and clients must remain independent of each family. | Assemble dependencies directly or pass a record of factories when that expresses compatibility. A single product kind does not justify a product-family abstraction. Adding product kinds affects every family. |
| [Builder](https://refactoring.guru/design-patterns/builder) | Construction has meaningful stages, many optional configurations, or reusable steps that produce different representations. | Prefer named parameters, a validated configuration value, or a construction function for straightforward initialization. A fluent API alone is not the problem. A director is optional. |
| [Prototype](https://refactoring.guru/design-patterns/prototype) | Clients need copies without knowing concrete types, or a configured instance is the right basis for new objects. | Use value copying or an explicit constructor when copying is simple. Specify deep versus shallow copy, identity, mutable sharing, and resource ownership before cloning graphs. External resources often need reconstruction. |
| [Singleton](https://refactoring.guru/design-patterns/singleton) | A stated invariant requires one instance within a defined scope, and global access is part of the required design. | Usually create one instance at the composition root and inject it. A shared dependency or module export does not prove uniqueness is required. Global mutable state hides dependencies and makes test isolation harder. |

## Distinguish the factory concepts

An ordinary factory function returns an object and can hide constructor details. The GoF Factory Method pattern lets creator subclasses override product creation within a creator's workflow. Call the former a factory function unless the latter extension mechanism exists. A static creation method alone does not establish Factory Method.

Abstract Factory selects a compatible family of product kinds. Builder controls construction steps. Name the actual source of variation before choosing between them. The [Refactoring Guru factory comparison](https://refactoring.guru/design-patterns/factory-comparison) separates these terms.

## Check a Singleton's scope and costs

Define whether the invariant applies to one application container, process, thread, or another scope. A process-local Singleton cannot enforce uniqueness across processes.

Account for dependency replacement in tests, reset and disposal ownership, initialization failure, and concurrent access. Safe initialization does not make mutable operations thread-safe. Prefer explicit lifetime management when the requirement is reuse rather than uniqueness.
