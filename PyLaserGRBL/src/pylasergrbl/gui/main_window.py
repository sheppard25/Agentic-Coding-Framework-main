"""
Fenêtre principale de l'application PyLaserGRBL.
"""

import os
import sys
import json
from typing import Optional, Dict, Any, List, Tuple

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStatusBar, QTabWidget, QMessageBox, QFileDialog,
    QComboBox, QDoubleSpinBox, QGroupBox, QFormLayout, QSplitter,
    QToolBar, QDockWidget, QListWidget, QListWidgetItem, QMenu, QMenuBar,
    QTextEdit, QLineEdit, QTabWidget, QSizePolicy, QSpacerItem, QFrame,
    QPlainTextEdit
)
from PyQt6.QtCore import Qt, QSize, QTimer, QSettings, QPoint, QSizeF, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QKeySequence, QPixmap, QTextCursor, QColor
from PyQt6.QtWidgets import QApplication

from ..core.grbl_controller import GRBLController, GRBLStatus
from .visualization_widget import VisualizationWidget
from .control_panel import ControlPanel

# Chemins des icônes (à créer dans le dossier assets/icons/)
ICON_PLAY = "assets/icons/play.png"
ICON_PAUSE = "assets/icons/pause.png"
ICON_STOP = "assets/icons/stop.png"
ICON_CONNECT = "assets/icons/connect.png"
ICON_DISCONNECT = "assets/icons/disconnect.png"
ICON_EMERGENCY = "assets/icons/emergency.png"
ICON_HOME = "assets/icons/home.png"
ICON_OPEN = "assets/icons/open.png"
ICON_SAVE = "assets/icons/save.png"
ICON_SETTINGS = "assets/icons/settings.png"
ICON_ABOUT = "assets/icons/about.png"

