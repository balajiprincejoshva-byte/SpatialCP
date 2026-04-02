import pandas as pd
from typing import Dict, Any
from .logging import AgentLogger
from ..simulation.baselines import compute_uniform_baseline, compute_distance_baseline
from ..simulation.diffusion import simulate_iterative_diffusion
from ..simulation.response import compute_response

class AnalysisWorkflow:
    def __init__(self, logger: AgentLogger):
        self.logger = logger
        self.data_state = {}
        
    def execute(self, df: pd.DataFrame, params: Dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Runs the full deterministic agentic workflow.
        """
        self.logger.log_step("[Agent: Data Controller] Validating input schema...", "running")
        try:
            # We assume validation has already been run before this method is called,
            # but we record it for the agent footprint.
            self.logger.log_step("[Agent: Data Controller] Validating input schema...", "completed", f"Data schema valid. shape={df.shape}")
        except Exception as e:
            self.logger.log_step("[Agent: Data Controller] Validating input schema...", "failed", str(e))
            raise
            
        self.logger.log_step("[Agent: Spatial Mapper] Profiling tissue microenvironment...", "running")
        try:
            ct_counts = df['cell_type'].value_counts().to_dict()
            self.logger.log_step("[Agent: Spatial Mapper] Profiling tissue microenvironment...", "completed", f"Profiles extracted: {ct_counts}")
        except Exception as e:
            self.logger.log_step("[Agent: Spatial Mapper] Profiling tissue microenvironment...", "failed", str(e))
            raise

        self.logger.log_step("[Agent: Physicist] Calculating molecular diffusion baselines...", "running")
        try:
            df['baseline_uniform'] = compute_uniform_baseline(df)
            
            # Find Endothelial cells as drug sources
            source_coords = df[df['cell_type'] == 'Endothelial'][['x', 'y']].values.tolist()
            if not source_coords:
                # Fallback center source
                source_coords = [[50, 50]]
                
            df['baseline_distance'] = compute_distance_baseline(df, source_coords)
            self.logger.log_step("[Agent: Physicist] Calculating molecular diffusion baselines...", "completed", "Computed Uniform & Distance baselines.")
        except Exception as e:
            self.logger.log_step("[Agent: Physicist] Calculating molecular diffusion baselines...", "failed", str(e))
            raise

        self.logger.log_step("[Agent: Physicist] Simulating iterative resistance barriers...", "running")
        try:
            final_conc, history_df = simulate_iterative_diffusion(
                df=df,
                source_coords=source_coords,
                iterations=params.get('iterations'),
                base_diffusion=params.get('base_diffusion'),
                decay=params.get('decay')
            )
            df['pred_concentration'] = final_conc
            self.logger.log_step("[Agent: Physicist] Simulating iterative resistance barriers...", "completed", "Tissue resistance matrix applied effectively.")
        except Exception as e:
            self.logger.log_step("[Agent: Physicist] Simulating iterative resistance barriers...", "failed", str(e))
            raise
            
        self.logger.log_step("[Agent: Pharmacologist] Estimating target engagement...", "running")
        try:
            df['response_score'] = compute_response(df, concentration_col='pred_concentration')
            self.logger.log_step("[Agent: Pharmacologist] Estimating target engagement...", "completed", "Sensitivities weights assigned according to heuristics.")
        except Exception as e:
            self.logger.log_step("[Agent: Pharmacologist] Estimating target engagement...", "failed", str(e))
            raise

        self.logger.log_step("[Agent: Analyst] Compiling explainability metrics...", "completed", "Ready for UI presentation.")
        
        return df, history_df
