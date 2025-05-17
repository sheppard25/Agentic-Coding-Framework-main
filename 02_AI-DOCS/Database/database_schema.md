# Schéma de la Base de Données - ReactGRBL Controller

## 1. Introduction

Ce document décrit le schéma de la base de données pour l'application ReactGRBL Controller. La base de données sera utilisée pour stocker les configurations de la machine, les informations sur les projets, les fichiers G-code et les paramètres de l'application.
Conformément au PRD (section 5.5), une base de données légère comme SQLite ou TinyDB sera utilisée.

## 2. Diagramme Entité-Relation (ERD)

Le diagramme suivant illustre les principales entités et leurs relations.

```mermaid
erDiagram
    Machine {
        string id PK "Identifiant unique de la machine"
        string name "Nom donné à la machine par l'utilisateur"
        string port "Port série (ex: COM3, /dev/ttyUSB0)"
        int baudRate "Vitesse de communication (ex: 115200)"
        json parameters "Paramètres GRBL spécifiques à la machine (ex: $0-$N)"
        json workArea "Dimensions de la zone de travail (ex: {width: 300, height: 200, depth: 50})"
        boolean default "Indique si c'est la machine par défaut"
    }

    Project {
        string id PK "Identifiant unique du projet"
        string name "Nom du projet"
        string description "Description du projet"
        datetime createdAt "Date de création"
        datetime modifiedAt "Date de dernière modification"
        string machineId FK "ID de la machine associée (optionnel)"
        json lastKnownState "Dernier état connu de la grille, des fichiers ouverts, etc."
    }

    File {
        string id PK "Identifiant unique du fichier"
        string projectId FK "ID du projet auquel ce fichier appartient"
        string name "Nom original du fichier"
        string storedPath "Chemin de stockage du fichier sur le serveur"
        string type "Type de fichier (GCODE, IMAGE_SOURCE, GCODE_FROM_IMAGE)"
        json metadata "Métadonnées (ex: dimensions pour une image, temps d'usinage estimé pour G-code)"
        datetime createdAt "Date d'importation/création"
        json conversionParams "Paramètres utilisés pour la conversion image vers G-code (si applicable)"
    }

    Setting {
        string key PK "Clé unique du paramètre (ex: app.theme, app.units, grbl.default_feedrate)"
        string value "Valeur du paramètre (stockée en JSON string)"
        string scope "Portée du paramètre (APP, MACHINE, PROJECT)"
        string parentId "ID de l'entité parente (Machine ID ou Project ID si scope MACHINE ou PROJECT)"
    }

    Machine ||--o{ Setting : "a des paramètres spécifiques"
    Project ||--o{ File : "contient"
    Project ||--o{ Setting : "a des paramètres spécifiques"
    Machine ||--o{ Project : "peut être associée à"