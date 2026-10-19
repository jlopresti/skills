# Maintenance ciblée

`strategy.py` emploie des fonctions comme stratégies : les deux formats sont isolés et un petit répartiteur garde le choix près de son usage. La sélection reste dans la boucle pour conserver le comportement avec un flux vide, un style à comparaison observable, et les erreurs ou effets de `emit` à leur position actuelle. Des classes ajouteraient ici une structure sans bénéfice concret.

`refactoring.py` extrait la boucle de `settle` dans `_prepare_rows`. La fonction reçoit le total et la liste existants et les renvoie; elle parcourt l'itérable une seule fois, conserve les objets ligne par identité et laisse l'événement `total` et les mises à jour `charged` dans leur ordre d'origine.

## Audit de `audit.py`

Le diagnostic **Long Method** est utile pour `finalize_round` (lignes 4–41) : une demande concrète de changement des remises devrait aujourd'hui être suivie au milieu de la validation/réservation du stock et de la mise en forme du reçu. Une découpe modeste isolerait le calcul des ajustements du montant (lignes 27–31) dans une fonction telle que `_adjusted_order_total`, qui reçoit le sous-total, la commande et le dépôt. La boucle principale garderait son orchestration; une fonction distincte pour réserver les lignes pourrait ensuite porter validations, décrément de stock et création du colis, tandis que les ajouts au reçu resteraient dans la présentation. Cette frontière évite que les règles de remise imposent de modifier ces responsabilités. Il faut préserver l'ordre actuel des validations et effets, notamment la réservation progressive du stock avant les erreurs ultérieures.
