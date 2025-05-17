# Spécification de l'API - ReactGRBL Controller

## 1. Introduction

Ce document décrit l'API REST et les protocoles de communication WebSocket pour l'application ReactGRBL Controller. L'API permet au frontend React de communiquer avec le backend Python pour contrôler les machines GRBL.

**URL de Base de l'API :** `/api/v1` (à confirmer/adapter selon la configuration du serveur backend)

**Authentification :** Pour la version initiale, aucune authentification complexe n'est requise. Des mécanismes d'authentification (par ex. JWT) pourront être ajoutés ultérieurement si nécessaire (voir PRD 5.7).

## 2. Conventions Générales

*   **Format des Données :** Toutes les requêtes et réponses utiliseront le format JSON.
*   **Codes de Statut HTTP :** Les codes de statut HTTP standard seront utilisés (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error, etc.).
*   **Gestion des Erreurs :** Les réponses d'erreur contiendront un objet JSON avec un champ `detail` expliquant l'erreur.
    ```json
    {
      "detail": "Description de l'erreur"
    }
    ```

## 3. API Endpoints REST

### 3.1. Gestion de la Connexion GRBL

*   **`POST /api/v1/grbl/connect`**
    *   Description : Établit une connexion avec le contrôleur GRBL.
    *   Requête (Body) :
        ```json
        {
          "port": "/dev/ttyUSB0", // ou "COM3" pour Windows
          "baudrate": 115200
        }
        ```
    *   Réponse (200 OK) :
        ```json
        {
          "status": "connected",
          "message": "Connecté avec succès à GRBL sur /dev/ttyUSB0."
        }
        ```
    *   Réponse (Erreur) : Code 400/500 avec détails.

*   **`POST /api/v1/grbl/disconnect`**
    *   Description : Ferme la connexion avec le contrôleur GRBL.
    *   Requête (Body) : Aucune.
    *   Réponse (200 OK) :
        ```json
        {
          "status": "disconnected",
          "message": "Déconnecté avec succès de GRBL."
        }
        ```

*   **`GET /api/v1/grbl/status`**
    *   Description : Récupère l'état actuel de la connexion et de la machine GRBL.
    *   Réponse (200 OK) :
        ```json
        {
          "connection_status": "connected" | "disconnected" | "connecting" | "error",
          "machine_status": "Idle" | "Run" | "Hold" | "Jog" | "Alarm" | "Door" | "Check" | "Home" | "Sleep", // États GRBL
          "current_position": { "x": 0.0, "y": 0.0, "z": 0.0 },
          "work_offset": { "x": 0.0, "y": 0.0, "z": 0.0 }
          // ... autres informations pertinentes
        }
        ```

### 3.2. Contrôle de la Machine

*   **`POST /api/v1/grbl/command`**
    *   Description : Envoie une commande G-code arbitraire à GRBL.
    *   Requête (Body) :
        ```json
        {
          "command": "G0 X10 Y10"
        }
        ```
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Commande envoyée.",
          "response_grbl": "ok" // ou la réponse de GRBL
        }
        ```

*   **`POST /api/v1/grbl/jog`**
    *   Description : Déplace la machine (jogging). (PRD 4.4.1)
    *   Requête (Body) :
        ```json
        {
          "axis": "X" | "Y" | "Z",
          "direction": 1 | -1, // 1 pour positif, -1 pour négatif
          "distance": 10.0, // en mm
          "feedrate": 500 // optionnel
        }
        ```
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Commande de jogging envoyée."
        }
        ```

*   **`POST /api/v1/grbl/home`**
    *   Description : Lance le cycle de homing de la machine.
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Cycle de Homing initié."
        }
        ```

*   **`POST /api/v1/grbl/unlock`**
    *   Description : Déverrouille GRBL (commande `$X`).
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Commande de déverrouillage envoyée."
        }
        ```

*   **`POST /api/v1/grbl/reset`**
    *   Description : Réinitialise GRBL (soft reset).
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Commande de réinitialisation envoyée."
        }
        ```

### 3.3. Gestion des Fichiers G-code

*   **`POST /api/v1/files/upload_gcode`**
    *   Description : Télécharge un fichier G-code sur le serveur. (PRD 4.3.1)
    *   Requête : `multipart/form-data` avec un champ `file`.
    *   Réponse (201 Created) :
        ```json
        {
          "filename": "mon_fichier.gcode",
          "size": 10240, // en bytes
          "message": "Fichier téléchargé avec succès."
        }
        ```

*   **`GET /api/v1/files/gcode`**
    *   Description : Liste les fichiers G-code disponibles.
    *   Réponse (200 OK) :
        ```json
        [
          { "filename": "mon_fichier.gcode", "size": 10240, "uploaded_at": "timestamp" },
          { "filename": "autre_fichier.nc", "size": 20480, "uploaded_at": "timestamp" }
        ]
        ```

*   **`GET /api/v1/files/gcode/{filename}`**
    *   Description : Récupère le contenu d'un fichier G-code spécifique ou sa prévisualisation.
    *   Paramètres de requête : `?preview=true` (optionnel, pour obtenir une prévisualisation des chemins)
    *   Réponse (200 OK - contenu) : Contenu texte du fichier G-code.
    *   Réponse (200 OK - preview) :
        ```json
        {
          "filename": "mon_fichier.gcode",
          "paths": [ /* ... structure de données pour les chemins ... */ ],
          "bounding_box": { "min_x": 0, "max_x": 100, "min_y": 0, "max_y": 50 }
        }
        ```

*   **`POST /api/v1/files/run_gcode/{filename}`**
    *   Description : Lance l'exécution d'un fichier G-code sur la machine. (PRD 4.4.2)
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Exécution de mon_fichier.gcode démarrée."
        }
        ```

