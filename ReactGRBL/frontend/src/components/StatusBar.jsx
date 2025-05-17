import React from 'react';

const StatusBar = ({ isConnected, machineStatus, machinePosition }) => {
  return (
    <div className="status-bar bg-gray-100 border-t p-1 flex justify-between items-center text-xs">
      <div className="flex items-center">
        <div className="mr-4">
          <span className="text-xs font-medium mr-1">État:</span>
          <span className={`text-xs ${machineStatus === 'Idle' ? 'text-success' : 'text-warning'}`}>
            {isConnected ? machineStatus : 'Non connecté'}
          </span>
        </div>

        {isConnected && (
          <div className="flex space-x-4">
            <div>
              <span className="text-xs font-medium mr-1">X:</span>
              <span className="text-xs font-mono">{machinePosition.x.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-xs font-medium mr-1">Y:</span>
              <span className="text-xs font-mono">{machinePosition.y.toFixed(2)}</span>
            </div>
          </div>
        )}
      </div>

      <div>
        <span className="text-xs text-gray-500">ReactGRBL Controller v1.0.0</span>
      </div>
    </div>
  );
};

export default StatusBar;
