import pandas as pd
import numpy as np

def generate_synthetic_spatial_data(num_cells=2000, seed=42):
    """
    Generates a biologically-inspired synthetic spatial transcriptomics dataset.
    Simulates a tumor microenvironment.
    """
    np.random.seed(seed)
    
    # 1. Generate coordinates in a 100x100 grid space
    x = np.random.uniform(0, 100, num_cells)
    y = np.random.uniform(0, 100, num_cells)
    
    df = pd.DataFrame({'x': x, 'y': y})
    
    # 2. Define center of the "tumor"
    center_x, center_y = 50, 50
    distances = np.sqrt((df['x'] - center_x)**2 + (df['y'] - center_y)**2)
    
    # 3. Assign cell types based on spatial rules
    cell_types = []
    for d in distances:
        if d < 15:
            # Core: Necrotic & Cancer
            ctype = np.random.choice(['Necrotic', 'Cancer'], p=[0.4, 0.6])
        elif d < 35:
            # Margin: High Cancer, some Stroma, very little Immune
            ctype = np.random.choice(['Cancer', 'Stroma', 'Immune'], p=[0.7, 0.2, 0.1])
        elif d < 45:
            # Infiltration Zone: Stroma, Immune, some Cancer escapes
            ctype = np.random.choice(['Stroma', 'Immune', 'Cancer'], p=[0.5, 0.4, 0.1])
        else:
            # Normal adjacent / healthy: Stroma, Endothelial, scattered Immune
            ctype = np.random.choice(['Stroma', 'Endothelial', 'Immune'], p=[0.7, 0.2, 0.1])
        cell_types.append(ctype)
        
    df['cell_type'] = cell_types
    
    # 4. Simulate Marker Expression (e.g., Target Antigen, Exhaustion Marker)
    # Target Antigen (high in cancer)
    df['marker_Target_Antigen'] = np.where(
        df['cell_type'] == 'Cancer',
        np.random.normal(0.8, 0.1, num_cells),
        np.random.normal(0.2, 0.1, num_cells)
    )
    
    # Resistance Marker (high in stroma)
    df['marker_Resistance'] = np.where(
        df['cell_type'] == 'Stroma',
        np.random.normal(0.7, 0.1, num_cells),
        np.random.normal(0.1, 0.1, num_cells)
    )
    
    # Clip markers to [0, 1]
    for col in df.columns:
        if col.startswith('marker_'):
            df[col] = np.clip(df[col], 0, 1)

    # 5. Add a source distance (Distance to nearest endothelial cell for baseline diffusion)
    # This simulates proximity to blood vessels
    endothelial_points = df[df['cell_type'] == 'Endothelial'][['x', 'y']].values
    if len(endothelial_points) > 0:
        # Distance to closest endothelial
        coords = df[['x', 'y']].values
        # Broadcasting to find min distance
        dist_matrix = np.linalg.norm(coords[:, np.newaxis] - endothelial_points, axis=2)
        df['distance_to_vessel'] = np.min(dist_matrix, axis=1)
    else:
        df['distance_to_vessel'] = 50.0 # Default fallback
        
    return df
