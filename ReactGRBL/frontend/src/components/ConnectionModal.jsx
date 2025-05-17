import React, { useState } from 'react';

const ConnectionModal = ({ onConnect, onCancel }) => {
  const [port, setPort] = useState('COM3');
  const [baudRate, setBaudRate] = useState(115200);
  const [isLoading, setIsLoading] = useState(false);
  
  // Simuler une liste de ports pour le développement
  const availablePorts = ['COM1', 'COM2', 'COM3', 'COM4', '/dev/ttyUSB0', '/dev/ttyUSB1'];
  const availableBaudRates = [9600, 19200, 38400, 57600, 115200, 230400];
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simuler un délai de connexion
    setTimeout(() => {
      onConnect(port, baudRate);
      setIsLoading(false);
    }, 1000);
  };
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 w-96">
        <h2 className="text-xl font-bold mb-4">Connexion au contrôleur GRBL</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group mb-4">
            <label className="form-label">Port</label>
            <select 
              className="form-control"
              value={port}
              onChange={(e) => setPort(e.target.value)}
              disabled={isLoading}
            >
              {availablePorts.map(p => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>
          
          <div className="form-group mb-6">
            <label className="form-label">Vitesse (baud)</label>
            <select 
              className="form-control"
              value={baudRate}
              onChange={(e) => setBaudRate(Number(e.target.value))}
              disabled={isLoading}
            >
              {availableBaudRates.map(b => (
                <option key={b} value={b}>{b}</option>
              ))}
            </select>
          </div>
          
          <div className="flex justify-end space-x-2">
            <button 
              type="button" 
              className="btn btn-outline"
              onClick={onCancel}
              disabled={isLoading}
            >
              Annuler
            </button>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={isLoading}
            >
              {isLoading ? 'Connexion...' : 'Connecter'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ConnectionModal;
