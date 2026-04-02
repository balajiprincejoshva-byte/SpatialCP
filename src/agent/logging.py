from datetime import datetime

class AgentLogger:
    """
    Simple logger to track workflow steps and present them nicely in Streamlit.
    """
    def __init__(self):
        self.logs = []
        
    def log_step(self, step_name: str, status: str, details: str = ""):
        """
        status: 'pending', 'running', 'completed', 'failed', 'skipped'
        """
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "step": step_name,
            "status": status,
            "details": details
        }
        self.logs.append(entry)
        
    def get_logs(self):
        return self.logs
        
    def clear(self):
        self.logs = []
