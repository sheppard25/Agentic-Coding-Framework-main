#!/usr/bin/env python3
"""
Point d'entrée principal pour PyLaserGRBL.
Gère automatiquement le PYTHONPATH pour le développement local.
"""
import sys
import os
from pathlib import Path

# Ajouter le répertoire src au PYTHONPATH
project_root = Path(__file__).parent.absolute()
src_path = str(project_root / 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Afficher le PYTHONPATH pour le débogage
print(f"PYTHONPATH: {sys.path}")

# Vérifier si le package est installé
try:
    import pylasergrbl
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("\nEssayez d'installer le package en mode développement avec:")
    print(f"cd {project_root}")
    print("pip install -e .")
    sys.exit(1)

# Importer et exécuter le main
from pylasergrbl.main import main

if __name__ == "__main__":
    print("Démarrage de PyLaserGRBL...")
    try:
        main()
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {e}")
        import traceback
        traceback.print_exc()
        input("Appuyez sur Entrée pour quitter...")