class MainWindow(QMainWindow):
    """Classe principale de l'application PyLaserGRBL."""
    
    # Signaux
    update_status_signal = pyqtSignal()
    
    def __init__(self):
        """Initialise la fenêtre principale."""
        super().__init__()
        
        # Configuration de base de la fenêtre
        self.setWindowTitle("PyLaserGRBL")
        self.setMinimumSize(1024, 768)
        
        # Initialisation du contrôleur GRBL
        self.grbl = GRBLController()
        
        # Variables d'état
        self.connected = False
        self.current_file = None
        self.gcode_lines = []
        self.current_line = 0
        self.running = False
        self.paused = False
        
        # Configuration de la barre d'état
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Prêt")
        
        # Configuration des paramètres
        self.settings = QSettings("PyLaserGRBL", "PyLaserGRBL")
        
        # Initialisation de l'interface utilisateur
        self._init_ui()
        
        # Configuration des signaux
        self._setup_signals()
        
        # Charger les paramètres
        self._load_settings()
        
        # Démarrer la mise à jour du statut
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(250)  # Mise à jour 4 fois par seconde
        
        # Mettre à jour l'interface utilisateur
        self.update_ui_state()
    
    def _init_ui(self):
        """Initialise l'interface utilisateur."""
        # Création du widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Création du widget de visualisation
        self.visualization = VisualizationWidget()
        self.visualization.position_clicked.connect(self.on_position_clicked)
        
        # Création du panneau de contrôle
        self.control_panel = ControlPanel()
        self.control_panel.setMaximumWidth(300)
        
        # Configuration des signaux du panneau de contrôle
        self.control_panel.move_relative.connect(self.move_relative)
        self.control_panel.move_absolute.connect(self.move_absolute)
        self.control_panel.home_machine.connect(self.home_machine)
        self.control_panel.set_zero.connect(self.set_zero)
        self.control_panel.set_laser_power.connect(self.set_laser_power)
        self.control_panel.jog_start.connect(self.start_jogging)
        self.control_panel.jog_stop.connect(self.stop_jogging)
        
        # Ajout des widgets au layout principal
        main_layout.addWidget(self.visualization)
        main_layout.addWidget(self.control_panel)
        
        # Création des actions
        self._create_actions()
        
        # Création de la barre d'outils
        self._create_toolbar()
        
        # Création de la barre de menu
        self._create_menubar()
        
        # Création de la barre d'état
        self._create_statusbar()
        
        # Création du panneau de console
        self._create_console()
    
    def _setup_signals(self):
        """Configure les signaux de l'application."""
        # Connexion des signaux du contrôleur GRBL
        self.grbl.status_updated.connect(self.on_grbl_status_updated)
        self.grbl.error_occurred.connect(self.on_grbl_error)
        self.grbl.message_received.connect(self.on_grbl_message)
        
        # Connexion des signaux de l'interface utilisateur
        self.update_status_signal.connect(self.update_status_ui)
    
    def _create_actions(self):
        """Crée les actions utilisées dans les menus et la barre d'outils."""
        # Actions de fichier
        self.new_action = QAction(QIcon.fromTheme("document-new"), "&Nouveau", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.triggered.connect(self.new_file)
        
        self.open_action = QAction(QIcon.fromTheme("document-open"), "&Ouvrir...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self.open_file)
        
        self.save_action = QAction(QIcon.fromTheme("document-save"), "&Enregistrer", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.triggered.connect(self.save_file)
        
        self.save_as_action = QAction("Enregistrer &sous...", self)
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.save_as_action.triggered.connect(self.save_file_as)
        
        self.exit_action = QAction("&Quitter", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)
        
        # Actions d'édition
        self.undo_action = QAction(QIcon.fromTheme("edit-undo"), "&Annuler", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        
        self.redo_action = QAction(QIcon.fromTheme("edit-redo"), "&Rétablir", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        
        # Actions de contrôle
        self.about_action = QAction("À &propos...", self)
        self.about_action.triggered.connect(self.show_about)
        
        self.zoom_out_action = QAction("Zoom a&rrière", self)
        self.zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        
        self.fit_view_action = QAction("&Ajuster la vue", self)
        self.fit_view_action.triggered.connect(self.fit_view)
        
        # Actions de contrôle de machine
        self.connect_action = QAction("Se &connecter", self)
        self.connect_action.triggered.connect(self.toggle_connection)
        
        self.run_action = QAction("&Exécuter", self)
        self.run_action.setShortcut("F5")
        self.run_action.triggered.connect(self.run_program)
        
        self.pause_action = QAction("&Pause", self)
        self.pause_action.setShortcut("F6")
        self.pause_action.triggered.connect(self.pause_program)
        self.pause_action.setEnabled(False)
        
        self.stop_action = QAction("A&rrêter", self)
        self.stop_action.setShortcut("F7")
        self.stop_action.triggered.connect(self.stop_program)
        self.stop_action.setEnabled(False)
        
        # Action de réinitialisation du laser
        self.reset_laser_action = QAction("Réinitialiser le laser", self)
        self.reset_laser_action.setShortcut("F9")
        self.reset_laser_action.triggered.connect(self.reset_laser)
        self.reset_laser_action.setEnabled(False)
    
    def _create_toolbar(self):
        """Crée la barre d'outils principale."""
        # Barre d'outils principale
        self.toolbar = self.addToolBar("Outils")
        self.toolbar.setIconSize(QSize(24, 24))
        
        # Boutons de fichier
        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addSeparator()
        
        # Boutons d'édition
        self.toolbar.addAction(self.undo_action)
        self.toolbar.addAction(self.redo_action)
        self.toolbar.addSeparator()
        
        # Boutons de contrôle
        self.run_toolbar_action = QAction("Exécuter", self)
        self.run_toolbar_action.setIcon(QIcon(ICON_PLAY) if os.path.exists(ICON_PLAY) else QIcon())
        self.run_toolbar_action.triggered.connect(self.run_program)
        self.run_toolbar_action.setShortcut("F5")
        self.toolbar.addAction(self.run_toolbar_action)
        
        self.pause_toolbar_action = QAction("Pause", self)
        self.pause_toolbar_action.setIcon(QIcon(ICON_PAUSE) if os.path.exists(ICON_PAUSE) else QIcon())
        self.pause_toolbar_action.triggered.connect(self.pause_program)
        self.pause_toolbar_action.setShortcut("F6")
        self.pause_toolbar_action.setEnabled(False)
        self.toolbar.addAction(self.pause_toolbar_action)
        
        self.stop_toolbar_action = QAction("Arrêter", self)
        self.stop_toolbar_action.setIcon(QIcon(ICON_STOP) if os.path.exists(ICON_STOP) else QIcon())
        self.stop_toolbar_action.triggered.connect(self.stop_program)
        self.stop_toolbar_action.setShortcut("F7")
        self.stop_toolbar_action.setEnabled(False)
        self.toolbar.addAction(self.stop_toolbar_action)
        
        self.toolbar.addSeparator()
        
        # Bouton de connexion
        self.connect_toolbar_action = QAction("Se connecter", self)
        self.connect_toolbar_action.setIcon(QIcon(ICON_CONNECT) if os.path.exists(ICON_CONNECT) else QIcon())
        self.connect_toolbar_action.triggered.connect(self.toggle_connection)
        self.toolbar.addAction(self.connect_toolbar_action)
        
        # Bouton de configuration GRBL (nouveau)
        self.configure_grbl_action = QAction("Configurer GRBL", self)
        self.configure_grbl_action.triggered.connect(self.configure_grbl)
        self.configure_grbl_action.setEnabled(False)
        self.toolbar.addAction(self.configure_grbl_action)
        
        # Bouton d'arrêt d'urgence
        self.emergency_toolbar_action = QAction("Arrêt d'urgence", self)
        self.emergency_toolbar_action.setIcon(QIcon(ICON_EMERGENCY) if os.path.exists(ICON_EMERGENCY) else QIcon())
        self.emergency_toolbar_action.triggered.connect(self.emergency_stop)
        self.emergency_toolbar_action.setShortcut("Escape")
        self.toolbar.addAction(self.emergency_toolbar_action)
        
        # Bouton d'origine
        self.home_toolbar_action = QAction("Origine", self)
        self.home_toolbar_action.setIcon(QIcon(ICON_HOME) if os.path.exists(ICON_HOME) else QIcon())
        self.home_toolbar_action.triggered.connect(lambda: self.home_machine())
        self.toolbar.addAction(self.home_toolbar_action)
    
    def _create_menubar(self):
        """Crée la barre de menu de l'application."""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("&Fichier")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        # Menu Édition
        edit_menu = menubar.addMenu("&Édition")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        
        # Menu Affichage
        view_menu = menubar.addMenu("&Affichage")
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.fit_view_action)
        
        # Menu Contrôle
        control_menu = menubar.addMenu("&Contrôle")
        control_menu.addAction(self.connect_action)
        control_menu.addAction(self.configure_grbl_action)
        control_menu.addAction(self.reset_laser_action)
        control_menu.addSeparator()
        control_menu.addAction(self.run_action)
        control_menu.addAction(self.pause_action)
        control_menu.addAction(self.stop_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("&Aide")
        help_menu.addAction(self.about_action)
    
    def _create_statusbar(self):
        """Crée la barre d'état."""
        # Barre d'état déjà créée dans __init__
        pass
    
    def _create_console(self):
        """Crée le panneau de console."""
        # Créer un dock widget pour la console
        self.console_dock = QDockWidget("Console", self)
        self.console_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                                     QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        
        # Créer le widget de la console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFontFamily("Courier")
        self.max_console_lines = 1000  # Limiter le nombre de lignes
        
        # Ajouter la console au dock
        self.console_dock.setWidget(self.console)
        
        # Ajouter le dock en bas de la fenêtre
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.console_dock)
    
    def log_message(self, message: str, level: str = "info"):
        """Ajoute un message à la console.
        
        Args:
            message: Le message à afficher
            level: Niveau de sévérité ("info", "warning", "error")
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Définir la couleur en fonction du niveau
        if level == "error":
            color = "#ff4444"  # Rouge
            prefix = "[ERREUR]"
        elif level == "warning":
            color = "#ffaa00"  # Orange
            prefix = "[ATTENTION]"
        else:
            color = "#ffffff"  # Blanc
            prefix = "[INFO]"
        
        # Formater le message
        formatted_message = f"<span style='color:#888888'>[{timestamp}]</span> <span style='color:{color}'><b>{prefix}</b> {message}</span>"
        
        # Ajouter le message à la console
        self.console.append(formatted_message)
        
        # Limiter le nombre de lignes
        doc = self.console.document()
        if doc.blockCount() > self.max_console_lines:
            cursor = self.console.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.KeepAnchor, 
                               doc.blockCount() - self.max_console_lines)
            cursor.removeSelectedText()
        
        # Faire défiler vers le bas
        self.console.verticalScrollBar().setValue(
            self.console.verticalScrollBar().maximum()
        )
        
        # Afficher une notification dans la barre d'état si c'est une erreur
        if level == "error":
            self.statusBar.showMessage(f"Erreur: {message}", 5000)
        elif level == "warning":
            self.statusBar.showMessage(f"Attention: {message}", 3000)
    
    def update_status(self):
        """Met à jour le statut en récupérant les informations de GRBL et en mettant à jour l'interface."""
        # Ne rien faire si l'application est en train de se connecter/déconnecter
        if not hasattr(self, 'connected') or not self.connected:
            return
            
        # Essayer de récupérer le statut mais sans provoquer d'erreurs
        try:
            # Récupérer directement le statut GRBL sans utiliser les signaux
            if self.grbl and self.grbl.is_connected():
                try:
                    status = self.grbl.get_status()
                    if status:
                        # Mettre à jour l'interface directement sans utiliser les signaux
                        status_text = f"Connecté | État: {status.state} | Position: X{status.x:.1f} Y{status.y:.1f} Z{status.z:.1f}"
                        self.statusBar.showMessage(status_text)
                        
                        # Mettre à jour la visualisation
                        self.visualization.set_machine_position(status.x, status.y)
                        
                        # Mettre à jour les états des boutons
                        self._update_ui_from_status(status)
                except Exception as e:
                    # Ne pas générer d'erreur, juste logger
                    print(f"Erreur lors de l'update_status: {str(e)}")
        except Exception as e:
            # Capturer toutes les erreurs sans les propager
            print(f"Erreur globale dans update_status: {str(e)}")
            
    def update_status_ui(self):
        """DEPRECATED: Remplacé par des mises à jour directes."""
        pass  # Cette méthode est maintenant vide pour éviter les problèmes de récursion
    
    def _update_ui_from_status(self, status):
        """Met à jour l'interface utilisateur en fonction du statut de la machine."""
        # Mettre à jour l'état des boutons de contrôle
        self.run_action.setEnabled(not self.running and not self.paused)
        self.run_toolbar_action.setEnabled(not self.running and not self.paused)
        
        self.pause_action.setEnabled(self.running and not self.paused)
        self.pause_toolbar_action.setEnabled(self.running and not self.paused)
        
        self.stop_action.setEnabled(self.running or self.paused)
        self.stop_toolbar_action.setEnabled(self.running or self.paused)
        
        # Mettre à jour le texte des boutons de pause/reprise
        if self.paused:
            self.pause_action.setText("Reprendre")
            self.pause_toolbar_action.setText("Reprendre")
            if hasattr(self.pause_toolbar_action, 'setIcon') and os.path.exists(ICON_PLAY):
                self.pause_toolbar_action.setIcon(QIcon(ICON_PLAY))
        else:
            self.pause_action.setText("Pause")
            self.pause_toolbar_action.setText("Pause")
            if hasattr(self.pause_toolbar_action, 'setIcon') and os.path.exists(ICON_PAUSE):
                self.pause_toolbar_action.setIcon(QIcon(ICON_PAUSE))
    
    def toggle_connection(self):
        """Bascule l'état de connexion avec la machine."""
        if self.connected:
            self.disconnect_from_grbl()
        else:
            self.connect_to_grbl()
    
    def connect_to_grbl(self):
        """Établit la connexion avec le contrôleur GRBL."""
        # Simplifier la connexion pour éviter la récursion
        try:
            # Demander le port série si non spécifié
            ports = self.grbl.list_ports()
            if not ports:
                QMessageBox.critical(self, "Erreur", "Aucun port série disponible.")
                return False
            
            # Pour l'instant, on prend le premier port disponible
            # Dans une version future, on pourrait afficher une boîte de dialogue de sélection
            port = ports[0]['device']
            
            # Tenter la connexion sans utiliser les signaux
            if self.grbl.connect(port):
                self.connected = True
                # Mettre à jour l'interface
                self.connect_action.setText("Déconnexion")
                self.connect_toolbar_action.setText("Déconnexion")
                if hasattr(self.connect_toolbar_action, 'setIcon') and os.path.exists(ICON_DISCONNECT):
                    self.connect_toolbar_action.setIcon(QIcon(ICON_DISCONNECT))
                
                self.log_message(f"Connecté à {port}")
                
                # Activer les contrôles sans utiliser l'update_status
                self.control_panel.setEnabled(True)
                self.run_action.setEnabled(True)
                self.run_toolbar_action.setEnabled(True)
                self.configure_grbl_action.setEnabled(True)
                self.reset_laser_action.setEnabled(True)
                
                # Désactiver le timer d'update pendant l'initialisation
                was_active = False
                if hasattr(self, 'status_timer') and self.status_timer.isActive():
                    was_active = True
                    self.status_timer.stop()
                
                # Attendre un peu pour que la connexion se stabilise
                QApplication.processEvents()
                
                # Réactiver le timer si nécessaire
                if was_active:
                    self.status_timer.start(250)
                
                return True
            else:
                self.log_message(f"Échec de la connexion à {port}", "error")
                return False
                
        except Exception as e:
            self.log_message(f"Erreur de connexion: {str(e)}", "error")
            return False
            
    def disconnect_from_grbl(self):
        """Ferme la connexion avec le contrôleur GRBL."""
        # Arrêter le timer pour éviter les problèmes d'update pendant la déconnexion
        if hasattr(self, 'status_timer') and self.status_timer.isActive():
            self.status_timer.stop()
            
        # Déconnecter directement sans utiliser les signaux
        try:
            if self.grbl.serial_connection and self.grbl.serial_connection.is_open:
                # Envoyer un arrêt d'urgence avant de se déconnecter
                if self.grbl.is_connected():
                    try: 
                        self.grbl.serial_connection.write(bytes([0x18]))  # Ctrl-X
                        self.grbl.serial_connection.flush()
                    except:
                        pass
                # Fermer la connexion
                try:
                    self.grbl.serial_connection.close()
                except:
                    pass
                self.grbl.serial_connection = None
                
            self.connected = False
            
            # Mettre à jour l'interface
            self.connect_action.setText("Connexion")
            self.connect_toolbar_action.setText("Connexion")
            if hasattr(self.connect_toolbar_action, 'setIcon') and os.path.exists(ICON_CONNECT):
                self.connect_toolbar_action.setIcon(QIcon(ICON_CONNECT))
            
            self.log_message("Déconnecté")
            
            # Désactiver les contrôles sans utiliser l'update_status
            self.control_panel.setEnabled(False)
            self.run_action.setEnabled(False)
            self.run_toolbar_action.setEnabled(False)
            self.configure_grbl_action.setEnabled(False)
            self.reset_laser_action.setEnabled(False)
            
            # Réactiver le timer
            self.status_timer.start(250)
            
            return True
        except Exception as e:
            self.log_message(f"Erreur lors de la déconnexion: {str(e)}", "error")
            return False
    
    def emergency_stop(self):
        """Arrêt d'urgence de la machine."""
        if self.connected:
            if self.grbl.emergency_stop():
                self.log_message("Arrêt d'urgence effectué", "warning")
                self.running = False
                self.paused = False
                self._update_ui_from_status(None)
                return True
            else:
                self.log_message("Échec de l'arrêt d'urgence", "error")
                return False
        return False
    
    def home_machine(self):
        """Envoie la machine à la position d'origine."""
        if self.connected:
            self.log_message("Déplacement vers la position d'origine...")
            if self.grbl.home():
                self.log_message("Machine en position d'origine")
                return True
            else:
                self.log_message("Échec du déplacement vers la position d'origine", "error")
                return False
        return False
    
    def move_relative(self, x=None, y=None, z=None, feed_rate=None):
        """Déplace la machine de manière relative."""
        if self.connected:
            return self.grbl.move_relative(x, y, z, feed_rate)
        return False
    
    def move_absolute(self, x=None, y=None, z=None, feed_rate=None):
        """Déplace la machine de manière absolue."""
        if self.connected:
            return self.grbl.move_absolute(x, y, z, feed_rate)
        return False
    
    def set_zero(self, axes='XYZ'):
        """Définit la position actuelle comme origine pour les axes spécifiés."""
        if self.connected:
            return self.grbl.set_zero_position(axes)
        return False
    
    def set_laser_power(self, power):
        """Définit la puissance du laser (0-1000)."""
        if self.connected:
            return self.grbl.set_laser_power(power)
        return False
    
    def start_jogging(self, axis, direction, feed_rate=None):
        """Commence un déplacement continu (jogging)."""
        if self.connected:
            return self.grbl.start_jogging(axis, direction, feed_rate)
        return False
    
    def stop_jogging(self):
        """Arrête le déplacement continu (jogging)."""
        if self.connected:
            return self.grbl.stop_jogging()
        return False
    
    def run_program(self):
        """Démarre l'exécution du programme en cours."""
        if not self.connected:
            self.log_message("Non connecté à la machine", "error")
            return False
            
        if not self.gcode_lines:
            self.log_message("Aucun programme à exécuter", "warning")
            return False
            
        self.running = True
        self.paused = False
        self.current_line = 0
        
        self.log_message("Démarrage de l'exécution du programme...")
        self._update_ui_from_status(None)
        
        # Démarrer l'exécution
        self._execute_next_line()
        
        return True
    
    def pause_program(self):
        """Met en pause ou reprend l'exécution du programme."""
        if not self.connected:
            return False
            
        if not self.running:
            return False
            
        if self.paused:
            # Reprendre l'exécution
            self.paused = False
            self.log_message("Reprise de l'exécution")
            self._execute_next_line()
        else:
            # Mettre en pause
            self.paused = True
            self.log_message("Exécution en pause")
            
        self._update_ui_from_status(None)
        return True
    
    def stop_program(self):
        """Arrête l'exécution du programme."""
        if not self.connected:
            return False
            
        self.running = False
        self.paused = False
        self.current_line = 0
        
        self.log_message("Arrêt de l'exécution du programme")
        self._update_ui_from_status(None)
        
        # Envoyer une commande d'arrêt au contrôleur
        self.grbl.stop()
        
        return True
    
    def _execute_next_line(self):
        """Exécute la ligne de G-code suivante."""
        if not self.running or self.paused or not self.connected:
            return
            
        if self.current_line >= len(self.gcode_lines):
            # Fin du programme
            self.running = False
            self.log_message("Exécution terminée")
            self._update_ui_from_status(None)
            return
            
        # Récupérer la ligne de G-code
        line = self.gcode_lines[self.current_line].strip()
        self.current_line += 1
        
        # Ignorer les lignes vides et les commentaires
        if not line or line.startswith(';') or line.startswith('('):
            self._execute_next_line()
            return
            
        # Envoyer la commande GRBL
        self.log_message(f"Exécution: {line}")
        
        # Ici, nous pourrions ajouter une logique pour gérer la réponse
        # et passer à la ligne suivante une fois la commande terminée
        # Pour l'instant, nous utilisons un timer simple
        if self.grbl.send_command(line):
            QTimer.singleShot(100, self._execute_next_line)
        else:
            self.log_message(f"Erreur d'exécution: {line}", "error")
            self.stop_program()
    
    def on_position_clicked(self, x, y):
        """Appelé lorsque l'utilisateur clique sur la zone de visualisation."""
        if self.connected:
            # Déplacer la machine à la position cliquée
            self.log_message(f"Déplacement vers X{x:.2f} Y{y:.2f}")
            self.move_absolute(x, y)
    
    def on_grbl_status_updated(self, status):
        """Appelé lorsque le statut GRBL est mis à jour."""
        self.update_status_signal.emit()
    
    def on_grbl_error(self, error):
        """Appelé lorsqu'une erreur GRBL se produit."""
        self.log_message(f"Erreur GRBL: {error}", "error")
    
    def on_grbl_message(self, message):
        """Appelé lorsqu'un message est reçu du contrôleur GRBL."""
        self.log_message(f"GRBL: {message}")
    
    def zoom_in(self):
        """Zoom avant dans la visualisation."""
        self.visualization.zoom_in()
    
    def zoom_out(self):
        """Zoom arrière dans la visualisation."""
        self.visualization.zoom_out()
    
    def fit_view(self):
        """Ajuste la vue pour afficher toute la zone de travail."""
        self.visualization.fit_view()
    
    def new_file(self):
        """Crée un nouveau fichier."""
        if self.current_file or self.gcode_lines:
            reply = QMessageBox.question(
                self, 'Nouveau fichier',
                'Voulez-vous enregistrer les modifications ?',
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                return
                
            if reply == QMessageBox.StandardButton.Yes:
                if not self.save_file():
                    return
        
        self.current_file = None
        self.gcode_lines = []
        self.setWindowTitle("PyLaserGRBL - Nouveau fichier")
        self.log_message("Nouveau fichier créé")
    
    def open_file(self, filename=None):
        """Ouvre un fichier G-code."""
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Ouvrir un fichier G-code",
                "",
                "Fichiers G-code (*.nc *.gcode *.ngc);;Tous les fichiers (*)"
            )
            
            if not filename:
                return False
        
        try:
            with open(filename, 'r') as f:
                self.gcode_lines = f.readlines()
                
            self.current_file = filename
            self.setWindowTitle(f"PyLaserGRBL - {os.path.basename(filename)}")
            self.log_message(f"Fichier chargé: {filename}")
            
            # Analyser le G-code pour la visualisation
            self._parse_gcode_for_visualization()
            
            return True
            
        except Exception as e:
            self.log_message(f"Erreur lors de l'ouverture du fichier: {str(e)}", "error")
            return False
    
    def save_file(self):
        """Enregistre le fichier G-code actuel."""
        if not self.current_file:
            return self.save_file_as()
            
        try:
            with open(self.current_file, 'w') as f:
                f.writelines(self.gcode_lines)
                
            self.log_message(f"Fichier enregistré: {self.current_file}")
            return True
            
        except Exception as e:
            self.log_message(f"Erreur lors de l'enregistrement du fichier: {str(e)}", "error")
            return False
    
    def save_file_as(self):
        """Enregistre le fichier G-code actuel sous un nouveau nom."""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le fichier G-code",
            "",
            "Fichiers G-code (*.nc *.gcode *.ngc);;Tous les fichiers (*)"
        )
        
        if not filename:
            return False
            
        # Ajouter l'extension si nécessaire
        if not any(filename.lower().endswith(ext) for ext in ['.nc', '.gcode', '.ngc']):
            filename += ".gcode"
            
        self.current_file = filename
        return self.save_file()
    
    def _parse_gcode_for_visualization(self):
        """Analyse le G-code pour la visualisation."""
        # Cette méthode analyserait le G-code pour extraire les trajectoires
        # et les afficher dans le widget de visualisation
        # Pour l'instant, c'est une implémentation simplifiée
        self.visualization.clear_trajectory()
        
        # Ici, nous pourrions ajouter une analyse plus poussée du G-code
        # pour extraire les mouvements et les afficher
        
        self.visualization.update()
    
    def undo(self):
        """Annule la dernière action."""
        # À implémenter
        pass
    
    def redo(self):
        """Rétablit la dernière action annulée."""
        # À implémenter
        pass
    
    def show_about(self):
        """Affiche la boîte de dialogue À propos."""
        about_text = """
        <h3>PyLaserGRBL</h3>
        <p>Version 1.0.0</p>
        <p>Une interface graphique pour contrôler une machine à commande numérique GRBL.</p>
        <p>Développé avec Python et PyQt6.</p>
        <p>© 2023 - Tous droits réservés</p>
        """
        
        QMessageBox.about(self, "À propos de PyLaserGRBL", about_text)
    
    def closeEvent(self, event):
        """Gère la fermeture de l'application."""
        # Vérifier s'il y a des modifications non enregistrées
        if self.gcode_lines:
            reply = QMessageBox.question(
                self, 'Quitter',
                'Voulez-vous enregistrer les modifications avant de quitter ?',
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
                
            if reply == QMessageBox.StandardButton.Yes:
                if not self.save_file():
                    event.ignore()
                    return
        
        # Arrêter la machine si elle est en cours d'exécution
        if self.running or self.paused:
            self.stop_program()
        
        # Fermer la connexion série
        if self.connected:
            self.disconnect_from_grbl()
        
        # Sauvegarder les paramètres
        self._save_settings()
        
        # Accepter l'événement de fermeture
        event.accept()
    
    def _load_settings(self):
        """Charge les paramètres de l'application."""
        # Charger la géométrie de la fenêtre
        geometry = self.settings.value("window/geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)
        
        # Charger l'état de la fenêtre (dock widgets, etc.)
        state = self.settings.value("window/state")
        if state is not None:
            self.restoreState(state)
    
    def _save_settings(self):
        """Enregistre les paramètres de l'application."""
        # Sauvegarder la géométrie de la fenêtre
        self.settings.setValue("window/geometry", self.saveGeometry())
        
        # Sauvegarder l'état de la fenêtre (dock widgets, etc.)
        self.settings.setValue("window/state", self.saveState())

    def _update_ui_connection_state(self, is_connected):
        """Met à jour l'interface utilisateur en fonction de l'état de connexion."""
        # Activer/désactiver le panneau de contrôle
        self.control_panel.setEnabled(is_connected)
        
        # Activer/désactiver les boutons de contrôle
        self.run_action.setEnabled(is_connected and not self.running and not self.paused)
        self.run_toolbar_action.setEnabled(is_connected and not self.running and not self.paused)
        
        self.configure_grbl_action.setEnabled(is_connected)
        self.reset_laser_action.setEnabled(is_connected)
        
        # Mettre à jour le texte et l'icône du bouton de connexion
        if is_connected:
            self.connect_action.setText("Déconnexion")
            self.connect_toolbar_action.setText("Déconnexion")
            if hasattr(self.connect_toolbar_action, 'setIcon') and os.path.exists(ICON_DISCONNECT):
                self.connect_toolbar_action.setIcon(QIcon(ICON_DISCONNECT))
        else:
            self.connect_action.setText("Connexion")
            self.connect_toolbar_action.setText("Connexion")
            if hasattr(self.connect_toolbar_action, 'setIcon') and os.path.exists(ICON_CONNECT):
                self.connect_toolbar_action.setIcon(QIcon(ICON_CONNECT))

    def update_ui_state(self):
        """Met à jour l'état de l'interface utilisateur en fonction de l'état actuel de l'application."""
        # Mettre à jour les boutons en fonction de l'état de connexion
        self._update_ui_connection_state(self.connected)
        
        # Mettre à jour les boutons de contrôle en fonction de l'état du programme
        self.run_action.setEnabled(self.connected and not self.running and not self.paused)
        self.run_toolbar_action.setEnabled(self.connected and not self.running and not self.paused)
        
        self.pause_action.setEnabled(self.connected and self.running and not self.paused)
        self.pause_toolbar_action.setEnabled(self.connected and self.running and not self.paused)
        
        self.stop_action.setEnabled(self.connected and (self.running or self.paused))
        self.stop_toolbar_action.setEnabled(self.connected and (self.running or self.paused))
        
        # Mettre à jour les étiquettes de texte des boutons de pause/reprise
        if self.paused:
            self.pause_action.setText("Reprendre")
            self.pause_toolbar_action.setText("Reprendre")
            if hasattr(self.pause_toolbar_action, 'setIcon') and os.path.exists(ICON_PLAY):
                self.pause_toolbar_action.setIcon(QIcon(ICON_PLAY))
        else:
            self.pause_action.setText("Pause")
            self.pause_toolbar_action.setText("Pause")
            if hasattr(self.pause_toolbar_action, 'setIcon') and os.path.exists(ICON_PAUSE):
                self.pause_toolbar_action.setIcon(QIcon(ICON_PAUSE))
                
        # Mettre à jour l'état des boutons de connexion
        if self.connected:
            self.connect_action.setText("Déconnexion")
            self.connect_toolbar_action.setText("Déconnexion")
            if hasattr(self.connect_toolbar_action, 'setIcon') and os.path.exists(ICON_DISCONNECT):
                self.connect_toolbar_action.setIcon(QIcon(ICON_DISCONNECT))
        else:
            self.connect_action.setText("Connexion")
            self.connect_toolbar_action.setText("Connexion")
            if hasattr(self.connect_toolbar_action, 'setIcon') and os.path.exists(ICON_CONNECT):
                self.connect_toolbar_action.setIcon(QIcon(ICON_CONNECT))

    def configure_grbl(self):
        """Configure le contrôleur GRBL avec les paramètres de l'utilisateur."""
        if not self.connected:
            self.log_message("Veuillez vous connecter avant de configurer GRBL", "warning")
            return
            
        # Demander confirmation
        reply = QMessageBox.question(
            self, 'Configuration GRBL',
            'Voulez-vous configurer GRBL avec les paramètres spécifiques à votre machine ?\n'
            'Cette opération va réinitialiser et configurer le contrôleur.',
            QMessageBox.StandardButton.Yes | 
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.log_message("Début de la configuration GRBL...", "info")
            try:
                # Lancer la configuration
                self.grbl._configure_grbl()
                self.log_message("Configuration GRBL terminée avec succès", "info")
            except Exception as e:
                self.log_message(f"Erreur lors de la configuration GRBL: {str(e)}", "error")

    def reset_laser(self):
        """Réinitialise le laser avec les commandes standard."""
        if not self.connected:
            self.log_message("Non connecté à la machine", "error")
            return False
            
        try:
            # Séquence d'initialisation standard
            self.log_message("Réinitialisation du laser...", "info")
            
            # Commandes à envoyer
            commands = [
                "G21",         # Mode millimètres
                "G90",         # Mode absolu
                "M5",          # Laser off
                "M3 S0"        # Laser on mais puissance à 0
            ]
            
            # Envoyer les commandes
            for cmd in commands:
                response = self.grbl.send_command(cmd)
                self.log_message(f"Envoi: {cmd} -> {response}", "info")
                
            self.log_message("Réinitialisation terminée", "info")
            return True
            
        except Exception as e:
            self.log_message(f"Erreur lors de la réinitialisation: {str(e)}", "error")
            return False
