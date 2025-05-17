"""
Contrôleur pour la communication avec le contrôleur GRBL.
"""

import serial
import serial.tools.list_ports
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
import time
import re
from PyQt6.QtCore import QObject, pyqtSignal

@dataclass
class GRBLStatus:
    """Classe pour stocker l'état actuel de la machine GRBL."""
    state: str = "Disconnected"
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    feed_rate: float = 0.0
    spindle_speed: float = 0.0
    buffer_available: int = 0
    buffer_size: int = 128
    feed_override: int = 100
    spindle_override: int = 100
    rapid_override: int = 100

class GRBLController(QObject):
    """Classe pour gérer la communication avec un contrôleur GRBL."""
    
    # Signaux PyQt
    status_updated = pyqtSignal(GRBLStatus)
    error_occurred = pyqtSignal(str)
    message_received = pyqtSignal(str)
    
    def __init__(self):
        """Initialise le contrôleur GRBL sans connexion active."""
        super().__init__()
        self.serial_connection = None
        self.status = GRBLStatus()
        self.last_error = None
        self._is_streaming = False
        self._streaming_paused = False
        self._streaming_queue = []
    
    def list_ports(self) -> List[Dict]:
        """Liste les ports série disponibles.
        
        Returns:
            List[Dict]: Liste des ports avec leurs informations
        """
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'name': port.name,
                'description': port.description,
                'hwid': port.hwid,
                'vid': port.vid,
                'pid': port.pid,
                'serial_number': port.serial_number,
                'manufacturer': port.manufacturer,
                'product': port.product,
                'interface': port.interface,
            })
        return ports
    
    def connect(self, port: str, baudrate: int = 115200) -> bool:
        """Établit une connexion avec le contrôleur GRBL.
        
        Args:
            port: Le port série à utiliser (ex: 'COM3')
            baudrate: La vitesse de communication en bauds (par défaut: 115200)
            
        Returns:
            bool: True si la connexion a réussi, False sinon
        """
        try:
            # Fermer d'abord toute connexion existante
            if self.serial_connection and self.serial_connection.is_open:
                try:
                    # Pas d'appel à disconnect() pour éviter la récursion
                    self.send_immediate(0x18)  # Ctrl-X pour arrêt d'urgence
                    self.serial_connection.close()
                    self.serial_connection = None
                    time.sleep(1)
                except:
                    pass
            
            # Ouvrir une nouvelle connexion
            # Ne pas utiliser message_received pour éviter des problèmes de signaux
            print(f"Tentative de connexion à {port} à {baudrate} bauds...")
            
            self.serial_connection = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=2.0,  # Timeout plus long
                xonxoff=False,
                rtscts=False,
                dsrdtr=False,
                write_timeout=2.0  # Timeout d'écriture
            )
            
            # Attendre que la connexion soit établie et stable
            time.sleep(2)  # Réduire légèrement le délai pour éviter les blocages
            
            # Vider les buffers
            self.serial_connection.reset_input_buffer()
            self.serial_connection.reset_output_buffer()
            
            # Envoyer un retour à la ligne pour réveiller GRBL
            self.serial_connection.write(b'\r\n')
            time.sleep(0.5)
            
            # Réinitialiser GRBL
            self.serial_connection.write(bytes([0x18]))  # Ctrl-X directly, not using send_immediate
            self.serial_connection.flush()
            time.sleep(1)
            
            # Lecture simple du buffer pour vider les messages initiaux
            self.serial_connection.timeout = 0.5
            welcome_buffer = b''
            try:
                while self.serial_connection.in_waiting > 0:
                    welcome_buffer += self.serial_connection.read(self.serial_connection.in_waiting)
                    time.sleep(0.1)
            except:
                # Ignorer les erreurs de lecture
                pass
                
            if welcome_buffer:
                print(f"Réponse de la machine: {welcome_buffer.decode('utf-8', errors='ignore')}")
            
            # Même sans confirmation Grbl, essayons de continuer
            self.status.state = "Connected"
            
            # Ne pas configurer GRBL tout de suite, laissons l'utilisateur le faire manuellement
            # self._configure_grbl()
            
            # Mettre à jour le statut
            self.status.state = "Idle"
            return True
            
        except Exception as e:
            self.last_error = str(e)
            print(f"Erreur de connexion: {str(e)}")
            if self.serial_connection and self.serial_connection.is_open:
                try:
                    self.serial_connection.close()
                except:
                    pass
            self.serial_connection = None
            return False
    
    def disconnect(self):
        """Ferme la connexion série."""
        if self.serial_connection and self.serial_connection.is_open:
            try:
                # Envoyer un arrêt d'urgence avant de se déconnecter
                self.send_immediate(0x18)  # Ctrl-X
                self.serial_connection.close()
            except:
                pass
        self.serial_connection = None
        self.status.state = "Disconnected"
    
    def is_connected(self) -> bool:
        """Vérifie si la connexion est active.
        
        Returns:
            bool: True si connecté, False sinon
        """
        return self.serial_connection is not None and self.serial_connection.is_open
    
    def send_command(self, command: str, timeout: float = 1.0) -> str:
        """Envoie une commande GRBL et attend la réponse.
        
        Args:
            command: La commande à envoyer (sans le retour à la ligne)
            timeout: Délai d'attente maximal en secondes
            
        Returns:
            str: La réponse reçue
        """
        if not self.is_connected():
            error_msg = "Non connecté à un contrôleur GRBL"
            self.error_occurred.emit(error_msg)
            raise RuntimeError(error_msg)
        
        # Ajouter le retour à la ligne si nécessaire
        if not command.endswith('\n'):
            command += '\n'
        
        # Envoyer la commande
        self.serial_connection.write(command.encode('utf-8'))
        self.serial_connection.flush()
        
        # Notifier de la commande envoyée
        self.message_received.emit(f"Commande envoyée: {command.strip()}")
        
        # Attendre et lire la réponse
        response = ""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.serial_connection.in_waiting > 0:
                response += self.serial_connection.read(self.serial_connection.in_waiting).decode('utf-8')
                if 'ok\r\n' in response or 'error:' in response.lower():
                    break
            time.sleep(0.01)
        
        # Notifier de la réponse reçue
        if "error:" in response.lower():
            self.error_occurred.emit(response.strip())
        else:
            self.message_received.emit(f"Réponse: {response.strip()}")
        
        return response.strip()
    
    def send_immediate(self, command: str) -> None:
        """Envoie une commande immédiate (sans attendre de réponse)."""
        if not self.is_connected():
            return
        
        if isinstance(command, int):  # Pour les commandes de contrôle (comme Ctrl-X)
            self.serial_connection.write(bytes([command]))
        else:
            if not command.endswith('\n'):
                command += '\n'
            self.serial_connection.write(command.encode('utf-8'))
        self.serial_connection.flush()
    
    def get_status(self) -> GRBLStatus:
        """Demande et met à jour l'état actuel de la machine.
        
        Returns:
            GRBLStatus: L'état actuel de la machine
        """
        if not self.is_connected():
            self.status.state = "Disconnected"
            return self.status
        
        try:
            # Envoyer la commande de statut
            self.serial_connection.write(b'?\n')
            self.serial_connection.flush()
            
            # Lire la réponse
            response = b''
            start_time = time.time()
            
            while time.time() - start_time < 0.5:  # Timeout de 500ms
                if self.serial_connection.in_waiting > 0:
                    response += self.serial_connection.read(self.serial_connection.in_waiting)
                    if b'<' in response and b'>' in response:
                        break
                time.sleep(0.01)
            
            # Parser la réponse
            self._parse_status(response.decode('utf-8').strip())
            
        except Exception as e:
            self.last_error = str(e)
            self.status.state = "Error"
            self.error_occurred.emit(f"Erreur lors de la récupération du statut: {str(e)}")
        
        return self.status
    
    def _parse_status(self, status_str: str) -> None:
        """Analyse la chaîne de statut GRBL et met à jour l'état interne.
        
        Args:
            status_str: La chaîne de statut au format GRBL
        """
        if not status_str or '<' not in status_str or '>' not in status_str:
            return
        
        # Extraire le contenu entre < et >
        content = status_str[status_str.find('<')+1:status_str.find('>')]
        
        # Mettre à jour l'état
        state_match = re.search(r'^([A-Za-z]+)', content)
        if state_match:
            self.status.state = state_match.group(1)
        
        # Mettre à jour la position
        pos_match = re.search(r'MPos:([\d.-]+),([\d.-]+)(?:,([\d.-]+))?', content)
        if pos_match:
            try:
                self.status.x = float(pos_match.group(1))
                self.status.y = float(pos_match.group(2))
                if pos_match.group(3):
                    self.status.z = float(pos_match.group(3))
            except (ValueError, AttributeError):
                pass
        
        # Mettre à jour la vitesse de déplacement
        feed_match = re.search(r'F:([\d.]+)', content)
        if feed_match:
            try:
                self.status.feed_rate = float(feed_match.group(1))
            except (ValueError, AttributeError):
                pass
        
        # Mettre à jour la vitesse de la broche
        spindle_match = re.search(r'S:([\d.]+)', content)
        if spindle_match:
            try:
                self.status.spindle_speed = float(spindle_match.group(1))
            except (ValueError, AttributeError):
                pass
        
        # Mettre à jour l'état du buffer
        buf_match = re.search(r'Bf:([\d]+),([\d]+)', content)
        if buf_match:
            try:
                self.status.buffer_available = int(buf_match.group(1))
                self.status.buffer_size = int(buf_match.group(2))
            except (ValueError, AttributeError):
                pass
        
        # Mettre à jour les surcharges
        ov_match = re.search(r'FS:([\d.]+),([\d.]+)', content)
        if ov_match:
            try:
                self.status.feed_override = int(ov_match.group(1))
                self.status.spindle_override = int(ov_match.group(2))
            except (ValueError, AttributeError):
                pass
        
        # Notifier les gestionnaires d'événements de statut
        self.status_updated.emit(self.status)
    
    def _configure_grbl(self):
        """Configure les paramètres GRBL spécifiques à la machine de l'utilisateur."""
        if not self.is_connected():
            return
            
        print("Début de la configuration GRBL...")
        
        try:
            # Réinitialiser GRBL
            self.serial_connection.write(bytes([0x18]))  # Ctrl-X
            self.serial_connection.flush()
            time.sleep(2)  # Donner du temps pour la réinitialisation
            
            # Vider le buffer de réception
            self.serial_connection.reset_input_buffer()
            
            # Configuration exacte de la machine de l'utilisateur - une commande à la fois
            grbl_config = [
                "$0=10",
                "$1=25",
                "$2=3",
                "$3=2",
                "$4=0",
                "$5=1",
                "$6=0",
                "$10=0",
                "$11=0.010",
                "$12=0.002",
                "$13=0",
                "$20=1",
                "$21=1",
                "$22=1",
                "$23=3",
                "$24=2500.000",
                "$25=1000.000",
                "$26=200.000",
                "$27=1.500",
                "$28=1000.000",
                "$30=1000.000",
                "$31=0.000",
                "$32=1",           # Mode laser activé
                "$38=0",
                "$40=1",
                "$100=401.020",    # Pas/mm pour l'axe X
                "$101=406.480",    # Pas/mm pour l'axe Y
                "$102=1.000",
                "$103=100.000",
                "$104=100.000",
                "$105=100.000",
                "$110=5000.000",   # Vitesse max X
                "$111=5000.000",   # Vitesse max Y
                "$112=500.000",
                "$113=1000.000",
                "$114=1000.000",
                "$115=1000.000",
                "$120=1000.000",   # Accélération X
                "$121=1000.000",   # Accélération Y
                "$122=1300.000",
                "$123=300.000",
                "$124=300.000",
                "$125=300.000",
                "$130=290.000",    # Course max X
                "$131=235.000",    # Course max Y
                "$132=0.000",
                "$133=0.000",
                "$134=0.000",
                "$135=0.000",
            ]
            
            # Envoyer la configuration de manière simplifiée pour éviter les signaux récursifs
            print("1. Envoi des paramètres GRBL...")
            for cmd in grbl_config:
                try:
                    cmd_bytes = (cmd + '\n').encode('utf-8')
                    self.serial_connection.write(cmd_bytes)
                    self.serial_connection.flush()
                    time.sleep(0.1)
                    
                    # Lire la réponse simplement
                    response = b''
                    timeout_time = time.time() + 1.0
                    while time.time() < timeout_time:
                        if self.serial_connection.in_waiting > 0:
                            response += self.serial_connection.read(self.serial_connection.in_waiting)
                            if b'ok' in response or b'error' in response:
                                break
                        time.sleep(0.01)
                    
                    print(f"Config: {cmd} -> {response.decode('utf-8', errors='ignore').strip()}")
                except Exception as e:
                    print(f"Erreur lors de la configuration ({cmd}): {str(e)}")
            
            # Informer via console plutôt que signal
            print("Paramètres GRBL appliqués à votre machine")
            
            # Séquence d'initialisation standard
            print("2. Déverrouillage et initialisation...")
            init_commands = [
                "$X\n",          # Déverrouiller
                "G21\n",         # Mode millimètres
                "G90\n",         # Mode absolu
                "M5\n",          # Laser off
                "M3 S0\n"        # Laser on mais puissance à 0
            ]
            
            # Envoyer les commandes d'initialisation
            for cmd in init_commands:
                try:
                    self.serial_connection.write(cmd.encode('utf-8'))
                    self.serial_connection.flush()
                    time.sleep(0.2)  # Pause un peu plus longue entre les commandes d'initialisation
                    
                    # Lire la réponse
                    response = b''
                    timeout_time = time.time() + 1.0
                    while time.time() < timeout_time:
                        if self.serial_connection.in_waiting > 0:
                            response += self.serial_connection.read(self.serial_connection.in_waiting)
                            if b'ok' in response or b'error' in response:
                                break
                        time.sleep(0.01)
                    
                    print(f"Init: {cmd.strip()} -> {response.decode('utf-8', errors='ignore').strip()}")
                except Exception as e:
                    print(f"Erreur lors de l'initialisation ({cmd.strip()}): {str(e)}")
            
            print("3. Configuration terminée - Machine prête à l'emploi")
                
        except Exception as e:
            print(f"Erreur générale lors de la configuration: {str(e)}")
    
    def _notify_status_handlers(self):
        """Notifie tous les gestionnaires d'événements de statut."""
        self.status_updated.emit(self.status)
        
    def home(self) -> bool:
        """Envoie la commande de retour à la position d'origine.
        
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
        
        try:
            self.send_command("$H")
            return True
        except:
            return False
    
    def unlock(self) -> bool:
        """Déverrouille la machine après une erreur.
        
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
        
        try:
            self.send_command("$X")
            return True
        except:
            return False
    
    def set_zero_position(self, axes='XYZ') -> bool:
        """Définit la position actuelle comme origine pour les axes spécifiés.
        
        Args:
            axes: Les axes à définir comme origine (par défaut 'XYZ')
            
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
            
        try:
            # G10 L20 P0 définit l'origine du système de coordonnées actuel
            command = "G10 L20 P0"
            
            if 'X' in axes:
                command += " X0"
            if 'Y' in axes:
                command += " Y0"
            if 'Z' in axes:
                command += " Z0"
                
            self.send_command(command)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Erreur lors de la définition de l'origine: {str(e)}")
            return False
    
    def move_to(self, x: float = None, y: float = None, z: float = None, 
                feed_rate: float = 1000, relative: bool = False) -> bool:
        """Déplace l'outil à la position spécifiée.
        
        Args:
            x: Position X (en mm)
            y: Position Y (en mm)
            z: Position Z (en mm)
            feed_rate: Vitesse de déplacement (en mm/min)
            relative: Si True, effectue un déplacement relatif
            
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
        
        try:
            # Déterminer le mode de déplacement
            mode = "G91" if relative else "G90"
            
            # Construire la commande de déplacement
            cmd_parts = [mode, "G1"]
            if x is not None:
                cmd_parts.append(f"X{x:.3f}")
            if y is not None:
                cmd_parts.append(f"Y{y:.3f}")
            if z is not None:
                cmd_parts.append(f"Z{z:.3f}")
            
            cmd_parts.append(f"F{feed_rate:.0f}")
            
            # Envoyer la commande
            self.send_command(" ".join(cmd_parts))
            return True
            
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def set_laser_power(self, power) -> bool:
        """Définit la puissance du laser.
        
        Args:
            power: Puissance du laser (0-1000)
            
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
            
        try:
            # S'assurer que la puissance est dans les limites
            power = max(0, min(1000, power))
            
            # Convertir la puissance en valeur S (0-1000)
            s_value = power
            
            # Activer le laser avec la puissance spécifiée
            if power > 0:
                self.send_command(f"M3 S{s_value}")
            else:
                self.send_command("M5")  # Éteindre le laser
                
            return True
        except Exception as e:
            self.error_occurred.emit(f"Erreur lors de la définition de la puissance du laser: {str(e)}")
            return False
    
    def emergency_stop(self) -> None:
        """Arrêt d'urgence de la machine."""
        if self.is_connected():
            self.send_immediate(0x18)  # Ctrl-X
    
    def move_relative(self, x=None, y=None, z=None, feed_rate=None) -> bool:
        """Déplace la machine de manière relative.
        
        Args:
            x: Déplacement relatif sur l'axe X (mm)
            y: Déplacement relatif sur l'axe Y (mm)
            z: Déplacement relatif sur l'axe Z (mm)
            feed_rate: Vitesse d'avance (mm/min)
            
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
            
        command = "G91"  # Mode relatif
        
        # Construire la commande de déplacement
        move_cmd = "G0"  # Mouvement rapide
        if feed_rate is not None:
            move_cmd = f"G1 F{feed_rate}"  # Mouvement avec vitesse spécifiée
            
        if x is not None:
            move_cmd += f" X{x}"
        if y is not None:
            move_cmd += f" Y{y}"
        if z is not None:
            move_cmd += f" Z{z}"
            
        try:
            # Passer en mode relatif
            self.send_command(command)
            # Envoyer la commande de déplacement
            self.send_command(move_cmd)
            # Revenir en mode absolu
            self.send_command("G90")
            return True
        except Exception as e:
            self.error_occurred.emit(f"Erreur de déplacement relatif: {str(e)}")
            return False
            
    def move_absolute(self, x=None, y=None, z=None, feed_rate=None) -> bool:
        """Déplace la machine à une position absolue.
        
        Args:
            x: Position absolue sur l'axe X (mm)
            y: Position absolue sur l'axe Y (mm)
            z: Position absolue sur l'axe Z (mm)
            feed_rate: Vitesse d'avance (mm/min)
            
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
            
        # S'assurer d'être en mode absolu
        command = "G90"  # Mode absolu
        
        # Construire la commande de déplacement
        move_cmd = "G0"  # Mouvement rapide
        if feed_rate is not None:
            move_cmd = f"G1 F{feed_rate}"  # Mouvement avec vitesse spécifiée
            
        if x is not None:
            move_cmd += f" X{x}"
        if y is not None:
            move_cmd += f" Y{y}"
        if z is not None:
            move_cmd += f" Z{z}"
            
        try:
            # Passer en mode absolu (par précaution)
            self.send_command(command)
            # Envoyer la commande de déplacement
            self.send_command(move_cmd)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Erreur de déplacement absolu: {str(e)}")
            return False
            
    def start_jogging(self, axis, direction, feed_rate=None) -> bool:
        """Commence un déplacement continu dans la direction spécifiée.
        
        Args:
            axis: L'axe à déplacer ('X', 'Y', ou 'Z')
            direction: La direction (1 pour positif, -1 pour négatif)
            feed_rate: La vitesse d'avance (mm/min)
            
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
            
        # En réalité, GRBL ne supporte pas le jogging continu natif
        # Nous allons donc simuler cela avec un petit déplacement relatif
        
        # Déterminer la distance de déplacement (petit pas)
        distance = 1.0 * direction  # 1mm dans la direction spécifiée
        
        # Définir la vitesse par défaut si non spécifiée
        if feed_rate is None:
            feed_rate = 1000  # 1000 mm/min par défaut
            
        # Construire le déplacement relatif
        if axis == 'X':
            return self.move_relative(x=distance, feed_rate=feed_rate)
        elif axis == 'Y':
            return self.move_relative(y=distance, feed_rate=feed_rate)
        elif axis == 'Z':
            return self.move_relative(z=distance, feed_rate=feed_rate)
        else:
            self.error_occurred.emit(f"Axe invalide pour le jogging: {axis}")
            return False
    
    def stop_jogging(self) -> bool:
        """Arrête le déplacement continu.
        
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
            
        try:
            # Envoyer une commande d'arrêt d'alimentation
            self.send_immediate('!')  # Feed hold (pause)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Erreur lors de l'arrêt du jogging: {str(e)}")
            return False
            
    def stop(self) -> bool:
        """Arrête toutes les opérations en cours.
        
        Returns:
            bool: True si la commande a été envoyée avec succès
        """
        if not self.is_connected():
            return False
            
        try:
            # Envoyer un feed hold puis un reset
            self.send_immediate('!')  # Feed hold
            time.sleep(0.1)
            self.send_immediate(0x18)  # Ctrl-X (reset)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Erreur lors de l'arrêt: {str(e)}")
            return False
