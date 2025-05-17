# Stratégie de Branchement (GitFlow)

Ce projet utilise une stratégie de branchement inspirée de GitFlow.

## Branches Principales

-   `main` (ou `master`): Cette branche contient le code de production. Tout ce qui est dans `main` est déployable. Ne committez jamais directement sur `main`. Les commits sur `main` ne proviennent que de merges depuis `develop` (pour les releases) ou de hotfixes.
-   `develop`: Cette branche contient le code le plus récent et stable intégrant les dernières fonctionnalités développées. C'est la branche principale pour le développement quotidien.

## Branches de Support

### 1. Branches de Fonctionnalité (`feature/`)

-   **Objectif**: Développer de nouvelles fonctionnalités.
-   **Création**: À partir de `develop`.
-   **Nommage**: `feature/<nom-descriptif-de-la-fonctionnalite>` (par exemple, `feature/user-authentication`, `feature/visualizer-grid`).
-   **Merge**: Une fois la fonctionnalité terminée et testée, elle est mergée dans `develop` via une Pull Request (PR).
-   **Suppression**: Supprimer la branche de fonctionnalité après le merge dans `develop`.

### 2. Branches de Release (`release/`)

-   **Objectif**: Préparer une nouvelle version de production. Permet de finaliser la release (corrections de bugs mineurs, préparation de métadonnées).
-   **Création**: À partir de `develop` lorsque `develop` a atteint un état stable et est prêt pour une release.
-   **Nommage**: `release/<version>` (par exemple, `release/v1.0.0`).
-   **Merge**:
    -   Une fois la branche de release prête, elle est mergée dans `main` (et taguée avec le numéro de version).
    -   Elle est également mergée dans `develop` pour s'assurer que les changements effectués pendant la phase de release (comme les corrections de bugs) sont réintégrés dans `develop`.
-   **Suppression**: Supprimer la branche de release après le merge dans `main` et `develop`.

### 3. Branches de Hotfix (`hotfix/`)

-   **Objectif**: Corriger rapidement des bugs critiques en production.
-   **Création**: À partir de `main` (depuis le tag de la version concernée).
-   **Nommage**: `hotfix/<description-du-bug-ou-numero-de-version>` (par exemple, `hotfix/login-bug-v1.0.1`).
-   **Merge**:
    -   Une fois le hotfix terminé et testé, il est mergé dans `main` (et tagué avec un nouveau numéro de version patch).
    -   Il est également mergé dans `develop` (ou la branche de release active, si elle existe) pour s'assurer que la correction est incluse dans les développements futurs.
-   **Suppression**: Supprimer la branche de hotfix après le merge dans `main` et `develop`.

## Flux de Travail Général

1.  Synchronisez votre branche `develop` locale avec le dépôt distant.
2.  Créez une branche de fonctionnalité (`feature/...`) à partir de `develop`.
3.  Travaillez sur votre fonctionnalité, committez régulièrement.
4.  Poussez votre branche de fonctionnalité sur le dépôt distant.
5.  Lorsque la fonctionnalité est prête, ouvrez une Pull Request (PR) pour merger votre branche de fonctionnalité dans `develop`.
6.  Après revue et approbation, la PR est mergée.
7.  Pour une release, une branche `release/...` est créée à partir de `develop`.
8.  Après stabilisation, la branche `release/...` est mergée dans `main` et `develop`. `main` est taguée.
9.  En cas de bug critique en production, une branche `hotfix/...` est créée à partir de `main`, corrigée, puis mergée dans `main` et `develop`.

## Messages de Commit

Utilisez des messages de commit clairs et descriptifs. Envisagez d'adopter une convention comme [Conventional Commits](https://www.conventionalcommits.org/).
Par exemple : `feat: add user login endpoint` ou `fix: resolve issue with visualizer scaling`.