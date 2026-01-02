"""
Adaptive Workflow Orchestrator - Main class

Brings together all modules into a cohesive agentic system
"""

from typing import Dict, Any, Optional
from datetime import datetime
import logging

from .ooda_loop import OODALoop
from .perception import PerceptionModule
from .cognitive import CognitiveEngine
from .action import ActionLayer
from .optimization import OptimizationLoop
from .modes import MorningBriefer, CoPilot, Architect


class AdaptiveWorkflowOrchestrator:
    """
    The Adaptive Workflow Orchestrator - A self-improving agentic system.

    This system:
    - Perceives your work environment (email, calendar, code, etc.)
    - Reasons about priorities and optimal actions
    - Acts on your behalf (with appropriate permissions)
    - Continuously improves by detecting patterns and proposing automations

    Core Philosophy: Manage, Automate, and Upgrade
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the orchestrator

        Args:
            config: Configuration dictionary
        """
        if config is None:
            config = self._get_default_config()

        self.config = config
        self.logger = self._setup_logging(config.get("logging", {}))

        self.logger.info("Initializing Adaptive Workflow Orchestrator")

        # Initialize all modules
        self.perception = PerceptionModule(config.get("perception", {}))
        self.cognitive = CognitiveEngine(config.get("cognitive", {}))
        self.action = ActionLayer(config.get("action", {}))
        self.optimization = OptimizationLoop(config.get("optimization", {}))

        # Initialize OODA loop with all modules
        self.ooda_loop = OODALoop(
            perception_module=self.perception,
            cognitive_engine=self.cognitive,
            action_layer=self.action,
            optimization_loop=self.optimization
        )

        # Initialize interaction modes
        self.morning_briefer = MorningBriefer(self)
        self.copilot = CoPilot(self)
        self.architect = Architect(self)

        # State
        self.current_mode: Optional[str] = None
        self.started_at = datetime.now()

        self.logger.info("Orchestrator initialized successfully")

    def start(self) -> Dict[str, Any]:
        """
        Start the orchestrator

        Returns:
            Startup information
        """
        self.logger.info("Starting Adaptive Workflow Orchestrator")

        startup_info = {
            "status": "running",
            "started_at": self.started_at.isoformat(),
            "version": "0.1.0",
            "modules": {
                "perception": "ready",
                "cognitive": "ready",
                "action": "ready",
                "optimization": "ready",
                "ooda_loop": "ready"
            },
            "modes_available": ["morning_briefer", "copilot", "architect"]
        }

        return startup_info

    def run_morning_briefing(self) -> str:
        """
        Run the morning briefing mode

        Returns:
            Formatted morning briefing
        """
        self.current_mode = "morning_briefer"
        self.logger.info("Running morning briefing")

        briefing = self.morning_briefer.run_morning_briefing()
        formatted = self.morning_briefer.format_briefing(briefing)

        return formatted

    def start_copilot(self) -> Dict[str, Any]:
        """
        Start co-pilot mode

        Returns:
            Session information
        """
        self.current_mode = "copilot"
        self.logger.info("Starting co-pilot mode")

        return self.copilot.start_session()

    def copilot_command(
        self,
        command: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send command to co-pilot

        Args:
            command: Natural language command
            context: Optional context

        Returns:
            Command response
        """
        return self.copilot.handle_command(command, context)

    def run_meta_review(self, period: str = "week") -> str:
        """
        Run architect meta-review

        Args:
            period: Review period (week, month, quarter)

        Returns:
            Formatted review
        """
        self.current_mode = "architect"
        self.logger.info(f"Running meta-review for {period}")

        review = self.architect.run_meta_review(period)
        formatted = self.architect.format_review(review)

        return formatted

    def run_ooda_cycle(
        self,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run a single OODA cycle

        Args:
            context: Optional context for the cycle

        Returns:
            Cycle results
        """
        self.logger.info("Running OODA cycle")
        return self.ooda_loop.run_cycle(context)

    def get_active_proposals(self) -> list[Dict[str, Any]]:
        """Get all active optimization proposals"""
        return self.optimization.get_active_proposals()

    def accept_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """Accept an optimization proposal"""
        return self.optimization.accept_proposal(proposal_id)

    def reject_proposal(self, proposal_id: str, reason: str = "") -> Dict[str, Any]:
        """Reject an optimization proposal"""
        return self.optimization.reject_proposal(proposal_id, reason)

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        return {
            "uptime_seconds": (datetime.now() - self.started_at).total_seconds(),
            "current_mode": self.current_mode,
            "perception": self.perception.get_statistics(),
            "action": self.action.get_statistics(),
            "optimization": self.optimization.get_optimization_stats(),
            "memory": self.cognitive.memory.get_memory_stats(),
            "ooda_cycles": len(self.ooda_loop.cycle_history)
        }

    def _setup_logging(self, logging_config: Dict[str, Any]) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("AdaptiveWorkflowOrchestrator")

        level = logging_config.get("level", "INFO")
        logger.setLevel(getattr(logging, level))

        # Console handler
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "logging": {
                "level": "INFO"
            },
            "perception": {
                "sources": {
                    "email": {"enabled": False},
                    "calendar": {"enabled": False},
                    "project_management": {"enabled": False},
                    "code": {"enabled": False},
                    "filesystem": {"enabled": False}
                },
                "filters": {
                    "spam_patterns": [],
                    "priority_keywords": ["urgent", "critical", "asap"],
                    "noise_senders": []
                }
            },
            "cognitive": {
                "memory": {
                    "short_term_capacity": 100,
                    "long_term": {}
                },
                "user_manual": {
                    "tone": "professional",
                    "timezone": "UTC",
                    "work_hours": {"start": "09:00", "end": "17:00"}
                },
                "llm": {
                    "model": "claude-sonnet-4",
                    "temperature": 0.7
                }
            },
            "action": {
                "executor": {
                    "sandbox_enabled": True
                },
                "permissions": {
                    "user_overrides": {}
                }
            },
            "optimization": {
                "pattern_recognition": {
                    "min_occurrences": 3,
                    "lookback_days": 30
                },
                "proposals": {}
            }
        }
