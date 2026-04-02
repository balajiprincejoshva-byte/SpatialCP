import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter
from ..config import TISSUE_RESISTANCE, SIMULATION_CONFIG

def simulate_iterative_diffusion(
    df: pd.DataFrame, 
    source_coords: list,
    iterations: int = None,
    base_diffusion: float = None,
    decay: float = None
) -> tuple[np.ndarray, pd.DataFrame]:
    """
    Iterative spatial diffusion with decay and resistance weighting.
    Uses a grid approach to model physically plausible penetration.
    Returns the final concentration array and a history dataframe for animation.
    """
    # Use config if none provided
    if iterations is None:
        iterations = SIMULATION_CONFIG["default_iterations"]
    if base_diffusion is None:
        base_diffusion = SIMULATION_CONFIG["default_diffusion_coefficient"]
    if decay is None:
        decay = SIMULATION_CONFIG["default_decay_rate"]

    # 1. Setup Grid
    # Spatial bounds
    x_min, x_max = df['x'].min(), df['x'].max()
    y_min, y_max = df['y'].min(), df['y'].max()
    
    # Add a little padding constraint
    grid_size = 100
    x_bins = np.linspace(x_min, x_max, grid_size)
    y_bins = np.linspace(y_min, y_max, grid_size)
    
    # 2. Assign Tissue Resistance to Grid
    resistance_grid = np.ones((grid_size, grid_size))
    
    # Map cells to grid index
    df['grid_x'] = np.digitize(df['x'], x_bins) - 1
    df['grid_y'] = np.digitize(df['y'], y_bins) - 1
    
    # Ensure bounds
    df['grid_x'] = df['grid_x'].clip(0, grid_size - 1)
    df['grid_y'] = df['grid_y'].clip(0, grid_size - 1)
    
    for _, row in df.iterrows():
        ct = row['cell_type']
        res = TISSUE_RESISTANCE.get(ct, 1.0)
        # Average or assign max resistance to grid cell
        resistance_grid[row['grid_y'], row['grid_x']] = max(resistance_grid[row['grid_y'], row['grid_x']], res)
        
    # 3. Initialize Source Concentration
    concentration_grid = np.zeros((grid_size, grid_size))
    
    for sx, sy in source_coords:
        gx = np.digitize(sx, x_bins) - 1
        gy = np.digitize(sy, y_bins) - 1
        gx = np.clip(gx, 0, grid_size - 1)
        gy = np.clip(gy, 0, grid_size - 1)
        concentration_grid[gy, gx] = 1.0  # Max dose at source
        
    history_dfs = []
    # Snapshot ~10 frames for a smooth but performant animation
    snapshot_interval = max(1, iterations // 10)
    
    # 4. Iterative Diffusion via Gaussian Kernel modified by resistance
    for _ in range(iterations):
        # Continuous source
        for sx, sy in source_coords:
            gx = np.clip(np.digitize(sx, x_bins) - 1, 0, grid_size - 1)
            gy = np.clip(np.digitize(sy, y_bins) - 1, 0, grid_size - 1)
            concentration_grid[gy, gx] = 1.0 
            
        # Diffusion step (approximated by slight blur)
        diffused = gaussian_filter(concentration_grid, sigma=base_diffusion * 10)
        
        # Apply Resistance
        concentration_grid = diffused * (1.0 / resistance_grid) * (1.0 - decay)
        
        # Capture animation frame
        if _ % snapshot_interval == 0 or _ == iterations - 1:
            frame_df = df.copy()
            frame_df['pred_concentration'] = [concentration_grid[row['grid_y'], row['grid_x']] for _, row in df.iterrows()]
            # Format step string so alphanumeric sorting works reasonably well or just an integer
            frame_df['Simulation_Step'] = f"Step {_:03d}"
            history_dfs.append(frame_df)
            
    # 5. Map back to cells for final output
    final_concentrations = np.array([concentration_grid[row['grid_y'], row['grid_x']] for _, row in df.iterrows()])
        
    return final_concentrations, pd.concat(history_dfs, ignore_index=True)
