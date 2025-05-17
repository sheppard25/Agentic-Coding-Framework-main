# PyLaserGRBL

Une interface moderne en Python pour le contrôle des graveurs laser utilisant le contrôleur GRBL.

## Fonctionnalités

- Connexion série au contrôleur GRBL
- Visualisation en temps réel de la zone de travail
- Téléversement et prévisualisation des fichiers G-code
- Contrôle manuel des axes (X, Y, Z)
- Gestion des paramètres GRBL
- Surveillance de l'état en temps réel

## Prérequis

- Python 3.9 ou supérieur
- PyQt6
- pyserial
- numpy
- matplotlib

## Installation

1. Clonez ce dépôt :
   ```
   git clone [URL_DU_DEPOT]
   cd PyLaserGRBL
   ```

2. Créez un environnement virtuel :
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Utilisation

```
python -m pylasergrbl.main
```

## Structure du projet

```
PyLaserGRBL/
├── src/
│   └── pylasergrbl/
│       ├── __init__.py
│       ├── main.py
│       ├── gui/          # Interface utilisateur
│       ├── core/         # Logique métier
│       └── utils/        # Utilitaires
├── tests/               # Tests automatisés
├── docs/                # Documentation
└── assets/              # Ressources graphiques
```

## Licence

MIT
