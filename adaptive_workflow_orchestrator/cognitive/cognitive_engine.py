"""
Cognitive Engine - The Brain of the Agent
Handles reasoning, decision-making, and planning
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from .memory_system import MemorySystem
from .user_manual import UserManual


class CognitiveEngine:
    """
    The LLM-powered cognitive system that understands, reasons, and plans.

    Key responsibilities:
    - Analyze context and understand situations
    - Prioritize tasks based on user preferences
    - Generate action plans
    - Learn from past interactions
    - Maintain user preferences and patterns
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize memory systems
        self.memory = MemorySystem(config.get("memory", {}))

        # Load user manual (preferences, tone, goals)
        self.user_manual = UserManual(config.get("user_manual", {}))

        # LLM configuration (in production, this would initialize actual LLM client)
        self.llm_config = config.get("llm", {
            "model": "claude-sonnet-4",
            "temperature": 0.7,
            "max_tokens": 4096
        })

    def analyze_context(self, filtered_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the current context from filtered perception data

        Args:
            filtered_data: Filtered and structured data from perception module

        Returns:
            Dict containing contextual understanding
        """
        self.logger.info("Analyzing context from filtered data")

        context = {
            "timestamp": datetime.now().isoformat(),
            "situation_summary": "",
            "key_themes": [],
            "urgency_level": "normal",
            "complexity": "medium",
            "dependencies": []
        }

        # Analyze priority items
        priority_count = len(filtered_data.get("priority_items", []))
        actionable_count = len(filtered_data.get("actionable_items", []))
        informational_count = len(filtered_data.get("informational_items", []))

        # Determine urgency level
        if priority_count > 5:
            context["urgency_level"] = "critical"
        elif priority_count > 2:
            context["urgency_level"] = "high"
        elif actionable_count > 10:
            context["urgency_level"] = "elevated"
        else:
            context["urgency_level"] = "normal"

        # Extract themes from items
        all_items = (filtered_data.get("priority_items", []) +
                    filtered_data.get("actionable_items", []))

        context["key_themes"] = self._extract_themes(all_items)

        # Generate situation summary
        context["situation_summary"] = self._generate_summary(
            priority_count, actionable_count, informational_count, context["key_themes"]
        )

        # Store in short-term memory
        self.memory.short_term.store("current_context", context)

        return context

    def prioritize_tasks(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prioritize tasks based on context, deadlines, and user preferences

        Args:
            context: Context from analyze_context

        Returns:
            List of prioritized tasks
        """
        self.logger.info("Prioritizing tasks")

        priorities = []

        # Get user preferences for task prioritization
        user_prefs = self.user_manual.get_preferences()

        # Retrieve similar past situations from long-term memory
        similar_situations = self.memory.long_term.search_similar(
            context["situation_summary"],
            limit=5
        )

        # In production, this would use LLM to intelligently prioritize
        # For now, using rule-based approach

        # Priority factors:
        # 1. Urgency (deadline proximity)
        # 2. Importance (impact on goals)
        # 3. Dependencies (blockers for other tasks)
        # 4. User energy levels
        # 5. Estimated effort

        # This is a placeholder - in production, LLM would generate this
        priorities = [
            {
                "id": f"task_{i}",
                "description": "Task description",
                "priority_score": 0.0,
                "rationale": "Why this priority",
                "estimated_effort": "medium",
                "deadline": None,
                "dependencies": []
            }
            for i in range(3)
        ]

        return sorted(priorities, key=lambda x: x["priority_score"], reverse=True)

    def identify_constraints(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify constraints affecting task execution

        Args:
            context: Current context

        Returns:
            Dict of identified constraints
        """
        self.logger.info("Identifying constraints")

        constraints = {
            "time": {},
            "resources": {},
            "dependencies": {},
            "energy": {}
        }

        # Time constraints (meetings, deadlines)
        constraints["time"] = {
            "available_blocks": self._calculate_available_time(),
            "hard_deadlines": [],
            "soft_deadlines": []
        }

        # Resource constraints (tools, access, information)
        constraints["resources"] = {
            "available_tools": self._get_available_tools(),
            "missing_information": [],
            "access_limitations": []
        }

        # Dependencies (waiting on others, blocked tasks)
        constraints["dependencies"] = {
            "blocking_tasks": [],
            "waiting_on_others": []
        }

        # User energy and focus constraints
        user_state = self.memory.short_term.retrieve("user_state")
        constraints["energy"] = {
            "current_level": user_state.get("energy_level", "medium") if user_state else "medium",
            "optimal_task_types": ["coding", "writing", "planning"],  # Based on current state
            "avoid_task_types": []
        }

        return constraints

    def assess_user_state(self, filtered_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess user's current state (energy, availability, preferences)

        Args:
            filtered_data: Filtered perception data

        Returns:
            Dict containing user state assessment
        """
        self.logger.info("Assessing user state")

        # Get historical patterns
        historical_patterns = self.memory.long_term.get_patterns("user_activity")

        user_state = {
            "timestamp": datetime.now().isoformat(),
            "energy_level": "medium",  # high, medium, low
            "availability": "available",  # available, busy, in_meeting
            "current_focus": None,
            "preferred_task_type": None,
            "cognitive_load": "moderate"
        }

        # Infer energy level from time of day and historical patterns
        current_hour = datetime.now().hour

        if 9 <= current_hour <= 11:
            user_state["energy_level"] = "high"  # Morning peak
        elif 13 <= current_hour <= 14:
            user_state["energy_level"] = "low"  # Post-lunch dip
        elif 15 <= current_hour <= 17:
            user_state["energy_level"] = "medium"  # Afternoon
        else:
            user_state["energy_level"] = "medium"

        # Check calendar for availability
        # (In production, would check actual calendar data)

        # Store in short-term memory
        self.memory.short_term.store("user_state", user_state)

        return user_state

    def generate_action_plan(
        self,
        priorities: List[Dict[str, Any]],
        constraints: Dict[str, Any],
        user_state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate an optimal action plan given priorities and constraints

        Args:
            priorities: Prioritized tasks
            constraints: Identified constraints
            user_state: Current user state

        Returns:
            List of planned actions
        """
        self.logger.info("Generating action plan")

        action_plan = []

        # Match tasks to available time blocks
        available_time = constraints.get("time", {}).get("available_blocks", [])

        # Match task complexity to user energy
        energy_level = user_state.get("energy_level", "medium")

        for task in priorities[:10]:  # Top 10 priorities
            action = {
                "id": task["id"],
                "type": "task_execution",
                "description": task["description"],
                "estimated_duration": self._estimate_duration(task),
                "requires_approval": self._requires_approval(task),
                "automation_candidate": self._can_automate(task),
                "optimal_time_slot": self._find_optimal_slot(task, available_time, energy_level),
                "dependencies": task.get("dependencies", []),
                "rationale": f"Priority score: {task['priority_score']}"
            }

            action_plan.append(action)

        return action_plan

    def identify_automatable_tasks(self, action_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identify which tasks can be automated

        Args:
            action_plan: Generated action plan

        Returns:
            List of tasks that can be automated
        """
        self.logger.info("Identifying automatable tasks")

        automatable = []

        for action in action_plan:
            if action.get("automation_candidate", False):
                automation_spec = {
                    "action_id": action["id"],
                    "automation_type": self._determine_automation_type(action),
                    "confidence": 0.8,  # How confident we are this can be automated
                    "script_template": None,
                    "requires_user_approval": True
                }

                automatable.append(automation_spec)

        return automatable

    def check_permissions(self, action_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Check which actions require user approval based on permission tiers

        Args:
            action_plan: Generated action plan

        Returns:
            List of actions requiring user confirmation
        """
        self.logger.info("Checking permissions for actions")

        needs_approval = []

        for action in action_plan:
            permission_tier = self._determine_permission_tier(action)

            if permission_tier in ["tier_2", "tier_3_first_run"]:
                needs_approval.append({
                    "action_id": action["id"],
                    "action_type": action["type"],
                    "description": action["description"],
                    "permission_tier": permission_tier,
                    "reason": self._get_approval_reason(permission_tier),
                    "estimated_impact": "medium"
                })

        return needs_approval

    # Helper methods

    def _extract_themes(self, items: List[Dict[str, Any]]) -> List[str]:
        """Extract common themes from items"""
        # In production, use LLM for theme extraction
        return ["project_management", "code_review", "communication"]

    def _generate_summary(
        self,
        priority_count: int,
        actionable_count: int,
        informational_count: int,
        themes: List[str]
    ) -> str:
        """Generate a situation summary"""
        return (
            f"You have {priority_count} critical tasks, "
            f"{actionable_count} actionable items, and "
            f"{informational_count} informational updates. "
            f"Key themes: {', '.join(themes[:3])}."
        )

    def _calculate_available_time(self) -> List[Dict[str, Any]]:
        """Calculate available time blocks"""
        # In production, would integrate with calendar
        return [
            {"start": "09:00", "end": "12:00", "duration_minutes": 180},
            {"start": "14:00", "end": "17:00", "duration_minutes": 180}
        ]

    def _get_available_tools(self) -> List[str]:
        """Get list of available automation tools"""
        return ["email", "calendar", "code_execution", "file_operations"]

    def _estimate_duration(self, task: Dict[str, Any]) -> int:
        """Estimate task duration in minutes"""
        effort = task.get("estimated_effort", "medium")
        duration_map = {"low": 15, "medium": 30, "high": 60}
        return duration_map.get(effort, 30)

    def _requires_approval(self, task: Dict[str, Any]) -> bool:
        """Check if task requires user approval"""
        # Default to requiring approval for safety
        return True

    def _can_automate(self, task: Dict[str, Any]) -> bool:
        """Check if task can be automated"""
        # Simple heuristic - in production, use LLM
        automatable_keywords = ["send", "schedule", "update", "move", "sort"]
        description = task.get("description", "").lower()
        return any(keyword in description for keyword in automatable_keywords)

    def _find_optimal_slot(
        self,
        task: Dict[str, Any],
        available_time: List[Dict[str, Any]],
        energy_level: str
    ) -> Optional[Dict[str, Any]]:
        """Find optimal time slot for task"""
        # Match high-effort tasks to high-energy slots
        if available_time:
            return available_time[0]
        return None

    def _determine_automation_type(self, action: Dict[str, Any]) -> str:
        """Determine type of automation for action"""
        action_type = action.get("type", "")
        if "email" in action_type:
            return "email_automation"
        elif "calendar" in action_type:
            return "calendar_automation"
        elif "code" in action_type:
            return "code_execution"
        return "generic_automation"

    def _determine_permission_tier(self, action: Dict[str, Any]) -> str:
        """Determine permission tier for action"""
        action_type = action.get("type", "")

        # Tier 1: Read-only (no approval needed)
        read_only_actions = ["search", "analyze", "summarize", "read"]
        if any(ro in action_type for ro in read_only_actions):
            return "tier_1"

        # Tier 3: Autonomous (background, pre-approved)
        autonomous_actions = ["sort", "organize", "tag"]
        if any(auto in action_type for auto in autonomous_actions):
            return "tier_3"

        # Tier 2: Draft (requires approval)
        return "tier_2"

    def _get_approval_reason(self, tier: str) -> str:
        """Get reason why approval is needed"""
        reasons = {
            "tier_2": "This action will modify data or send messages",
            "tier_3_first_run": "First time running this automation",
        }
        return reasons.get(tier, "Requires approval for safety")
