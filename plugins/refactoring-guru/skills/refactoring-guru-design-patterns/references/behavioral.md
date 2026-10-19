# Behavioral pattern decisions

These original selection notes follow the ten behavioral entries in the [Refactoring Guru catalog](https://refactoring.guru/design-patterns/catalog). Identify who owns the decision, execution, and state.

| Pattern and source | Concrete reason to consider it | Simpler option or reason to reject it |
| --- | --- | --- |
| [Chain of Responsibility](https://refactoring.guru/design-patterns/chain-of-responsibility) | A configurable sequence of potential handlers decides whether to handle or forward a request. | Use a loop over functions or direct branching for a fixed sequence. Define ordering, short-circuit behavior, and the unhandled outcome. This differs from an unconditional transformation pipeline. |
| [Command](https://refactoring.guru/design-patterns/command) | An action needs its own identity and captured arguments for deferred execution, history, queuing, or undo. | Use a closure for a local deferred action. A stored command record helps persistence only with explicit versioning, retries, and execution semantics. Undo requires a real inverse or captured prior state. |
| [Iterator](https://refactoring.guru/design-patterns/iterator) | Traversal needs independent progress or interchangeable traversal rules without exposing a collection's representation. | Use the language's iterable protocol or a generator. Direct iteration suits a simple collection. Define mutation, exhaustion, resource cleanup, and cancellation semantics when relevant. |
| [Mediator](https://refactoring.guru/design-patterns/mediator) | Peer-to-peer coordination couples components that must otherwise change or be reused independently. | Put coordination in an existing controller or application function. Reject a central object that merely relocates all business logic. Give the mediator a bounded coordination responsibility. |
| [Memento](https://refactoring.guru/design-patterns/memento) | A component must restore previous private state without exposing its representation to the history owner. | Use immutable state snapshots when sufficient. Define snapshot size, retention, and restore compatibility. Restoring memory does not undo an email, payment, or another external effect. |
| [Observer](https://refactoring.guru/design-patterns/observer) | An event publisher must notify a changing set of subscribers without depending on each subscriber's concrete type. | Use a callback for one recipient or an existing event facility. Define subscription lifetime, delivery order, reentrancy, and failure policy. Local notification alone supplies no durable-delivery guarantee. |
| [State](https://refactoring.guru/design-patterns/state) | An object's allowed operations and transitions depend on its lifecycle, and state-specific behavior has become difficult to maintain together. | Prefer a tagged union, reducer, or transition table for a small explicit machine. A few stable branches rarely earn state classes. Keep legal transitions and their effects visible. |
| [Strategy](https://refactoring.guru/design-patterns/strategy) | A caller or configuration must select among interchangeable ways to perform the same task. | Pass a function or callable when one operation varies. Keep direct branches for a few stable variants. The caller must understand selection criteria, and all strategies must satisfy the same behavioral contract. |
| [Template Method](https://refactoring.guru/design-patterns/template-method) | An established inheritance API fixes an algorithm's sequence while subclasses customize specific steps. | Use a function with callbacks or composed operations when inheritance is unnecessary. Avoid overridable hooks with undocumented ordering assumptions. Use Strategy when clients need to swap behavior independently of the subclass. |
| [Visitor](https://refactoring.guru/design-patterns/visitor) | A stable set of element types needs frequent new operations, and changing each element for every operation is costly. | Prefer pattern matching over a closed data type or an ordinary traversal when clearer. Adding element types changes visitors. Visitor is a poor fit when element kinds change more often than operations. |

## Distinguish State from Strategy

State represents where an object is in a lifecycle. A transition can change which operations are legal and what later events mean. Strategy represents the chosen way to perform a task. Strategies can remain independent of one another.

Ask whether the selection changes because of a domain transition or because the caller chooses an algorithm. An order moving from draft to submitted suggests State. Choosing a delivery-cost algorithm suggests Strategy. Neither case requires a class hierarchy.

A state machine is broader than the object-oriented State pattern. A reducer or table can express the same lifecycle more clearly. If transitions themselves vary independently from algorithms, model those concerns separately instead of treating every mode flag as a Strategy.

## Distinguish Command from Strategy

Command represents a particular requested action and its arguments. Strategy represents a replaceable algorithm. A command can call a strategy, but interchangeability alone does not give an action undo, history, or persistence semantics.
