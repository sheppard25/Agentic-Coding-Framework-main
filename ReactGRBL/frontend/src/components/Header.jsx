import React from 'react';

const Header = ({ isConnected, onConnect, onDisconnect, onUnlock }) => {
  return (
    <header className="bg-primary p-2 text-white">
      <div className="container flex justify-between items-center">
        <div className="flex items-center">
          <h1 className="text-xl font-bold">ReactGRBL Controller</h1>
        </div>

        <div className="flex items-center">
          {isConnected ? (
            <div className="flex items-center">
              <span className="mr-2 flex items-center">
                <span className="inline-block w-2 h-2 rounded-full bg-success mr-1"></span>
                Connecté
              </span>
              <button
                className="btn btn-sm btn-outline text-white border-white mr-2"
                onClick={onUnlock}
              >
                Déverrouiller ($X)
              </button>
              <button
                className="btn btn-sm btn-outline text-white border-white"
                onClick={onDisconnect}
              >
                Déconnecter
              </button>
            </div>
          ) : (
            <button
              className="btn btn-sm btn-outline text-white border-white"
              onClick={onConnect}
            >
              Connecter
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
