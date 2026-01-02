"""
Proposal System - Generates and manages optimization proposals
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import uuid


class ProposalSystem:
    """
    Generates proposals for automations and optimizations.

    Proposals include:
    - Description of what will be automated
    - Estimated time savings
    - Script or automation to be enabled
    - Risk assessment
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Rejection learning
        self.rejection_patterns: List[Dict[str, Any]] = []

    def generate_automation_proposal(
        self,
        action: Dict[str, Any],
        result: Dict[str, Any],
        historical_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a proposal to automate a specific action

        Args:
            action: The action to automate
            result: Result of the action
            historical_data: Historical action log

        Returns:
            Automation proposal
        """
        proposal_id = str(uuid.uuid4())

        # Calculate time savings
        estimated_savings = self._estimate_time_savings(action, historical_data)

        # Generate automation script/config
        automation_spec = self._generate_automation_spec(action)

        # Assess risk
        risk_assessment = self._assess_risk(action)

        proposal = {
            "id": proposal_id,
            "type": "automation",
            "created_at": datetime.now().isoformat(),
            "status": "pending",

            "title": f"Automate {action.get('type', 'action')}",
            "description": self._generate_proposal_description(action, historical_data),

            "action_to_automate": action,
            "automation_spec": automation_spec,

            "estimated_time_savings_minutes": estimated_savings,
            "estimated_frequency": self._estimate_frequency(action, historical_data),

            "risk_level": risk_assessment["level"],
            "risk_factors": risk_assessment["factors"],

            "reversible": self._is_reversible(action),
            "requires_setup": automation_spec.get("requires_setup", False),

            "preview": self._generate_preview(automation_spec)
        }

        return proposal

    def generate_pattern_proposal(
        self,
        pattern: Dict[str, Any],
        historical_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a proposal based on a detected pattern

        Args:
            pattern: Detected pattern
            historical_data: Historical action log

        Returns:
            Pattern-based proposal
        """
        proposal_id = str(uuid.uuid4())

        # Different proposal strategies based on pattern type
        pattern_type = pattern.get("type")

        if pattern_type == "temporal":
            proposal = self._generate_temporal_automation(pattern)
        elif pattern_type == "sequential":
            proposal = self._generate_workflow_automation(pattern)
        elif pattern_type == "trigger":
            proposal = self._generate_trigger_automation(pattern)
        elif pattern_type == "bulk":
            proposal = self._generate_bulk_automation(pattern)
        else:
            proposal = self._generate_generic_automation(pattern)

        proposal["id"] = proposal_id
        proposal["created_at"] = datetime.now().isoformat()
        proposal["status"] = "pending"

        return proposal

    def execute_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an accepted proposal (enable the automation)

        Args:
            proposal: The proposal to execute

        Returns:
            Execution result
        """
        self.logger.info(f"Executing proposal: {proposal.get('id')}")

        automation_spec = proposal.get("automation_spec", {})

        # In production, this would actually enable the automation
        # For now, simulate it
        result = {
            "status": "enabled",
            "automation_id": f"auto_{proposal.get('id')}",
            "enabled_at": datetime.now().isoformat(),
            "message": f"Automation enabled: {proposal.get('title')}"
        }

        return result

    def learn_from_rejection(self, proposal: Dict[str, Any], reason: str) -> None:
        """
        Learn from rejected proposals to improve future suggestions

        Args:
            proposal: The rejected proposal
            reason: Reason for rejection
        """
        self.logger.info(f"Learning from rejection: {proposal.get('id')}")

        rejection_pattern = {
            "proposal_type": proposal.get("type"),
            "action_type": proposal.get("action_to_automate", {}).get("type"),
            "reason": reason,
            "risk_level": proposal.get("risk_level"),
            "rejected_at": datetime.now().isoformat()
        }

        self.rejection_patterns.append(rejection_pattern)

        # Adjust future proposal generation based on rejection
        # (In production, this would use ML to refine proposals)

    # Helper methods

    def _estimate_time_savings(
        self,
        action: Dict[str, Any],
        historical_data: List[Dict[str, Any]]
    ) -> int:
        """Estimate time savings in minutes per week"""

        # Calculate frequency
        action_type = action.get("type", "")
        similar_actions = [
            entry for entry in historical_data
            if entry.get("action", {}).get("type") == action_type
        ]

        # Estimate average duration
        durations = [
            entry.get("result", {}).get("duration_seconds", 60)
            for entry in similar_actions
        ]
        avg_duration_minutes = sum(durations) / max(len(durations), 1) / 60

        # Frequency per week
        frequency_per_week = min(len(similar_actions), 52)  # Cap at daily

        return int(avg_duration_minutes * frequency_per_week)

    def _estimate_frequency(
        self,
        action: Dict[str, Any],
        historical_data: List[Dict[str, Any]]
    ) -> str:
        """Estimate how frequently this action occurs"""

        action_type = action.get("type", "")
        count = sum(
            1 for entry in historical_data
            if entry.get("action", {}).get("type") == action_type
        )

        if count >= 30:
            return "daily"
        elif count >= 7:
            return "weekly"
        elif count >= 2:
            return "occasionally"
        else:
            return "rarely"

    def _generate_automation_spec(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the automation specification"""

        return {
            "type": "automated_action",
            "action_type": action.get("type"),
            "parameters": action.get("params", {}),
            "trigger": "manual",  # Or could be scheduled, event-driven, etc.
            "requires_setup": False,
            "script": self._generate_script(action)
        }

    def _generate_script(self, action: Dict[str, Any]) -> str:
        """Generate automation script (pseudo-code)"""

        action_type = action.get("type", "")

        # Simple script template
        script = f"""
# Automation script for {action_type}
def automated_{action_type.replace(' ', '_')}():
    # Execute {action_type}
    result = execute_action({action})

    # Log result
    log_automation_result(result)

    return result
"""
        return script.strip()

    def _assess_risk(self, action: Dict[str, Any]) -> Dict[str, str]:
        """Assess risk of automating this action"""

        risk_factors = []
        risk_level = "low"

        action_type = action.get("type", "").lower()

        # High-risk actions
        if any(keyword in action_type for keyword in ["delete", "remove", "drop"]):
            risk_factors.append("Destructive action")
            risk_level = "high"

        # Medium-risk actions
        if any(keyword in action_type for keyword in ["send", "publish", "deploy"]):
            risk_factors.append("External communication")
            risk_level = "medium" if risk_level != "high" else risk_level

        # Low-risk actions
        if any(keyword in action_type for keyword in ["read", "search", "analyze"]):
            risk_factors.append("Read-only operation")

        if not risk_factors:
            risk_factors.append("Standard operation")

        return {
            "level": risk_level,
            "factors": risk_factors
        }

    def _is_reversible(self, action: Dict[str, Any]) -> bool:
        """Check if action is reversible"""

        action_type = action.get("type", "").lower()

        # Irreversible actions
        irreversible_keywords = ["delete", "send", "publish", "deploy", "drop"]

        return not any(keyword in action_type for keyword in irreversible_keywords)

    def _generate_preview(self, automation_spec: Dict[str, Any]) -> str:
        """Generate a preview of what the automation will do"""

        return f"This automation will {automation_spec.get('action_type', 'perform action')} automatically."

    def _generate_proposal_description(
        self,
        action: Dict[str, Any],
        historical_data: List[Dict[str, Any]]
    ) -> str:
        """Generate human-readable proposal description"""

        action_type = action.get("type", "")
        frequency = self._estimate_frequency(action, historical_data)
        time_savings = self._estimate_time_savings(action, historical_data)

        return (
            f"I noticed you perform '{action_type}' {frequency}. "
            f"I can automate this to save you approximately {time_savings} minutes per week. "
            f"Shall I enable this automation?"
        )

    def _generate_temporal_automation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Generate automation for temporal patterns"""

        details = pattern.get("details", {})

        return {
            "type": "scheduled_automation",
            "title": f"Schedule {details.get('action_type')} for {details.get('day_of_week')}s",
            "description": pattern.get("description", "") + ". I can automate this on a schedule.",
            "automation_spec": {
                "type": "scheduled",
                "schedule": f"every {details.get('day_of_week')} at {details.get('hour')}:00",
                "action": details.get("action_type")
            },
            "estimated_time_savings_minutes": pattern.get("frequency", 0) * 15,
            "risk_level": "low",
            "reversible": True
        }

    def _generate_workflow_automation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Generate automation for sequential patterns"""

        details = pattern.get("details", {})
        sequence = details.get("sequence", [])

        return {
            "type": "workflow_automation",
            "title": f"Automate workflow: {' → '.join(sequence)}",
            "description": f"I can combine these steps into a single automated workflow.",
            "automation_spec": {
                "type": "workflow",
                "steps": sequence
            },
            "estimated_time_savings_minutes": len(sequence) * 5 * pattern.get("frequency", 1),
            "risk_level": "medium",
            "reversible": True
        }

    def _generate_trigger_automation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Generate automation for trigger-based patterns"""

        details = pattern.get("details", {})

        return {
            "type": "trigger_automation",
            "title": f"Auto-respond to {details.get('trigger')}",
            "description": pattern.get("description", "") + ". I can automate this response.",
            "automation_spec": {
                "type": "trigger",
                "trigger": details.get("trigger"),
                "action": details.get("response")
            },
            "estimated_time_savings_minutes": pattern.get("frequency", 0) * 10,
            "risk_level": "medium",
            "reversible": True
        }

    def _generate_bulk_automation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Generate automation for bulk processing patterns"""

        details = pattern.get("details", {})

        return {
            "type": "bulk_automation",
            "title": f"Batch process {details.get('action_type')}",
            "description": "I can process these in bulk automatically.",
            "automation_spec": {
                "type": "bulk",
                "action": details.get("action_type"),
                "batch_size": details.get("typical_batch_size", 10)
            },
            "estimated_time_savings_minutes": details.get("typical_batch_size", 10) * 2,
            "risk_level": "low",
            "reversible": True
        }

    def _generate_generic_automation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Generate generic automation proposal"""

        return {
            "type": "automation",
            "title": f"Automate {pattern.get('pattern', 'task')}",
            "description": pattern.get("description", "I can automate this task."),
            "automation_spec": {
                "type": "generic",
                "pattern": pattern
            },
            "estimated_time_savings_minutes": 30,
            "risk_level": "low",
            "reversible": True
        }
