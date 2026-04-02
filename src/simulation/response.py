import pandas as pd
import numpy as np
from ..config import SENSITIVITY_WEIGHTS

def compute_response(df: pd.DataFrame, concentration_col: str = "pred_concentration") -> np.ndarray:
    """
    Computes a cell-specific response score based on:
    - Predicted local drug concentration
    - Inherent cell-type sensitivity weighting
    - Expression of relevant markers (if any)
    """
    responses = []
    
    for _, row in df.iterrows():
        ct = row['cell_type']
        conc = row[concentration_col]
        
        # Base Sensitivity Modifier
        base_weight = SENSITIVITY_WEIGHTS.get(ct, 0.5)
        
        # Marker Modifiers
        # e.g., high target antigen = better response
        target_expr = row.get('marker_Target_Antigen', 0.5)
        # e.g., high resistance marker = worse response
        resistance_expr = row.get('marker_Resistance', 0.0)
        
        # Calculate score
        # Formula: (Concentration * SensitivityWeight) + Target Bonus - Resistance Penalty
        score = (conc * base_weight) * (1 + target_expr) * (1 - resistance_expr * 0.5)
        
        # Clip score between 0 and 1
        responses.append(min(max(score, 0.0), 1.0))
        
    return np.array(responses)
