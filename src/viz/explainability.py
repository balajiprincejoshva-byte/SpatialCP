import pandas as pd
from typing import Dict, Any

def generate_quick_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes summary insights to be displayed dynamically in the UI.
    """
    insights = {}
    
    # Highest penetration region
    # Dividing the 100x100 grid into 4 quadrants
    if 'x' in df.columns and 'y' in df.columns and 'pred_concentration' in df.columns:
        df['quadrant'] = 'Top-Left'
        df.loc[(df['x'] > 50) & (df['y'] <= 50), 'quadrant'] = 'Bottom-Right'
        df.loc[(df['x'] <= 50) & (df['y'] > 50), 'quadrant'] = 'Bottom-Left'
        df.loc[(df['x'] > 50) & (df['y'] > 50), 'quadrant'] = 'Top-Right'
        
        top_quad = df.groupby('quadrant')['pred_concentration'].mean().idxmax()
        insights['Highest Penetration Region'] = top_quad

    if 'response_score' in df.columns and 'cell_type' in df.columns:
        mean_responses = df.groupby('cell_type')['response_score'].mean()
        most_sensitive = mean_responses.idxmax()
        most_resistant = mean_responses.idxmin()
        insights['Most Sensitive Cell Type'] = most_sensitive
        insights['Most Resistant Cell Type'] = most_resistant
        
        target_cells = df[df['cell_type'] == 'Cancer']
        if not target_cells.empty:
            avg_cancer_exposure = target_cells['pred_concentration'].mean()
            if avg_cancer_exposure < 0.3:
                insights['Tumor Core Targeting'] = 'Low Exposure (Diffusion Barrier Active)'
            elif avg_cancer_exposure < 0.6:
                insights['Tumor Core Targeting'] = 'Moderate Exposure'
            else:
                insights['Tumor Core Targeting'] = 'High Exposure'
                
    return insights
