"""
Widget pour la visualisation de la zone de travail et de la position de la machine.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPointF, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush, QFont, QFontMetrics
import numpy as np

class VisualizationWidget(QWidget):
    """Widget pour la visualisation de la zone de travail."""
    
    # Signaux
    position_clicked = pyqtSignal(float, float)  # Émis lorsque l'utilisateur clique sur la zone de visualisation
    
    def __init__(self, parent=None):
        """Initialise le widget de visualisation."""
        super().__init__(parent)
        
        # Configuration de base
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(400, 400)
        
        # Variables d'état
        self.machine_position = (0, 0)  # Position actuelle de la machine (mm)
        self.target_position = (0, 0)   # Position cible (mm)
        self.work_area = (290, 235)     # Taille de la zone de travail (mm) adaptée à la machine de l'utilisateur
        self.scale = 1.0               # Échelle de visualisation (pixels/mm)
        self.offset = (0, 0)            # Décalage de la vue (pixels)
        self.show_grid = True           # S'assurer que la grille est activée
        self.show_coordinates = True
        self.show_machine_position = True
        self.show_target_position = True
        self.show_trajectory = True
        self.trajectory = []            # Historique des positions
        self.max_trajectory_points = 1000
        
        # Configuration de l'origine (0,0 en haut à droite)
        self.origin_top_right = True
        
        # Couleurs - Augmenter encore plus le contraste
        self.background_color = QColor(15, 15, 15)        # Fond très sombre
        self.grid_color = QColor(140, 140, 140)           # Grille beaucoup plus claire
        self.axis_color = QColor(220, 220, 220)           # Axes presque blancs
        self.frame_color = QColor(180, 180, 255)          # Cadre bleu clair très visible
        self.machine_color = QColor(50, 255, 50)          # Position machine vert vif
        self.target_color = QColor(255, 50, 50)           # Position cible rouge vif
        self.trajectory_color = QColor(50, 50, 255, 220)  # Trajectoire bleue plus visible
        self.text_color = QColor(255, 255, 255)           # Texte blanc
        
        # Configuration du suivi de la souris
        self.setMouseTracking(True)
        self.dragging = False
        self.last_mouse_pos = None
        
        # Mise à jour périodique
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start(50)  # 20 FPS
        
        # Placer la position machine et la cible à l'origine (0,0) pour correspondre au point A
        self.set_machine_position(0, 0)
        self.set_target_position(0, 0)
    
    def set_machine_position(self, x: float, y: float):
        """Définit la position actuelle de la machine.
        
        Args:
            x: Position X en mm
            y: Position Y en mm
        """
        self.machine_position = (x, y)
        
        # Ajouter à l'historique des positions
        if len(self.trajectory) >= self.max_trajectory_points:
            self.trajectory.pop(0)
        self.trajectory.append((x, y))
    
    def set_target_position(self, x: float, y: float):
        """Définit la position cible de la machine.
        
        Args:
            x: Position X cible en mm
            y: Position Y cible en mm
        """
        self.target_position = (x, y)
    
    def set_work_area(self, width: float, height: float):
        """Définit la taille de la zone de travail.
        
        Args:
            width: Largeur en mm
            height: Hauteur en mm
        """
        self.work_area = (width, height)
        self.fit_view()
    
    def fit_view(self):
        """Ajuste la vue pour afficher toute la zone de travail."""
        if not self.work_area[0] or not self.work_area[1]:
            return
        
        # Dimension de la zone de visualisation
        view_width = self.width()
        view_height = self.height()
        
        # Calculer une échelle qui convient bien à la taille de la fenêtre
        available_width = view_width * 0.7  # Utiliser 70% de la largeur
        scale_x = available_width / self.work_area[0]
        scale_y = view_height / self.work_area[1]
        self.scale = min(scale_x, scale_y) * 0.75  # Échelle ajustée
        
        # Toujours utiliser l'origine en haut à droite
        self.origin_top_right = True
        
        # Mieux centrer la grille dans la zone visible et la remonter encore plus
        self.offset = (
            view_width * 0.35,  # Positionner plus à gauche
            view_height * 0.12   # Beaucoup plus haut (12% de la hauteur)
        )
        
        # Forcer une mise à jour pour appliquer les changements
        self.update()
    
    def mm_to_pixel(self, x: float, y: float) -> tuple:
        """Convertit des coordonnées machine (mm) en coordonnées écran (pixels)."""
        if self.origin_top_right:
            # Origine en haut à droite: X va vers la gauche, Y vers le bas
            px = self.offset[0] - x * self.scale
            py = self.offset[1] + y * self.scale
        else:
            # Configuration standard: X va vers la droite, Y vers le haut
            px = self.offset[0] + x * self.scale
            py = self.offset[1] - y * self.scale
        return (px, py)
    
    def pixel_to_mm(self, px: float, py: float) -> tuple:
        """Convertit des coordonnées écran (pixels) en coordonnées machine (mm)."""
        if self.origin_top_right:
            # Origine en haut à droite
            x = (self.offset[0] - px) / self.scale
            y = (py - self.offset[1]) / self.scale
        else:
            # Configuration standard
            x = (px - self.offset[0]) / self.scale
            y = (self.offset[1] - py) / self.scale
        return (x, y)
    
    def paintEvent(self, event):
        """Gère l'événement de peinture du widget."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fond
        painter.fillRect(self.rect(), self.background_color)
        
        # Dessiner le cadre de la zone de travail (en premier pour qu'il soit derrière les autres éléments)
        self._draw_work_area_frame(painter)
        
        # Ajuster la vue si nécessaire ou à chaque redimensionnement
        if not hasattr(self, '_view_initialized') or not self._view_initialized:
            self.fit_view()
            self._view_initialized = True
        
        # Récupérer les coordonnées du point A (coin supérieur droit)
        if self.origin_top_right:
            point_a = (0, 0)  # Dans le système de coordonnées avec origine en haut à droite
        else:
            point_a = (self.work_area[0], self.work_area[1])  # Dans le système standard
        
        # Sauvegarder l'état du peintre
        painter.save()
        
        # Définir la transformation
        if self.origin_top_right:
            # Origine en haut à droite
            painter.translate(self.offset[0], self.offset[1])
            painter.scale(-self.scale, self.scale)  # X inversé, Y standard
        else:
            # Configuration standard
            painter.translate(self.offset[0], self.offset[1])
            painter.scale(self.scale, -self.scale)  # X standard, Y inversé
        
        # Grille (dessiner en premier pour qu'elle soit sous les autres éléments)
        if self.show_grid:
            self._draw_grid(painter)
        
        # Trajectoire
        if self.show_trajectory and len(self.trajectory) > 1:
            self._draw_trajectory(painter)
        
        # Position cible - Forcer au point A
        if self.show_target_position:
            # Sauvegarder la position actuelle
            old_target = self.target_position
            # Définir la nouvelle position au point A
            self.target_position = point_a
            # Dessiner la cible
            self._draw_target_position(painter)
            # Restaurer la position d'origine
            self.target_position = old_target
        
        # Position de la machine - Forcer au point A
        if self.show_machine_position:
            # Sauvegarder la position actuelle
            old_machine = self.machine_position
            # Définir la nouvelle position au point A
            self.machine_position = point_a
            # Dessiner la position de la machine
            self._draw_machine_position(painter)
            # Restaurer la position d'origine
            self.machine_position = old_machine
        
        # Restaurer l'état du peintre
        painter.restore()
        
        # Temporairement commenter les règles pour mieux voir la grille avec les lettres
        # self._draw_rulers(painter)
        
        # Légendes et coordonnées
        if self.show_coordinates:
            self._draw_coordinates(painter)
    
    def _draw_rulers(self, painter):
        """Dessine les règles graduées après la transformation pour qu'elles soient visibles et lisibles."""
        # Définir la taille des graduations
        ruler_grid = 20  # Graduation des règles tous les 20mm
        
        # Configuration graphique
        painter.save()
        pen = QPen(self.axis_color, 1.5)
        painter.setPen(pen)
        font = QFont("Arial", 8)
        painter.setFont(font)
        
        # Calculer les positions des axes
        if self.origin_top_right:
            # Convertir les coordonnées pour l'origine (0,0) en haut à droite
            origin_x = self.mm_to_pixel(0, 0)[0]
            origin_y = self.mm_to_pixel(0, 0)[1]
            
            # Dessiner l'indicateur d'origine (0,0) bien visible
            painter.setPen(QPen(QColor(255, 180, 0), 2.0))  # Orange vif pour l'origine
            painter.drawText(QPointF(origin_x - 25, origin_y - 10), "0,0")
            painter.setPen(pen)  # Rétablir la couleur d'origine
            
            # Dessiner un point à l'origine
            painter.drawEllipse(QPointF(origin_x, origin_y), 3, 3)
            
            # Règle X (axe horizontal)
            x_position = -ruler_grid
            while x_position >= -self.work_area[0]:
                # Convertir la position en pixels
                pixel_x, pixel_y = self.mm_to_pixel(x_position, 0)
                
                # Dessiner la graduation (ligne verticale sur l'axe X)
                painter.drawLine(int(pixel_x), int(origin_y), int(pixel_x), int(origin_y + 5))
                
                # Ajouter le texte de la graduation (valeur absolue, à l'extérieur)
                text = str(abs(int(x_position)))
                painter.drawText(QPointF(pixel_x - 10, origin_y - 5), text)
                
                x_position -= ruler_grid
            
            # Règle Y (axe vertical) à droite avec 0 en haut
            # Utiliser directement l'origine comme point de départ pour l'axe Y
            right_axis_x = origin_x + 20  # Décaler légèrement à droite de l'origine
            
            y_position = 0  # Commencer à 0
            while y_position <= self.work_area[1]:
                # Convertir la position en pixels
                _, pixel_y = self.mm_to_pixel(0, y_position)
                
                # Dessiner la graduation (ligne horizontale sur l'axe Y)
                painter.drawLine(int(right_axis_x - 5), int(pixel_y), int(right_axis_x), int(pixel_y))
                
                # Ajouter le texte de la graduation (à droite)
                text = str(int(y_position))
                painter.drawText(QPointF(right_axis_x + 5, pixel_y + 4), text)
                
                y_position += ruler_grid
        else:
            # Configuration standard (origine en bas à gauche)
            # Code similaire pour l'origine standard si besoin
            pass
        
        painter.restore()
    
    def _draw_grid(self, painter):
        """Dessine la grille de la zone de travail."""
        width, height = self.work_area
        
        # Définir la taille des cellules de la grille (en mm)
        major_grid = 50  # Tous les 50mm
        minor_grid = 10  # Tous les 10mm
        
        # Dessiner la grille mineure avec une ligne plus visible
        pen = QPen(self.grid_color, 0.5, Qt.PenStyle.DotLine)  # Augmenter l'épaisseur de 0 à 0.5
        painter.setPen(pen)
        
        # Adapter les coordonnées selon la position de l'origine
        if self.origin_top_right:
            # Origine en haut à droite - X va de 0 à -width, Y va de 0 à height
            
            # Lignes verticales mineures
            x = 0
            while x >= -width:
                if x % major_grid != 0:  # Ne pas dessiner les lignes majeures ici
                    painter.drawLine(x, 0, x, height)
                x -= minor_grid
            
            # Lignes horizontales mineures
            y = 0
            while y <= height:
                if y % major_grid != 0:  # Ne pas dessiner les lignes majeures ici
                    painter.drawLine(0, y, -width, y)
                y += minor_grid
            
            # Dessiner la grille majeure avec une ligne plus visible
            pen = QPen(self.grid_color, 1.0, Qt.PenStyle.DashLine)  # Augmenter l'épaisseur à 1.0
            painter.setPen(pen)
            
            # Lignes verticales majeures
            x = 0
            while x >= -width:
                painter.drawLine(x, 0, x, height)
                x -= major_grid
            
            # Lignes horizontales majeures
            y = 0
            while y <= height:
                painter.drawLine(0, y, -width, y)
                y += major_grid
            
            # Axes
            pen = QPen(self.axis_color, 2.5)  # Augmenter l'épaisseur des axes à 2.5
            painter.setPen(pen)
            painter.drawLine(0, 0, -width, 0)  # Axe X (vers la gauche)
            painter.drawLine(0, 0, 0, height)  # Axe Y (vers le bas)
        else:
            # Configuration standard - X va de 0 à width, Y va de 0 à height
            
            # Lignes verticales mineures
            x = 0
            while x <= width:
                if x % major_grid != 0:  # Ne pas dessiner les lignes majeures ici
                    painter.drawLine(x, 0, x, height)
                x += minor_grid
            
            # Lignes horizontales mineures
            y = 0
            while y <= height:
                if y % major_grid != 0:  # Ne pas dessiner les lignes majeures ici
                    painter.drawLine(0, y, width, y)
                y += minor_grid
            
            # Dessiner la grille majeure avec une ligne plus visible
            pen = QPen(self.grid_color, 1.0, Qt.PenStyle.DashLine)  # Augmenter l'épaisseur à 1.0
            painter.setPen(pen)
            
            # Lignes verticales majeures
            x = 0
            while x <= width:
                painter.drawLine(x, 0, x, height)
                x += major_grid
            
            # Lignes horizontales majeures
            y = 0
            while y <= height:
                painter.drawLine(0, y, width, y)
                y += major_grid
            
            # Axes
            pen = QPen(self.axis_color, 2.5)  # Augmenter l'épaisseur des axes à 2.5
            painter.setPen(pen)
            painter.drawLine(0, 0, width, 0)  # Axe X
            painter.drawLine(0, 0, 0, height)  # Axe Y
    
    def _draw_machine_position(self, painter):
        """Dessine la position actuelle de la machine."""
        x, y = self.machine_position
        
        # Taille du repère de position (en mm)
        size = 5
        
        # Dessiner le cercle de position
        painter.save()
        painter.setPen(QPen(self.machine_color, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(x, y), size, size)
        
        # Dessiner les lignes de croix - Utiliser QPointF pour accepter des coordonnées flottantes
        painter.drawLine(QPointF(x - size, y), QPointF(x + size, y))
        painter.drawLine(QPointF(x, y - size), QPointF(x, y + size))
        
        # Dessiner le point central
        painter.setBrush(self.machine_color)
        painter.drawEllipse(QPointF(x, y), 1, 1)
        painter.restore()
    
    def _draw_target_position(self, painter):
        """Dessine la position cible de la machine."""
        x, y = self.target_position
        
        # Taille du repère de position (en mm)
        size = 5
        
        # Dessiner le X de la position cible
        painter.save()
        painter.setPen(QPen(self.target_color, 2))
        painter.drawLine(QPointF(x - size, y - size), QPointF(x + size, y + size))
        painter.drawLine(QPointF(x + size, y - size), QPointF(x - size, y + size))
        
        # Dessiner le point central
        painter.setBrush(self.target_color)
        painter.drawEllipse(QPointF(x, y), 1, 1)
        painter.restore()
    
    def _draw_trajectory(self, painter):
        """Dessine la trajectoire récente de la machine."""
        if len(self.trajectory) < 2:
            return
        
        path = QPainterPath()
        x, y = self.trajectory[0]
        path.moveTo(x, y)
        
        for point in self.trajectory[1:]:
            x, y = point
            path.lineTo(x, y)
        
        painter.save()
        painter.setPen(QPen(self.trajectory_color, 0.5))
        painter.drawPath(path)
        painter.restore()
    
    def _draw_coordinates(self, painter):
        """Affiche les coordonnées et les informations de la vue."""
        # Afficher la position du pointeur de la souris
        if hasattr(self, 'mouse_pos_mm'):
            x, y = self.mouse_pos_mm
            text = f"X: {x:.1f} mm  Y: {y:.1f} mm"
            
            # Calculer la taille du texte
            font = QFont("Arial", 8)
            metrics = QFontMetrics(font)
            text_rect = metrics.boundingRect(text)
            
            # Position du texte (en bas à droite)
            margin = 10
            text_x = self.width() - text_rect.width() - margin
            text_y = self.height() - margin
            
            # Dessiner le fond du texte
            bg_rect = text_rect.adjusted(-5, -2, 5, 2)
            bg_rect.moveTo(text_x - 5, text_y - text_rect.height() - 2)
            
            painter.save()
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(0, 0, 0, 180))
            painter.drawRoundedRect(bg_rect, 3, 3)
            
            # Dessiner le texte
            painter.setFont(font)
            painter.setPen(self.text_color)
            painter.drawText(text_x, text_y, text)
            painter.restore()
    
    def mousePressEvent(self, event):
        """Gère les événements de clic de souris."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Convertir la position du clic en coordonnées machine
            x, y = self.pixel_to_mm(event.position().x(), event.position().y())
            self.position_clicked.emit(x, y)
        elif event.button() == Qt.MouseButton.RightButton:
            # Commencer le déplacement de la vue
            self.dragging = True
            self.last_mouse_pos = event.position()
    
    def mouseReleaseEvent(self, event):
        """Gère les événements de relâchement de souris."""
        if event.button() == Qt.MouseButton.RightButton:
            self.dragging = False
    
    def mouseMoveEvent(self, event):
        """Gère les événements de déplacement de souris."""
        # Mettre à jour la position de la souris pour l'affichage des coordonnées
        self.mouse_pos_mm = self.pixel_to_mm(event.position().x(), event.position().y())
        
        # Gérer le déplacement de la vue avec le bouton droit de la souris
        if self.dragging and self.last_mouse_pos is not None:
            delta = event.position() - self.last_mouse_pos
            self.offset = (self.offset[0] + delta.x(), self.offset[1] + delta.y())
            self.last_mouse_pos = event.position()
            self.update()
    
    def wheelEvent(self, event):
        """Gère les événements de molette de souris pour le zoom."""
        # Position de la souris avant le zoom
        mouse_pos = event.position()
        old_mouse_mm = self.pixel_to_mm(mouse_pos.x(), mouse_pos.y())
        
        # Facteur de zoom
        zoom_factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        new_scale = self.scale * zoom_factor
        
        # Limiter le zoom
        min_scale = 0.1  # Zoom arrière maximal
        max_scale = 100.0  # Zoom avant maximal
        
        if min_scale <= new_scale <= max_scale:
            # Mettre à jour l'échelle
            old_scale = self.scale
            self.scale = new_scale
            
            # Ajuster le décalage pour zoomer vers le curseur
            mouse_pos_after_zoom = self.mm_to_pixel(*old_mouse_mm)
            self.offset = (
                self.offset[0] + (mouse_pos.x() - mouse_pos_after_zoom[0]) * (self.scale / old_scale),
                self.offset[1] + (mouse_pos.y() - mouse_pos_after_zoom[1]) * (self.scale / old_scale)
            )
            
            self.update()
    
    def resizeEvent(self, event):
        """Gère les événements de redimensionnement du widget."""
        # Réajuster la vue lorsque la taille du widget change
        self.fit_view()
        super().resizeEvent(event)
    
    def _draw_work_area_frame(self, painter):
        """Dessine un cadre autour de la zone de travail pour la rendre plus visible."""
        width, height = self.work_area
        
        # Convertir les coins de la zone de travail en pixels
        if self.origin_top_right:
            top_left = self.mm_to_pixel(-width, 0)
            top_right = self.mm_to_pixel(0, 0)
            bottom_left = self.mm_to_pixel(-width, height)
            bottom_right = self.mm_to_pixel(0, height)
        else:
            top_left = self.mm_to_pixel(0, height)
            top_right = self.mm_to_pixel(width, height)
            bottom_left = self.mm_to_pixel(0, 0)
            bottom_right = self.mm_to_pixel(width, 0)
        
        # Dessiner un rectangle plus visible autour de la zone de travail
        painter.save()
        pen = QPen(self.frame_color, 3)  # Ligne plus épaisse et couleur distinctive
        painter.setPen(pen)
        
        # Dessiner les lignes du cadre
        painter.drawLine(int(top_left[0]), int(top_left[1]), int(top_right[0]), int(top_right[1]))
        painter.drawLine(int(top_right[0]), int(top_right[1]), int(bottom_right[0]), int(bottom_right[1]))
        painter.drawLine(int(bottom_right[0]), int(bottom_right[1]), int(bottom_left[0]), int(bottom_left[1]))
        painter.drawLine(int(bottom_left[0]), int(bottom_left[1]), int(top_left[0]), int(top_left[1]))
        
        # Ajouter les lettres A, B, C, D aux coins
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Couleur contrastée pour les lettres
        painter.setPen(QPen(QColor(255, 255, 0), 2))  # Jaune
        
        # Placement des lettres avec un petit décalage pour éviter qu'elles soient exactement sur les coins
        margin = 15
        # A: coin supérieur gauche
        painter.drawText(QPointF(top_left[0] + margin, top_left[1] + margin), "A")
        # B: coin supérieur droit
        painter.drawText(QPointF(top_right[0] - margin * 2, top_right[1] + margin), "B")
        # C: coin inférieur droit
        painter.drawText(QPointF(bottom_right[0] - margin * 2, bottom_right[1] - margin), "C")
        # D: coin inférieur gauche
        painter.drawText(QPointF(bottom_left[0] + margin, bottom_left[1] - margin), "D")
        
        painter.restore()
