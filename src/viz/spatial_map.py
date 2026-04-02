import plotly.express as px
import pandas as pd
import numpy as np
from ..config import COLOR_THEME, CELL_TYPE_COLORS

def plot_spatial_map(df: pd.DataFrame, color_col: str, title: str, is_categorical: bool = False, hover_data: list = None, animation_frame: str = None):
    """
    Generate an interactive spatial plot upgraded to 3D for spatial realism.
    """
    if 'cell_id' not in df.columns:
        df['cell_id'] = [f"Cell_{i}" for i in df.index]
        
    if 'z' not in df.columns:
        # Create deterministic Z value so frames don't jitter
        np.random.seed(42)
        unique_cells = df[['x', 'y']].drop_duplicates()
        unique_cells['z'] = np.random.normal(0, 1.5, len(unique_cells))
        df = df.merge(unique_cells, on=['x', 'y'], how='left')
        
    hover_base = ['cell_id', 'cell_type']
    if 'pred_concentration' in df.columns and 'pred_concentration' not in hover_base:
        hover_base.append('pred_concentration')
        
    hover_cols = hover_data if hover_data is not None else hover_base

    layout_args = {
        'paper_bgcolor': COLOR_THEME['background'],
        'plot_bgcolor': COLOR_THEME['background'],
        'font': {'color': COLOR_THEME['text']},
        'margin': dict(l=0, r=0, t=30, b=0)
    }

    if is_categorical:
        fig = px.scatter_3d(
            df, x='x', y='y', z='z', color=color_col,
            color_discrete_map=CELL_TYPE_COLORS,
            title=title, hover_data=hover_cols,
            animation_frame=animation_frame
        )
    else:
        # Continuous color scale suitable for dark mode
        range_c = [0, 1] if color_col == 'pred_concentration' else None
        fig = px.scatter_3d(
            df, x='x', y='y', z='z', color=color_col,
            color_continuous_scale="Viridis",
            title=title, hover_data=hover_cols,
            animation_frame=animation_frame,
            range_color=range_c
        )
        
    fig.update_traces(marker=dict(size=3, opacity=0.8, line=dict(width=0)))
    
    fig.update_layout(**layout_args)
    fig.update_layout(
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", visible=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", visible=False),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", visible=False)
        )
    )
    
    return fig
