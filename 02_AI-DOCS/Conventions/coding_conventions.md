# Conventions de Codage - ReactGRBL Controller

## 1. Introduction

Ce document définit les conventions de codage à suivre pour le développement du projet ReactGRBL Controller. L'objectif est d'assurer la lisibilité, la maintenabilité et la cohérence du code à travers l'ensemble du projet. Ces conventions s'appliquent à la fois au backend Python et au frontend JavaScript/React.

## 2. Conventions Générales (Applicables à Python et JavaScript)

### 2.1. Nommage

*   **Langue :** Utiliser l'anglais pour tous les noms de variables, fonctions, classes, fichiers, etc. Les commentaires et la documentation peuvent être en français si cela facilite la compréhension pour l'équipe.
*   **Clarté :** Choisir des noms descriptifs et sans ambiguïté. Éviter les abréviations excessives.
*   **Cohérence :** Utiliser le même style de nommage pour des concepts similaires à travers le projet.

### 2.2. Formatage

*   **Indentation :** Utiliser 4 espaces pour l'indentation. Ne pas utiliser de tabulations.
*   **Longueur des Lignes :** Essayer de limiter la longueur des lignes à 100-120 caractères pour une meilleure lisibilité.
*   **Lignes Vides :** Utiliser les lignes vides pour séparer logiquement les blocs de code (par exemple, entre les définitions de fonctions, ou pour regrouper des sections de code au sein d'une fonction).

### 2.3. Commentaires

*   **Quand commenter :** Commenter le code qui n'est pas immédiatement évident. Expliquer le "pourquoi" plutôt que le "comment" si le code est déjà clair sur le "comment".
*   **Style :**
    *   Commentaires de bloc pour expliquer des sections complexes ou des algorithmes.
    *   Commentaires en ligne pour des clarifications ponctuelles.
*   **TODOs :** Utiliser `// TODO:` ou `# TODO:` pour marquer les sections de code qui nécessitent un travail futur, avec une brève explication.

### 2.4. Gestion des Erreurs

*   Utiliser des mécanismes de gestion des erreurs robustes (try-except en Python, try-catch en JavaScript).
*   Fournir des messages d'erreur clairs et informatifs.
*   Éviter de masquer les erreurs silencieusement.

### 2.5. Contrôle de Version (Git)

*   **Messages de Commit :** Rédiger des messages de commit clairs et concis, en anglais. Utiliser le présent et un style impératif (ex: "Add feature X", "Fix bug Y").
    *   Format suggéré : `type(scope): short description` (ex: `feat(api): add user authentication endpoint`, `fix(ui): correct button alignment`).
*   **Branches :** Utiliser des branches pour les nouvelles fonctionnalités (`feature/`) et les corrections de bugs (`fix/`).
*   **Pull Requests (PRs) / Merge Requests (MRs) :** Fournir une description claire des changements dans les PRs/MRs. S'assurer que le code est revu avant d'être fusionné dans la branche principale.

## 3. Conventions Spécifiques au Backend (Python)

### 3.1. Style de Code

*   **PEP 8 :** Suivre les recommandations du [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).
*   **Linters et Formatteurs :** Utiliser des outils comme `Flake8` pour le linting et `Black` ou `autopep8` pour le formatage automatique du code.

### 3.2. Nommage Python

*   **Modules :** `module_name.py` (minuscules avec underscores).
*   **Packages :** `package_name` (minuscules).
*   **Classes :** `ClassName` (CapWords/PascalCase).
*   **Fonctions et Méthodes :** `function_name` (minuscules avec underscores).
*   **Variables :** `variable_name` (minuscules avec underscores).
*   **Constantes :** `CONSTANT_NAME` (majuscules avec underscores).

### 3.3. Docstrings

*   **PEP 257 :** Suivre les [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/).
*   Utiliser des docstrings pour tous les modules, classes, fonctions et méthodes publiques.
*   Format suggéré : Google Style Docstrings ou NumPy/SciPy style.

### 3.4. Imports

*   Organiser les imports en haut du fichier, dans l'ordre suivant :
    1.  Bibliothèques standard Python.
    2.  Bibliothèques tierces.
    3.  Modules locaux de l'application.
*   Séparer chaque groupe par une ligne vide.
*   Éviter les imports `from module import *`.

### 3.5. Environnements Virtuels

*   Toujours utiliser un environnement virtuel (ex: `venv`, `conda`) pour gérer les dépendances du projet.
*   Maintenir un fichier `requirements.txt` (ou `environment.yml` pour Conda) à jour.

## 4. Conventions Spécifiques au Frontend (JavaScript/React)

### 4.1. Style de Code

*   **Standard :** Suivre un guide de style JavaScript populaire comme [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) ou [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html). Choisir un standard et s'y tenir.
*   **Linters et Formatteurs :** Utiliser `ESLint` pour le linting et `Prettier` pour le formatage automatique du code. Configurer ces outils pour qu'ils s'alignent sur le guide de style choisi.

### 4.2. Nommage JavaScript/React

*   **Variables et Fonctions :** `variableName`, `functionName` (camelCase).
*   **Constantes :** `CONSTANT_NAME` (majuscules avec underscores) ou `const constantName` (camelCase) si la valeur n'est pas une primitive "dure".
*   **Classes et Composants React :** `ClassName`, `ComponentName` (PascalCase).
*   **Fichiers de Composants :** `ComponentName.js` ou `ComponentName.jsx`.
*   **Fichiers de Services/Utilitaires :** `serviceName.js`, `utils.js` (camelCase ou PascalCase pour les classes).

### 4.3. React

*   **Composants Fonctionnels :** Préférer les composants fonctionnels avec les Hooks React plutôt que les composants basés sur les classes, sauf si une raison spécifique justifie l'utilisation de classes.
*   **Props :** Utiliser `propTypes` (ou TypeScript) pour la validation des types des props.
*   **Structure des Composants :** Organiser la structure des dossiers des composants de manière logique (par exemple, par fonctionnalité ou par type de composant).
*   **Gestion de l'État :**
    *   Utiliser l'état local (`useState`) pour les états spécifiques à un composant.
    *   Utiliser `useReducer` pour une logique d'état plus complexe au sein d'un composant.
    *   Utiliser l'API Context (`useContext`) ou une bibliothèque de gestion d'état globale (Redux, Zustand, etc.) pour l'état partagé entre plusieurs composants. Le choix sera basé sur la complexité du PRD.

### 4.4. Imports/Exports

*   Utiliser les modules ES6 (`import` / `export`).
*   Préférer les exports nommés plutôt que les exports par défaut pour une meilleure clarté, sauf pour les composants React où l'export par défaut est courant.
    ```javascript
    // Préféré pour les utilitaires
    export const utilFunction = () => {};
    export const anotherUtil = () => {};

    // Courant pour les composants React
    const MyComponent = () => { /* ... */ };
    export default MyComponent;
    ```

### 4.5. Gestion des Dépendances

*   Utiliser `npm` ou `yarn` pour gérer les dépendances du projet.
*   Maintenir le fichier `package.json` et `package-lock.json` (ou `yarn.lock`) à jour et versionnés.

## 5. Outils

*   **Linters :**
    *   Python: `Flake8`
    *   JavaScript/React: `ESLint`
*   **Formatteurs :**
    *   Python: `Black` ou `autopep8`
    *   JavaScript/React: `Prettier`
*   **Intégration :** Configurer ces outils pour qu'ils s'exécutent dans l'IDE et potentiellement dans un hook de pre-commit (ex: Husky).

---
*Ce document sera mis à jour si nécessaire pour refléter l'évolution des meilleures pratiques ou des décisions de l'équipe.*
