---
name: refactoring-guru-code-smells
description: Diagnose code smells with Refactoring Guru terminology when asked to audit maintainability, identify code smells, or explain a suspected structural problem. Produce evidence and refactoring candidates. Audit and review requests default to analysis.
---

# Diagnose code smells

Use the [Refactoring Guru code smells catalog](https://refactoring.guru/refactoring/smells) as a vocabulary for investigation. A smell is a maintenance hypothesis. Establish the relationship in the code and its cost before reporting a finding.

## Investigate the requested scope

1. Read the repository instructions and identify the requested files, diff, or subsystem. Follow callers, data ownership, and relevant tests far enough to check a suspected smell.
2. Load the reference for the observed family. For a broad audit, inspect each family, then concentrate on the code that supports a concern.
3. Compare the evidence with the reference's counterexamples. Use call paths, repeated invariants, concrete change requirements, or relevant history to establish the maintenance consequence. Code size and syntax alone establish no finding.
4. Separate demonstrated findings from suspects. For a suspect, state the missing evidence and the check that would settle it. Accept a clean result.

Read only the references needed by the scope:

- Read [bloaters](references/bloaters.md) for mixed responsibilities, repeated data groups, domain values, and difficult call signatures.
- Read [object-orientation abusers](references/object-orientation-abusers.md) for inheritance, inconsistent equivalent interfaces, repeated dispatch, and operation-specific fields.
- Read [change preventers](references/change-preventers.md) for scattered edits, unrelated reasons to change one component, and synchronized hierarchies.
- Read [dispensables](references/dispensables.md) for explanatory comments, duplication, data containers, apparently unused code, and unearned abstractions.
- Read [couplers and library limits](references/couplers.md) for misplaced behavior, internal knowledge, object navigation, delegation, and missing library operations.

The catalog uses object-oriented terms. Match its concepts to the repository's paradigm. Functions over records, algebraic data types, and modules can express sound designs without classes. Assess where invariants and dependencies live.

For a Long Method hypothesis or its extraction boundary, read the self-contained [Long Method diagnosis and examples](references/long-method.md).

## Report the decision

For each demonstrated finding, give the canonical smell name, exact file and line evidence, the maintenance consequence, and the relevant counterexample you ruled out. Suggest the smallest useful response and its tradeoff. Link the matching catalog entry. Rank findings by the cost or risk supported by the evidence. A smell alone establishes no bug severity.

Keep suspects separate and concise. State the audit's coverage and any unavailable evidence. Recommendations can include leaving the design unchanged when an abstraction would cost more than the demonstrated problem. Explain the result in the user's language and retain canonical smell names for lookup.

## Change code only within authorization

Audit, review, explanation, and diagnosis requests authorize analysis. Modify code when the user requests a fix or refactoring, or has already authorized that work. A candidate technique is an option, not an instruction to apply it.

For an authorized change, preserve observable behavior and contracts. Establish the relevant behavior before editing, make a focused change, and check that behavior afterward. Report any verification limits. Before deleting apparently unused code, check exports, external callers, configuration, reflection, plugin registration, generated access, and runtime entrypoints.

The references are original diagnostic notes informed by the public catalog, checked on 2026-10-19. Consult the linked pages for full treatments.
