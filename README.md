# Skills

Trois skills indépendants pour analyser et améliorer du code avec les concepts de [Refactoring Guru](https://refactoring.guru/).

| Skill | Usage |
| --- | --- |
| [refactoring-guru-code-smells](refactoring-guru-code-smells/SKILL.md) | Diagnostiquer les problèmes de structure avec des preuves dans le code et des contre-exemples. |
| [refactoring-guru-refactoring](refactoring-guru-refactoring/SKILL.md) | Planifier ou appliquer une transformation en préservant le comportement observable. |
| [refactoring-guru-design-patterns](refactoring-guru-design-patterns/SKILL.md) | Comparer les patterns adaptés à un problème et leur coût face à une solution plus simple. |

Chaque dossier contient son `SKILL.md`, ses métadonnées et ses références. Copiez le dossier complet dans l'emplacement de skills pris en charge par votre agent. Les skills peuvent s'utiliser séparément. Les instructions sont en anglais et demandent une réponse dans la langue de l'utilisateur.

Exemples de demandes explicites pour un agent qui accepte la syntaxe `$skill-name`.

```text
$refactoring-guru-code-smells Audite ce module et justifie chaque constat avec un emplacement précis. Garde le code inchangé.

$refactoring-guru-refactoring Simplifie les conditions de cette fonction en conservant les résultats, les erreurs et les effets de bord.

$refactoring-guru-design-patterns Compare State et Strategy pour ce workflow. Évalue aussi une table de transitions.
```

Les références contiennent des critères de décision originaux et des liens vers les pages publiques du site. Consultez seulement les familles utiles à la tâche. Les noms canoniques suivent les catalogues de [code smells](https://refactoring.guru/refactoring/smells), de [refactorings](https://refactoring.guru/refactoring/techniques) et de [design patterns](https://refactoring.guru/design-patterns/catalog), consultés le 19 octobre 2026.

Un [pilote de fiches autonomes](comparisons/reference-depth/README.md) détaille Strategy, Long Method et Extract Method avec des exemples avant/après, les contrôles exécutables et la comparaison avec les versions initiales.
