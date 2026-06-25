**<h2>3. Questions de réflexion</h2>**

1. **Gestion de version**

   * Comment organiser le travail en groupe avec des branches (`feature/api`, `bugfix/zero-value`…)?   
   * Quels avantages apportent les Pull Requests par rapport à un push direct sur `main`?

**Réponse 1) D'abord on crée une branche develop à partir de main et ensuite à partir de develop on crée des branches par fonctionnalités et types de maintenance. \
Les  Pull requests permettent de déclencher des tests automatiques via Github Actions par exmeple et de permettre à d'autre personne de revoir et approuver le code.** 

2. **Qualité et tests**

   * Qu’est-ce qu’un test unitaire et pourquoi est-il important?
   * Pourquoi automatiser les tests dans GitHub Actions avant d’accepter une PR?

** Réponse 2) Les tests unitaires sont des tests qui permettent de tester chaque fonction indépendament des autres. Ils sont importants car ils permettent de s'assurer que chaque fonctionnalité fonctionne comme prévu et donc de détecter les erreurs plus facilement.
Automatiser les tests permets déviter les régresssions lors de l'ajout d'une nouvelle fonctionnalité par exemple et s'assurer que que le nouveau code n'a pas cassé d'ancienne fonctionnalité.**

3. **Refactoring**

   * Quelles dettes techniques observez-vous dans le code initial?
   * Quelles modifications ont amélioré la maintenabilité et la lisibilité?

** Répones 3) On observe que la logique métier n'est pas séparé, que les taux sont en brut, et qu'il n'y a aucun test en cas d'erreur et test_unitaire. \
La maintenance perfective a permis d'améliorer la maintenance en divisant le code en plusieurs fichier (logique métier) et la lisibilité en ajoutant des commentaires et \ utilisant black et flake8.**

4. **Maintenance**

   * Classez vos modifications selon les quatre types de maintenance.
   * Quelle partie vous semble la plus fréquente dans un projet réel?

Réponse 4) **
Maintenance corrective :
- vérification pour les montants nuls ou négatifs.
- Vérifier que la devise source et la devise cible ne sont pas identiques.
- message d’erreur clair si ces conditions ne sont pas respectées.

Maintenance évolutive :
-  bouton pour inverser les devises sélectionnées.
- nouvelle devise JPY, CAD.
- ajout d'un historique de conversions 

Maintenance adaptative:
- Remplacement des taux codés en dur par des données récupérées via une API externe.
- Adaptation de la logique pour utiliser ces taux dynamiques dans la fonction de conversion.

Maintenance perfective :
- Refactorisation de la logique métier dans un fichier app_functions.py.
- Création d'une fonction convert(amount, from_currency, to_currency, rates) qui renvoie le résultat.
- Ajout de tests unitaires dans test_app.py pour valider la conversion.
- Mise en place d'un workflow GitHub Actions pour exécuter automatiquement les tests à chaque Pull Request.

Dans un projet réel la maintenance la plus fréquente est la maintenance évolutive selon nous.

** 