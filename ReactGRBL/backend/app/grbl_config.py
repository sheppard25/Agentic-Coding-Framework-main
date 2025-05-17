"""
Configuration GRBL pour le contrôleur ReactGRBL.
Ce fichier contient les paramètres spécifiques à la machine de l'utilisateur.
"""

# Paramètres GRBL de la machine
GRBL_PARAMETERS = {
    "$0": "10",       # Step pulse time, microseconds
    "$1": "25",       # Step idle delay, milliseconds
    "$2": "3",        # Step pulse invert, mask
    "$3": "2",        # Step direction invert, mask
    "$4": "0",        # Invert step enable pin, boolean
    "$5": "1",        # Invert limit pins, boolean
    "$6": "0",        # Invert probe pin, boolean
    "$10": "0",       # Status report options, mask
    "$11": "0.010",   # Junction deviation, millimeters
    "$12": "0.002",   # Arc tolerance, millimeters
    "$13": "0",       # Report in inches, boolean
    "$20": "1",       # Soft limits enable, boolean
    "$21": "1",       # Hard limits enable, boolean
    "$22": "1",       # Homing cycle enable, boolean
    "$23": "3",       # Homing direction invert, mask
    "$24": "2500.000", # Homing locate feed rate, mm/min
    "$25": "1000.000", # Homing search seek rate, mm/min
    "$26": "200.000", # Homing switch debounce delay, milliseconds
    "$27": "1.500",   # Homing switch pull-off distance, millimeters
    "$28": "1000.000", # G73 retract distance, millimeters
    "$30": "1000.000", # Maximum spindle speed, RPM
    "$31": "0.000",   # Minimum spindle speed, RPM
    "$32": "1",       # Laser mode enable, boolean
    "$38": "0",       # Spindle PWM frequency, Hz
    "$40": "1",       # Spindle PWM behavior, boolean
    "$100": "401.020", # X-axis steps per millimeter
    "$101": "406.480", # Y-axis steps per millimeter
    "$102": "1.000",  # Z-axis steps per millimeter
    "$103": "100.000", # A-axis steps per millimeter
    "$104": "100.000", # B-axis steps per millimeter
    "$105": "100.000", # C-axis steps per millimeter
    "$110": "5000.000", # X-axis maximum rate, mm/min
    "$111": "5000.000", # Y-axis maximum rate, mm/min
    "$112": "500.000", # Z-axis maximum rate, mm/min
    "$113": "1000.000", # A-axis maximum rate, mm/min
    "$114": "1000.000", # B-axis maximum rate, mm/min
    "$115": "1000.000", # C-axis maximum rate, mm/min
    "$120": "1000.000", # X-axis acceleration, mm/sec^2
    "$121": "1000.000", # Y-axis acceleration, mm/sec^2
    "$122": "1300.000", # Z-axis acceleration, mm/sec^2
    "$123": "300.000", # A-axis acceleration, mm/sec^2
    "$124": "300.000", # B-axis acceleration, mm/sec^2
    "$125": "300.000", # C-axis acceleration, mm/sec^2
    "$130": "290.000", # X-axis maximum travel, millimeters
    "$131": "235.000", # Y-axis maximum travel, millimeters
    "$132": "0.000",  # Z-axis maximum travel, millimeters
    "$133": "0.000",  # A-axis maximum travel, millimeters
    "$134": "0.000",  # B-axis maximum travel, millimeters
    "$135": "0.000",  # C-axis maximum travel, millimeters
}

# Commandes d'initialisation standard à envoyer après la configuration
INIT_COMMANDS = [
    "$X",           # Déverrouiller
    "G21",          # Mode millimètres
    "G90",          # Mode absolu
    "M5",           # Laser off
    "M3 S0"         # Laser on mais puissance à 0
]

# Dimensions de la zone de travail (en mm)
WORK_AREA = {
    "width": 290.0,  # Basé sur $130
    "height": 235.0  # Basé sur $131
}

# Position de l'origine par défaut
DEFAULT_ORIGIN = "top-right"

# Espacement de la grille par défaut (en mm)
DEFAULT_GRID_SPACING = 20

# Vitesse d'avance par défaut (en mm/min)
DEFAULT_FEED_RATE = 1000

# Puissance du laser par défaut (0-1000)
DEFAULT_LASER_POWER = 50

def get_grbl_config_commands():
    """
    Retourne la liste des commandes de configuration GRBL.
    
    Returns:
        list: Liste des commandes de configuration GRBL
    """
    return [f"{param}={value}" for param, value in GRBL_PARAMETERS.items()]
