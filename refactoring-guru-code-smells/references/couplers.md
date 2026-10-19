# Couplers and library limits

Evaluate which component must know another component's decisions. Public calls and delegation are ordinary design tools. Their maintenance cost determines whether there is a finding.

## Feature Envy

[Catalog entry](https://refactoring.guru/smells/feature-envy).

An operation repeatedly interprets another component's data or rules. Trace the shared invariant and changes it causes in the caller. [Move Method](https://refactoring.guru/move-method) may put the operation near its owner.

Pure transformations over records, serializers, strategies, and visitors can intentionally separate data and behavior. Reading another value more often than local state is insufficient evidence. Preserve dependency direction and independent variation.

## Inappropriate Intimacy

[Catalog entry](https://refactoring.guru/smells/inappropriate-intimacy).

Components depend on each other's representation, private helpers, or coordinated mutation. Locate the internal assumption and a change that propagates through it. [Move Method](https://refactoring.guru/move-method) or a narrower boundary may restore an owner for the invariant.

Closely coordinated implementation parts inside one encapsulated module may be appropriate. Public immutable data is also an intentional contract. Establish which promised boundary the knowledge crosses and the resulting burden.

## Message Chains

[Catalog entry](https://refactoring.guru/smells/message-chains).

A caller navigates several objects to obtain a capability, and therefore knows their relationships. Trace which intermediate relationship changes would force caller edits. [Hide Delegate](https://refactoring.guru/hide-delegate) may expose the needed operation closer to the caller.

Fluent builders, stream pipelines, and stable schema paths can be deliberate APIs. Several dots alone are insufficient evidence. Check whether hiding the chain would create a pass-through layer with its own maintenance burden.

## Middle Man

[Catalog entry](https://refactoring.guru/smells/middle-man).

A component mostly forwards calls while adding no useful policy or boundary. Inspect what it hides and which clients use that boundary before considering [Remove Middle Man](https://refactoring.guru/remove-middle-man).

Proxies, decorators, facades, compatibility layers, authorization, and isolation can justify delegation. Removing them can expose dependency details or change behavior. Assess their actual role even when their methods look trivial.

## Incomplete Library Class

[Catalog entry](https://refactoring.guru/smells/incomplete-library-class).

A dependency lacks a needed operation, and callers repeat compensating code outside its control. Establish the missing capability against the dependency version and supported extension points. [Introduce Foreign Method](https://refactoring.guru/introduce-foreign-method) suggests a local operation around a few missing behaviors.

A single local operation can already be sufficient. A wrapper may cost more than the missing behavior, and a supported newer API may remove the need. Keep dependency files under their package manager's ownership. Account for upgrade behavior when proposing an extension.
