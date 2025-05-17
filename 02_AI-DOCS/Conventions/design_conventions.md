# Conventions de design et guide de style

## Vue d'ensemble

Ce document définit les conventions de design et les directives de style pour le projet ReactGRBL Controller, visant à créer une expérience utilisateur (UX) et une interface utilisateur (UI) de qualité professionnelle qui s'alignent avec les meilleures pratiques modernes. Suivre ces conventions assure la cohérence, l'intuitivité, l'élégance et une esthétique "pixel-perfect" dans toute l'application.

## I. Principes fondamentaux de l'excellent design UI/UX

### Clarté et simplicité

- **Spécificités du projet :** 
  - Interface épurée avec des contrôles clairement identifiables
  - Étiquettes explicites pour toutes les fonctionnalités
  - Regroupement logique des fonctionnalités connexes (contrôle de machine, gestion de fichiers, visualisation)
  - Utilisation d'icônes universellement reconnues avec des tooltips

### Cohérence

- **Spécificités du projet :**
  - Palette de couleurs uniforme dans toute l'application
  - Styles de boutons cohérents selon leur fonction (primaire, secondaire, danger)
  - Comportements d'interaction prévisibles (hover, focus, active)
  - Terminologie cohérente pour les concepts GRBL

### Contrôle utilisateur et prévisibilité

- **Spécificités du projet :**
  - Confirmation avant les actions destructives ou irréversibles
  - Option d'annulation pour les modifications de position ou de fichier
  - Chemins de sortie clairs pour toutes les opérations
  - Feedback visuel pour les opérations en cours

### Accessibilité et inclusivité (Principes WCAG POUR)

- **Spécificités du projet :**
  - Cible WCAG AA pour tous les éléments
  - Navigation complète au clavier, particulièrement importante pour les contrôles de machine
  - Attributs ARIA pour les composants personnalisés
  - Contraste suffisant pour la lisibilité dans différents environnements

### Hiérarchie visuelle

