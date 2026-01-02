"""
Adaptive Workflow Orchestrator
A self-improving agentic system that manages, automates, and upgrades workflows.
"""

__version__ = "0.1.0"

from .orchestrator import AdaptiveWorkflowOrchestrator
from .ooda_loop import OODALoop

__all__ = ["AdaptiveWorkflowOrchestrator", "OODALoop"]
