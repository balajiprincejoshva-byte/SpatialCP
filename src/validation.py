import pandas as pd
from typing import Tuple, List, Dict

def validate_spatial_dataframe(df: pd.DataFrame) -> Tuple[bool, str, List[str]]:
    """
    Validates the spatial dataframe.
    Requires: 'x', 'y', 'cell_type'
    Returns:
        is_valid (bool)
        message (str)
        markers (List[str]) - list of recognized marker columns
    """
    required_cols = ['x', 'y', 'cell_type']
    missing = [c for c in required_cols if c not in df.columns]
    
    if missing:
        return False, f"Missing required columns: {', '.join(missing)}", []
        
    # Check numeric coordinates
    if not pd.api.types.is_numeric_dtype(df['x']) or not pd.api.types.is_numeric_dtype(df['y']):
        return False, "'x' and 'y' columns must be numeric.", []
        
    # Find markers (columns starting with 'marker_' or any other numeric columns)
    markers = [c for c in df.columns if c not in required_cols and pd.api.types.is_numeric_dtype(df[c]) and c != "distance_to_vessel"]
    
    # Handle NaN values
    if df[required_cols].isnull().any().any():
        return False, "Data contains missing values in 'x', 'y', or 'cell_type'. Please clean data before uploading.", []
        
    return True, "Validation successful.", markers

def summarize_data(df: pd.DataFrame) -> Dict:
    """Returns a dictionary summarizing the dataset for quality checks."""
    summary = {
        "num_cells": len(df),
        "num_cell_types": df['cell_type'].nunique(),
        "cell_type_counts": df['cell_type'].value_counts().to_dict(),
        "x_range": (float(df['x'].min()), float(df['x'].max())),
        "y_range": (float(df['y'].min()), float(df['y'].max())),
    }
    return summary
