# src/config.py
import numpy as np

# -------------------------------------------------------------
# APP SETTINGS
# -------------------------------------------------------------
APP_TITLE = "SpatialCP — Spatial Cellular Pharmacokinetics"
APP_DESCRIPTION = "Agentic workflow for spatial diffusion and response modeling in tissue microenvironments."
VERSION = "1.0.0"

# -------------------------------------------------------------
# VISUALIZATION SETTINGS (Dark Mode / Biotech Vibe)
# -------------------------------------------------------------
COLOR_THEME = {
    "background": "#0E1117", # Charcoal / Deep Space
    "text": "#FAFAFA",
    "primary": "#AAF0D1",    # Magic Mint
    "secondary": "#0892D0",  # Rich Electric Blue
    "danger": "#FF4444",
    "grid": "#49494B"        # Onyx
}
CELL_TYPE_COLORS = {
    "Cancer": "#39FF14",      # Bright neon green
    "Immune": "#FF00FF",      # Magenta
    "Stroma": "#0047FF",      # DAPI Blue
    "Endothelial": "#FFA500", # Orange
    "Necrotic": "#4B5563"     # Gray
}

# -------------------------------------------------------------
# DEFAULT DIFFUSION PARAMETERS
# -------------------------------------------------------------
SIMULATION_CONFIG = {
    "default_diffusion_coefficient": 0.05,
    "default_decay_rate": 0.01,
    "default_iterations": 50,
    "anisotropy_factor": 0.8, # degree of directional dependence
}

# -------------------------------------------------------------
# BIOLOGICAL HEURISTICS & RESISTANCE MAPPING
# -------------------------------------------------------------
# Resistance modifiers effectively decrease the diffusion coefficient locally.
TISSUE_RESISTANCE = {
    "Cancer": 1.2,        # High cell density, higher resistance
    "Immune": 0.9,        # Moderate
    "Stroma": 1.5,        # Dense ECM, high resistance barrier
    "Endothelial": 0.5,   # Source of drug, extremely permeable
    "Necrotic": 0.8       # Loose tissue, lower resistance
}

# -------------------------------------------------------------
# CELL-TYPE SENSITIVITY WEIGHTS (Response Modeling)
# -------------------------------------------------------------
# Base sensitivity of cell types to the simulated agent.
# > 1.0 means highly sensitive
# < 1.0 means resistant
SENSITIVITY_WEIGHTS = {
    "Cancer": 1.5,       # Target cells
    "Immune": 0.6,       # Off-target, relatively robust
    "Stroma": 0.3,       # Highly resistant support cells
    "Endothelial": 0.8,  # Moderate off-target effects
    "Necrotic": 0.0      # Already dead, no response
}

# -------------------------------------------------------------
# THRESHOLDS
# -------------------------------------------------------------
THRESHOLDS = {
    "high_response": 0.7,
    "low_response": 0.2,
    "high_exposure": 0.6
}