- **Spécificités du projet :**
  - Mise en évidence des contrôles critiques (arrêt d'urgence, pause)
  - Organisation visuelle claire avec la zone de visualisation comme élément central
  - Utilisation de la taille, couleur et espacement pour établir l'importance
  - Regroupement visuel des fonctionnalités connexes

### Feedback et prévention des erreurs

- **Spécificités du projet :**
  - Feedback visuel immédiat pour les actions utilisateur
  - Messages d'erreur clairs avec suggestions de résolution
  - Validation en temps réel des entrées utilisateur
  - Indicateurs d'état pour les opérations longues

### Efficacité

- **Spécificités du projet :**
  - Raccourcis clavier pour les opérations fréquentes
  - Préréglages et favoris pour les configurations courantes
  - Minimisation des clics pour les tâches fréquentes
  - Persistance des préférences utilisateur

### Équilibre esthétique et fonctionnel

- **Spécificités du projet :**
  - Design moderne et professionnel adapté à un outil technique
  - Esthétique industrielle/technique qui reflète la nature du produit
  - Priorité à la lisibilité et à la précision sur les effets visuels
  - Utilisation judicieuse des animations pour améliorer la compréhension

## II. Architecture de l'information et système de design

### Architecture de l'information (IA)

- **Organisation du contenu :**
  - Regroupement par fonction principale : Visualisation, Contrôle, Fichiers, Configuration
  - Navigation principale simple et directe
  - Structure hiérarchique claire avec maximum 2-3 niveaux de profondeur

- **Modèles de navigation :**
  - Barre de navigation principale en haut
  - Panneaux latéraux pour les contrôles et paramètres
  - Zone centrale pour la visualisation
  - Barre d'état en bas pour les informations système

- **Flux utilisateur :**
  - Flux principaux optimisés : connexion → chargement de fichier → positionnement → exécution
  - Minimisation des étapes pour les tâches courantes
  - Chemins clairs pour la récupération des erreurs

### Système de design

- **Configuration Tailwind CSS (`tailwind.config.js`) :**
  - **Couleurs :**
    - Primaire: `#2563eb` (bleu)
    - Secondaire: `#4f46e5` (indigo)
    - Accent: `#f59e0b` (ambre)
    - Palette neutre: 
      - Fond: `#f8fafc` (slate-50)
      - Texte: `#1e293b` (slate-800)
      - Bordures: `#cbd5e1` (slate-300)
    - Couleurs sémantiques:
      - Succès: `#10b981` (vert émeraude)
      - Erreur: `#ef4444` (rouge)
      - Avertissement: `#f59e0b` (ambre)
      - Information: `#3b82f6` (bleu)
  
  - **Typographie :**
    - Familles de polices:
      - Titres: `'Inter', sans-serif`
      - Corps: `'Inter', sans-serif`
      - Monospace (pour code/coordonnées): `'Roboto Mono', monospace`
    - Tailles de police:
      - h1: `text-2xl` (24px)
      - h2: `text-xl` (20px)
      - h3: `text-lg` (18px)
      - Corps: `text-base` (16px)
      - Petit: `text-sm` (14px)
      - Très petit: `text-xs` (12px)
    - Poids de police:
      - Léger: `font-light` (300)
      - Normal: `font-normal` (400)
      - Medium: `font-medium` (500)
      - Gras: `font-bold` (700)
    - Hauteurs de ligne:
      - Compact: `leading-tight` (1.25)
      - Normal: `leading-normal` (1.5)
      - Relâché: `leading-relaxed` (1.625)
  
  - **Échelle d'espacement :** Basée sur une unité de 4px (0.25rem dans Tailwind)
  
  - **Points de rupture :**
    - sm: 640px
    - md: 768px
    - lg: 1024px
    - xl: 1280px
    - 2xl: 1536px
  
  - **Rayons de bordure :**
    - Aucun: `rounded-none` (0px)
    - Petit: `rounded-sm` (2px)
    - Normal: `rounded` (4px)
    - Medium: `rounded-md` (6px)
    - Grand: `rounded-lg` (8px)
  
  - **Ombres :**
    - Légère: `shadow-sm`
    - Normale: `shadow`
    - Medium: `shadow-md`
    - Élevée: `shadow-lg`

- **Architecture des composants :**
  - **Composants UI principaux :**
    - Button (variantes: primary, secondary, danger, icon)
    - Input (variantes: text, number, select)
    - Card (variantes: standard, compact)
    - Modal (variantes: standard, confirmation)
    - Tabs (variantes: horizontal, vertical)
    - ControlPanel (pour les contrôles de machine)
    - VisualizationCanvas (pour la grille et le G-code)
    - FileManager (pour la gestion des fichiers)
    - StatusBar (pour les informations d'état)
    - Tooltip (pour l'aide contextuelle)
  
  - **Stratégie d'abstraction :**
    - Création de composants React qui encapsulent les classes Tailwind
    - Utilisation de props pour les variantes et états
    - Composition de composants pour des interfaces complexes
    - Utilisation de hooks personnalisés pour la logique réutilisable

- **CSS global (`global.css`) :**
  - **Styles de base :**
    - Reset CSS moderne
    - `box-sizing: border-box` pour tous les éléments
    - Styles de base pour les éléments HTML courants
  
  - **Chargement de polices personnalisées :**
    ```css
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap');
    ```

- **Thématisation (mode clair/sombre) :**
  - Support du mode sombre via les variantes `dark:` de Tailwind
  - Utilisation de variables CSS pour les valeurs de couleur
  - Détection automatique des préférences système avec option de remplacement manuel

## III. Raffinement et polish UI

### Micro-interactions et animations

- **Transitions de page :** Transitions subtiles entre les vues principales
- **Feedback des boutons :** Changements d'état visuels clairs (hover, active, focus)
- **Animations fonctionnelles :**
  - Animation de la position de l'outil en temps réel
  - Transitions fluides pour le zoom et le déplacement dans la visualisation
  - Indicateurs de progression pour les opérations longues
- **Timing et courbes :** 
  - Animations rapides (150-300ms) pour le feedback immédiat
  - Courbes d'accélération naturelles pour les mouvements

### Typographie

- **Hiérarchie claire :** Différenciation visuelle entre titres, corps et données
- **Lisibilité optimisée :** 
  - Taille de police minimum de 12px pour les informations critiques
  - Contraste élevé entre le texte et l'arrière-plan
  - Espacement adéquat entre les lignes et les paragraphes
- **Cohérence :** Utilisation cohérente des styles dans toute l'application

### Utilisation de la couleur

- **Palette fonctionnelle :** 
  - Couleurs primaires pour les actions principales
  - Couleurs sémantiques pour les états et notifications
  - Couleurs neutres pour l'interface générale
- **Accessibilité des couleurs :** 
  - Contraste WCAG AA minimum pour tout le texte
  - Ne pas utiliser la couleur comme seul indicateur d'information
- **Cohérence :** Application cohérente des couleurs selon leur signification

### Espacement et composition

- **Grille cohérente :** Utilisation d'une grille basée sur 4px pour tous les espacements
- **Hiérarchie par espacement :** 
  - Espacement plus grand entre les sections distinctes
  - Espacement plus petit entre les éléments liés
- **Respiration visuelle :** 
  - Marges adéquates autour des éléments principaux
  - Éviter la surcharge visuelle

### Iconographie

- **Style cohérent :** Utilisation d'un ensemble d'icônes unifié (Heroicons ou Material Icons)
- **Signification claire :** Icônes universellement reconnues ou accompagnées de texte
- **Taille et alignement :** 
  - Tailles standardisées (16px, 20px, 24px)
  - Alignement précis avec le texte et autres éléments

## IV. Accessibilité

### Navigation au clavier

- **Focus visible :** Indicateurs de focus clairs et visibles pour tous les éléments interactifs
- **Ordre de tabulation logique :** Parcours de focus qui suit la structure visuelle de la page
- **Raccourcis clavier :** Raccourcis pour les actions fréquentes, documentés et personnalisables

### Attributs ARIA

- **Rôles appropriés :** Utilisation correcte des rôles ARIA pour les composants personnalisés
- **États et propriétés :** Mise à jour dynamique des attributs ARIA en fonction de l'état
- **Labels et descriptions :** Étiquettes descriptives pour tous les contrôles

### HTML sémantique

- **Structure correcte :** Utilisation appropriée des éléments HTML5 (`<header>`, `<nav>`, `<main>`, etc.)
- **Formulaires accessibles :** Labels explicitement associés aux champs, groupement logique
- **Tableaux accessibles :** En-têtes de tableau appropriés, résumés si nécessaire

### Contraste des couleurs

- **Texte :** Ratio de contraste minimum de 4.5:1 pour le texte normal, 3:1 pour le grand texte
- **Éléments d'interface :** Contraste suffisant pour les contrôles et indicateurs
- **Vérification :** Tests réguliers avec des outils de vérification de contraste

### Texte alternatif pour les images

- **Alt text descriptif :** Descriptions significatives pour toutes les images informatives
- **Images décoratives :** Alt text vide pour les images purement décoratives
- **Icônes :** Texte alternatif ou labels pour les icônes fonctionnelles

## V. Responsive design

### Approche mobile-first

- **Design progressif :** Commencer par l'expérience mobile et enrichir pour les écrans plus grands
- **Contenu prioritaire :** Identifier et prioriser le contenu essentiel pour les petits écrans
- **Simplification :** Interfaces simplifiées pour les appareils mobiles

### Points de rupture et adaptations

- **Adaptations spécifiques :**
  - Mobile (<640px) : Interface simplifiée, contrôles empilés
  - Tablette (640px-1024px) : Disposition hybride, panneaux redimensionnés
  - Desktop (>1024px) : Expérience complète avec tous les panneaux visibles
- **Comportements responsifs :**
  - Menus hamburger sur petits écrans
  - Panneaux rétractables sur écrans moyens
  - Disposition flexible sur grands écrans

### Tests multi-appareils

- **Appareils cibles :** Tests sur smartphones, tablettes et ordinateurs de bureau
- **Orientation :** Vérification des dispositions en portrait et paysage
- **Navigateurs :** Tests sur Chrome, Firefox, Safari et Edge

## VI. Implémentation et processus

### Outils et ressources

- **Bibliothèques UI :** Utilisation de composants React personnalisés avec Tailwind CSS
- **Ressources graphiques :** Icônes SVG optimisées, illustrations minimalistes si nécessaire
- **Outils de test :** Tests d'accessibilité automatisés, tests de responsive design

### Revue et raffinement

- **Processus de revue :** Revue régulière du design par rapport aux standards établis
- **Feedback utilisateur :** Incorporation des retours utilisateurs dans les itérations de design
- **Raffinement continu :** Amélioration progressive basée sur l'utilisation réelle

## VII. Liste de vérification pour la revue de design

- **Principes fondamentaux :**
  - Le design est-il clair, simple et intuitif ?
  - La cohérence est-elle maintenue à travers tous les éléments et interactions ?
  - L'utilisateur a-t-il un contrôle adéquat et les résultats sont-ils prévisibles ?
  - Le design est-il accessible (conforme WCAG, navigable au clavier, contraste suffisant) ?
  - Y a-t-il une hiérarchie visuelle claire guidant l'utilisateur ?
  - Le feedback est-il fourni efficacement et les erreurs sont-elles prévenues/gérées avec élégance ?
  - Le design est-il efficace pour l'accomplissement des tâches ?
  - Y a-t-il un bon équilibre entre esthétique et fonctionnalité ?

- **Architecture de l'information :**
  - Le contenu est-il organisé logiquement ?
  - La navigation est-elle claire et intuitive ?
  - Les utilisateurs peuvent-ils facilement trouver ce dont ils ont besoin ?

- **Système de design et styling (Tailwind CSS) :**
  - Le design respecte-t-il la configuration Tailwind définie (couleurs, typographie, espacement, etc.) ?
  - Les composants sont-ils bien abstraits et réutilisables ?
  - Le CSS global est-il utilisé de manière appropriée et correctement intégré avec Tailwind ?

- **Polish UI :**
  - Les micro-interactions améliorent-elles l'UX sans être distrayantes ?
  - La typographie est-elle appliquée de manière cohérente et lisible ?
  - La couleur est-elle utilisée de manière intentionnelle et efficace ?
  - L'espacement (espace blanc) est-il bien géré pour améliorer la clarté et l'organisation ?
  - Les animations/transitions sont-elles fluides et significatives ?
  - L'iconographie est-elle cohérente et claire ?

- **Design responsive :**
  - Le design s'adapte-t-il correctement à tous les points de rupture spécifiés ?
  - L'expérience est-elle optimisée pour chaque taille d'écran ?
  - Les éléments interactifs sont-ils utilisables sur les appareils tactiles ?

---

*Ce document doit être revu et mis à jour régulièrement à mesure que le projet évolue.*
