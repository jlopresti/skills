# Notes de maintenance

## `strategy.py`

`render_batch` utilisait deux algorithmes dans sa boucle. Les fonctions `_render_label` et `_render_slug` isolent ces variations; la petite sélection locale rend l’ajout d’un style direct, sans introduire de hiérarchie de classes. La sélection reste dans la première itération : un flux vide n’évalue toujours pas le style, et un style inconnu échoue après la récupération du premier élément, comme avant. Chaque élément est toujours rendu avant l’appel à `emit`, et l’ajout au résultat n’a lieu qu’après le succès du rappel.

## `refactoring.py`

`_prepare_settlement` porte la boucle de lecture et retourne le total avec la liste des dictionnaires acceptés. Il consomme le flux une seule fois, journalise chaque élément au même moment et conserve les références d’origine. `settle` garde l’ordre « début, préparation, total, marquage »; les mutations `charged` restent donc après l’événement du total.

## Audit `audit.py`

Le diagnostic **Long Method** est utile pour `finalize_round` (lignes 4–41) : une seule fonction combine validation de commande, réservation et calcul des lignes (10–26), ajustements de prix (27–31), écritures du ledger et notifications (33–36), puis total et reçu final (37–40). Le besoin concret de modifier les remises touche les lignes 27–28, alors que le stock est diminué aux lignes 20–22 et que la présentation est assemblée aux lignes 7, 26, 34, 38 et 40. Ce sont des responsabilités à raisons de changement distinctes; la taille seule ne justifierait pas l’extraction.

Découpe adaptée : extraire les lignes 27–28 dans `_apply_order_discounts(order, order_total)`, qui retourne le montant après remise. L’appel reste après le calcul des lignes et avant les frais distants (29–30), en conservant l’arrondi à la ligne 31. Le calcul de remise devient modifiable sans déplacer la réservation du stock ni le formatage des reçus. Éviter d’extraire toute la fonction en wrappers d’étapes : cela ne clarifierait pas la règle demandée et compliquerait l’ordre observable des diminutions de stock, entrées du ledger et notifications. `audit.py` est resté intact.
