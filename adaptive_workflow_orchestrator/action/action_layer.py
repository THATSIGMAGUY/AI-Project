"""
Action Layer - Executes planned actions
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from .executor import Executor
from .permission_manager import PermissionManager, PermissionTier


class ActionLayer:
    """
    The action execution system - the agent's hands.

    Capabilities:
    - Code execution in sandboxed environment
    - API webhook triggers (email, Slack, calendar, etc.)
    - File operations
    - Data manipulation
    - External tool integrations
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.executor = Executor(config.get("executor", {}))
        self.permission_manager = PermissionManager(config.get("permissions", {}))

        # Track execution history
        self.execution_history: List[Dict[str, Any]] = []

        # Statistics
        self.stats = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "pending_approvals": 0
        }

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a planned action

        Args:
            action: Action specification from cognitive engine

        Returns:
            Dict containing execution result
        """
        self.logger.info(f"Executing action: {action.get('id')}")
        self.stats["total_executions"] += 1

        result = {
            "action_id": action.get("id"),
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "output": None,
            "error": None,
            "requires_approval": False
        }

        try:
            # Check permissions
            permission_check = self.permission_manager.check_permission(action)

            if not permission_check["allowed"]:
                result["status"] = "blocked"
                result["error"] = permission_check["reason"]
                result["requires_approval"] = True
                self.stats["pending_approvals"] += 1
                return result

            # Route to appropriate executor based on action type
            action_type = action.get("type", "")

            if "email" in action_type:
                output = self.executor.execute_email_action(action)
            elif "calendar" in action_type:
                output = self.executor.execute_calendar_action(action)
            elif "code" in action_type:
                output = self.executor.execute_code_action(action)
            elif "file" in action_type:
                output = self.executor.execute_file_action(action)
            elif "webhook" in action_type:
                output = self.executor.execute_webhook_action(action)
            else:
                output = self.executor.execute_generic_action(action)

            result["status"] = "success"
            result["output"] = output
            self.stats["successful_executions"] += 1

        except Exception as e:
            self.logger.error(f"Error executing action {action.get('id')}: {e}")
            result["status"] = "failed"
            result["error"] = str(e)
            self.stats["failed_executions"] += 1

        # Store in execution history
        self.execution_history.append({
            "action": action,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        return result

    def execute_batch(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute multiple actions in batch

        Args:
            actions: List of actions to execute

        Returns:
            List of execution results
        """
        self.logger.info(f"Executing batch of {len(actions)} actions")

        results = []
        for action in actions:
            result = self.execute(action)
            results.append(result)

            # Stop if we hit a critical failure
            if result["status"] == "failed" and action.get("critical", False):
                self.logger.warning("Critical action failed, stopping batch execution")
                break

        return results

    def execute_with_approval(
        self,
        action: Dict[str, Any],
        approval_callback: callable
    ) -> Dict[str, Any]:
        """
        Execute action with user approval

        Args:
            action: Action to execute
            approval_callback: Function to call for user approval

        Returns:
            Execution result
        """
        # Request approval
        approval_request = {
            "action": action,
            "description": action.get("description", ""),
            "estimated_impact": action.get("estimated_impact", "medium"),
            "reversible": action.get("reversible", False)
        }

        approved = approval_callback(approval_request)

        if not approved:
            return {
                "action_id": action.get("id"),
                "status": "cancelled",
                "error": "User denied approval",
                "timestamp": datetime.now().isoformat()
            }

        # Execute if approved
        return self.execute(action)

    def rollback(self, action_id: str) -> Dict[str, Any]:
        """
        Attempt to rollback a previously executed action

        Args:
            action_id: ID of action to rollback

        Returns:
            Rollback result
        """
        self.logger.info(f"Attempting to rollback action: {action_id}")

        # Find the action in history
        action_record = None
        for record in self.execution_history:
            if record["action"].get("id") == action_id:
                action_record = record
                break

        if not action_record:
            return {
                "status": "failed",
                "error": f"Action {action_id} not found in history"
            }

        # Check if action is reversible
        if not action_record["action"].get("reversible", False):
            return {
                "status": "failed",
                "error": f"Action {action_id} is not reversible"
            }

        # Attempt rollback
        try:
            rollback_result = self.executor.rollback_action(
                action_record["action"],
                action_record["result"]
            )

            return {
                "status": "success",
                "action_id": action_id,
                "rollback_result": rollback_result
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    def get_execution_history(
        self,
        limit: Optional[int] = None,
        action_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get execution history

        Args:
            limit: Maximum number of records to return
            action_type: Filter by action type

        Returns:
            List of execution records
        """
        history = self.execution_history

        # Filter by type if specified
        if action_type:
            history = [
                record for record in history
                if action_type in record["action"].get("type", "")
            ]

        # Limit results
        if limit:
            history = history[-limit:]

        return history

    def get_statistics(self) -> Dict[str, Any]:
        """Get action layer statistics"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_executions"] / max(self.stats["total_executions"], 1)
            ),
            "history_size": len(self.execution_history)
        }

    def clear_history(self) -> None:
        """Clear execution history"""
        self.execution_history.clear()
        self.logger.info("Execution history cleared")
