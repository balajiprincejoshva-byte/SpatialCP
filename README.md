# SpatialCP 🧬: Agentic Modeling of Cellular Pharmacokinetics in Spatial Transcriptomics

![SpatialCP Status](https://img.shields.io/badge/Status-Proprietary_Prototype-0892D0?style=for-the-badge) ![Architecture](https://img.shields.io/badge/Agentic-Orchestration-AAF0D1?style=for-the-badge) ![Deployment](https://img.shields.io/badge/Deployed-Streamlit_Cloud-191970?style=for-the-badge)

**SpatialCP** (Spatial Cellular Pharmacokinetics) is an enterprise-grade, agent-orchestrated decision-support architecture. It bridges modern Spatial Transcriptomics (ST) and *in silico* mass transport modeling to predict and overcome physical drug resistance within the Tumor Microenvironment (TME). 

By simulating localized target exposure against mapped stromal barriers, SpatialCP computes cell-specific pharmacodynamic (PD) response probabilities at single-cell resolution.

---

## 🎥 Agentic Workflow Demonstration
<!-- DROP YOUR DEMO VIDEO OR GIF RIGHT HERE -->
*[Replace this line with your video file link or embedded GIF]*

*(Demonstrating real-time 3D interactive diffusion bounds, time-lapse physics, and streaming agent orchestration).*

---

## 🔬 Executive Summary: The Spatial Biology Defense Mechanism
In solid tumors, localized desmoplastic stroma and dense extracellular matrix (ECM) often prevent small molecules and biologics from sufficiently penetrating the tumor core. Standard bulk RNA-seq or dissociated single-cell sequencing cannot capture these micro-anatomical barriers, routinely resulting in clinical trial failures due to unpredicted physical obstruction rather than intrinsic target resistance.

**SpatialCP solves this architectural blind spot:**
1. **Inferring Physical Barriers:** Ingesting spatial coordinates and multiplexed annotations to compile an actionable 2D/3D tissue resistance matrix.
2. **Iterative Spatial Diffusion Engine:** Moving far beyond uniform biological assumptions by simulating physiologically accurate molecular distributions using dampening Gaussian kernels, heavily constrained by local stromal density.
3. **Agentic Orchestration:** Utilizing specialized analytical personas (`[Agent: Spatial Mapper]`, `[Agent: Physicist]`, `[Agent: Pharmacologist]`) to execute deterministic, sequential computations on the coordinate data. This guarantees auditability, yielding transparent validation logs identical to clinical software standards.
4. **Deterministic XAI:** Outputting instantaneous insights and downloadable, interactive HTML telemetry reports to bridge the gap between computational biologists and clinical decision-makers.

## 🚀 Architectural & Methodological Highlights

### Multiplexed Immunofluorescence (IF) Emulation
The visual engine Abandons generic data-science plotting in favor of custom-styled 3D point-cloud renderings mimicking multiplexed tissue staining (e.g., DAPI Stroma, Neon Target-Cancer clusters, Magenta Immune populations) suspended against a true dark-field `#0E1117` microscopy canvas.

### The Physics Sandbox
Users are biologically anchored by inputting compound nomenclature (e.g. "Imatinib"), triggering automated logic that scales estimated molecular weight resistance against diffusion coefficients. The resulting penetration time-lapse animates the physical spread and decay of the agent through the 3D tumor mass, explicitly contrasting naïve uniform exposure against advanced ECM-resisted exposure.

## 💻 Deployment & Usage

### 🌐 Live Hosted Version
This platform is deployed securely via Streamlit Community Cloud. 
**Access the live prototype here:** https://spatialcp-avtduabwglnuhgcm22jjhc.streamlit.app/

### Run Locally (Docker / Python)
```bash
# 1. Clone repo
git clone https://github.com/balajiprincejoshva-byte/SpatialCP.git
cd SpatialCP

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Initialize Agent Engine
streamlit run app.py
```

## ⚠️ Pipeline Assumptions & Translation Constraints
- **Dimensional Extrapolation:** Current ST methods routinely yield 2D contiguous slices. The module projects a synthetic Z-variance representing micrometer tissue thickness for rotatable inspection, paving the way for true volumetric arrays.
- **Damped Equation Simplification:** The diffusion kernels proxy generalized mass transport but do not dynamically resolve active endocytosis or localized vascular efflux pressures unless parameterized by specific user-provided transcript markers.
- **In Vitro Calibration Need:** The `[Agent: Pharmacologist]` uses scaled heuristics to dictate PD response; transitioning this from prototype to clinical grade requires calibration against multiplexed phenotypic viability screens.

## 🔮 Strategic Next Steps
- **Direct AnnData Ingestion:** Linking the ingestion pipeline to native `.h5ad` formats for massive-scale integration from standard Scanpy/Squidpy pipelines.
- **Spatial Autocorrelation (Moran's I):** Identifying statistically significant resistance clusters algorithmically. 
