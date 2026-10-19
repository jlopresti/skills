# Skills Refactoring Guru

Ce dépôt distribue trois skills indépendants pour analyser et améliorer du code avec les concepts de [Refactoring Guru](https://refactoring.guru/). Le plugin `refactoring-guru` installe les trois ensemble. Les guides sont indépendants du site Refactoring Guru et ne représentent pas une publication officielle de celui-ci.

| Skill | Usage |
| --- | --- |
| [refactoring-guru-code-smells](plugins/refactoring-guru/skills/refactoring-guru-code-smells/SKILL.md) | Diagnostiquer les problèmes de structure avec des preuves dans le code et des contre-exemples. |
| [refactoring-guru-refactoring](plugins/refactoring-guru/skills/refactoring-guru-refactoring/SKILL.md) | Planifier ou appliquer une transformation en préservant le comportement observable. |
| [refactoring-guru-design-patterns](plugins/refactoring-guru/skills/refactoring-guru-design-patterns/SKILL.md) | Comparer les patterns adaptés à un problème et leur coût face à une solution plus simple. |

## Installer depuis le dépôt GitHub

Les commandes suivantes utilisent la branche par défaut du dépôt. Enregistrez le marketplace puis installez le plugin. Le contenu de cette branche doit inclure les catalogues et le plugin. Le dépôt est privé : votre compte ou votre client Git doit avoir accès à `jlopresti/skills`. Le marketplace du dépôt permet une distribution privée; il ne constitue pas une inscription dans un catalogue public de plugins.

Dans Codex CLI :

```sh
codex plugin marketplace add jlopresti/skills
codex plugin add refactoring-guru@jlopresti-skills
```

Dans GitHub Copilot CLI :

```sh
copilot plugin marketplace add jlopresti/skills
copilot plugin install refactoring-guru@jlopresti-skills
```

Pour utiliser la branche avant la fusion, clonez ce dépôt ou ouvrez son checkout local. Passez **le chemin absolu de sa racine**, qui contient `.agents/`, `.github/` et `plugins/`, à la commande du client :

```sh
codex plugin marketplace add /chemin/absolu/vers/skills
codex plugin add refactoring-guru@jlopresti-skills

copilot plugin marketplace add /chemin/absolu/vers/skills
copilot plugin install refactoring-guru@jlopresti-skills
```

Dans Visual Studio Code, la documentation d'Agent Plugins indique que `chat.plugins.marketplaces` accepte les dépôts GitHub et que le panneau **Agent Plugins** permet leur installation. Activez `chat.plugins.enabled` si nécessaire. Ajoutez `jlopresti/skills` à la liste existante de `chat.plugins.marketplaces` dans les paramètres, sans supprimer les autres entrées, puis installez `refactoring-guru` depuis **Agent Plugins**. Cette procédure suit la documentation de VS Code; l'interface n'a pas été testée pour ce dépôt. L'accès au dépôt privé reste nécessaire.

## Utiliser les skills

Formulez la demande dans votre langue habituelle. Par exemple :

```text
Audite ce module avec Refactoring Guru Code Smells et justifie chaque constat avec un emplacement précis. Garde le code inchangé.

Simplifie les conditions de cette fonction avec Refactoring Guru Refactoring en conservant les résultats, les erreurs et les effets de bord.

Compare State et Strategy pour ce workflow avec Refactoring Guru Design Patterns. Évalue aussi une table de transitions.
```

Dans Codex, le plugin expose par exemple `$refactoring-guru:refactoring-guru-code-smells`. Un skill installé seul conserve son nom court, tel que `$refactoring-guru-code-smells`. Pour les autres clients, sélectionnez le nom affiché dans leur liste de skills. Les instructions des skills sont en anglais et demandent une réponse dans la langue de l'utilisateur. Chaque dossier contient son `SKILL.md`, ses métadonnées et ses références; les liens internes restent dans ce dossier.

Si vous préférez installer un seul skill sans marketplace, copiez **son dossier complet** depuis `plugins/refactoring-guru/skills/` dans le répertoire de skills reconnu par votre agent, par exemple `.agents/skills/` pour un projet Codex ou `.github/skills/` pour un projet Copilot. Ne copiez pas seulement `SKILL.md`, car les références et les métadonnées font partie du skill.

## Mettre à jour

Après une modification du dépôt distant, actualisez le catalogue Codex ou le catalogue et le plugin Copilot :

```sh
codex plugin marketplace upgrade jlopresti-skills

copilot plugin marketplace update jlopresti-skills
copilot plugin update refactoring-guru
```

Dans Codex, installez ensuite la version souhaitée depuis le catalogue actualisé. Pour un marketplace local, les fichiers proviennent du checkout. Mettez ce checkout à jour, puis redémarrez le client ou ouvrez une nouvelle session. Vous pouvez vérifier les liens et les catalogues du paquet avec `python3 scripts/validate-marketplace.py`.

Les formats et commandes suivent la [documentation des plugins Codex](https://developers.openai.com/plugins/build/plugins), la [référence des plugins Copilot CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference), le [guide des marketplaces Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) et la [documentation des plugins dans VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins). Les noms canoniques des concepts suivent les catalogues de [code smells](https://refactoring.guru/refactoring/smells), de [refactorings](https://refactoring.guru/refactoring/techniques) et de [design patterns](https://refactoring.guru/design-patterns/catalog), consultés le 19 octobre 2026.
