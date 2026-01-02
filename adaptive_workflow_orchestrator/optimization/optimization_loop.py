"""
Optimization Loop - Analyzes behavior and proposes improvements
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

from .pattern_recognizer import PatternRecognizer
from .proposal_system import ProposalSystem


class OptimizationLoop:
    """
    The self-improvement system that makes the agent better over time.

    Key responsibilities:
    - Log user actions and manual patterns
    - Recognize repetitive tasks
    - Propose automations
    - Generate scripts to replace manual work
    - Track optimization impact
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.pattern_recognizer = PatternRecognizer(config.get("pattern_recognition", {}))
        self.proposal_system = ProposalSystem(config.get("proposals", {}))

        # Action log for pattern analysis
        self.action_log: List[Dict[str, Any]] = []

        # Proposals tracking
        self.active_proposals: List[Dict[str, Any]] = []
        self.accepted_proposals: List[Dict[str, Any]] = []
        self.rejected_proposals: List[Dict[str, Any]] = []

        # Metrics
        self.metrics = {
            "total_actions_logged": 0,
            "patterns_detected": 0,
            "proposals_made": 0,
            "proposals_accepted": 0,
            "time_saved_minutes": 0
        }

    def log_action(self, action: Dict[str, Any], result: Dict[str, Any]) -> None:
        """
        Log an action for pattern analysis

        Args:
            action: The action that was taken
            result: The result of the action
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result": result,
            "was_manual": action.get("was_manual", False),
            "duration_seconds": result.get("duration_seconds", 0)
        }

        self.action_log.append(log_entry)
        self.metrics["total_actions_logged"] += 1

        self.logger.debug(f"Logged action: {action.get('type')}")

        # Periodically analyze patterns (every 10 actions)
        if len(self.action_log) % 10 == 0:
            self._trigger_pattern_analysis()

    def log_manual_action(self, action_description: str, metadata: Dict[str, Any]) -> None:
        """
        Log a manual user action for pattern detection

        Args:
            action_description: Description of what the user did
            metadata: Additional context about the action
        """
        manual_action = {
            "timestamp": datetime.now().isoformat(),
            "description": action_description,
            "metadata": metadata,
            "was_manual": True,
            "type": "manual_action"
        }

        self.action_log.append(manual_action)
        self.logger.info(f"Logged manual action: {action_description}")

    def analyze_cycle(self, cycle_result: Dict[str, Any]) -> None:
        """
        Analyze a completed OODA cycle for optimization opportunities

        Args:
            cycle_result: Results from a complete OODA cycle
        """
        self.logger.info(f"Analyzing cycle #{cycle_result.get('cycle_number')}")

        # Extract actions from cycle
        executed_actions = cycle_result.get("phases", {}).get("act", {}).get("executed_actions", [])

        # Look for optimization opportunities
        for action_record in executed_actions:
            action = action_record.get("action")
            result = action_record.get("result")

            # Check if this could have been automated
            if self._could_be_automated(action, result):
                self._create_automation_proposal(action, result)

    def _trigger_pattern_analysis(self) -> None:
        """Analyze recent actions for patterns"""
        self.logger.info("Analyzing recent actions for patterns")

        # Get recent actions (last 50)
        recent_actions = self.action_log[-50:]

        # Detect patterns
        patterns = self.pattern_recognizer.detect_patterns(recent_actions)

        for pattern in patterns:
            self.metrics["patterns_detected"] += 1
            self.logger.info(f"Detected pattern: {pattern.get('type')}")

            # Create proposal if pattern is significant
            if pattern.get("frequency", 0) >= 3:  # Occurred 3+ times
                self._create_pattern_proposal(pattern)

    def _could_be_automated(self, action: Dict[str, Any], result: Dict[str, Any]) -> bool:
        """Check if an action could potentially be automated"""
        # Actions that were manual are candidates for automation
        if action.get("was_manual", False):
            return True

        # Actions that took significant time
        if result.get("duration_seconds", 0) > 60:  # More than 1 minute
            return True

        # Actions that are repetitive
        action_signature = f"{action.get('type')}:{action.get('subtype')}"
        recent_count = sum(
            1 for log_entry in self.action_log[-20:]
            if f"{log_entry.get('action', {}).get('type')}:{log_entry.get('action', {}).get('subtype')}" == action_signature
        )

        return recent_count >= 2  # Done 2+ times recently

    def _create_automation_proposal(self, action: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Create a proposal to automate an action"""
        self.logger.info(f"Creating automation proposal for {action.get('type')}")

        proposal = self.proposal_system.generate_automation_proposal(
            action=action,
            result=result,
            historical_data=self.action_log
        )

        self.active_proposals.append(proposal)
        self.metrics["proposals_made"] += 1

    def _create_pattern_proposal(self, pattern: Dict[str, Any]) -> None:
        """Create a proposal based on detected pattern"""
        self.logger.info(f"Creating pattern-based proposal for {pattern.get('type')}")

        proposal = self.proposal_system.generate_pattern_proposal(
            pattern=pattern,
            historical_data=self.action_log
        )

        self.active_proposals.append(proposal)
        self.metrics["proposals_made"] += 1

    def get_active_proposals(self) -> List[Dict[str, Any]]:
        """Get all active (pending) proposals"""
        return self.active_proposals

    def accept_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """
        Accept an optimization proposal

        Args:
            proposal_id: ID of the proposal to accept

        Returns:
            Result of accepting the proposal
        """
        # Find proposal
        proposal = None
        for i, p in enumerate(self.active_proposals):
            if p.get("id") == proposal_id:
                proposal = self.active_proposals.pop(i)
                break

        if not proposal:
            return {
                "status": "error",
                "message": f"Proposal {proposal_id} not found"
            }

        self.logger.info(f"Accepting proposal: {proposal_id}")

        # Execute proposal (enable automation)
        result = self.proposal_system.execute_proposal(proposal)

        # Move to accepted
        proposal["accepted_at"] = datetime.now().isoformat()
        proposal["execution_result"] = result
        self.accepted_proposals.append(proposal)

        self.metrics["proposals_accepted"] += 1

        # Estimate time savings
        estimated_savings = proposal.get("estimated_time_savings_minutes", 0)
        self.metrics["time_saved_minutes"] += estimated_savings

        return {
            "status": "success",
            "proposal_id": proposal_id,
            "execution_result": result,
            "estimated_savings_minutes": estimated_savings
        }

    def reject_proposal(self, proposal_id: str, reason: str = "") -> Dict[str, Any]:
        """
        Reject an optimization proposal

        Args:
            proposal_id: ID of the proposal to reject
            reason: Optional reason for rejection

        Returns:
            Result of rejection
        """
        # Find proposal
        proposal = None
        for i, p in enumerate(self.active_proposals):
            if p.get("id") == proposal_id:
                proposal = self.active_proposals.pop(i)
                break

        if not proposal:
            return {
                "status": "error",
                "message": f"Proposal {proposal_id} not found"
            }

        self.logger.info(f"Rejecting proposal: {proposal_id}")

        # Move to rejected
        proposal["rejected_at"] = datetime.now().isoformat()
        proposal["rejection_reason"] = reason
        self.rejected_proposals.append(proposal)

        # Learn from rejection
        self.proposal_system.learn_from_rejection(proposal, reason)

        return {
            "status": "success",
            "proposal_id": proposal_id,
            "message": "Proposal rejected"
        }

    def generate_weekly_report(self) -> Dict[str, Any]:
        """
        Generate a weekly optimization report

        Returns:
            Dict containing optimization metrics and insights
        """
        self.logger.info("Generating weekly optimization report")

        # Calculate metrics for past week
        week_ago = datetime.now() - timedelta(days=7)

        recent_patterns = [
            p for p in self.pattern_recognizer.detected_patterns
            if datetime.fromisoformat(p.get("detected_at", "2020-01-01")) > week_ago
        ]

        recent_accepted = [
            p for p in self.accepted_proposals
            if datetime.fromisoformat(p.get("accepted_at", "2020-01-01")) > week_ago
        ]

        report = {
            "period": "past_7_days",
            "generated_at": datetime.now().isoformat(),
            "metrics": {
                "actions_logged": len([
                    a for a in self.action_log
                    if datetime.fromisoformat(a.get("timestamp", "2020-01-01")) > week_ago
                ]),
                "patterns_detected": len(recent_patterns),
                "proposals_made": len([
                    p for p in (self.active_proposals + recent_accepted)
                    if datetime.fromisoformat(p.get("created_at", "2020-01-01")) > week_ago
                ]),
                "proposals_accepted": len(recent_accepted),
                "estimated_time_saved_minutes": sum(
                    p.get("estimated_time_savings_minutes", 0)
                    for p in recent_accepted
                )
            },
            "top_patterns": recent_patterns[:5],
            "top_automations": recent_accepted[:5],
            "recommendations": self._generate_recommendations()
        }

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        # Check if there are pending proposals
        if len(self.active_proposals) > 0:
            recommendations.append(
                f"You have {len(self.active_proposals)} pending optimization proposals. "
                "Review them to save time on repetitive tasks."
            )

        # Check for frequently manual tasks
        manual_actions = [
            entry for entry in self.action_log[-100:]
            if entry.get("was_manual", False)
        ]

        if len(manual_actions) > 20:
            recommendations.append(
                f"You've performed {len(manual_actions)} manual actions recently. "
                "Consider enabling more automations."
            )

        # Check time spent on certain task types
        # (This would be more sophisticated in production)

        return recommendations

    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization statistics"""
        return {
            **self.metrics,
            "active_proposals": len(self.active_proposals),
            "accepted_proposals": len(self.accepted_proposals),
            "rejected_proposals": len(self.rejected_proposals),
            "action_log_size": len(self.action_log)
        }
