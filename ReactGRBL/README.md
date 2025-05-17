# ReactGRBL Controller

Un contrôleur GRBL moderne avec interface React JavaScript et backend Python pour la communication avec le matériel.

## Fonctionnalités

- Interface utilisateur moderne et intuitive en React
- Grille X/Y graduée tous les 20mm avec origine en haut à droite
- Images déplaçables et zoomables
- Gestion complète du graveur (connexion, contrôle)
- Gestion des fichiers à graver
- Communication robuste avec le contrôleur GRBL via Python

## Prérequis

- Node.js (v14+)
- Python (v3.8+)
- Un contrôleur GRBL connecté via port série

## Installation et démarrage rapide

### Méthode simple (recommandée)

Utilisez le fichier batch fourni pour installer les dépendances et démarrer l'application en une seule étape :

```bash
start_app.bat
```

Ce script va :
1. Vérifier que Python et Node.js sont installés
2. Installer toutes les dépendances nécessaires
3. Démarrer le backend Python et le frontend React
4. Ouvrir l'application dans votre navigateur

### Démarrage rapide (sans installation des dépendances)

Si vous avez déjà installé toutes les dépendances et souhaitez simplement démarrer l'application :

```bash
run_app.bat
```

Ce script va uniquement démarrer le backend et le frontend sans réinstaller les dépendances.

### Installation manuelle

Si vous préférez démarrer les composants séparément :

#### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

#### Backend (Python)

```bash
cd backend
pip install -r requirements.txt
python run.py
```

## Utilisation

1. Démarrez le backend et le frontend
2. Ouvrez votre navigateur à l'adresse http://localhost:5173
3. Connectez-vous à votre contrôleur GRBL via l'interface
4. Importez vos fichiers G-code ou images
5. Utilisez la grille pour positionner vos fichiers
6. Contrôlez votre machine via l'interface

## Structure du projet

```
ReactGRBL/
├── frontend/               # Application React
│   ├── src/                # Code source
│   │   ├── components/     # Composants React
│   │   ├── App.jsx         # Composant principal
│   │   └── main.js         # Point d'entrée
│   ├── public/             # Fichiers statiques
│   └── package.json        # Dépendances
│
├── backend/                # Serveur Python
│   ├── app/                # Code source
│   │   ├── main.py         # Point d'entrée FastAPI
│   │   ├── grbl_controller.py # Communication avec GRBL
│   │   └── file_service.py # Gestion des fichiers
│   ├── data/               # Données (créé automatiquement)
│   │   ├── files/          # Fichiers téléchargés
│   │   ├── settings.json   # Paramètres utilisateur
│   │   └── files_index.json # Index des fichiers
│   ├── requirements.txt    # Dépendances Python
│   └── run.py              # Script de démarrage
│
└── README.md               # Documentation
```

## Personnalisation

### Grille et origine

Par défaut, la grille est graduée tous les 20mm et l'origine (0,0) est positionnée en haut à droite. Vous pouvez modifier ces paramètres dans l'onglet "Paramètres" de l'interface.

### Connexion au contrôleur

L'application détecte automatiquement les ports série disponibles. Sélectionnez le port approprié et la vitesse de communication (baud rate) pour vous connecter à votre contrôleur GRBL.

## Développement

### Frontend

Le frontend est développé avec React et utilise les technologies suivantes :
- React pour l'interface utilisateur
- Canvas pour la visualisation de la grille et du G-code
- Socket.io pour la communication en temps réel avec le backend

Pour lancer le serveur de développement avec rechargement à chaud :

```bash
cd frontend
npm run dev
```

### Backend

Le backend est développé avec Python et utilise les technologies suivantes :
- FastAPI pour l'API REST
- PySerial pour la communication avec le contrôleur GRBL
- WebSockets pour les mises à jour en temps réel

Pour lancer le serveur de développement avec rechargement à chaud :

```bash
cd backend
python run.py
```

## Dépannage

### Problèmes courants

#### Erreur "The JSX syntax extension is not currently enabled"

Si vous rencontrez cette erreur lors du démarrage du frontend, cela signifie que la configuration de Vite n'est pas correctement configurée pour traiter les fichiers JSX.

Solution :
1. Assurez-vous que le plugin React pour Vite est installé :
   ```bash
   cd frontend
   npm install @vitejs/plugin-react --save-dev
   ```

2. Vérifiez que le fichier `vite.config.js` existe et contient la configuration correcte :
   ```javascript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'

   export default defineConfig({
     plugins: [react()],
   })
   ```

3. Assurez-vous que les fichiers JSX ont l'extension `.jsx` et non `.js`

#### Erreur "Failed to resolve import 'react-dom/client'"

Si vous rencontrez cette erreur, cela signifie que les packages React et React DOM ne sont pas correctement installés.

Solution :
1. Installez React et React DOM :
   ```bash
   cd frontend
   npm install react react-dom
   ```

2. Vérifiez que ces dépendances sont correctement listées dans votre fichier `package.json` :
   ```json
   "dependencies": {
     "react": "^18.2.0",
     "react-dom": "^18.2.0",
     // autres dépendances...
   }
   ```

#### Le backend ne démarre pas

Si le backend Python ne démarre pas correctement, vérifiez les points suivants :

1. Python 3.8+ est installé et accessible dans le PATH
2. Toutes les dépendances sont installées :
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Les ports nécessaires (8000 pour le backend) ne sont pas déjà utilisés par d'autres applications

#### Problèmes de connexion au contrôleur GRBL

Si vous ne parvenez pas à vous connecter à votre contrôleur GRBL :

1. Vérifiez que le contrôleur est correctement branché et alimenté
2. Assurez-vous que le port série est correct (COM1, COM2, etc.)
3. Vérifiez que la vitesse de communication (baud rate) correspond à celle configurée sur votre contrôleur
4. Assurez-vous qu'aucun autre logiciel n'utilise déjà le port série

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