*   **`POST /api/v1/files/stop_gcode`**
    *   Description : Arrête l'exécution en cours du G-code.
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Exécution arrêtée."
        }
        ```

*   **`POST /api/v1/files/pause_resume_gcode`**
    *   Description : Met en pause ou reprend l'exécution du G-code.
    *   Requête (Body) :
        ```json
        {
          "action": "pause" | "resume"
        }
        ```
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Exécution mise en pause/reprise."
        }
        ```

### 3.4. Conversion Image vers G-code (PRD 4.3.2)

*   **`POST /api/v1/files/upload_image`**
    *   Description : Télécharge une image (SVG, PNG, JPG, etc.) pour conversion.
    *   Requête : `multipart/form-data` avec un champ `file`.
    *   Réponse (201 Created) :
        ```json
        {
          "image_id": "unique_image_id", // ID temporaire pour l'image
          "filename": "mon_image.png",
          "message": "Image téléchargée, prête pour la configuration de la conversion."
        }
        ```

*   **`POST /api/v1/convert/image_to_gcode`**
    *   Description : Convertit une image précédemment téléchargée en G-code.
    *   Requête (Body) :
        ```json
        {
          "image_id": "unique_image_id",
          "conversion_params": {
            "scale": 1.0,
            "origin_x": 0,
            "origin_y": 0,
            "engraving_depth": 1.0,
            "feed_rate": 1000,
            "tool_diameter": 0.1
            // ... autres paramètres spécifiques à la conversion (noir et blanc, seuil, etc.)
          },
          "output_filename": "mon_image_convertie.gcode" // Optionnel
        }
        ```
    *   Réponse (200 OK) :
        ```json
        {
          "gcode_filename": "mon_image_convertie.gcode",
          "message": "Image convertie en G-code avec succès."
        }
        ```

### 3.5. Paramètres GRBL et Application

*   **`GET /api/v1/settings/grbl`**
    *   Description : Récupère les paramètres actuels de GRBL (ex: `$0`, `$1`, etc.).
    *   Réponse (200 OK) :
        ```json
        {
          "$0": 10,
          "$1": 25,
          // ... tous les paramètres GRBL
        }
        ```

*   **`POST /api/v1/settings/grbl`**
    *   Description : Modifie un ou plusieurs paramètres GRBL.
    *   Requête (Body) :
        ```json
        {
          "$0": 10,
          "$1": 25
          // ... paramètres à modifier
        }
        ```
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Paramètres GRBL mis à jour."
        }
        ```

*   **`GET /api/v1/settings/app`**
    *   Description : Récupère les paramètres de l'application (ex: unités, thèmes, etc.).
    *   Réponse (200 OK) :
        ```json
        {
          "units": "mm",
          "theme": "dark"
          // ...
        }
        ```

*   **`POST /api/v1/settings/app`**
    *   Description : Modifie les paramètres de l'application.
    *   Requête (Body) :
        ```json
        {
          "units": "inches"
          // ...
        }
        ```
    *   Réponse (200 OK) :
        ```json
        {
          "message": "Paramètres de l'application mis à jour."
        }
        ```

## 4. Communication WebSocket

Le canal WebSocket est utilisé pour la communication en temps réel entre le backend et le frontend.
**Endpoint WebSocket :** `/ws`

### 4.1. Messages du Serveur vers le Client

*   **Statut GRBL :**
    *   Description : Envoyé régulièrement ou lors d'un changement d'état.
    *   Message :
        ```json
        {
          "type": "grbl_status",
          "payload": {
            "machine_status": "Idle" | "Run" | "Alarm" | ...,
            "current_position": { "x": 0.0, "y": 0.0, "z": 0.0 },
            "work_offset": { "x": 0.0, "y": 0.0, "z": 0.0 },
            "feedrate_actual": 500,
            "spindle_actual": 10000
            // ...
          }
        }
        ```

*   **Logs/Console GRBL :**
    *   Description : Transmet les messages bruts de la console GRBL.
    *   Message :
        ```json
        {
          "type": "grbl_console_output",
          "payload": {
            "line": "ok" // ou "error:9" ou tout autre message de GRBL
          }
        }
        ```

*   **Progression de la Tâche G-code :**
    *   Description : Envoyé pendant l'exécution d'un fichier G-code.
    *   Message :
        ```json
        {
          "type": "gcode_progress",
          "payload": {
            "filename": "mon_fichier.gcode",
            "current_line": 150,
            "total_lines": 1000,
            "percentage": 15.0,
            "estimated_time_remaining": 3600 // en secondes
          }
        }
        ```

*   **Alertes/Erreurs :**
    *   Description : Pour les notifications importantes ou les erreurs non sollicitées.
    *   Message :
        ```json
        {
          "type": "alert",
          "payload": {
            "level": "error" | "warning" | "info",
            "message": "Description de l'alerte."
          }
        }
        ```

### 4.2. Messages du Client vers le Serveur (si nécessaire au-delà de REST)

*   *Initialement, la plupart des commandes client peuvent passer par REST. Cette section peut être développée si des interactions WebSocket initiées par le client sont identifiées comme plus appropriées pour certaines fonctionnalités (par exemple, un flux continu de commandes de jogging à faible latence).*

## 5. Modèles de Données Détaillés (Payloads)

*   *(Cette section peut être utilisée pour détailler davantage la structure des objets JSON complexes si nécessaire, par exemple, la structure des `conversion_params` pour la conversion d'image).*

---
*Ce document sera mis à jour au fur et à mesure de l'évolution de l'API.*