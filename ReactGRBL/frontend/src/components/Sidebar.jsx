import React, { useState } from 'react';

const Sidebar = ({ isConnected, onFileSelect, activeFile }) => {
  const [activeTab, setActiveTab] = useState('control');

  // Simuler quelques fichiers pour le développement
  const demoFiles = [
    { id: 1, name: 'test_square.gcode', size: '45 KB', date: '2023-05-15' },
    { id: 2, name: 'logo.svg', size: '12 KB', date: '2023-05-10' },
    { id: 3, name: 'calibration.gcode', size: '28 KB', date: '2023-05-05' },
  ];

  const handleJog = (axis, direction) => {
    if (axis === 'xy') {
      // Gestion des déplacements en diagonale
      const xDir = direction.charAt(0);
      const yDir = direction.charAt(1);
      console.log(`Jog diagonal X${xDir} Y${yDir}`);
      // Ici, nous enverrions une commande au backend pour un déplacement en diagonale
    } else {
      console.log(`Jog ${axis} ${direction}`);
      // Ici, nous enverrions une commande au backend pour un déplacement simple
    }
  };

  const handleHome = () => {
    console.log('Home command');
    // Ici, nous enverrions une commande d'initialisation (homing) au backend
  };

  const renderControlTab = () => (
    <div className="p-4">
      <h3 className="text-lg font-medium mb-4">Contrôle manuel</h3>

      <div className="mb-4">
        <div className="border rounded p-2">
          <h4 className="text-sm font-medium mb-2">Contrôle des mouvements</h4>

          <div className="mb-4" style={{ maxWidth: "220px", margin: "0 auto" }}>
            {/* Première ligne: X-Y+ | Y+ | X+Y+ */}
            <div className="flex justify-between mb-2">
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={() => handleJog('xy', '-+')}
                title="X- Y+"
                style={{ width: "70px" }}
              >↖</button>
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={() => handleJog('y', '+')}
                title="Y+"
                style={{ width: "70px" }}
              >↑</button>
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={() => handleJog('xy', '++')}
                title="X+ Y+"
                style={{ width: "70px" }}
              >↗</button>
            </div>

            {/* Deuxième ligne: X- | Home | X+ */}
            <div className="flex justify-between mb-2">
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={() => handleJog('x', '-')}
                title="X-"
                style={{ width: "70px" }}
              >←</button>
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={handleHome}
                title="Home"
                style={{ width: "70px" }}
              >Home</button>
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={() => handleJog('x', '+')}
                title="X+"
                style={{ width: "70px" }}
              >→</button>
            </div>

            {/* Troisième ligne: X-Y- | Y- | X+Y- */}
            <div className="flex justify-between mb-2">
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={() => handleJog('xy', '--')}
                title="X- Y-"
                style={{ width: "70px" }}
              >↙</button>
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={() => handleJog('y', '-')}
                title="Y-"
                style={{ width: "70px" }}
              >↓</button>
              <button
                className="bg-gray-200 border border-gray-300 p-1"
                onClick={() => handleJog('xy', '+-')}
                title="X+ Y-"
                style={{ width: "70px" }}
              >↘</button>
            </div>
          </div>

          {/* Sélecteur de pas */}
          <div className="mb-2">
            <label className="text-sm font-medium">Pas (mm):</label>
            <select className="w-full p-1 border rounded mt-1">
              <option value="0.1">0.1</option>
              <option value="1">1</option>
              <option value="10">10</option>
              <option value="20" selected>20</option>
              <option value="100">100</option>
            </select>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <h4 className="text-sm font-medium mb-2">Commandes</h4>
        <div className="grid grid-cols-2 gap-2">
          <button className="btn btn-outline p-2">Reset</button>
          <button className="btn btn-outline p-2">Unlock</button>
          <button className="btn btn-danger p-2 col-span-2">Stop</button>
        </div>
      </div>
    </div>
  );

  const renderFilesTab = () => (
    <div className="p-4">
      <h3 className="text-lg font-medium mb-4">Fichiers</h3>

      <div className="mb-4">
        <button className="btn btn-primary mb-2 w-full">Importer un fichier</button>
      </div>

      <div className="border rounded">
        {demoFiles.map(file => (
          <div
            key={file.id}
            className={`p-2 border-b flex justify-between items-center cursor-pointer hover:bg-gray-100 ${activeFile?.id === file.id ? 'bg-gray-100' : ''}`}
            onClick={() => onFileSelect(file)}
          >
            <div>
              <div className="font-medium">{file.name}</div>
              <div className="text-xs text-gray-500">{file.size} • {file.date}</div>
            </div>
            <button className="btn btn-outline p-1 text-xs">Ouvrir</button>
          </div>
        ))}
      </div>
    </div>
  );

  const renderSettingsTab = () => (
    <div className="p-4">
      <h3 className="text-lg font-medium mb-4">Paramètres</h3>

      <div className="mb-4">
        <h4 className="text-sm font-medium mb-2">Paramètres de la grille</h4>
        <div className="form-group">
          <label className="form-label">Graduation (mm)</label>
          <input type="number" className="form-control" defaultValue={20} />
        </div>
        <div className="form-group">
          <label className="form-label">Position de l'origine</label>
          <select className="form-control">
            <option value="top-right">Haut droite</option>
            <option value="top-left">Haut gauche</option>
            <option value="bottom-right">Bas droite</option>
            <option value="bottom-left">Bas gauche</option>
          </select>
        </div>
      </div>

      <div className="mb-4">
        <h4 className="text-sm font-medium mb-2">Paramètres de la machine</h4>
        <div className="form-group">
          <label className="form-label">Vitesse par défaut (mm/min)</label>
          <input type="number" className="form-control" defaultValue={1000} />
        </div>
        <div className="form-group">
          <label className="form-label">Puissance laser par défaut (%)</label>
          <input type="number" className="form-control" defaultValue={50} />
        </div>
      </div>
    </div>
  );

  return (
    <div className="sidebar border-r bg-white flex flex-col" style={{ width: '250px', minWidth: '250px' }}>
      <div className="tabs flex border-b">
        <button
          className={`flex-1 p-1 text-xs ${activeTab === 'control' ? 'border-b-2 border-primary' : ''}`}
          onClick={() => setActiveTab('control')}
        >
          Contrôle
        </button>
        <button
          className={`flex-1 p-1 text-xs ${activeTab === 'files' ? 'border-b-2 border-primary' : ''}`}
          onClick={() => setActiveTab('files')}
        >
          Fichiers
        </button>
        <button
          className={`flex-1 p-1 text-xs ${activeTab === 'settings' ? 'border-b-2 border-primary' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          Paramètres
        </button>
      </div>

      <div className="flex-1 overflow-auto">
        {activeTab === 'control' && renderControlTab()}
        {activeTab === 'files' && renderFilesTab()}
        {activeTab === 'settings' && renderSettingsTab()}
      </div>
    </div>
  );
};

export default Sidebar;
