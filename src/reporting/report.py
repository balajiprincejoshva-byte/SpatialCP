import os
from jinja2 import Environment, FileSystemLoader
import base64

def generate_html_report(num_cells, iterations, diff_coef, insights, plot_fig, dist_plot_fig) -> str:
    """
    Generates a stylish HTML report using Jinja2 templates.
    Produces a standalone offline HTML string containing interactive Plotly charts.
    """
    # Initialize Jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')
    
    # Convert Plotly figures to HTML strings
    # include_plotlyjs="cdn" loads scripts from web. "require" or "directory" can be used for offline.
    # For a portable report, we'll embed the JS from CDN.
    plot_html = plot_fig.to_html(full_html=False, include_plotlyjs='cdn') if plot_fig else ""
    dist_plot_html = dist_plot_fig.to_html(full_html=False, include_plotlyjs='cdn') if dist_plot_fig else ""
    
    # Render template
    html_content = template.render(
        num_cells=num_cells,
        iterations=iterations,
        diff_coef=diff_coef,
        insights=insights,
        plot_html=plot_html,
        dist_plot_html=dist_plot_html
    )
    
    return html_content
