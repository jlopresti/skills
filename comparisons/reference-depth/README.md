# Pilote de fiches autonomes

Trois fiches locales ajoutent des mécanismes, des contre-exemples et des exemples Python avant/après pour Strategy, Long Method et Extract Method. Leur contenu se charge lorsque le concept devient pertinent. Les scripts de ce dossier vérifient les exemples et conservent une comparaison avec les skills précédents.

## Résultat

La comparaison initiale ne démontre aucun gain global de qualité. Les deux versions réussissent les contrôles prévus. Une extension de la revue révèle une différence de comportement que ces contrôles ne couvraient pas. Cette observation a conduit à préciser la fiche Strategy, puis à faire une confirmation distincte.

| Exécution | Modèle | Documentation | Contrôles prévus | Extension sur les comparaisons |
| --- | --- | --- | --- | --- |
| cedar | gpt-6-sol, high | Initiale | 16 cas réussis | Divergence |
| willow | gpt-6-sol, high | Fiches enrichies V1 | 16 cas réussis | Divergence |
| maple | gpt-6-luna, high | Initiale | 16 cas réussis | Comportement conservé |
| birch | gpt-6-luna, high | Fiches enrichies V1 | 16 cas réussis | Divergence |

Les préparations de `settle` rendent toutes le total et les mêmes dictionnaires après un seul parcours. Les erreurs, les événements et les mutations contrôlés restent équivalents. Tous les audits identifient la difficulté de modifier les remises dans `finalize_round`. Les deux sorties Sol expliquent aussi pourquoi le décodeur plus long reste cohésif. Les deux sorties Luna initiales omettent ce contre-exemple sans le signaler comme un problème.

Le [verdict à l'aveugle](results/blinded-verdict.md) ne désigne aucun vainqueur global. Ses labels sont S1 pour birch, S2 pour cedar, S3 pour maple et S4 pour willow. L'évaluateur a reçu les sorties, les entrées communes et des résultats de contrôle anonymisés, sans l'identité des modèles ni celle des versions.

## Ce qui a été comparé

La version initiale est le commit `f2e7be6fa6293099c1d4a02c945b9f1432831119`. La version enrichie V1 est le commit `f9a0892afc8d73a9b4f5582708bff01bdad42146`. Le [manifest](results/manifest.json) conserve les affectations et les empreintes de leurs documents. Il permet de vérifier la version réellement fournie, même après les modifications ultérieures.

Chaque modèle a reçu les deux versions, avec le même effort et la même [demande](input/request.txt). Chaque exécution disposait de son projet privé. Les sorties ont été lues intégralement par l'agent principal puis appréciées ensemble par un évaluateur Astra. La grille portait sur la proportion du Strategy, le diagnostic et son contre-exemple, les contrats d'Extract Method, la lecture documentaire consignée et le périmètre autorisé. Elle utilisait les catégories complet, partiel et absent, sans score global.

`verify_outputs.py` contrôle des attentes écrites indépendamment des sorties, puis recoupe les observations avec l'original figé. Il vérifie notamment les montants, l'identité des objets, la consommation des générateurs, les effets intercalés et les erreurs. Il exige `notes.md` et contrôle l'empreinte de `audit.py`. La substance du diagnostic et des choix de structure relève de la lecture, et non de ce script.

Les [contrôles négatifs](results/controls.json) montrent le rejet d'un livrable absent, d'un total perdu, de lignes copiées, d'effets réordonnés et d'une validation anticipée. Les traces `reading.jsonl` des deux sorties enrichies attestent l'accès aux trois nouvelles fiches, avec leurs empreintes. Elles n'attestent pas toutes les opérations du runtime.

## Extension et correction de Strategy

La grille initiale utilisait des noms de styles ordinaires. L'évaluateur a ensuite fourni un style dérivé de `str` dont la deuxième comparaison lève une erreur. L'original compare à chaque élément. Trois sorties mémorisent le choix au premier élément et suppriment donc l'erreur ultérieure. Maple conserve la comparaison répétée. L'agent principal a reproduit cette différence sans modifier les sorties. Les [observations de l'extension](results/style-effects.json) restent séparées des 16 cas prévus.

La fiche Strategy précise désormais que la sélection peut avoir des effets. Déplacer ou mémoriser des comparaisons exige un contrat qui les rende pures. Passer d'un branchement à un dictionnaire ajoute aussi des exigences de hachage. Son exemple précise son domaine de valeurs natives. Cette clarification intervient après V1 et ne fait pas partie de la comparaison initiale.

Une nouvelle exécution indépendante, elm, a reçu la même demande et la fiche clarifiée, avec gpt-6-luna et l'effort high. Elle conserve la sélection à chaque élément. Les 16 cas et l'extension passent. Ses [sorties](results/elm/notes.md), traces et résultats sont conservés séparément. Ses repères de lignes dans le diagnostic sont toutefois imprécis par rapport à `input/audit.py`. Cette confirmation n'établit donc ni une amélioration globale ni un résultat sans limite.

## Reproduire les contrôles

Exécutez ces commandes depuis la racine du dépôt avec Python standard. Elles n'effectuent aucun accès réseau.

```sh
python3 comparisons/reference-depth/check_examples.py --controls
python3 comparisons/reference-depth/verify_outputs.py comparisons/reference-depth/input --source-only --controls
```

Pour rejouer les sorties conservées, préparez un nouveau dossier. La préparation exige un historique Git contenant le commit initial et refuse d'écraser un dossier déjà rempli.

```sh
python3 comparisons/reference-depth/prepare_projects.py --repo . --destination /tmp/routebook-replay
cp comparisons/reference-depth/results/cedar/strategy.py comparisons/reference-depth/results/cedar/refactoring.py comparisons/reference-depth/results/cedar/notes.md /tmp/routebook-replay/cedar/
python3 comparisons/reference-depth/verify_outputs.py /tmp/routebook-replay/cedar
```

Les autres sorties se rejouent de la même manière. Le script d'extension lit seulement `strategy.py`. La commande suivante restitue les trois divergences connues et termine avec le code 1. Elle ne constitue pas un contrôle vert de ces sorties.

```sh
python3 comparisons/reference-depth/check_style_effects.py --original comparisons/reference-depth/input/strategy.py comparisons/reference-depth/results/cedar comparisons/reference-depth/results/willow comparisons/reference-depth/results/birch comparisons/reference-depth/results/maple
```

La même commande avec `comparisons/reference-depth/results/elm` seul réussit.

## Limites et suite recommandée

Ce pilote contient une demande regroupant trois concepts et une exécution par modèle et version. Les consignes explicites sur les générateurs et l'identité aident toutes les versions. Les modèles disposent aussi de connaissances préalables. Toutes les variantes de modèles appartiennent à la famille GPT. Aucun écart statistique, gain de temps ou lien causal n'est établi.

L'accès Web était interdit par consigne. Les transcriptions complètes des outils n'étaient pas disponibles. Les traces locales prouvent les lectures enregistrées et l'intégrité des documents, pas une isolation réseau imposée ni l'exclusivité des accès.

Les fiches apportent des exemples exécutables et des mécanismes disponibles localement. Ce résultat justifie de conserver le pilote et sa correction. Pour étendre le catalogue, privilégiez de nouveaux cas variés, des répétitions et la vérification des citations de lignes avant de conclure que des fiches plus longues améliorent les décisions.
