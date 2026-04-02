# SpatialCP 🧬 — Spatial Cellular Pharmacokinetics

![SpatialCP Overview](https://img.shields.io/badge/Status-Prototype-00FFC6?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge) ![Streamlit](https://img.shields.io/badge/Streamlit-Dark_Mode-A855F7?style=for-the-badge)

**SpatialCP** is an interactive, agent-orchestrated decision-support platform designed to model drug diffusion and predict cell-specific pharmacodynamic responses within complex tumor microenvironments (TMEs) using **Spatial Transcriptomics** (ST) data.

This project bridges software engineering, computational biology, and medicinal chemistry to provide actionable heuristics for early-stage drug candidate screening and tissue penetrance modeling.

## 🔬 Motivation & Biological Use Case
In solid tumors, localized regions (like dense desmoplastic stroma) prevent therapeutic molecules from penetrating the tumor core, leading to varied cellular exposure and resistance. Standard bulk RNA-seq or single-cell sequencing cannot map these spatial barriers.

**SpatialCP solves this by:**
1. **Inferring Spatial Barriers:** Reading spatial transcriptomics coordinates and cell-type annotations to build a tissue resistance matrix.
2. **Advanced Diffusion Modeling:** Moving beyond naive distance-decay models to simulate iterative spatial diffusion constrained by localized ECM/stromal density.
3. **Response Prediction:** Weighting predicted local drug concentration with intrinsic cell-type sensitivities and baseline marker expression (e.g., target antigens).
4. **Agentic Explanations:** Wrapping the analysis in a deterministic agentic workflow that logs execution traces, verifies inputs, and highlights "tumor core barriers" robustly.

## 🚀 Key Features
- **Synthetic TME Generator:** Generates an immediate built-in bio-mimetic spatial dataset to demonstrate functionality without requiring external `.h5ad` or `.csv` files.
- **Dynamic Parameter Sensitivities:** Interactive UI altering the Diffusion Coefficient, Decay Rate, and Iterations on-the-fly.
- **Tissue Resistance Matrix mapping.**
- **Baseline Comparisons:** Visually compare naive distance models against advanced heterogeneous resistance models.
- **Explainable AI (XAI):** "Quick Insights" intelligently isolate the most targeted regions and resistant subtypes.
- **Downloadable XAI Reports:** Generates polished HTML reports natively embedding interactive Plotly components utilizing a custom Jinja2 rendering pipeline.

## 🛠️ Tech Stack & Architecture
- **Language**: Python 3.10
- **Frontend / Application Engine**: Streamlit (Dark Mode enabled via CSS injection)
- **Data & Computation**: Pandas, NumPy, SciPy (for Gaussian kernel convolution and distance broadcasting)
- **Visualization**: Plotly Express (scatter, box charts)
- **Reporting**: Jinja2 (HTML/CSS Templating)
- **Deployment**: Dockerized

### Directory Structure
```bash
SpatialCP/
├── app.py                     # Main Streamlit Dashboard Entry
├── requirements.txt           # Python Environment
├── Dockerfile                 # Container Deployment
├── src/
│   ├── config.py              # Constants, Tuning Parameters, Aesthetic colors
│   ├── data_loader.py         # CSV Parsing & Ingestion
│   ├── sample_data.py         # Generates Synthetic Tumor Microenvironment
│   ├── validation.py          # Input Schema Enforcement
│   ├── simulation/            # Core Analytical Engines
│   │   ├── baselines.py       # Distance and Uniform implementations
│   │   ├── diffusion.py       # Iterative Resistance Diffusion Model
│   │   └── response.py        # PD Response scoring logic
│   ├── agent/                 # Workflow Orchestrator
│   │   ├── workflow.py        # Deterministic Multi-Step Execution
│   │   └── logging.py         # Agent Logging Footprint
│   ├── viz/
│   │   ├── charts.py          # Distribution plotting
│   │   ├── explainability.py  # Quick Insight Heuristics
│   │   └── spatial_map.py     # Interactive Plotly Generation
│   └── reporting/
│       └── report.py          # Jinja2 HTML rendering
└── templates/                 # Contains report_template.html XAI Layout
```

## 💻 How to Run Locally

Using **Python virtual environment**:
```bash
# 1. Clone repo
git clone https://github.com/yourusername/SpatialCP.git
cd SpatialCP

# 2. Install Dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Launch App
streamlit run app.py
```

Using **Docker**:
```bash
docker build -t spatialcp .
docker run -p 8501:8501 spatialcp
```

Go to `http://localhost:8501` in your browser.

## ⚠️ Assumptions & Limitations
- **2D Slice Constraints**: Current ST methodologies mostly provide 2D slices. 3D spatial extrapolation represents an adjacent opportunity.
- **Simplified Graph/Grid Convolution**: Heat equation models proxy diffusion but ignore active transport mechanisms (e.g., P-gp efflux pumps) unless explicitly mapped by transcript markers.
- **Heuristic Cellular Response**: Response predictions dynamically multiply local drug concentrations with inferred sensitivity constants. This is a robust framework, but the constant values themselves are demonstrative and would require *in vitro* calibration (e.g. from highly multiplexed viability screens) for clinical inference.

## 🔮 Future Enhancements
- **Spatial Autocorrelation metrics** (Moran's I) to statistically test the clustering of response predictions.
- **Native Scanpy/AnnData support** for `.h5ad` ingestion directly from standard bioinformatics pipelines.
- **Parallel processing** via `Dask` when scaling point-clouds beyond millions of cells encompassing whole-slide imaging.
