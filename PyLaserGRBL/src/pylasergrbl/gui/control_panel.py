"""
Panneau de contrôle pour les commandes manuelles de la machine.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QDoubleSpinBox, QGroupBox, QComboBox,
    QSizePolicy, QSpacerItem, QFrame, QSlider
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut

class ControlPanel(QWidget):
    """Panneau de contrôle pour les commandes manuelles."""
    
    # Signaux
    move_relative = pyqtSignal(float, float, float)  # dx, dy, dz
    move_absolute = pyqtSignal(float, float, float)  # x, y, z
    home_machine = pyqtSignal()
    set_zero = pyqtSignal(str)  # 'X', 'Y', 'Z', 'XY', 'XYZ', etc.
    set_laser_power = pyqtSignal(int)  # 0-1000
    jog_start = pyqtSignal(str, float)  # axis, feed_rate
    jog_stop = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialise le panneau de contrôle."""
        super().__init__(parent)
        
        # Variables
        self.jog_feed_rate = 1000  # mm/min
        self.jog_step = 1.0  # mm
        self.laser_power = 0  # 0-1000
        self.is_jogging = False
        self.current_jog_axis = None
        self.current_jog_direction = 0
        
        # Configuration de l'interface
        self._setup_ui()
        
        # Configuration des raccourcis clavier
        self._setup_shortcuts()
        
        # Configuration du minuteur de jogging
        self.jog_timer = QTimer(self)
        self.jog_timer.setInterval(50)  # 20 FPS
        self.jog_timer.timeout.connect(self._on_jog_timer)
    
    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        # Groupe de commandes de déplacement
        move_group = QGroupBox("Déplacement Manuel")
        move_layout = QVBoxLayout()
        
        # Sélecteur de pas de déplacement
        step_layout = QHBoxLayout()
        step_layout.addWidget(QLabel("Pas:"))
        
        self.step_selector = QComboBox()
        self.step_selector.addItems(["0.1 mm", "0.5 mm", "1.0 mm", "5.0 mm", "10.0 mm"])
        self.step_selector.setCurrentText("1.0 mm")
        self.step_selector.currentTextChanged.connect(self._on_step_changed)
        step_layout.addWidget(self.step_selector)
        
        move_layout.addLayout(step_layout)
        
        # Boutons de déplacement XY
        xy_layout = QHBoxLayout()
        
        # Espaceur à gauche
        xy_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Bouton Y+
        self.btn_y_plus = QPushButton("▲")
        self.btn_y_plus.setFixedSize(40, 40)
        self.btn_y_plus.pressed.connect(lambda: self._on_jog_button_pressed('Y', 1))
        self.btn_y_plus.released.connect(self._on_jog_button_released)
        xy_layout.addWidget(self.btn_y_plus)
        
        # Espaceur au centre
        xy_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        move_layout.addLayout(xy_layout)
        
        # Ligne des boutons X- et X+
        x_layout = QHBoxLayout()
        
        # Bouton X-
        self.btn_x_minus = QPushButton("◄")
        self.btn_x_minus.setFixedSize(40, 40)
        self.btn_x_minus.pressed.connect(lambda: self._on_jog_button_pressed('X', -1))
        self.btn_x_minus.released.connect(self._on_jog_button_released)
        x_layout.addWidget(self.btn_x_minus)
        
        # Bouton d'arrêt
        self.btn_stop = QPushButton("STOP")
        self.btn_stop.setFixedSize(40, 40)
        self.btn_stop.setStyleSheet("background-color: #ff4444; color: white; font-weight: bold;")
        self.btn_stop.clicked.connect(self._on_stop_clicked)
        x_layout.addWidget(self.btn_stop)
        
        # Bouton X+
        self.btn_x_plus = QPushButton("►")
        self.btn_x_plus.setFixedSize(40, 40)
        self.btn_x_plus.pressed.connect(lambda: self._on_jog_button_pressed('X', 1))
        self.btn_x_plus.released.connect(self._on_jog_button_released)
        x_layout.addWidget(self.btn_x_plus)
        
        move_layout.addLayout(x_layout)
        
        # Ligne du bouton Y-
        xy_layout = QHBoxLayout()
        
        # Espaceur à gauche
        xy_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Bouton Y-
        self.btn_y_minus = QPushButton("▼")
        self.btn_y_minus.setFixedSize(40, 40)
        self.btn_y_minus.pressed.connect(lambda: self._on_jog_button_pressed('Y', -1))
        self.btn_y_minus.released.connect(self._on_jog_button_released)
        xy_layout.addWidget(self.btn_y_minus)
        
        # Espaceur à droite
        xy_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        move_layout.addLayout(xy_layout)
        
        # Boutons Z
        z_layout = QHBoxLayout()
        
        # Bouton Z+
        self.btn_z_plus = QPushButton("Z+")
        self.btn_z_plus.setFixedSize(40, 30)
        self.btn_z_plus.pressed.connect(lambda: self._on_jog_button_pressed('Z', 1))
        self.btn_z_plus.released.connect(self._on_jog_button_released)
        z_layout.addWidget(self.btn_z_plus)
        
        # Bouton Z-
        self.btn_z_minus = QPushButton("Z-")
        self.btn_z_minus.setFixedSize(40, 30)
        self.btn_z_minus.pressed.connect(lambda: self._on_jog_button_pressed('Z', -1))
        self.btn_z_minus.released.connect(self._on_jog_button_released)
        z_layout.addWidget(self.btn_z_minus)
        
        move_layout.addLayout(z_layout)
        
        move_group.setLayout(move_layout)
        main_layout.addWidget(move_group)
        
        # Groupe de commandes de position
        pos_group = QGroupBox("Position")
        pos_layout = QVBoxLayout()
        
        # Boutons de mise à zéro
        zero_layout = QHBoxLayout()
        
        self.btn_zero_x = QPushButton("Zéro X")
        self.btn_zero_x.clicked.connect(lambda: self.set_zero.emit('X'))
        zero_layout.addWidget(self.btn_zero_x)
        
        self.btn_zero_y = QPushButton("Zéro Y")
        self.btn_zero_y.clicked.connect(lambda: self.set_zero.emit('Y'))
        zero_layout.addWidget(self.btn_zero_y)
        
        self.btn_zero_z = QPushButton("Zéro Z")
        self.btn_zero_z.clicked.connect(lambda: self.set_zero.emit('Z'))
        zero_layout.addWidget(self.btn_zero_z)
        
        self.btn_zero_all = QPushButton("Origine")
        self.btn_zero_all.clicked.connect(lambda: self.set_zero.emit('XYZ'))
        zero_layout.addWidget(self.btn_zero_all)
        
        pos_layout.addLayout(zero_layout)
        
        # Bouton d'initialisation (homing)
        self.btn_home = QPushButton("Initialiser la machine (Homing)")
        self.btn_home.clicked.connect(lambda: self.home_machine.emit())
        pos_layout.addWidget(self.btn_home)
        
        pos_group.setLayout(pos_layout)
        main_layout.addWidget(pos_group)
        
        # Groupe de commandes du laser
        laser_group = QGroupBox("Contrôle du Laser")
        laser_layout = QVBoxLayout()
        
        # Curseur de puissance
        power_layout = QHBoxLayout()
        power_layout.addWidget(QLabel("Puissance (0-1000):"))
        
        self.power_slider = QSlider(Qt.Orientation.Horizontal)
        self.power_slider.setMinimum(0)
        self.power_slider.setMaximum(1000)
        self.power_slider.setValue(0)
        self.power_slider.valueChanged.connect(self._on_laser_power_changed)
        power_layout.addWidget(self.power_slider)
        
        self.power_value = QLabel("0")
        self.power_value.setFixedWidth(40)
        power_layout.addWidget(self.power_value)
        
        laser_layout.addLayout(power_layout)
        
        # Boutons de contrôle du laser
        btn_layout = QHBoxLayout()
        
        self.btn_laser_on = QPushButton("Laser ON")
        self.btn_laser_on.setStyleSheet("background-color: #ff4444; color: white;")
        self.btn_laser_on.clicked.connect(lambda: self.set_laser_power.emit(self.laser_power))
        btn_layout.addWidget(self.btn_laser_on)
        
        self.btn_laser_off = QPushButton("Laser OFF")
        self.btn_laser_off.clicked.connect(lambda: self.set_laser_power.emit(0))
        btn_layout.addWidget(self.btn_laser_off)
        
        laser_layout.addLayout(btn_layout)
        laser_group.setLayout(laser_layout)
        main_layout.addWidget(laser_group)
        
        # Étirer l'espace vide en bas
        main_layout.addStretch()
    
    def _setup_shortcuts(self):
        """Configure les raccourcis clavier."""
        # Touches fléchées pour le déplacement XY
        QShortcut(QKeySequence("Left"), self, activated=lambda: self._on_jog_key_pressed('X', -1))
        QShortcut(QKeySequence("Right"), self, activated=lambda: self._on_jog_key_pressed('X', 1))
        QShortcut(QKeySequence("Up"), self, activated=lambda: self._on_jog_key_pressed('Y', 1))
        QShortcut(QKeySequence("Down"), self, activated=lambda: self._on_jog_key_pressed('Y', -1))
        
        # Touches PageUp/PageDown pour le déplacement Z
        QShortcut(QKeySequence("PageUp"), self, activated=lambda: self._on_jog_key_pressed('Z', 1))
        QShortcut(QKeySequence("PageDown"), self, activated=lambda: self._on_jog_key_pressed('Z', -1))
        
        # Touche d'arrêt
        QShortcut(QKeySequence("Space"), self, activated=self._on_stop_clicked)
        QShortcut(QKeySequence("Escape"), self, activated=self._on_stop_clicked)
        
        # Touche d'arrêt d'urgence (Ctrl+Espace)
        QShortcut(QKeySequence("Ctrl+Space"), self, activated=self._on_emergency_stop)
    
    def _on_step_changed(self, text):
        """Met à jour le pas de déplacement."""
        self.jog_step = float(text.split()[0])
    
    def _on_jog_button_pressed(self, axis, direction):
        """Déclenché lorsqu'un bouton de déplacement est enfoncé."""
        self.current_jog_axis = axis
        self.current_jog_direction = direction
        self._start_jogging()
    
    def _on_jog_button_released(self):
        """Déclenché lorsqu'un bouton de déplacement est relâché."""
        self._stop_jogging()
    
    def _on_jog_key_pressed(self, axis, direction):
        """Déclenché lorsqu'une touche de déplacement est pressée."""
        self.current_jog_axis = axis
        self.current_jog_direction = direction
        self._start_jogging()
    
    def _on_jog_key_released(self, event):
        """Déclenché lorsqu'une touche de déplacement est relâchée."""
        key = event.key()
        if key in (Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, 
                  Qt.Key.Key_Down, Qt.Key.Key_PageUp, Qt.Key.Key_PageDown):
            self._stop_jogging()
        else:
            super().keyReleaseEvent(event)
    
    def _start_jogging(self):
        """Démarre le déplacement continu."""
        if not self.is_jogging and self.current_jog_axis is not None:
            self.is_jogging = True
            self.jog_timer.start()
    
    def _stop_jogging(self):
        """Arrête le déplacement continu."""
        if self.is_jogging:
            self.is_jogging = False
            self.jog_timer.stop()
            self.jog_stop.emit()
    
    def _on_jog_timer(self):
        """Déclenché à intervalles réguliers pendant le déplacement."""
        if self.is_jogging and self.current_jog_axis is not None:
            distance = self.jog_step * self.current_jog_direction
            if self.current_jog_axis == 'X':
                self.move_relative.emit(distance, 0, 0)
            elif self.current_jog_axis == 'Y':
                self.move_relative.emit(0, distance, 0)
            elif self.current_jog_axis == 'Z':
                self.move_relative.emit(0, 0, distance)
    
    def _on_stop_clicked(self):
        """Arrête tous les mouvements en cours."""
        self._stop_jogging()
        # Émettre un signal d'arrêt (peut être utilisé pour arrêter d'autres mouvements)
        self.jog_stop.emit()
    
    def _on_emergency_stop(self):
        """Arrêt d'urgence."""
        self._stop_jogging()
        self.set_laser_power.emit(0)  # Éteindre le laser
        # Émettre un signal d'arrêt d'urgence
        self.jog_stop.emit()
    
    def _on_laser_power_changed(self, value):
        """Met à jour l'affichage de la puissance du laser."""
        self.laser_power = value
        self.power_value.setText(str(value))
    
    def keyPressEvent(self, event):
        """Gère les événements de touche pressée."""
        # La gestion des touches est déjà faite par les QShortcut
        # Cette méthode est surchargée pour éviter le comportement par défaut
        pass
    
    def keyReleaseEvent(self, event):
        """Gère les événements de touche relâchée."""
        # La gestion des touches est déjà faite par les QShortcut
        # Cette méthode est surchargée pour éviter le comportement par défaut
        pass
