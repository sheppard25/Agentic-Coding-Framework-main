# Document des Exigences du Produit (PRD)
# ReactGRBL Controller

**Version:** 1.0  
**Date:** 2023-11-15  
**Auteur:** IA Assistant  
**Statut:** Draft  

## Table des matières

1. [Introduction](#1-introduction)
2. [Objectifs et portée](#2-objectifs-et-portée)
3. [Utilisateurs cibles](#3-utilisateurs-cibles)
4. [Exigences fonctionnelles](#4-exigences-fonctionnelles)
5. [Exigences techniques](#5-exigences-techniques)
6. [Conception de l'interface utilisateur](#6-conception-de-linterface-utilisateur)
7. [Plan de déploiement](#7-plan-de-déploiement)
8. [Métriques de succès](#8-métriques-de-succès)
9. [Annexes](#9-annexes)

## 1. Introduction

### 1.1 Contexte

Les contrôleurs GRBL sont largement utilisés pour piloter des machines CNC et des graveurs laser. Cependant, les interfaces existantes présentent des limitations en termes de personnalisation de la visualisation et de manipulation des fichiers. ReactGRBL Controller vise à combler ces lacunes en offrant une interface moderne, intuitive et hautement personnalisable.

### 1.2 Vision du produit

ReactGRBL Controller est une interface moderne pour contrôler les machines utilisant le firmware GRBL, combinant un frontend React JavaScript pour une expérience utilisateur fluide et un backend Python pour une communication robuste avec le matériel. Le produit se distingue par sa grille de visualisation graduée tous les 20mm et son origine (0,0) positionnée en haut à droite par défaut, ainsi que par ses fonctionnalités avancées de manipulation d'images.

### 1.3 Objectifs commerciaux

- Créer une alternative open source aux solutions existantes
- Établir une communauté active d'utilisateurs et de contributeurs
- Offrir une expérience utilisateur supérieure pour les utilisateurs de machines GRBL
- Servir de base pour d'éventuelles extensions ou services premium à l'avenir

## 2. Objectifs et portée

### 2.1 Objectifs du produit

1. Développer une interface utilisateur moderne et intuitive pour contrôler les machines GRBL
2. Offrir une visualisation personnalisable avec grille graduée tous les 20mm et origine en haut à droite
3. Permettre une manipulation fluide des images (déplacement, zoom)
4. Assurer une communication fiable et robuste avec les contrôleurs GRBL
5. Fournir une solution multi-plateforme accessible via navigateur web

### 2.2 Portée du produit

#### Inclus dans la portée

- Interface web basée sur React pour le contrôle des machines GRBL
- Backend Python pour la communication avec le matériel
- Visualisation personnalisable avec grille graduée et origine configurable
- Manipulation des fichiers G-code et conversion d'images
- Contrôle manuel et automatique de la machine
- Documentation utilisateur et développeur

#### Hors de portée

- Fonctionnalités CAD/CAM avancées
- Support pour d'autres firmwares que GRBL (Marlin, Smoothieware, etc.)
- Applications mobiles natives (bien qu'une interface responsive soit prévue)
- Intégration avec des services cloud tiers

### 2.3 Critères de réussite

1. Interface fonctionnelle permettant de contrôler efficacement une machine GRBL
2. Visualisation avec grille graduée tous les 20mm et origine en haut à droite
3. Manipulation fluide des images (déplacement, zoom)
4. Communication stable et fiable avec le matériel
5. Retours positifs des utilisateurs sur l'expérience globale

## 3. Utilisateurs cibles

### 3.1 Personas

#### 3.1.1 Marc - Le Maker Débutant
- **Profil**: Homme de 35 ans, ingénieur en informatique, débutant en CNC/laser
- **Équipement**: Graveur laser 5W récemment acheté avec contrôleur GRBL
- **Besoins**: Interface simple à configurer, visualisation claire, aide contextuelle
- **Frustrations**: Difficulté à comprendre les logiciels existants, problèmes de connexion
- **Objectifs**: Réaliser ses premiers projets de gravure sans frustration

#### 3.1.2 Sophie - La Créatrice Intermédiaire
- **Profil**: Femme de 28 ans, designer, utilise régulièrement sa machine depuis 1 an
- **Équipement**: Graveur laser 10W et petite fraiseuse CNC, tous deux avec GRBL
- **Besoins**: Flexibilité, personnalisation, manipulation précise des fichiers
- **Frustrations**: Limitations des interfaces existantes, manque de personnalisation
- **Objectifs**: Optimiser son flux de travail, gagner en précision et en efficacité

#### 3.1.3 Thomas - Le Professionnel
- **Profil**: Homme de 42 ans, propriétaire d'une petite entreprise de fabrication
- **Équipement**: Plusieurs machines CNC et laser avec différents contrôleurs
- **Besoins**: Fiabilité, fonctionnalités avancées, gestion efficace des fichiers
- **Frustrations**: Instabilité des solutions existantes, manque d'uniformité
- **Objectifs**: Maximiser la productivité, minimiser les temps d'arrêt

### 3.2 Scénarios d'utilisation

#### 3.2.1 Configuration initiale
Marc vient d'acheter son premier graveur laser. Il installe ReactGRBL Controller, qui le guide à travers le processus de connexion et de configuration. L'interface intuitive lui permet de comprendre rapidement les bases et de réaliser un premier test de gravure avec succès.

#### 3.2.2 Projet de gravure d'image
Sophie souhaite graver une photo sur du bois. Elle importe l'image dans ReactGRBL Controller, ajuste les paramètres de conversion, puis utilise les fonctionnalités de déplacement et zoom pour positionner précisément l'image sur la grille. La visualisation claire avec origine en haut à droite lui permet de s'assurer que l'image sera gravée exactement où elle le souhaite.

#### 3.2.3 Production en série
Thomas doit réaliser une série de gravures identiques pour un client. Il configure le premier travail dans ReactGRBL Controller, l'exécute, puis utilise les fonctionnalités de sauvegarde et de réutilisation des paramètres pour reproduire rapidement le même travail sur plusieurs pièces, maximisant ainsi sa productivité.

## 4. Exigences fonctionnelles

### 4.1 Connexion et configuration

#### 4.1.1 Connexion au contrôleur GRBL
- **Priorité**: Élevée
- **Description**: L'application doit permettre la connexion à un contrôleur GRBL via port série/USB.
- **Critères d'acceptation**:
  - Détection automatique des ports disponibles
  - Configuration des paramètres de connexion (port, baud rate)
  - Indication claire de l'état de connexion
  - Récupération automatique en cas de déconnexion

#### 4.1.2 Configuration de la machine
- **Priorité**: Moyenne
- **Description**: L'application doit permettre la configuration des paramètres GRBL de la machine.
- **Critères d'acceptation**:
  - Interface pour visualiser et modifier les paramètres GRBL ($)
  - Sauvegarde et chargement des configurations
  - Validation des valeurs entrées
  - Préréglages pour les machines courantes

### 4.2 Visualisation et interface

#### 4.2.1 Grille de visualisation
- **Priorité**: Élevée
- **Description**: L'application doit afficher une grille graduée tous les 20mm avec l'origine (0,0) en haut à droite par défaut.
- **Critères d'acceptation**:
  - Grille X/Y graduée tous les 20mm
  - Origine (0,0) positionnée en haut à droite par défaut
  - Option pour modifier la position de l'origine
  - Affichage des coordonnées au survol

#### 4.2.2 Manipulation des images
- **Priorité**: Élevée
- **Description**: L'application doit permettre le déplacement et le zoom des images importées.
- **Critères d'acceptation**:
  - Déplacement fluide des images par glisser-déposer
  - Zoom avant/arrière avec la molette ou les boutons
  - Rotation des images
  - Redimensionnement proportionnel ou libre

#### 4.2.3 Prévisualisation du G-code
- **Priorité**: Moyenne
- **Description**: L'application doit afficher une prévisualisation du G-code sur la grille.
- **Critères d'acceptation**:
  - Rendu visuel des trajectoires G-code
  - Différenciation par couleur des types de mouvements
  - Estimation du temps d'exécution
  - Visualisation de la position actuelle de l'outil

### 4.3 Gestion des fichiers

#### 4.3.1 Importation de fichiers
- **Priorité**: Élevée
- **Description**: L'application doit permettre l'importation de fichiers G-code et d'images.
- **Critères d'acceptation**:
  - Support des formats G-code (.nc, .gcode, .cnc, etc.)
  - Support des formats d'image (.png, .jpg, .svg, etc.)
  - Glisser-déposer depuis le système de fichiers
  - Validation des fichiers importés

#### 4.3.2 Conversion d'images
- **Priorité**: Moyenne
- **Description**: L'application doit convertir les images en G-code pour la gravure.
- **Critères d'acceptation**:
  - Algorithmes de conversion (dithering, grayscale, vectorisation)
  - Paramètres ajustables (puissance, vitesse, résolution)
  - Prévisualisation du résultat
  - Optimisation du G-code généré

#### 4.3.3 Gestion de la bibliothèque
- **Priorité**: Basse
- **Description**: L'application doit permettre la gestion d'une bibliothèque de fichiers.
- **Critères d'acceptation**:
  - Sauvegarde des fichiers récents
  - Organisation en projets/dossiers
  - Métadonnées et tags
  - Recherche et filtrage

### 4.4 Contrôle de la machine

#### 4.4.1 Contrôle manuel (Jogging)
- **Priorité**: Élevée
- **Description**: L'application doit permettre le contrôle manuel des axes de la machine.
- **Critères d'acceptation**:
  - Contrôles directionnels (X, Y, Z)
  - Ajustement de la distance et de la vitesse
  - Boutons pour les opérations courantes (homing, reset)
  - Retour visuel sur la grille

#### 4.4.2 Exécution de G-code
- **Priorité**: Élevée
- **Description**: L'application doit permettre l'envoi et l'exécution de fichiers G-code.
- **Critères d'acceptation**:
  - Chargement et envoi de fichiers G-code
  - Contrôles de lecture (démarrer, pause, arrêter)
  - Indication de la progression et du temps restant
  - Gestion des erreurs pendant l'exécution

#### 4.4.3 Contrôle en temps réel
- **Priorité**: Moyenne
- **Description**: L'application doit permettre l'ajustement des paramètres pendant l'exécution.
- **Critères d'acceptation**:
  - Ajustement de la vitesse (feed rate override)
  - Ajustement de la puissance (pour les lasers)
  - Pause et reprise à un point spécifique
  - Visualisation en temps réel de la position

## 5. Exigences techniques

### 5.1 Architecture système

#### 5.1.1 Architecture générale
- **Frontend**: Application React JavaScript
- **Backend**: Serveur Python
- **Communication**: API REST et WebSockets
- **Stockage**: Système de fichiers local et base de données légère

#### 5.1.2 Diagramme d'architecture
```
+-------------------+      +-------------------+      +-------------------+
|                   |      |                   |      |                   |
|  Frontend React   |<---->|  Backend Python   |<---->|  Contrôleur GRBL  |
|                   |      |                   |      |                   |
+-------------------+      +-------------------+      +-------------------+
        ^                          ^
        |                          |
        v                          v
+-------------------+      +-------------------+
|                   |      |                   |
|  Stockage local   |      |  Base de données  |
|                   |      |                   |
+-------------------+      +-------------------+
```

### 5.2 Exigences frontend

#### 5.2.1 Technologies
- React.js pour l'interface utilisateur
- Canvas/WebGL pour la visualisation
- Redux/Context API pour la gestion d'état
- Styled Components/Tailwind CSS pour le styling

#### 5.2.2 Compatibilité navigateur
- Chrome (dernières 2 versions majeures)
- Firefox (dernières 2 versions majeures)
- Edge (dernières 2 versions majeures)
- Safari (dernières 2 versions majeures)

#### 5.2.3 Responsive design
- Support des écrans de bureau (1024px et plus)
- Adaptation basique pour tablettes (768px et plus)
- Interface simplifiée pour petits écrans si possible

### 5.3 Exigences backend

#### 5.3.1 Technologies
- Python 3.8+ pour le serveur
- Flask/FastAPI pour l'API REST
- PySerial pour la communication série
- Websockets pour les mises à jour en temps réel
- SQLite/TinyDB pour le stockage léger

#### 5.3.2 Communication matérielle
- Support du protocole GRBL 1.1+
- Gestion des buffers et du flux de données
- Détection et récupération d'erreurs
- Support des extensions GRBL courantes

#### 5.3.3 Performance
- Temps de réponse < 100ms pour les opérations standard
- Support de fichiers G-code jusqu'à 10MB
- Gestion efficace de la mémoire pour les grandes images
- Optimisation pour les systèmes à ressources limitées (Raspberry Pi)

### 5.4 Intégration et déploiement

#### 5.4.1 Packaging
- Application web autonome
- Option d'installation desktop via Electron
- Packages pour systèmes d'exploitation courants
- Conteneurisation Docker pour déploiement simplifié

#### 5.4.2 Mise à jour
- Vérification automatique des mises à jour
- Processus de mise à jour transparent
- Conservation des paramètres utilisateur
- Gestion des migrations de données

### 5.5 Modèle de données

#### 5.5.1 Entités principales
- **Machine**: Paramètres et configuration d'une machine
- **Fichier**: Métadonnées et chemin des fichiers G-code et images
- **Projet**: Regroupement de fichiers et paramètres
- **Paramètre**: Configurations utilisateur et préférences

#### 5.5.2 Schéma simplifié
```
Machine {
  id: string
  name: string
  port: string
  baudRate: number
  parameters: {key: value}
  workArea: {width: number, height: number}
}

File {
  id: string
  name: string
  path: string
  type: enum(GCODE, IMAGE, SVG)
  metadata: {key: value}
  createdAt: datetime
  modifiedAt: datetime
}

Project {
  id: string
  name: string
  description: string
  files: [FileId]
  settings: {key: value}
  createdAt: datetime
  modifiedAt: datetime
}

Setting {
  key: string
  value: any
  scope: enum(GLOBAL, PROJECT, MACHINE)
  parentId: string
}
```

## 6. Conception de l'interface utilisateur

### 6.1 Principes de conception

- **Simplicité**: Interface claire et intuitive, même pour les débutants
- **Flexibilité**: Options avancées disponibles mais non intrusives
- **Cohérence**: Éléments d'interface cohérents dans toute l'application
- **Feedback**: Retour visuel clair pour toutes les actions
- **Accessibilité**: Respect des standards d'accessibilité de base

### 6.2 Wireframes principaux

#### 6.2.1 Écran principal
```
+---------------------------------------------------------------+
|  Logo   [Connexion ▼]   [Fichier ▼]   [Outils ▼]   [Aide ▼]   |
+---------------------------------------------------------------+
|                                       |                       |
|                                       |  Contrôle Machine     |
|                                       |  +----------------+   |
|                                       |  | X+ Y+ Z+ |▲|▲|▲|   |
|                                       |  | X- Y- Z- |▼|▼|▼|   |
|                                       |  +----------------+   |
|                                       |                       |
|                                       |  État Machine         |
|                                       |  +----------------+   |
|     Zone de Visualisation             |  | Idle  X:0 Y:0 Z:0  |
|     avec Grille Graduée               |  +----------------+   |
|     (Origine en haut à droite)        |                       |
|                                       |  Fichier              |
|                                       |  +----------------+   |
|                                       |  | [Ouvrir] [Envoyer] |
|                                       |  | Progression: 0%    |
|                                       |  +----------------+   |
|                                       |                       |
+---------------------------------------------------------------+
|  Messages: Prêt                           [Réinitialiser]     |
+---------------------------------------------------------------+
```

#### 6.2.2 Écran d'importation d'image
```
+---------------------------------------------------------------+
|  [Retour]   Importation d'image                               |
+---------------------------------------------------------------+
|                                       |                       |
|                                       |  Paramètres           |
|                                       |  +----------------+   |
|                                       |  | Mode: [Grayscale▼] |
|                                       |  | Résolution: [▒▒▒▒] |
|                                       |  | Contraste:  [▒▒▒▒] |
|     Prévisualisation de l'image       |  | Luminosité: [▒▒▒▒] |
|     avec contrôles de                 |  +----------------+   |
|     déplacement et zoom               |                       |
|                                       |  Laser               |
|                                       |  +----------------+   |
|                                       |  | Puissance:  [▒▒▒▒] |
|                                       |  | Vitesse:    [▒▒▒▒] |
|                                       |  | Passes:     [▒▒▒▒] |
|                                       |  +----------------+   |
|                                       |                       |
+---------------------------------------------------------------+
|  [Annuler]                                      [Générer G-code] |
+---------------------------------------------------------------+
```

### 6.3 Flux utilisateur

#### 6.3.1 Connexion à une machine
1. L'utilisateur ouvre l'application
2. Il clique sur le menu "Connexion"
3. Il sélectionne un port série dans la liste ou configure manuellement
4. Il clique sur "Connecter"
5. L'application établit la connexion et affiche l'état de la machine
6. La grille de visualisation s'active avec l'origine en haut à droite

#### 6.3.2 Importation et positionnement d'une image
1. L'utilisateur clique sur "Fichier" > "Importer une image"
2. Il sélectionne une image sur son système
3. L'application affiche l'écran d'importation d'image
4. L'utilisateur ajuste les paramètres de conversion
5. Il utilise les contrôles pour déplacer et zoomer l'image
6. Il clique sur "Générer G-code"
7. L'application convertit l'image et affiche le G-code sur la grille
8. L'utilisateur peut encore ajuster la position avant de lancer la gravure

#### 6.3.3 Exécution d'un travail
1. L'utilisateur positionne la tête de la machine au point de départ
2. Il définit ce point comme origine de travail
3. Il clique sur "Envoyer" pour démarrer le travail
4. L'application affiche la progression et le temps estimé
5. L'utilisateur peut ajuster la vitesse ou la puissance pendant l'exécution
6. Une fois terminé, l'application affiche un message de confirmation

## 7. Plan de déploiement

### 7.1 Phases de développement

#### 7.1.1 Phase 1: MVP (2-3 mois)
- Interface de base avec grille graduée et origine en haut à droite
- Connexion et communication avec les contrôleurs GRBL
- Visualisation de G-code et contrôle manuel basique
- Importation et exécution de fichiers G-code

#### 7.1.2 Phase 2: Fonctionnalités avancées (2-3 mois)
- Manipulation avancée des images (déplacement, zoom)
- Conversion d'images en G-code
- Éditeur de G-code intégré
- Sauvegarde et gestion des paramètres

#### 7.1.3 Phase 3: Expansion et optimisation (3-4 mois)
- Support pour connexions réseau
- Fonctionnalités avancées de surveillance et contrôle
- Interface mobile/tablette
- Optimisations de performance et stabilité

### 7.2 Stratégie de lancement

#### 7.2.1 Alpha (interne)
- Tests avec un groupe restreint de développeurs
- Focus sur la stabilité et les fonctionnalités de base
- Correction des bugs critiques

#### 7.2.2 Beta (utilisateurs sélectionnés)
- Déploiement auprès d'un groupe d'utilisateurs tests
- Collecte de retours sur l'expérience utilisateur
- Ajustements basés sur les retours

#### 7.2.3 Release publique
- Publication sur GitHub et autres plateformes
- Documentation complète
- Tutoriels vidéo et guides de démarrage
- Mise en place d'un forum ou canal de support

### 7.3 Maintenance et évolution

#### 7.3.1 Mises à jour régulières
- Corrections de bugs (mensuel)
- Améliorations mineures (trimestriel)
- Nouvelles fonctionnalités (semestriel)

#### 7.3.2 Support communautaire
- Mise en place d'un système de suivi des problèmes (GitHub Issues)
- Documentation pour les contributeurs
- Processus de revue des contributions

## 8. Métriques de succès

### 8.1 Métriques d'adoption

- Nombre de téléchargements/installations
- Nombre d'utilisateurs actifs mensuels
- Taux de rétention après 1, 3 et 6 mois
- Nombre de machines connectées

### 8.2 Métriques de qualité

- Nombre de bugs signalés par version
- Temps moyen entre les plantages
- Taux de réussite des connexions
- Temps de réponse de l'interface

### 8.3 Métriques d'engagement

- Nombre de projets créés par utilisateur
- Temps moyen passé dans l'application
- Taux d'utilisation des fonctionnalités avancées
- Contributions à la communauté (code, documentation, support)

## 9. Annexes

### 9.1 Glossaire

- **GRBL**: Firmware open-source pour contrôler les mouvements des machines CNC
- **G-code**: Langage de programmation utilisé pour contrôler les machines CNC
- **Jogging**: Déplacement manuel des axes de la machine
- **Override**: Ajustement en temps réel des paramètres pendant l'exécution
- **Origine**: Point de référence (0,0) pour les coordonnées de la machine

### 9.2 Références

- Spécification GRBL: [https://github.com/gnea/grbl/wiki](https://github.com/gnea/grbl/wiki)
- Documentation React: [https://reactjs.org/docs/getting-started.html](https://reactjs.org/docs/getting-started.html)
- Documentation Python: [https://docs.python.org/3/](https://docs.python.org/3/)
- Étude de marché: [market_research.md](market_research.md)
- Concept principal: [core_concept.md](core_concept.md)
