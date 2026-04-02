import numpy as np
import pandas as pd
from typing import Tuple

def compute_uniform_baseline(df: pd.DataFrame, source_intensity: float = 1.0) -> np.ndarray:
    """
    Uniform distribution baseline. Assumes perfect, instant penetration
    ignoring all spatial and tissue barriers.
    """
    return np.ones(len(df)) * source_intensity

def compute_distance_baseline(df: pd.DataFrame, source_coords: list, decay_rate: float = 0.05) -> np.ndarray:
    """
    Distance-only baseline. Predicts concentration solely based on Euclidean distance
    from the drug source, ignoring tissue resistance and heterogeneity.
    """
    coords = df[['x', 'y']].values
    
    # If multiple sources, compute min distance to any source
    dist_matrix = np.linalg.norm(coords[:, np.newaxis] - source_coords, axis=2)
    min_distances = np.min(dist_matrix, axis=1)
    
    # Exponential decay based on distance
    concentration = np.exp(-decay_rate * min_distances)
    return concentration
