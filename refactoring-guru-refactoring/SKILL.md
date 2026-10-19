---
name: refactoring-guru-refactoring
description: Plan or perform behavior-preserving code refactoring using Refactoring Guru techniques. Use for a requested extraction, move, rename, simplification, or structural cleanup. Use diagnosis alone for a code smell audit and treat bug fixes or changed requirements as separate behavior changes.
---

# Refactor while preserving behavior

Use the techniques as candidate transformations. Choose the smallest change that resolves the demonstrated maintenance problem. Follow the project's language idioms, including functions, records, modules, and algebraic data types where appropriate.

## Establish the contract

1. Identify the requested scope and whether the user wants a plan or implementation. A request for advice remains a plan.
2. Read the affected code, its callers, and the repository's instructions. Use the repository's configured code index first when required.
3. State the maintenance problem and the behavior that must remain observable. Include outputs, errors, side effects, evaluation order, mutation, identity, and public contracts when relevant.
4. Find the existing verification that observes those behaviors. Run a relevant baseline before editing. For untested, consequential behavior, add a focused characterization check or record the verification limit before making a narrow change.

Keep bug fixes and feature changes separate. Existing surprising behavior still belongs to the baseline unless the user authorized changing it.

## Select a transformation

Read only the reference matching the affected structure. Each contains a compact technique index and checks that affect selection.

- For method bodies, expressions, and local variables, read [composing methods](references/composing-methods.md).
- For responsibility and delegation boundaries, read [moving features](references/moving-features.md).
- For values, identity, collections, and type codes, read [organizing data](references/organizing-data.md).
- For branches and absence handling, read [conditional expressions](references/conditional-expressions.md).
- For signatures, visibility, construction, and error contracts, read [method calls](references/method-calls.md).
- For inheritance and shared interfaces, read [generalization](references/generalization.md).

Name the selected technique, why it fits this code, and the simpler alternative. An existing structure can remain when the alternative adds more coordination than it removes. Resolve a meaningful semantic uncertainty before choosing the transformation.

The source names often describe object-oriented code. Adapt their intent to the language. A local function extraction does not require a class. A closed exhaustive match does not require polymorphism.

## Apply and verify

For an implementation request, make one coherent transformation at a time and run the relevant checks. Inspect call sites after signature or ownership changes. Preserve externally consumed contracts unless migration is within the authorized scope. Account for configuration, serialization, reflection, and dynamic dispatch before deleting old names.

Check the properties the change could disturb. Extraction can change captured variables or asynchronous timing. Moving a field can change ownership. Replacing a query can repeat effects or expensive work. Guard clauses can change error precedence or cleanup. Shared abstractions can merge concepts that evolve separately.

Finish with the concrete change, the technique used, the observed verification result, and any remaining limits. State when a proposal was left as a plan. Claim equivalence only for the behavior actually checked. Explain the result in the user's language and retain canonical technique names for lookup.

## Source use

This skill's selection checks are original engineering guidance. The canonical technique names and linked catalog come from [Refactoring Guru](https://refactoring.guru/refactoring/techniques), checked on 2026-10-19. Use linked pages for a technique's detailed mechanics when needed. If a page is unavailable, use the packaged guidance and state any source-dependent uncertainty. Attribute explanations derived from a source and write examples for the user's code.
