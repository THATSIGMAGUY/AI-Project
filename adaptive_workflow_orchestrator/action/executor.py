"""
Executor - Handles actual execution of different action types
"""

from typing import Dict, Any
import logging
import subprocess
import tempfile
import os


class Executor:
    """
    Executes different types of actions.

    Provides sandboxed execution environments and safe interfaces
    to external systems.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Configure sandbox environment
        self.sandbox_enabled = config.get("sandbox_enabled", True)
        self.allowed_modules = config.get("allowed_python_modules", [
            "json", "csv", "datetime", "math", "statistics"
        ])

    def execute_email_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an email-related action

        Supported actions:
        - send_email
        - draft_email
        - reply_email
        - archive_email
        """
        self.logger.info(f"Executing email action: {action.get('subtype')}")

        subtype = action.get("subtype", "")

        if subtype == "send_email":
            return self._send_email(action.get("params", {}))
        elif subtype == "draft_email":
            return self._draft_email(action.get("params", {}))
        elif subtype == "reply_email":
            return self._reply_email(action.get("params", {}))
        elif subtype == "archive_email":
            return self._archive_email(action.get("params", {}))
        else:
            raise ValueError(f"Unknown email action subtype: {subtype}")

    def execute_calendar_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a calendar-related action

        Supported actions:
        - create_event
        - update_event
        - delete_event
        - find_available_slots
        """
        self.logger.info(f"Executing calendar action: {action.get('subtype')}")

        subtype = action.get("subtype", "")

        if subtype == "create_event":
            return self._create_calendar_event(action.get("params", {}))
        elif subtype == "update_event":
            return self._update_calendar_event(action.get("params", {}))
        elif subtype == "delete_event":
            return self._delete_calendar_event(action.get("params", {}))
        elif subtype == "find_available_slots":
            return self._find_available_slots(action.get("params", {}))
        else:
            raise ValueError(f"Unknown calendar action subtype: {subtype}")

    def execute_code_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute code in a sandboxed environment

        Supported languages:
        - Python
        - Bash (limited)
        - JavaScript (future)
        """
        self.logger.info(f"Executing code action: {action.get('language', 'python')}")

        language = action.get("language", "python")
        code = action.get("code", "")

        if language == "python":
            return self._execute_python_code(code, action.get("params", {}))
        elif language == "bash":
            return self._execute_bash_command(code, action.get("params", {}))
        else:
            raise ValueError(f"Unsupported language: {language}")

    def execute_file_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute file-related actions

        Supported actions:
        - read_file
        - write_file
        - move_file
        - delete_file
        - organize_files
        """
        self.logger.info(f"Executing file action: {action.get('subtype')}")

        subtype = action.get("subtype", "")

        if subtype == "read_file":
            return self._read_file(action.get("params", {}))
        elif subtype == "write_file":
            return self._write_file(action.get("params", {}))
        elif subtype == "move_file":
            return self._move_file(action.get("params", {}))
        elif subtype == "delete_file":
            return self._delete_file(action.get("params", {}))
        elif subtype == "organize_files":
            return self._organize_files(action.get("params", {}))
        else:
            raise ValueError(f"Unknown file action subtype: {subtype}")

    def execute_webhook_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute webhook/API actions

        Triggers external services via HTTP requests
        """
        self.logger.info(f"Executing webhook action: {action.get('url')}")

        # In production, this would make actual HTTP requests
        return {
            "status": "simulated",
            "url": action.get("url"),
            "method": action.get("method", "POST"),
            "response": "Webhook execution simulated"
        }

    def execute_generic_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a generic action"""
        self.logger.info(f"Executing generic action: {action.get('type')}")

        return {
            "status": "executed",
            "action_type": action.get("type"),
            "message": "Generic action executed"
        }

    def rollback_action(
        self,
        action: Dict[str, Any],
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Attempt to rollback an action

        Args:
            action: Original action
            result: Result of the original action

        Returns:
            Rollback result
        """
        self.logger.info(f"Rolling back action: {action.get('id')}")

        action_type = action.get("type", "")

        # Different rollback strategies based on action type
        if "email" in action_type and "send" in action.get("subtype", ""):
            # Can't unsend email, but could send a follow-up
            return {"status": "partial", "message": "Cannot unsend email"}

        elif "file" in action_type:
            # File operations can often be reversed
            return self._rollback_file_action(action, result)

        elif "calendar" in action_type:
            # Calendar events can be deleted/restored
            return self._rollback_calendar_action(action, result)

        else:
            return {"status": "not_supported", "message": "Rollback not supported for this action type"}

    # Private helper methods

    def _send_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send an email (simulated)"""
        self.logger.info(f"Sending email to {params.get('to')}")
        return {
            "status": "sent",
            "to": params.get("to"),
            "subject": params.get("subject"),
            "message_id": "simulated_message_id"
        }

    def _draft_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create email draft"""
        self.logger.info("Creating email draft")
        return {
            "status": "draft_created",
            "draft_id": "simulated_draft_id",
            "content": params.get("body", "")
        }

    def _reply_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Reply to an email"""
        return {
            "status": "reply_sent",
            "original_message_id": params.get("message_id"),
            "reply_id": "simulated_reply_id"
        }

    def _archive_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Archive an email"""
        return {
            "status": "archived",
            "message_id": params.get("message_id")
        }

    def _create_calendar_event(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create calendar event"""
        return {
            "status": "created",
            "event_id": "simulated_event_id",
            "title": params.get("title"),
            "start": params.get("start"),
            "end": params.get("end")
        }

    def _update_calendar_event(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update calendar event"""
        return {
            "status": "updated",
            "event_id": params.get("event_id")
        }

    def _delete_calendar_event(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Delete calendar event"""
        return {
            "status": "deleted",
            "event_id": params.get("event_id")
        }

    def _find_available_slots(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Find available time slots"""
        return {
            "status": "found",
            "slots": [
                {"start": "2026-01-03T10:00:00", "end": "2026-01-03T11:00:00"},
                {"start": "2026-01-03T14:00:00", "end": "2026-01-03T15:00:00"}
            ]
        }

    def _execute_python_code(self, code: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Python code in a sandbox

        In production, this would use a proper sandboxing solution
        """
        if not self.sandbox_enabled:
            self.logger.warning("Sandbox is disabled - code execution blocked")
            return {
                "status": "blocked",
                "reason": "Sandbox disabled"
            }

        self.logger.info("Executing Python code in sandbox")

        # For production, use docker/vm sandboxing
        # This is a simplified simulation
        return {
            "status": "executed",
            "output": "Code execution simulated (sandbox)",
            "return_code": 0
        }

    def _execute_bash_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute bash command (very limited for safety)"""
        # Only allow very specific safe commands
        allowed_commands = ["ls", "pwd", "echo"]

        command_parts = command.split()
        if not command_parts or command_parts[0] not in allowed_commands:
            return {
                "status": "blocked",
                "reason": f"Command not in allowed list: {allowed_commands}"
            }

        self.logger.info(f"Executing safe bash command: {command}")
        return {
            "status": "executed",
            "output": "Command execution simulated",
            "return_code": 0
        }

    def _read_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read file"""
        file_path = params.get("path")
        return {
            "status": "read",
            "path": file_path,
            "content": "File content (simulated)"
        }

    def _write_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Write file"""
        return {
            "status": "written",
            "path": params.get("path"),
            "bytes_written": len(params.get("content", ""))
        }

    def _move_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Move file"""
        return {
            "status": "moved",
            "from": params.get("from"),
            "to": params.get("to")
        }

    def _delete_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Delete file"""
        return {
            "status": "deleted",
            "path": params.get("path")
        }

    def _organize_files(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Organize files by type/date/etc"""
        return {
            "status": "organized",
            "files_moved": 0,
            "folders_created": 0
        }

    def _rollback_file_action(
        self,
        action: Dict[str, Any],
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Rollback file operation"""
        # Implementation depends on what was done
        return {"status": "rollback_simulated"}

    def _rollback_calendar_action(
        self,
        action: Dict[str, Any],
        result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Rollback calendar operation"""
        return {"status": "rollback_simulated"}
