#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Point d'entrée principal de l'application PyLaserGRBL.
"""

import sys
from PyQt6.QtWidgets import QApplication
from pylasergrbl.gui.main_window import MainWindow

def main():
    """Fonction principale de l'application."""
    app = QApplication(sys.argv)
    app.setApplicationName("PyLaserGRBL")
    app.setApplicationVersion("0.1.0")
    
    # Création de la fenêtre principale
    main_window = MainWindow()
    main_window.show()
    
    # Exécution de l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
