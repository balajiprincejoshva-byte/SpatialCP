import plotly.express as px
import pandas as pd
from ..config import COLOR_THEME, CELL_TYPE_COLORS

def plot_response_distribution(df: pd.DataFrame):
    """
    Plots the distribution of response scores, categorized by cell type.
    """
    layout_args = {
        'paper_bgcolor': COLOR_THEME['background'],
        'plot_bgcolor': COLOR_THEME['background'],
        'font': {'color': COLOR_THEME['text']},
    }
    
    fig = px.box(
        df, x='cell_type', y='response_score', color='cell_type',
        color_discrete_map=CELL_TYPE_COLORS,
        title="Cell Type Response Distributions"
    )
    
    fig.update_layout(**layout_args)
    fig.update_yaxes(gridcolor=COLOR_THEME['grid'])
    
    return fig
    
def plot_baseline_comparison(df: pd.DataFrame):
    """
    Compare baseline distance to model concentration predictions.
    """
    # Sample 10% for lighter plotting
    plot_df = df.sample(frac=0.1) if len(df) > 1000 else df
    
    fig = px.scatter(
        plot_df, x='baseline_distance', y='pred_concentration', 
        color='cell_type', color_discrete_map=CELL_TYPE_COLORS,
        title="Baseline (Distance) vs. Advanced Resistance Diffusion Strategy",
        labels={
            'baseline_distance': 'Naïve Distance Exposure',
            'pred_concentration': 'Advanced Model Exposure'
        }
    )
    
    fig.update_layout(
        paper_bgcolor=COLOR_THEME['background'],
        plot_bgcolor=COLOR_THEME['background'],
        font=dict(color=COLOR_THEME['text'])
    )
    fig.update_xaxes(gridcolor=COLOR_THEME['grid'])
    fig.update_yaxes(gridcolor=COLOR_THEME['grid'])
    
    return fig
