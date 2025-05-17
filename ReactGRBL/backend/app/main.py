from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import socketio
import uvicorn
import json
import os
import asyncio
import time
from typing import List, Dict, Optional, Any
from .grbl_controller import GRBLController
from .file_service import FileService

# Initialiser l'application FastAPI
app = FastAPI(title="ReactGRBL Backend API")

# Configurer CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez l'origine exacte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser les services
grbl_controller = GRBLController()
file_service = FileService()

# Modèles de données
class ConnectionRequest(BaseModel):
    port: str
    baud_rate: int = 115200

class JogCommand(BaseModel):
    axis: str
    distance: float
    feed_rate: Optional[float] = None

class GCodeCommand(BaseModel):
    command: str

class MachineSettings(BaseModel):
    origin_position: str = "top-right"
    grid_spacing: int = 20
    default_feed_rate: int = 1000
    default_laser_power: int = 50

# Routes API
@app.get("/")
async def root():
    return {"message": "ReactGRBL Backend API"}

@app.get("/ports")
async def get_ports():
    """Récupérer la liste des ports série disponibles"""
    ports = grbl_controller.get_available_ports()
    return {"ports": ports}

@app.post("/connect")
async def connect(request: ConnectionRequest):
    """Se connecter au contrôleur GRBL"""
    try:
        success = grbl_controller.connect(request.port, request.baud_rate)
        if success:
            return {"status": "connected", "message": f"Connecté à {request.port} à {request.baud_rate} bauds"}
        else:
            raise HTTPException(status_code=400, detail="Échec de la connexion")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/disconnect")
async def disconnect():
    """Se déconnecter du contrôleur GRBL"""
    try:
        grbl_controller.disconnect()
        return {"status": "disconnected", "message": "Déconnecté du contrôleur GRBL"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Récupérer l'état actuel de la machine"""
    if not grbl_controller.is_connected():
        raise HTTPException(status_code=400, detail="Non connecté au contrôleur GRBL")

    status = grbl_controller.get_status()
    return status

@app.post("/jog")
async def jog(command: JogCommand):
    """Déplacer la machine selon un axe et une distance spécifiés"""
    if not grbl_controller.is_connected():
        raise HTTPException(status_code=400, detail="Non connecté au contrôleur GRBL")

    try:
        success = grbl_controller.jog(command.axis, command.distance, command.feed_rate)
        if success:
            return {"status": "success", "message": f"Déplacement {command.axis} de {command.distance}mm"}
        else:
            raise HTTPException(status_code=400, detail="Échec du déplacement")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/command")
async def send_command(command: GCodeCommand):
    """Envoyer une commande G-code directe"""
    if not grbl_controller.is_connected():
        raise HTTPException(status_code=400, detail="Non connecté au contrôleur GRBL")

    try:
        response = grbl_controller.send_command(command.command)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/home")
async def home():
    """Exécuter la commande de homing"""
    if not grbl_controller.is_connected():
        raise HTTPException(status_code=400, detail="Non connecté au contrôleur GRBL")

    try:
        success = grbl_controller.home()
        if success:
            return {"status": "success", "message": "Homing terminé"}
        else:
            raise HTTPException(status_code=400, detail="Échec du homing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset():
    """Réinitialiser le contrôleur GRBL"""
    if not grbl_controller.is_connected():
        raise HTTPException(status_code=400, detail="Non connecté au contrôleur GRBL")

    try:
        success = grbl_controller.reset()
        if success:
            return {"status": "success", "message": "Contrôleur réinitialisé"}
        else:
            raise HTTPException(status_code=400, detail="Échec de la réinitialisation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/configure")
async def configure_grbl():
    """Configurer le contrôleur GRBL avec les paramètres spécifiques de la machine"""
    if not grbl_controller.is_connected():
        raise HTTPException(status_code=400, detail="Non connecté au contrôleur GRBL")

    try:
        success = grbl_controller.configure_grbl()
        if success:
            return {"status": "success", "message": "Configuration GRBL terminée avec succès"}
        else:
            raise HTTPException(status_code=400, detail="Échec de la configuration GRBL")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/unlock")
async def unlock_machine():
    """Déverrouiller la machine GRBL ($X) et initialiser"""
    if not grbl_controller.is_connected():
        raise HTTPException(status_code=400, detail="Non connecté au contrôleur GRBL")

    try:
        # Utiliser une approche simplifiée pour le déverrouillage
        # Envoyer directement la commande de déverrouillage
        response1 = grbl_controller.send_command("$X")

        # Attendre un peu
        time.sleep(0.5)

        # Configurer les modes de base
        response2 = grbl_controller.send_command("G21") # Mode millimètres
        response3 = grbl_controller.send_command("G90") # Mode absolu

        return {
            "status": "success",
            "message": "Machine déverrouillée et initialisée",
            "responses": [response1, response2, response3]
        }
    except Exception as e:
        print(f"Erreur de déverrouillage: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def get_files():
    """Récupérer la liste des fichiers disponibles"""
    try:
        files = file_service.get_files()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Télécharger un fichier"""
    try:
        file_info = await file_service.save_file(file)
        return file_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{file_id}")
async def get_file(file_id: str):
    """Récupérer les informations d'un fichier spécifique"""
    try:
        file_info = file_service.get_file(file_id)
        if file_info:
            return file_info
        else:
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Supprimer un fichier"""
    try:
        success = file_service.delete_file(file_id)
        if success:
            return {"status": "success", "message": "Fichier supprimé"}
        else:
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files/{file_id}/send")
async def send_file(file_id: str):
    """Envoyer un fichier au contrôleur GRBL pour exécution"""
    if not grbl_controller.is_connected():
        raise HTTPException(status_code=400, detail="Non connecté au contrôleur GRBL")

    try:
        file_path = file_service.get_file_path(file_id)
        if not file_path:
            raise HTTPException(status_code=404, detail="Fichier non trouvé")

        success = grbl_controller.send_file(file_path)
        if success:
            return {"status": "success", "message": "Fichier envoyé pour exécution"}
        else:
            raise HTTPException(status_code=400, detail="Échec de l'envoi du fichier")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/settings")
async def get_settings():
    """Récupérer les paramètres actuels"""
    try:
        settings = file_service.get_settings()
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/settings")
async def update_settings(settings: MachineSettings):
    """Mettre à jour les paramètres"""
    try:
        updated_settings = file_service.update_settings(settings.dict())
        return updated_settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket pour les mises à jour en temps réel
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Ajouter le websocket à la liste des clients
    client_id = id(websocket)
    grbl_controller.add_client(client_id, websocket)

    try:
        while True:
            # Attendre les messages du client
            data = await websocket.receive_text()
            message = json.loads(data)

            # Traiter les messages selon leur type
            if message.get("type") == "command":
                response = grbl_controller.send_command(message.get("command", ""))
                await websocket.send_json({"type": "response", "data": response})
    except WebSocketDisconnect:
        # Supprimer le client lorsqu'il se déconnecte
        grbl_controller.remove_client(client_id)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        grbl_controller.remove_client(client_id)

# Démarrer le serveur si exécuté directement
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
