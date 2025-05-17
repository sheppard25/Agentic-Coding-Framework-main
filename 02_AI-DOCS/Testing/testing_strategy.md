# Stratégie de Test - ReactGRBL Controller

## 1. Introduction

Ce document décrit la stratégie de test pour le projet ReactGRBL Controller. L'objectif est d'assurer la qualité, la fiabilité et la robustesse de l'application grâce à une approche de test complète couvrant les tests unitaires, les tests d'intégration et les tests de bout en bout (E2E).

## 2. Objectifs des Tests

*   Vérifier que chaque unité de code (fonction, module, composant) fonctionne comme prévu.
*   S'assurer que les différentes parties de l'application (frontend, backend, API, base de données) interagissent correctement.
*   Valider que les fonctionnalités clés de l'application répondent aux exigences du PRD du point de vue de l'utilisateur.
*   Identifier et corriger les bugs le plus tôt possible dans le cycle de développement.
*   Faciliter la refactorisation et la maintenance du code en fournissant un filet de sécurité.
*   Garantir une expérience utilisateur stable et de haute qualité.

## 3. Niveaux de Test

### 3.1. Tests Unitaires (TU)

*   **Objectif :** Tester les plus petites unités de code isolément (fonctions, méthodes, composants React).
*   **Backend (Python) :**
    *   **Outils :** `pytest` (préféré) ou `unittest` (module standard).
    *   **Couverture :** Fonctions logiques, classes, utilitaires, interactions avec des mocks de dépendances externes (ex: GRBL, base de données).
    *   **Exemples :**
        *   Tester la logique de connexion/déconnexion GRBL (avec un simulateur GRBL mocké).
        *   Tester les fonctions de parsing de commandes G-code.
        *   Tester les opérations CRUD sur les modèles de base de données (avec une base de données en mémoire).
        *   Tester la logique de conversion image vers G-code (avec des images et des paramètres de test).
*   **Frontend (JavaScript/React) :**
    *   **Outils :** `Jest` avec `React Testing Library`.
    *   **Couverture :** Composants React (rendu, interactions utilisateur de base, état), fonctions utilitaires, hooks personnalisés.
    *   **Exemples :**
        *   Tester le rendu correct d'un composant avec différentes props.
        *   Tester les interactions utilisateur (clics sur les boutons, saisie dans les champs).
        *   Tester la logique des hooks personnalisés.
        *   Tester les fonctions de formatage de données.

### 3.2. Tests d'Intégration (TI)

*   **Objectif :** Tester l'interaction entre plusieurs composants ou modules.
*   **Backend (Python) :**
    *   **Outils :** `pytest`.
    *   **Couverture :** Interaction entre les services, les contrôleurs API et la base de données. Communication avec le simulateur GRBL.
    *   **Exemples :**
        *   Tester un endpoint API complet (requête -> traitement -> réponse) en interagissant avec une base de données de test.
        *   Tester le flux de connexion à GRBL, envoi d'une commande, et réception de la réponse via le simulateur.
        *   Tester le processus de téléversement de fichier G-code et son enregistrement.
*   **Frontend (JavaScript/React) :**
    *   **Outils :** `Jest` avec `React Testing Library`, `Mock Service Worker (MSW)` pour mocker les appels API.
    *   **Couverture :** Interaction entre plusieurs composants React, flux de données, appels API mockés.
    *   **Exemples :**
        *   Tester un formulaire complet (saisie, validation, soumission et mise à jour de l'UI basée sur une réponse API mockée).
        *   Tester la navigation entre différentes vues de l'application.
        *   Tester la mise à jour de l'état global suite à une action utilisateur.

### 3.3. Tests de Bout en Bout (E2E)

*   **Objectif :** Tester l'application complète du point de vue de l'utilisateur, simulant des scénarios réels.
*   **Outils :** `Playwright` (préféré) ou `Cypress`.
*   **Couverture :** Flux utilisateurs critiques définis dans le PRD.
*   **Exemples :**
    *   Scénario : Connexion à une machine GRBL simulée, chargement d'un fichier G-code, démarrage de l'usinage, mise en pause, et arrêt.
    *   Scénario : Téléversement d'une image, configuration des paramètres de conversion, génération du G-code, et prévisualisation.
    *   Scénario : Navigation dans les paramètres de l'application et modification d'un paramètre.
    *   Scénario : Jogging de la machine sur différents axes.

## 4. Environnement de Test

*   **Base de Données de Test :** Utiliser une base de données SQLite en mémoire ou des fichiers de test pour les tests backend afin d'isoler les tests et d'assurer la rapidité.
*   **Simulateur GRBL :** Développer ou utiliser un simulateur GRBL simple pour les tests backend et E2E afin de ne pas dépendre d'une machine physique. Ce simulateur devra pouvoir répondre aux commandes de base et simuler des états.
*   **Mocking API :** Utiliser `Mock Service Worker (MSW)` ou des mocks Jest pour les appels API dans les tests d'intégration frontend.

## 5. Stratégie d'Exécution des Tests

*   **Développement Local :** Les développeurs exécutent les tests unitaires et d'intégration pertinents localement avant de pousser le code.
*   **Intégration Continue (CI) :**
    *   Mettre en place un pipeline CI (ex: GitHub Actions, GitLab CI).
    *   Tous les tests (unitaires, intégration, E2E) sont exécutés automatiquement à chaque push sur les branches principales ou lors de la création de Pull Requests.
    *   Un build ne sera considéré comme réussi que si tous les tests passent.
*   **Couverture de Code :**
    *   Utiliser des outils de mesure de couverture de code (ex: `coverage.py` pour Python, `Jest --coverage` pour JavaScript).
    *   Viser une couverture de code élevée pour les tests unitaires et d'intégration (cible > 80%).

## 6. Gestion des Bugs

*   Utiliser un système de suivi des problèmes (ex: GitHub Issues).
*   Chaque bug rapporté doit inclure des étapes claires pour le reproduire.
*   Prioriser la correction des bugs en fonction de leur sévérité et de leur impact.
*   Écrire un test (unitaire ou d'intégration) qui reproduit le bug avant de le corriger, pour s'assurer qu'il est bien résolu et éviter les régressions (Test-Driven Development pour les bugs).

## 7. Types de Tests Spécifiques

*   **Tests de Performance :** (Phase ultérieure) Pourraient être envisagés pour identifier les goulots d'étranglement, en particulier pour le traitement de gros fichiers G-code ou la communication WebSocket.
*   **Tests d'Utilisabilité :** (Phase ultérieure, manuels) Recueillir les retours des utilisateurs bêta pour améliorer l'expérience utilisateur.
*   **Tests de Compatibilité :** S'assurer que l'application fonctionne correctement sur les navigateurs cibles (si application web) et les systèmes d'exploitation cibles (si application de bureau avec Electron).

## 8. Responsabilités

*   **Développeurs :** Responsables de l'écriture des tests unitaires et d'intégration pour le code qu'ils produisent.
*   **Responsable Qualité/Lead Dev :** Superviser la stratégie de test, s'assurer de la couverture et de la qualité des tests, et gérer le pipeline CI.

---
*Ce document sera mis à jour au besoin pour refléter l'évolution du projet et des outils.*