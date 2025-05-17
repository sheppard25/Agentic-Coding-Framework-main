import React, { useRef, useEffect, useState } from 'react';

const VisualizationPanel = ({ isConnected, machinePosition, activeFile }) => {
  const canvasRef = useRef(null);
  // Zoom initial beaucoup plus grand pour que la grille occupe tout l'espace
  const [zoom, setZoom] = useState(2.0);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [canvasSize, setCanvasSize] = useState({ width: 0, height: 0 });

  // Configuration de la grille
  const gridSpacing = 20; // Graduation tous les 20mm
  const gridColor = '#e0e0e0'; // Gris clair pour les lignes mineures
  const gridColorMajor = '#c0c0c0'; // Gris moyen pour les lignes majeures
  const axisColor = '#ff0000'; // Rouge pour les axes
  const machinePositionColor = '#2563eb'; // Bleu pour la position de la machine
  const labelColorX = '#0000ff'; // Bleu pour les graduations X
  const labelColorY = '#ff0000'; // Rouge pour les graduations Y

  // Taille des polices pour les graduations
  const fontSizeMajor = '12px'; // Taille pour les graduations majeures
  const fontSizeMinor = '10px'; // Taille pour les graduations mineures

  // Épaisseur des lignes (ajustée pour meilleure visibilité)
  const gridLineWidth = 0.5; // Lignes mineures
  const gridLineWidthMajor = 0.8; // Lignes majeures

  // Dimensions de la machine (basées sur les paramètres GRBL $130 et $131)
  const machineWidth = 290; // mm (basé sur $130)
  const machineHeight = 235; // mm (basé sur $131)

  // Fonction pour dessiner la grille avec origine en haut à droite, style similaire à l'image de référence
  const drawGrid = (ctx, width, height) => {
    ctx.clearRect(0, 0, width, height);

    // Définir un fond blanc pour la grille
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);

    // Calculer les dimensions de la zone de travail en pixels
    const workAreaWidth = machineWidth * zoom;
    const workAreaHeight = machineHeight * zoom;

    // Calculer la position de la grille pour qu'elle soit parfaitement centrée dans la page
    // Tout en gardant l'origine (0,0) en haut à droite de la grille
    const marginTop = 40; // Marge en haut pour le titre et les graduations
    const marginRight = 40; // Marge à droite pour les graduations

    // Calculer le centre exact de la zone de dessin
    const canvasCenterX = width / 2;
    const canvasCenterY = height / 2;

    // Positionner la grille pour qu'elle soit parfaitement centrée
    // L'origine (0,0) reste en haut à droite de la grille
    const originX = canvasCenterX + workAreaWidth / 2 - marginRight;
    const originY = canvasCenterY - workAreaHeight / 2 + marginTop;

    // Appliquer le pan
    const effectiveOriginX = originX + pan.x;
    const effectiveOriginY = originY + pan.y;

    // Calculer les limites de la grille visible
    // Ajuster gridRight pour qu'il soit exactement aligné avec la graduation 0
    const exactGridRight = effectiveOriginX;
    const gridRight = Math.round(exactGridRight) - 0.5; // Ajustement pour un trait net
    const gridTop = effectiveOriginY;
    const gridBottom = effectiveOriginY + workAreaHeight;

    // Calculer la position exacte de la graduation 300 (15 * gridSpacing)
    const exactGridLeft = gridRight - (machineWidth * zoom);
    // Arrondir pour avoir un pixel exact
    const gridLeft = Math.round(exactGridLeft) + 0.5; // Ajustement pour un trait net

    // Calculer le nombre de lignes de grille
    const numLinesX = Math.ceil(machineWidth / gridSpacing);
    const numLinesY = Math.ceil(machineHeight / gridSpacing);

    // Dessiner les lignes de la grille

    // Dessiner le cadre de la grille
    ctx.beginPath();
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = 1;

    // Utiliser directement les positions calculées pour le cadre
    // Ces positions sont déjà ajustées pour être parfaitement alignées avec les graduations
    const gridWidth = gridRight - gridLeft;

    // Dessiner le cadre
    ctx.rect(gridLeft, gridTop, gridWidth, workAreaHeight);
    ctx.stroke();

    // Stocker ces valeurs pour les utiliser dans le reste du dessin
    const adjustedGridLeft = gridLeft;
    const adjustedGridRight = gridRight;

    // Dessiner les lignes verticales
    for (let i = 0; i <= numLinesX; i++) {
      // Calculer la position exacte de chaque ligne verticale
      // Pour que la dernière ligne (i=0) soit exactement à la position adjustedGridRight
      // et la première ligne (i=numLinesX) soit exactement à la position adjustedGridLeft
      const spacing = gridWidth / numLinesX;
      const xPos = adjustedGridRight - i * spacing;
      const isMajor = i % 5 === 0;

      ctx.beginPath();
      ctx.strokeStyle = isMajor ? gridColorMajor : gridColor;
      ctx.lineWidth = isMajor ? gridLineWidthMajor : gridLineWidth;
      ctx.moveTo(xPos, gridTop);
      ctx.lineTo(xPos, gridBottom);
      ctx.stroke();

      // Ajouter les graduations X en haut (en bleu) pour chaque ligne
      const xValue = i * gridSpacing;
      ctx.fillStyle = labelColorX;
      ctx.font = isMajor ? `bold ${fontSizeMajor} Arial` : `${fontSizeMinor} Arial`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'bottom';
      ctx.fillText(xValue.toString(), xPos, gridTop - 5);
    }

    // Dessiner les lignes horizontales
    for (let i = 0; i <= numLinesY; i++) {
      // Calculer la position exacte de chaque ligne horizontale
      const spacing = workAreaHeight / numLinesY;
      const y = gridTop + i * spacing;
      const isMajor = i % 5 === 0;

      ctx.beginPath();
      ctx.strokeStyle = isMajor ? gridColorMajor : gridColor;
      ctx.lineWidth = isMajor ? gridLineWidthMajor : gridLineWidth;
      ctx.moveTo(adjustedGridLeft, y);
      ctx.lineTo(adjustedGridRight, y);
      ctx.stroke();

      // Ajouter les graduations Y à droite (en rouge) pour chaque ligne
      const yValue = i * gridSpacing;
      ctx.fillStyle = labelColorY;
      ctx.font = isMajor ? `bold ${fontSizeMajor} Arial` : `${fontSizeMinor} Arial`;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText(yValue.toString(), adjustedGridRight + 5, y);
    }

    // Dessiner les axes X et Y en rouge
    ctx.beginPath();
    ctx.strokeStyle = axisColor;
    ctx.lineWidth = 2;

    // Axe X (horizontal) - ligne rouge horizontale à Y=0
    ctx.moveTo(adjustedGridLeft, gridTop);
    ctx.lineTo(adjustedGridRight, gridTop);

    // Axe Y (vertical) - ligne rouge verticale à X=0
    ctx.moveTo(adjustedGridRight, gridTop);
    ctx.lineTo(adjustedGridRight, gridBottom);

    ctx.stroke();

    // Dessiner la position actuelle de la machine
    if (isConnected) {
      // Calculer la position de la machine dans le système de coordonnées de la grille
      // Utiliser adjustedGridRight au lieu de gridRight pour un alignement parfait avec l'axe Y
      const machineX = adjustedGridRight - machinePosition.x * zoom;
      // Utiliser gridTop pour un alignement parfait avec l'axe X
      const machineY = gridTop + machinePosition.y * zoom;

      // Dessiner un marqueur plus précis à la position de la machine
      // Cercle principal
      ctx.beginPath();
      ctx.arc(machineX, machineY, 5, 0, Math.PI * 2);
      ctx.fillStyle = machinePositionColor;
      ctx.fill();
      ctx.strokeStyle = '#000000';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Ajouter une croix au centre pour plus de précision
      ctx.beginPath();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      // Ligne horizontale
      ctx.moveTo(machineX - 3, machineY);
      ctx.lineTo(machineX + 3, machineY);
      // Ligne verticale
      ctx.moveTo(machineX, machineY - 3);
      ctx.lineTo(machineX, machineY + 3);
      ctx.stroke();

      // Ajouter un petit cercle au centre pour encore plus de précision
      ctx.beginPath();
      ctx.arc(machineX, machineY, 1, 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.fill();

      // Afficher les coordonnées de la machine avec un fond blanc pour meilleure lisibilité
      const coordText = `X: ${machinePosition.x.toFixed(2)}, Y: ${machinePosition.y.toFixed(2)}`;
      const textMetrics = ctx.measureText(coordText);
      const textHeight = 16; // Estimation de la hauteur du texte
      const padding = 4;

      // Dessiner un fond blanc avec bordure pour les coordonnées
      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.fillRect(
        machineX + 8 - padding,
        machineY + 8 - padding,
        textMetrics.width + padding * 2,
        textHeight + padding * 2
      );
      ctx.strokeStyle = '#cccccc';
      ctx.lineWidth = 1;
      ctx.strokeRect(
        machineX + 8 - padding,
        machineY + 8 - padding,
        textMetrics.width + padding * 2,
        textHeight + padding * 2
      );

      // Afficher le texte des coordonnées
      ctx.fillStyle = '#000000';
      ctx.font = '12px Arial';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';
      ctx.fillText(coordText, machineX + 8, machineY + 8);
    }

    // Dessiner le fichier actif si disponible
    if (activeFile) {
      // Ici, nous simulons juste un rectangle pour représenter le fichier
      ctx.beginPath();
      ctx.rect(gridRight - 100 * zoom, gridTop + 50 * zoom, 50 * zoom, 50 * zoom);
      ctx.strokeStyle = '#00aa00';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // Ajouter un titre pour la grille - remonté pour ne pas être dans les graduations
    ctx.fillStyle = '#0000ff'; // Bleu pour le titre
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    ctx.fillText('Zone de travail', adjustedGridLeft + workAreaWidth / 2, gridTop - 40);

    // Fin du dessin
    ctx.restore();
  };

  // Gérer le redimensionnement du canvas et centrer la vue
  useEffect(() => {
    const updateCanvasSize = () => {
      const canvas = canvasRef.current;
      if (canvas) {
        const { width, height } = canvas.getBoundingClientRect();
        canvas.width = width;
        canvas.height = height;
        setCanvasSize({ width, height });

        // Centrer la vue sur la zone de travail de la machine lors du premier chargement
        if (pan.x === 0 && pan.y === 0) {
          // La grille est déjà centrée dans la fonction de dessin
          // Pas besoin de décalage initial
          setPan({ x: 0, y: 0 });
        }
      }
    };

    updateCanvasSize();
    window.addEventListener('resize', updateCanvasSize);

    return () => {
      window.removeEventListener('resize', updateCanvasSize);
    };
  }, [zoom, machineWidth, machineHeight, pan.x, pan.y]);

  // Dessiner la grille lorsque les dépendances changent
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      drawGrid(ctx, canvas.width, canvas.height);
    }
  }, [zoom, pan, canvasSize, isConnected, machinePosition, activeFile]);

  // Gérer le zoom avec la molette de la souris
  const handleWheel = (e) => {
    // Pas besoin de preventDefault() qui cause des avertissements
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    setZoom(prevZoom => Math.max(0.1, Math.min(10, prevZoom * delta)));
  };

  // Gérer le déplacement de la grille
  const handleMouseDown = (e) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX, y: e.clientY });
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      const dx = e.clientX - dragStart.x;
      const dy = e.clientY - dragStart.y;
      setPan(prevPan => ({ x: prevPan.x + dx, y: prevPan.y + dy }));
      setDragStart({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Ajouter les gestionnaires d'événements avec l'option passive
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      // Utiliser l'option { passive: true } pour éviter les avertissements
      canvas.addEventListener('wheel', handleWheel, { passive: true });
    }

    return () => {
      if (canvas) {
        canvas.removeEventListener('wheel', handleWheel);
      }
    };
  }, []);

  return (
    <div className="visualization-panel bg-white relative" style={{ width: '100%', height: '100%', position: 'relative', overflow: 'hidden', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <canvas
        ref={canvasRef}
        className="cursor-grab"
        style={{ width: '100%', height: '100%' }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        // onWheel supprimé car géré par addEventListener
      />

      <div className="absolute bottom-4 right-4 bg-white p-2 rounded shadow">
        <button
          className="btn btn-outline p-1 mr-1"
          onClick={() => setZoom(prevZoom => Math.min(10, prevZoom * 1.2))}
        >
          +
        </button>
        <button
          className="btn btn-outline p-1 mr-1"
          onClick={() => setZoom(prevZoom => Math.max(0.1, prevZoom / 1.2))}
        >
          -
        </button>
        <button
          className="btn btn-outline p-1"
          onClick={() => {
            // Remettre le zoom à 2.0 pour une grille qui occupe tout l'espace
            setZoom(2.0);
            // Centrer la grille dans la vue
            setPan({ x: 0, y: 0 });
          }}
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default VisualizationPanel;
