Évaluation en aveugle : échelle commune **complet / partiel / absent**, sans score global. Les références sont relatives au dossier de chaque solution.

| Critère | S1 | S2 | S3 | S4 |
|---|---|---|---|---|
| 1. Strategy, contrat commun et effets/erreurs | partiel | partiel | complet | partiel |
| 2. Long Method, besoin concret et contre-exemple | partiel | complet | partiel | complet |
| 3. Extract Method et comportement observable | complet | complet | complet | complet |
| 4. Accès documentaire local consigné | complet | complet | complet | complet |
| 5. Périmètre et justification proportionnés | complet | complet | complet | complet |

**Strategy.** Toutes isolent les deux algorithmes dans des fonctions interchangeables de contrat commun `item → texte` (`strategy.py:1–6`). Cette représentation convient au module ; ni classes ni forme particulière du sélecteur ne sont nécessaires. Les boucles conservent le rendu, puis `emit`, puis l'ajout au résultat. Un flux vide n'évalue pas le style et une erreur du rappel interrompt le parcours.

Différence concrète : S1 (`strategy.py:11–20`), S2 et S4 (`19–23`) sélectionnent une seule fois. S3 (`9–21`) compare à chaque élément, comme l'original. J'ai exécuté, sans modifier les sources, une extension ciblée : deux éléments produits par générateur, avec un style dérivé de `str`, égal à `label`, dont la deuxième comparaison lève `RuntimeError`. L'original et S3 émettent le premier texte, récupèrent le deuxième élément, puis lèvent ; S1, S2 et S4 émettent aussi le deuxième texte et retournent normalement. C'est une régression sur un style à comparaison observable, accepté par la signature actuelle. Avec des chaînes ordinaires, les résultats fournis ne distinguent pas ces variantes. S3 décrit explicitement ce cas dans `notes.md:3`.

**Long Method.** Les quatre diagnostics relient la difficulté concrète de changer les remises aux responsabilités entremêlées de `finalize_round`. S1 (`notes.md:13–15`) propose d'extraire seulement la remise, lignes 27–28 ; S2 (`:5`), S3 (`:9`) et S4 (`:5`) isolent les ajustements, frais et arrondi, lignes 27–31. Ces découpes sont toutes utiles et proportionnées, avec maintien de l'orchestration et des effets progressifs. S2 et S4 expliquent explicitement que `decode_station_frame` reste cohésif malgré sa longueur. S1 et S3 l'omettent : aucun faux positif déclaré, mais aucune démonstration explicite de ce contre-exemple, d'où « partiel ».

**Extract Method.** Égalité sur la substance. Dans chaque `refactoring.py`, la préparation retourne le total et la liste ; `settle` récupère ces valeurs à la ligne 14. S3 passe les variables déjà initialisées ; les autres les initialisent dans le helper. Toutes gardent un seul parcours, les mêmes dictionnaires, les opérations arithmétiques et accès dans le même ordre, puis l'événement du total avant les mutations `charged`. Aucune régression identifiée ici.

**Traçabilité et périmètre.** Chaque `contracts.json:10` consigne un accès documentaire local. Ce constat ne prouve ni l'application d'un skill ni une indépendance générale vis-à-vis des sources ; les transcriptions complètes manquent. Les vérifications d'artefacts fournies établissent `audit.py` inchangé, avec la même empreinte (`contracts.json:5`). Les modifications et notes restent ciblées, sans changement étranger à la demande.

**Verdict et limites.** S2 et S4 sont à égalité sur cette grille. Aucun vainqueur global : S3 préserve davantage le comportement Python, tandis que S2/S4 documentent mieux le contre-exemple. Les quatre rapports annoncent 16 cas réussis, des attendus manuscrits recoupés avec l'original figé et aucune divergence. Cela étaye les cas exercés, sans prouver l'équivalence générale : ni leurs définitions détaillées ni les transcriptions d'exécution ne sont fournies. L'extension sur la comparaison observable, décrite et exécutée ci-dessus, constitue précisément un test discriminant à ajouter.
