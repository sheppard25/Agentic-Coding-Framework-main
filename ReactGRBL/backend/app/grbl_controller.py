import serial
import serial.tools.list_ports
import time
import threading
import json
import re
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from .grbl_config import GRBL_PARAMETERS, INIT_COMMANDS, WORK_AREA, get_grbl_config_commands

class GRBLController:
    def __init__(self):
        self.serial_port = None
        self.is_connected_flag = False
        self.clients = {}  # WebSocket clients pour les mises à jour en temps réel
        self.status_thread = None
        self.stop_status_thread = threading.Event()
        self.machine_position = {"x": 0, "y": 0}
        self.work_position = {"x": 0, "y": 0}
        self.state = "Idle"
        self.buffer_state = 0
        self.last_error = None
        self.last_alarm = None

    def get_available_ports(self) -> List[Dict[str, str]]:
        """Récupérer la liste des ports série disponibles"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid
            })
        return ports

    def connect(self, port: str, baud_rate: int = 115200) -> bool:
        """Se connecter au contrôleur GRBL"""
        try:
            # Fermer la connexion existante si elle est ouverte
            if self.is_connected_flag:
                self.disconnect()

            # Ouvrir la nouvelle connexion
            self.serial_port = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)  # Attendre que GRBL s'initialise

            # Vider le buffer
            self.serial_port.flushInput()

            # Envoyer une commande de réveil
            self.serial_port.write(b"\r\n\r\n")
            time.sleep(2)

            # Vérifier si nous recevons une réponse
            response = self.serial_port.readline().decode('utf-8').strip()
            if "Grbl" in response or "GRBL" in response:
                self.is_connected_flag = True

                # Démarrer le thread de surveillance d'état
                self.stop_status_thread.clear()
                self.status_thread = threading.Thread(target=self._status_polling)
                self.status_thread.daemon = True
                self.status_thread.start()

                # Initialiser la machine automatiquement
                init_success = self._initialize_machine()
                if not init_success:
                    print("Avertissement: L'initialisation automatique a échoué. Utilisez le bouton 'Déverrouiller' manuellement.")

                return True
            else:
                self.serial_port.close()
                self.serial_port = None
                return False
        except Exception as e:
            print(f"Error connecting to GRBL: {str(e)}")
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            self.serial_port = None
            return False

    def _initialize_machine(self) -> bool:
        """Initialise la machine avec la séquence complète et robuste."""
        if not self.is_connected():
            return False

        print("=== INITIALISATION DE LA MACHINE ===")

        try:
            # Reset complet du contrôleur
            self.serial_port.write(b"\x18")  # Ctrl+X - reset complet
            time.sleep(2)  # Attente suffisante après reset

            # Vider les buffers
            self.serial_port.reset_input_buffer()
            self.serial_port.reset_output_buffer()

            # Configuration des paramètres GRBL avec les valeurs réelles
            print("1. Configuration des paramètres...")
            settings_commands = [
                # Utiliser les valeurs réelles fournies par l'utilisateur
                "$110=5000",   # Vitesse max X (5000 mm/min)
                "$111=5000",   # Vitesse max Y (5000 mm/min)
                "$120=1000",   # Accélération X (1000 mm/s²)
                "$121=1000",   # Accélération Y (1000 mm/s²)
                "$100=401.020", # Pas/mm X (401.020 steps/mm)
                "$101=406.480"  # Pas/mm Y (406.480 steps/mm)
            ]

            for cmd in settings_commands:
                self.send_command(cmd)
                time.sleep(0.2)

            # Séquence d'initialisation standard
            print("2. Déverrouillage et initialisation...")
            init_commands = [
                "$X",          # Déverrouiller
                "G21",         # Mode millimètres
                "G90",         # Mode absolu
                "M5",          # Laser off
                "M3 S0"        # Laser on mais puissance à 0
            ]

            # Envoyer chaque commande
            for cmd in init_commands:
                response = self.send_command(cmd)
                print(f"Commande: {cmd} -> Réponse: {response}")
                time.sleep(0.3)

            print("=== MACHINE PRÊTE (position actuelle) ===")
            return True

        except Exception as e:
            print(f"!!! ERREUR: {str(e)}")
            return False

    def disconnect(self) -> bool:
        """Se déconnecter du contrôleur GRBL"""
        try:
            # Arrêter le thread de surveillance d'état
            if self.status_thread and self.status_thread.is_alive():
                self.stop_status_thread.set()
                self.status_thread.join(timeout=2)

            # Fermer la connexion série
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()

            self.serial_port = None
            self.is_connected_flag = False
            return True
        except Exception as e:
            print(f"Error disconnecting from GRBL: {str(e)}")
            return False

    def is_connected(self) -> bool:
        """Vérifier si le contrôleur est connecté"""
        return self.is_connected_flag and self.serial_port and self.serial_port.is_open

    def send_command(self, command: str) -> str:
        """Envoyer une commande G-code au contrôleur"""
        if not self.is_connected():
            raise Exception("Not connected to GRBL controller")

        try:
            # Nettoyer la commande
            command = command.strip() + "\n"

            # Envoyer la commande
            self.serial_port.write(command.encode())

            # Attendre et lire la réponse
            time.sleep(0.1)
            response = ""
            while self.serial_port.in_waiting > 0:
                line = self.serial_port.readline().decode('utf-8').strip()
                response += line + "\n"

            return response.strip()
        except Exception as e:
            print(f"Error sending command: {str(e)}")
            raise

    def jog(self, axis: str, distance: float, feed_rate: Optional[float] = None) -> bool:
        """Déplacer la machine selon un axe et une distance spécifiés"""
        if not self.is_connected():
            return False

        try:
            # Vérifier que l'axe est valide
            if axis.lower() not in ['x', 'y']:
                return False

            # Construire la commande de déplacement
            if feed_rate:
                command = f"G91 G1 {axis.upper()}{distance} F{feed_rate}"
            else:
                command = f"G91 G1 {axis.upper()}{distance}"

            # Envoyer la commande
            self.send_command(command)

            # Revenir en mode absolu
            self.send_command("G90")

            return True
        except Exception as e:
            print(f"Error during jog: {str(e)}")
            return False

    def home(self) -> bool:
        """Exécuter la commande de homing"""
        if not self.is_connected():
            return False

        try:
            # Envoyer la commande de homing
            response = self.send_command("$H")

            # Vérifier si la commande a été acceptée
            if "error" in response.lower():
                return False

            return True
        except Exception as e:
            print(f"Error during homing: {str(e)}")
            return False

    def reset(self) -> bool:
        """Réinitialiser le contrôleur GRBL"""
        if not self.is_connected():
            return False

        try:
            # Envoyer le caractère de réinitialisation
            self.serial_port.write(b"\x18")  # Ctrl+X
            time.sleep(2)  # Attendre que GRBL redémarre

            # Vider le buffer
            self.serial_port.flushInput()

            return True
        except Exception as e:
            print(f"Error resetting GRBL: {str(e)}")
            return False

    def send_file(self, file_path: str) -> bool:
        """Envoyer un fichier G-code au contrôleur"""
        if not self.is_connected():
            return False

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Ignorer les commentaires et les lignes vides
                    line = line.strip()
                    if line and not line.startswith(';') and not line.startswith('('):
                        # Envoyer la ligne et attendre la réponse
                        self.send_command(line)
                        # Ajouter un petit délai pour éviter de surcharger le buffer
                        time.sleep(0.1)

            return True
        except Exception as e:
            print(f"Error sending file: {str(e)}")
            return False

    def configure_grbl(self) -> bool:
        """Configurer le contrôleur GRBL avec les paramètres spécifiques de la machine"""
        if not self.is_connected():
            return False

        try:
            # Réinitialiser d'abord le contrôleur
            self.reset()
            time.sleep(2)  # Attendre que GRBL redémarre

            # Envoyer les paramètres de configuration
            config_commands = get_grbl_config_commands()
            for cmd in config_commands:
                response = self.send_command(cmd)
                if "error" in response.lower():
                    print(f"Erreur lors de la configuration ({cmd}): {response}")
                time.sleep(0.1)  # Petit délai entre les commandes

            # Envoyer les commandes d'initialisation
            for cmd in INIT_COMMANDS:
                response = self.send_command(cmd)
                if "error" in response.lower():
                    print(f"Erreur lors de l'initialisation ({cmd}): {response}")
                time.sleep(0.1)

            print("Configuration GRBL terminée avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors de la configuration GRBL: {str(e)}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Récupérer l'état actuel de la machine"""
        return {
            "state": self.state,
            "machine_position": self.machine_position,
            "work_position": self.work_position,
            "buffer_state": self.buffer_state,
            "last_error": self.last_error,
            "last_alarm": self.last_alarm
        }

    def add_client(self, client_id: int, websocket) -> None:
        """Ajouter un client WebSocket pour les mises à jour en temps réel"""
        self.clients[client_id] = websocket

    def remove_client(self, client_id: int) -> None:
        """Supprimer un client WebSocket"""
        if client_id in self.clients:
            del self.clients[client_id]

    def _status_polling(self) -> None:
        """Thread pour interroger périodiquement l'état de la machine"""
        while not self.stop_status_thread.is_set():
            try:
                if self.is_connected():
                    # Envoyer la commande d'état
                    self.serial_port.write(b"?")
                    time.sleep(0.1)

                    # Lire la réponse
                    if self.serial_port.in_waiting > 0:
                        response = self.serial_port.readline().decode('utf-8').strip()

                        # Analyser la réponse d'état
                        if response.startswith('<') and response.endswith('>'):
                            self._parse_status(response)

                            # Envoyer les mises à jour aux clients WebSocket
                            self._broadcast_status()
            except Exception as e:
                print(f"Error in status polling: {str(e)}")

            # Attendre avant la prochaine interrogation
            time.sleep(0.5)

    def _parse_status(self, status_string: str) -> None:
        """Analyser la chaîne d'état de GRBL"""
        # Format typique: <Idle|MPos:0.000,0.000,0.000|WPos:0.000,0.000,0.000|Buf:0>
        try:
            # Extraire l'état
            state_match = re.search(r'<([^|]+)', status_string)
            if state_match:
                self.state = state_match.group(1)

            # Extraire la position machine
            mpos_match = re.search(r'MPos:([^|]+)', status_string)
            if mpos_match:
                mpos_values = mpos_match.group(1).split(',')
                if len(mpos_values) >= 3:
                    self.machine_position = {
                        "x": float(mpos_values[0]),
                        "y": float(mpos_values[1])
                    }

            # Extraire la position de travail
            wpos_match = re.search(r'WPos:([^|]+)', status_string)
            if wpos_match:
                wpos_values = wpos_match.group(1).split(',')
                if len(wpos_values) >= 3:
                    self.work_position = {
                        "x": float(wpos_values[0]),
                        "y": float(wpos_values[1])
                    }

            # Extraire l'état du buffer
            buf_match = re.search(r'Buf:(\d+)', status_string)
            if buf_match:
                self.buffer_state = int(buf_match.group(1))
        except Exception as e:
            print(f"Error parsing status: {str(e)}")

    async def _broadcast_status(self) -> None:
        """Envoyer l'état actuel à tous les clients WebSocket"""
        if not self.clients:
            return

        status_data = {
            "type": "status",
            "data": self.get_status()
        }

        # Convertir en JSON
        message = json.dumps(status_data)

        # Envoyer à tous les clients
        for client_id, websocket in list(self.clients.items()):
            try:
                asyncio.create_task(websocket.send_text(message))
            except Exception as e:
                print(f"Error sending to client {client_id}: {str(e)}")
                # Supprimer le client en cas d'erreur
                self.remove_client(client_id)
