# Generalization

Canonical names follow [Refactoring Guru's generalization family](https://refactoring.guru/refactoring/techniques/dealing-with-generalization). Selection checks below are local engineering guidance.

| Technique | Selection cue |
| --- | --- |
| [Pull Up Field](https://refactoring.guru/pull-up-field) | Subtypes share one field meaning. |
| [Pull Up Method](https://refactoring.guru/pull-up-method) | Subtypes share one behavior contract. |
| [Pull Up Constructor Body](https://refactoring.guru/pull-up-constructor-body) | Initialization shares an invariant. |
| [Push Down Field](https://refactoring.guru/push-down-field) | A field belongs to fewer subtypes. |
| [Push Down Method](https://refactoring.guru/push-down-method) | Behavior belongs to fewer subtypes. |
| [Extract Subclass](https://refactoring.guru/extract-subclass) | A subset has specialized behavior. |
| [Extract Superclass](https://refactoring.guru/extract-superclass) | Existing types share substitutable behavior. |
| [Extract Interface](https://refactoring.guru/extract-interface) | Consumers need a smaller contract. |
| [Collapse Hierarchy](https://refactoring.guru/collapse-hierarchy) | A level adds no useful distinction. |
| [Form Template Method](https://refactoring.guru/form-template-method) | Algorithms share order, vary steps. |
| [Replace Inheritance with Delegation](https://refactoring.guru/replace-inheritance-with-delegation) | Reuse does not imply substitutability. |
| [Replace Delegation with Inheritance](https://refactoring.guru/replace-delegation-with-inheritance) | Substitutability justifies inherited behavior. |

## Selection checks

Verify subtype contracts, dispatch, construction order, and visibility. Similar text alone does not establish a shared abstraction. Composition and functions can express reuse without a hierarchy. Inheritance introduces coupling to future superclass changes.
