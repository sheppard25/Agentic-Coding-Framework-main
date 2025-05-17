import os
import json
import uuid
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import UploadFile
import aiofiles

class FileService:
    def __init__(self):
        # Créer les répertoires nécessaires s'ils n'existent pas
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.files_dir = os.path.join(self.base_dir, "files")
        self.settings_file = os.path.join(self.base_dir, "settings.json")
        self.files_index = os.path.join(self.base_dir, "files_index.json")
        
        self._ensure_directories()
        self._load_settings()
        self._load_files_index()
    
    def _ensure_directories(self) -> None:
        """S'assurer que les répertoires nécessaires existent"""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.files_dir, exist_ok=True)
    
    def _load_settings(self) -> None:
        """Charger les paramètres depuis le fichier"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            else:
                # Paramètres par défaut
                self.settings = {
                    "origin_position": "top-right",
                    "grid_spacing": 20,
                    "default_feed_rate": 1000,
                    "default_laser_power": 50
                }
                self._save_settings()
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
            # Paramètres par défaut en cas d'erreur
            self.settings = {
                "origin_position": "top-right",
                "grid_spacing": 20,
                "default_feed_rate": 1000,
                "default_laser_power": 50
            }
    
    def _save_settings(self) -> None:
        """Sauvegarder les paramètres dans le fichier"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {str(e)}")
    
    def _load_files_index(self) -> None:
        """Charger l'index des fichiers"""
        try:
            if os.path.exists(self.files_index):
                with open(self.files_index, 'r') as f:
                    self.files = json.load(f)
            else:
                self.files = []
                self._save_files_index()
        except Exception as e:
            print(f"Error loading files index: {str(e)}")
            self.files = []
    
    def _save_files_index(self) -> None:
        """Sauvegarder l'index des fichiers"""
        try:
            with open(self.files_index, 'w') as f:
                json.dump(self.files, f, indent=2)
        except Exception as e:
            print(f"Error saving files index: {str(e)}")
    
    def get_settings(self) -> Dict[str, Any]:
        """Récupérer les paramètres actuels"""
        return self.settings
    
    def update_settings(self, new_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour les paramètres"""
        # Mettre à jour uniquement les clés existantes
        for key in new_settings:
            if key in self.settings:
                self.settings[key] = new_settings[key]
        
        # Sauvegarder les paramètres mis à jour
        self._save_settings()
        
        return self.settings
    
    def get_files(self) -> List[Dict[str, Any]]:
        """Récupérer la liste des fichiers"""
        return self.files
    
    def get_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer les informations d'un fichier spécifique"""
        for file in self.files:
            if file["id"] == file_id:
                return file
        return None
    
    def get_file_path(self, file_id: str) -> Optional[str]:
        """Récupérer le chemin d'un fichier spécifique"""
        file_info = self.get_file(file_id)
        if file_info:
            return os.path.join(self.files_dir, file_info["filename"])
        return None
    
    async def save_file(self, file: UploadFile) -> Dict[str, Any]:
        """Sauvegarder un fichier téléchargé"""
        # Générer un ID unique pour le fichier
        file_id = str(uuid.uuid4())
        
        # Obtenir l'extension du fichier
        _, ext = os.path.splitext(file.filename)
        
        # Créer un nom de fichier unique
        filename = f"{file_id}{ext}"
        file_path = os.path.join(self.files_dir, filename)
        
        # Sauvegarder le fichier
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Déterminer le type de fichier
        file_type = self._get_file_type(ext)
        
        # Créer les métadonnées du fichier
        file_info = {
            "id": file_id,
            "original_name": file.filename,
            "filename": filename,
            "type": file_type,
            "size": len(content),
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat()
        }
        
        # Ajouter à l'index des fichiers
        self.files.append(file_info)
        self._save_files_index()
        
        return file_info
    
    def delete_file(self, file_id: str) -> bool:
        """Supprimer un fichier"""
        file_info = self.get_file(file_id)
        if not file_info:
            return False
        
        # Supprimer le fichier physique
        file_path = os.path.join(self.files_dir, file_info["filename"])
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
            return False
        
        # Supprimer de l'index
        self.files = [f for f in self.files if f["id"] != file_id]
        self._save_files_index()
        
        return True
    
    def _get_file_type(self, extension: str) -> str:
        """Déterminer le type de fichier en fonction de l'extension"""
        extension = extension.lower()
        
        if extension in ['.gcode', '.nc', '.ngc', '.tap', '.cnc']:
            return "gcode"
        elif extension in ['.svg', '.dxf']:
            return "vector"
        elif extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            return "image"
        else:
            return "unknown"
