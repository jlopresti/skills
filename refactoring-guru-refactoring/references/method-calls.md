# Method calls

Names follow [Refactoring Guru's call family](https://refactoring.guru/refactoring/techniques/simplifying-method-calls). Selection checks are local guidance.

| Technique | Selection cue |
| --- | --- |
| [Rename Method](https://refactoring.guru/rename-method) | The name misstates behavior. |
| [Add Parameter](https://refactoring.guru/add-parameter) | Required context becomes explicit. |
| [Remove Parameter](https://refactoring.guru/remove-parameter) | An input is redundant. |
| [Separate Query from Modifier](https://refactoring.guru/separate-query-from-modifier) | Reads and effects need separation. |
| [Parameterize Method](https://refactoring.guru/parameterize-method) | Methods differ by meaningful data. |
| [Replace Parameter with Explicit Methods](https://refactoring.guru/replace-parameter-with-explicit-methods) | A flag selects separate intentions. |
| [Preserve Whole Object](https://refactoring.guru/preserve-whole-object) | Callers unpack one cohesive value. |
| [Replace Parameter with Method Call](https://refactoring.guru/replace-parameter-with-method-call) | A pure query supplies the value. |
| [Introduce Parameter Object](https://refactoring.guru/introduce-parameter-object) | Parameters form one domain concept. |
| [Remove Setting Method](https://refactoring.guru/remove-setting-method) | Construction fixes a value. |
| [Hide Method](https://refactoring.guru/hide-method) | A method is internal. |
| [Replace Constructor with Factory Method](https://refactoring.guru/replace-constructor-with-factory-method) | Construction needs a named boundary. |
| [Replace Error Code with Exception](https://refactoring.guru/replace-error-code-with-exception) | Authorized callers can migrate errors. |
| [Replace Exception with Test](https://refactoring.guru/replace-exception-with-test) | A predictable case has a safe check. |

## Selection checks

Preserve external contracts and effect ordering. Changing error mechanisms can require explicit API migration. Prechecks cannot prevent concurrent failures. A construction function need not implement the GoF Factory Method pattern.
