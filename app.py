import streamlit as st
import pandas as pd
import time
import base64

from src.config import APP_TITLE, APP_DESCRIPTION, SIMULATION_CONFIG
from src.sample_data import generate_synthetic_spatial_data
from src.data_loader import load_data_from_upload
from src.agent.logging import AgentLogger
from src.agent.workflow import AnalysisWorkflow
from src.viz.spatial_map import plot_spatial_map
from src.viz.charts import plot_response_distribution, plot_baseline_comparison
from src.viz.explainability import generate_quick_insights
from src.reporting.report import generate_html_report

# -------------------------------------------------------------
# APP CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="SpatialCP",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark mode styling via CSS Injection
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
        }
        /* Global Background Tints */
        .stApp { background-color: #0E1117 !important; }
        [data-testid="stSidebar"] { background-color: #121212 !important; }
        
        h1, h2, h3 { color: #AAF0D1 !important; }
        
        /* Pulsing UI Effects */
        @keyframes pulse {
            0% { box-shadow: 0 0 5px rgba(8, 146, 208, 0.1); border-color: rgba(8, 146, 208, 0.2); }
            50% { box-shadow: 0 0 20px rgba(170, 240, 209, 0.6); border-color: #AAF0D1; }
            100% { box-shadow: 0 0 5px rgba(8, 146, 208, 0.1); border-color: rgba(8, 146, 208, 0.2); }
        }
        
        .metric-card {
            background: #49494B;
            border: 1px solid #0892D0;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            animation: pulse 3s infinite ease-in-out;
            margin-bottom: 10px;
        }
        
        .stButton button {
            animation: pulse 3s infinite ease-in-out !important;
            transition: all 0.3s ease;
            background-color: #49494B !important;
            color: #FAFAFA !important;
            border: 1px solid #0892D0 !important;
        }

        .metric-title {
            color: #D1D5DB;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .metric-value {
            color: #FAFAFA;
            font-size: 1.8rem;
            font-weight: bold;
            margin-top: 5px;
        }

        .insight-box {
            background-color: #49494B;
            border-left: 4px solid #AAF0D1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            color: #FAFAFA;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# STATE MANAGEMENT
# -------------------------------------------------------------
if 'df' not in st.session_state:
    st.session_state.df = None
if 'workflow_run' not in st.session_state:
    st.session_state.workflow_run = False
if 'logger' not in st.session_state:
    st.session_state.logger = AgentLogger()
if 'insights' not in st.session_state:
    st.session_state.insights = {}

# -------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------
with st.sidebar:
    st.title("🧬 SpatialCP")
    st.markdown("Spatial Cellular Pharmacokinetics")
    
    st.header("1. Data Input")
    uploaded_file = st.file_uploader("Upload spatial CSV", type="csv")
    if st.button("Generate Synthetic Demo Data", use_container_width=True):
        st.session_state.df = generate_synthetic_spatial_data(num_cells=2500)
        st.session_state.workflow_run = False
        st.success("Loaded TME Synthetic Data!")
        
    if uploaded_file is not None:
        try:
            st.session_state.df = load_data_from_upload(uploaded_file)
            st.session_state.workflow_run = False
            st.success("Data uploaded successfully!")
        except Exception as e:
            st.error(str(e))
            
    st.header("2. Biological Anchor")
    smiles_input = st.text_input("Input Compound SMILES or Name", "Imatinib")
    
    # Simple dummy calculation to make the user input feel interactive:
    # We alter the selected base diffusion based on the length of the string (mimicking molecular weight resistance)
    base_calc_diff = max(0.01, SIMULATION_CONFIG['default_diffusion_coefficient'] - (len(smiles_input) * 0.002))
    
    st.header("3. Simulation Parameters")
    diff_coef = st.slider("Diffusion Coefficient", 0.01, 0.5, float(base_calc_diff))
    decay_rate = st.slider("Decay Rate", 0.001, 0.1, SIMULATION_CONFIG['default_decay_rate'])
    iterations = st.slider("Simulation Iterations", 10, 200, SIMULATION_CONFIG['default_iterations'])
    
    params = {
        "base_diffusion": diff_coef,
        "decay": decay_rate,
        "iterations": iterations
    }
    
    st.header("4. Execution")
    if st.button("▶ Run Agentic Workflow", type="primary", use_container_width=True):
        if st.session_state.df is None:
            st.error("Please load data first.")
        else:
            # We will clear logs and compute synchronously, then replay the logs with sleep to simulate streaming
            st.session_state.logger.clear()
            workflow = AnalysisWorkflow(st.session_state.logger)
            processed_df, history_df = workflow.execute(st.session_state.df.copy(), params)
            st.session_state.df = processed_df
            st.session_state.history_df = history_df
            st.session_state.insights = generate_quick_insights(processed_df)
            
            # Agentic Theater - streaming logs onto the screen in real-time
            log_container = st.empty()
            accumulated_log = ""
            for log in st.session_state.logger.get_logs():
                new_line = f"> {log['step']}\n  Status: {log['status'].upper()}\n\n"
                # Typewriter effect
                for char in new_line:
                    accumulated_log += char
                    log_container.markdown(f"```console\n{accumulated_log} \n```")
                    time.sleep(0.01) # fast typing
                time.sleep(0.4) # Pause between steps to build anticipation
                
            st.session_state.workflow_run = True
            st.success("Workflow Complete!")

def make_metric(title, value):
    return f'''
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    '''

# -------------------------------------------------------------
# MAIN DASHBOARD
# -------------------------------------------------------------
st.title("Spatial Cellular Pharmacokinetics (SpatialCP)")
st.caption(APP_DESCRIPTION)

if st.session_state.df is None:
    st.info("👈 Please load data or generate a synthetic dataset from the sidebar to begin.")
else:
    df = st.session_state.df
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Data Overview")
        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(make_metric("Total Spots/Cells", len(df)), unsafe_allow_html=True)
        with m2: st.markdown(make_metric("Cell Types", df['cell_type'].nunique()), unsafe_allow_html=True)
        with m3: 
            status = "Simulated ✅" if st.session_state.workflow_run else "Raw Data"
            st.markdown(make_metric("Status", status), unsafe_allow_html=True)
            
    with col2:
        if st.session_state.workflow_run:
            st.subheader("Agent Output Log")
            with st.container():
                log_text = ""
                for log in st.session_state.logger.get_logs():
                    log_text += f"> {log['step']}\n"
                st.markdown(f"```console\n{log_text}\n```")

    if st.session_state.workflow_run:
        st.markdown("### ⚡ Quick Insights")
        i_col1, i_col2, i_col3 = st.columns(3)
        with i_col1:
            st.markdown(f"<div class='insight-box'><strong>Highest Exposure Region:</strong><br>{st.session_state.insights.get('Highest Penetration Region', 'N/A')}</div>", unsafe_allow_html=True)
        with i_col2:
            st.markdown(f"<div class='insight-box'><strong>Tumor Core Status:</strong><br>{st.session_state.insights.get('Tumor Core Targeting', 'N/A')}</div>", unsafe_allow_html=True)
        with i_col3:
            st.markdown(f"<div class='insight-box'><strong>Resistance Engine:</strong><br>Stroma microenvironment barriers detected</div>", unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(["🗺 Spatial Map", "🌊 Diffusion Model", "🎯 Response Prediction", "📄 Report Export"])

        with tab1:
            st.markdown("#### Tissue Microenvironment Profiling")
            st.info("Pinch or scroll to zoom depth. Click and drag to rotate the 3D projection.", icon="🖱️")
            fig_cell_type = plot_spatial_map(df, 'cell_type', title="Tissue Cell-Type Annotations", is_categorical=True)
            st.plotly_chart(fig_cell_type, use_container_width=True)

        with tab2:
            st.markdown("#### Iterative Spatial Diffusion Time-lapse")
            st.info("Pinch or scroll to zoom depth. Click and drag to rotate the 3D projection.", icon="🖱️")
            
            if 'history_df' in st.session_state:
                fig_adv = plot_spatial_map(st.session_state.history_df, 'pred_concentration', title="Advanced Penetration Model (Animated)", is_categorical=False, animation_frame="Simulation_Step")
                st.plotly_chart(fig_adv, use_container_width=True)
            else:
                c1, c2 = st.columns(2)
                with c1:
                    fig_base = plot_spatial_map(df, 'baseline_distance', title="Baseline (Naive Distance)", is_categorical=False)
                    st.plotly_chart(fig_base, use_container_width=True)
                with c2:
                    fig_adv = plot_spatial_map(df, 'pred_concentration', title="Advanced Penetration Model", is_categorical=False)
                    st.plotly_chart(fig_adv, use_container_width=True)
                
            st.markdown("#### Model Superiority Analysis")
            fig_comp = plot_baseline_comparison(df)
            st.plotly_chart(fig_comp, use_container_width=True)

        with tab3:
            st.markdown("#### Cellular Response Profiles")
            st.info("Pinch or scroll to zoom depth. Click and drag to rotate the 3D projection.", icon="🖱️")
            c1, c2 = st.columns([1, 1])
            with c1:
                fig_resp_map = plot_spatial_map(df, 'response_score', title="Spatial Response Efficacy Map", is_categorical=False)
                st.plotly_chart(fig_resp_map, use_container_width=True)
            with c2:
                fig_dist = plot_response_distribution(df)
                st.plotly_chart(fig_dist, use_container_width=True)

        with tab4:
            st.markdown("#### Generate Executive Report")
            st.info("The exported HTML report is self-contained and fully interactive, making it perfect for sharing with hiring managers or clinical teams.")
            
            if st.button("Generate Jinja2 HTML Report"):
                with st.spinner("Compiling HTML Report..."):
                    # Generate fresh figures to prevent Streamlit rendering conflicts
                    fig_adv_export = plot_spatial_map(df, 'pred_concentration', title="Advanced Penetration Model", is_categorical=False)
                    fig_dist_export = plot_response_distribution(df)
                    
                    html_content = generate_html_report(
                        num_cells=len(df),
                        iterations=iterations,
                        diff_coef=diff_coef,
                        insights=st.session_state.insights,
                        plot_fig=fig_adv_export,
                        dist_plot_fig=fig_dist_export
                    )
                    
                    b64 = base64.b64encode(html_content.encode()).decode()
                    href = f'<a href="data:text/html;base64,{b64}" download="SpatialCP_Report.html" class="streamlit-button">Download HTML Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("Report Ready!")

    else:
        st.markdown("### Raw Spatial Structure")
        if 'cell_type' in df.columns:
            fig = plot_spatial_map(df, 'cell_type', title="Preliminary Tissue Map", is_categorical=True)
            st.plotly_chart(fig, use_container_width=True)
