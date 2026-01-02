"""
User Manual - User preferences, tone, and strategic goals
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import json


class UserManual:
    """
    The User Manual contains the agent's understanding of the user.

    It includes:
    - Communication preferences (tone, verbosity)
    - Work preferences (task types, energy patterns)
    - Strategic goals (short-term and long-term)
    - Personal context (timezone, work hours, tools)
    - Learning history (what works, what doesn't)
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Load or initialize user preferences
        self.preferences = self._load_preferences(config)

        # Learning log - tracks what works and what doesn't
        self.learning_log: List[Dict[str, Any]] = []

    def _load_preferences(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Load user preferences from config"""
        return {
            # Communication preferences
            "communication": {
                "tone": config.get("tone", "professional"),
                "verbosity": config.get("verbosity", "balanced"),  # terse, balanced, detailed
                "notification_style": config.get("notification_style", "summary"),
                "preferred_channels": config.get("preferred_channels", ["email", "slack"])
            },

            # Work preferences
            "work": {
                "timezone": config.get("timezone", "UTC"),
                "work_hours": config.get("work_hours", {"start": "09:00", "end": "17:00"}),
                "break_times": config.get("break_times", [{"start": "12:00", "end": "13:00"}]),
                "focus_time_blocks": config.get("focus_time_blocks", []),
                "preferred_task_duration": config.get("preferred_task_duration", 30),  # minutes
            },

            # Task preferences
            "tasks": {
                "prioritization_style": config.get("prioritization_style", "impact_first"),
                "batch_similar_tasks": config.get("batch_similar_tasks", True),
                "max_concurrent_tasks": config.get("max_concurrent_tasks", 3),
                "break_frequency": config.get("break_frequency", 90),  # minutes
            },

            # Energy patterns (learned over time)
            "energy_patterns": {
                "peak_hours": config.get("peak_hours", [9, 10, 11]),
                "low_hours": config.get("low_hours", [13, 14]),
                "best_for_creative": config.get("best_for_creative", [9, 10]),
                "best_for_analytical": config.get("best_for_analytical", [10, 11, 15]),
                "best_for_administrative": config.get("best_for_administrative", [14, 16]),
            },

            # Strategic goals
            "goals": {
                "short_term": config.get("short_term_goals", []),
                "long_term": config.get("long_term_goals", []),
                "key_results": config.get("key_results", []),
            },

            # Tool preferences
            "tools": {
                "preferred_editor": config.get("preferred_editor", "vscode"),
                "preferred_terminal": config.get("preferred_terminal", "bash"),
                "preferred_project_manager": config.get("preferred_project_manager", "notion"),
            },

            # Automation preferences
            "automation": {
                "autonomy_level": config.get("autonomy_level", "medium"),  # low, medium, high
                "require_approval_for": config.get("require_approval_for", [
                    "send_email", "schedule_meeting", "modify_code", "delete_files"
                ]),
                "auto_approve": config.get("auto_approve", [
                    "sort_files", "tag_emails", "create_drafts"
                ]),
            }
        }

    def get_preferences(self) -> Dict[str, Any]:
        """Get all user preferences"""
        return self.preferences

    def get_preference(self, category: str, key: str, default: Any = None) -> Any:
        """
        Get a specific preference

        Args:
            category: Preference category (e.g., "communication", "work")
            key: Preference key
            default: Default value if not found

        Returns:
            Preference value or default
        """
        return self.preferences.get(category, {}).get(key, default)

    def update_preference(self, category: str, key: str, value: Any) -> None:
        """
        Update a user preference

        Args:
            category: Preference category
            key: Preference key
            value: New value
        """
        if category not in self.preferences:
            self.preferences[category] = {}

        old_value = self.preferences[category].get(key)
        self.preferences[category][key] = value

        self.logger.info(f"Updated preference {category}.{key}: {old_value} -> {value}")

        # Log the learning
        self.learning_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "preference_update",
            "category": category,
            "key": key,
            "old_value": old_value,
            "new_value": value
        })

    def learn_from_feedback(self, action: Dict[str, Any], feedback: str, rating: int) -> None:
        """
        Learn from user feedback on actions

        Args:
            action: The action that was taken
            feedback: User's feedback (text)
            rating: Numerical rating (1-5)
        """
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "action_feedback",
            "action": action,
            "feedback": feedback,
            "rating": rating
        }

        self.learning_log.append(learning_entry)
        self.logger.info(f"Learned from feedback: {action.get('type')} rated {rating}/5")

        # Adjust preferences based on feedback
        if rating >= 4:
            # Positive feedback - reinforce this approach
            self._reinforce_successful_pattern(action)
        elif rating <= 2:
            # Negative feedback - avoid this approach
            self._avoid_unsuccessful_pattern(action)

    def _reinforce_successful_pattern(self, action: Dict[str, Any]) -> None:
        """Reinforce patterns from successful actions"""
        # In production, this would use ML to identify patterns
        # For now, simple heuristics
        action_type = action.get("type", "")

        if "email" in action_type:
            # User liked this email approach
            tone = action.get("tone", "professional")
            self.update_preference("communication", "tone", tone)

    def _avoid_unsuccessful_pattern(self, action: Dict[str, Any]) -> None:
        """Learn to avoid patterns from unsuccessful actions"""
        # Mark patterns to avoid
        self.learning_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "pattern_to_avoid",
            "action": action
        })

    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of what has been learned"""
        successful_actions = [
            entry for entry in self.learning_log
            if entry.get("type") == "action_feedback" and entry.get("rating", 0) >= 4
        ]

        unsuccessful_actions = [
            entry for entry in self.learning_log
            if entry.get("type") == "action_feedback" and entry.get("rating", 0) <= 2
        ]

        return {
            "total_learnings": len(self.learning_log),
            "successful_patterns": len(successful_actions),
            "unsuccessful_patterns": len(unsuccessful_actions),
            "preference_updates": len([
                entry for entry in self.learning_log
                if entry.get("type") == "preference_update"
            ]),
            "recent_learnings": self.learning_log[-10:]  # Last 10
        }

    def export_preferences(self) -> str:
        """Export preferences to JSON string"""
        return json.dumps(self.preferences, indent=2)

    def import_preferences(self, preferences_json: str) -> None:
        """Import preferences from JSON string"""
        try:
            new_preferences = json.loads(preferences_json)
            self.preferences.update(new_preferences)
            self.logger.info("Imported user preferences")
        except json.JSONDecodeError as e:
            self.logger.error(f"Error importing preferences: {e}")
