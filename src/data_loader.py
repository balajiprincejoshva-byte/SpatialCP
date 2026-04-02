import pandas as pd
import io
from .validation import validate_spatial_dataframe

def load_data_from_upload(uploaded_file) -> pd.DataFrame:
    """
    Loads data from Streamlit uploaded file (CSV).
    Raises ValueError if validation fails.
    """
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        raise ValueError(f"Could not read CSV file: {e}")
        
    is_valid, msg, markers = validate_spatial_dataframe(df)
    
    if not is_valid:
        raise ValueError(msg)
        
    return df
