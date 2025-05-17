import { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import VisualizationPanel from './components/VisualizationPanel';
import StatusBar from './components/StatusBar';
import ConnectionModal from './components/ConnectionModal';

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [machineStatus, setMachineStatus] = useState('Idle');
  const [machinePosition, setMachinePosition] = useState({ x: 0, y: 0 });
  const [showConnectionModal, setShowConnectionModal] = useState(false);
  const [activeFile, setActiveFile] = useState(null);

  // Établir une connexion réelle au contrôleur GRBL
  const handleConnect = (port, baudRate) => {
    console.log(`Connecting to ${port} at ${baudRate} baud...`);

    // En mode développement, simuler une connexion réussie immédiatement
    if (process.env.NODE_ENV === 'development') {
      console.log('Mode développement: simulation de connexion réussie sans backend');
      setIsConnected(true);
      setShowConnectionModal(false);
      return;
    }

    // En mode production, essayer de se connecter au backend
    try {
      // Vérifier d'abord si le backend est accessible
      fetch('http://localhost:8000/status')
        .then(response => {
          if (!response.ok) {
            throw new Error('Le backend n\'est pas accessible');
          }
          return response.json();
        })
        .then(() => {
          // Si le backend est accessible, tenter de se connecter au port série
          return fetch('http://localhost:8000/connect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ port, baudRate: parseInt(baudRate) })
          });
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Échec de la connexion au port série');
          }
          return response.json();
        })
        .then(data => {
          console.log('Connexion réussie:', data);
          setIsConnected(true);
          setShowConnectionModal(false);
        })
        .catch(error => {
          console.error('Erreur de connexion:', error);
          alert(`Erreur de connexion: ${error.message}\n\nVérifiez que le backend est en cours d'exécution à l'adresse http://localhost:8000`);
          // Pour le développement, permettre quand même la connexion
          if (process.env.NODE_ENV === 'development') {
            console.log('Mode développement: simulation de connexion réussie');
            setIsConnected(true);
            setShowConnectionModal(false);
          }
        });
    } catch (error) {
      console.error('Erreur critique:', error);
      if (process.env.NODE_ENV === 'development') {
        console.log('Mode développement: simulation de connexion réussie malgré l\'erreur');
        setIsConnected(true);
        setShowConnectionModal(false);
      } else {
        alert(`Erreur critique: ${error.message}`);
      }
    }
  };

  const handleDisconnect = () => {
    setIsConnected(false);
  };

  const handleFileSelect = (file) => {
    setActiveFile(file);
  };

  // Fonction pour déverrouiller la machine
  const handleUnlock = () => {
    console.log("Déverrouillage et initialisation de la machine...");

    // Mettre à jour le statut pour indiquer que l'opération est en cours
    setMachineStatus('Déverrouillage...');

    // En mode développement, simuler un déverrouillage réussi immédiatement
    if (process.env.NODE_ENV === 'development') {
      console.log('Mode développement: simulation de déverrouillage réussi sans backend');
      setTimeout(() => {
        setMachineStatus('Idle');
        // Pas d'alerte en mode développement pour éviter de perturber l'utilisateur
      }, 500);
      return;
    }

    // En mode production, essayer de se connecter au backend
    try {
      // Vérifier d'abord si le backend est accessible
      fetch('http://localhost:8000/status')
        .then(response => {
          if (!response.ok) {
            throw new Error('Le backend n\'est pas accessible');
          }
          return response.json();
        })
        .then(statusData => {
          // Vérifier si le contrôleur est connecté
          if (!statusData.connected) {
            throw new Error('Le contrôleur GRBL n\'est pas connecté');
          }

          // Si tout est OK, envoyer directement la commande de déverrouillage
          return fetch('http://localhost:8000/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: '$X' })
          });
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Échec du déverrouillage');
          }
          return response.json();
        })
        .then(data => {
          console.log("Réponse:", data);
          // Afficher un message de succès
          alert("Machine déverrouillée avec succès!");
          setMachineStatus('Idle');
        })
        .catch(error => {
          console.error("Erreur:", error);

          // Message d'erreur plus détaillé
          let errorMessage = "Erreur lors du déverrouillage: " + error.message;
          if (error.message.includes("backend n'est pas accessible")) {
            errorMessage += "\n\nVérifiez que le backend est en cours d'exécution à l'adresse http://localhost:8000";
          }

          alert(errorMessage);

          // En mode développement, simuler quand même le déverrouillage
          if (process.env.NODE_ENV === 'development') {
            console.log('Mode développement: simulation de déverrouillage réussi');
            setMachineStatus('Idle');
          } else {
            setMachineStatus('Erreur');
          }
        });
    } catch (error) {
      console.error('Erreur critique:', error);
      if (process.env.NODE_ENV === 'development') {
        console.log('Mode développement: simulation de déverrouillage réussi malgré l\'erreur');
        setMachineStatus('Idle');
      } else {
        alert(`Erreur critique: ${error.message}`);
        setMachineStatus('Erreur');
      }
    }
  };

  // Fonction pour gérer les déplacements (jog)
  const handleJog = (axis, direction, stepSize = 20) => {
    console.log(`Jog ${axis} ${direction} with step size ${stepSize}`);

    // En mode développement, simuler le déplacement
    if (process.env.NODE_ENV === 'development') {
      // Calculer les nouveaux déplacements en fonction de l'axe et de la direction
      if (axis === 'x') {
        // Déplacement sur l'axe X
        const step = direction === '+' ? stepSize : -stepSize;
        setMachinePosition(prev => ({
          ...prev,
          x: prev.x + step
        }));
      } else if (axis === 'y') {
        // Déplacement sur l'axe Y
        const step = direction === '+' ? stepSize : -stepSize;
        setMachinePosition(prev => ({
          ...prev,
          y: prev.y + step
        }));
      } else if (axis === 'xy') {
        // Déplacement en diagonale
        const xDir = direction.charAt(0);
        const yDir = direction.charAt(1);
        const xStep = xDir === '+' ? stepSize : -stepSize;
        const yStep = yDir === '+' ? stepSize : -stepSize;
        setMachinePosition(prev => ({
          x: prev.x + xStep,
          y: prev.y + yStep
        }));
      }
    } else {
      // En mode production, envoyer la commande au backend
      fetch('http://localhost:8000/jog', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ axis, direction, stepSize })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Échec du déplacement');
        }
        return response.json();
      })
      .then(data => {
        console.log('Déplacement réussi:', data);
        // Le backend devrait renvoyer la nouvelle position
        if (data.position) {
          setMachinePosition(data.position);
        }
      })
      .catch(error => {
        console.error('Erreur de déplacement:', error);
        alert(`Erreur de déplacement: ${error.message}`);
      });
    }
  };

  // Fonction pour gérer la commande Home
  const handleHomeCommand = () => {
    console.log('Home command');

    // En mode développement, simuler le retour à l'origine
    if (process.env.NODE_ENV === 'development') {
      setMachinePosition({ x: 0, y: 0 });
    } else {
      // En mode production, envoyer la commande au backend
      fetch('http://localhost:8000/home', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Échec de la commande Home');
        }
        return response.json();
      })
      .then(data => {
        console.log('Commande Home réussie:', data);
        setMachinePosition({ x: 0, y: 0 });
      })
      .catch(error => {
        console.error('Erreur de commande Home:', error);
        alert(`Erreur de commande Home: ${error.message}`);
      });
    }
  };

  return (
    <div className="app">
      <Header
        isConnected={isConnected}
        onConnect={() => setShowConnectionModal(true)}
        onDisconnect={handleDisconnect}
        onUnlock={handleUnlock}
      />

      <div className="main-content" style={{ display: 'flex', height: 'calc(100vh - 80px)', overflow: 'hidden' }}>
        <Sidebar
          isConnected={isConnected}
          onFileSelect={handleFileSelect}
          activeFile={activeFile}
          style={{ width: '250px', minWidth: '250px', overflowY: 'auto' }}
        />

        <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '20px' }}>
          <VisualizationPanel
            isConnected={isConnected}
            machinePosition={machinePosition}
            activeFile={activeFile}
            style={{ width: '100%', height: '100%' }}
          />
        </div>
      </div>

      <StatusBar
        isConnected={isConnected}
        machineStatus={machineStatus}
        machinePosition={machinePosition}
      />

      {showConnectionModal && (
        <ConnectionModal
          onConnect={handleConnect}
          onCancel={() => setShowConnectionModal(false)}
        />
      )}
    </div>
  );
}

export default App;
