"""
Morning Briefer Mode - Management and planning mode

Runs at the start of the day to provide a comprehensive briefing
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging


class MorningBriefer:
    """
    Mode A: The Morning Briefer (Management)

    Provides a synthesized, prioritized view of the day ahead.

    Features:
    - Scans all inboxes and calendars
    - Identifies critical tasks and blockers
    - Calculates available deep work time
    - Presents a single, actionable priority list
    - Eliminates decision fatigue
    """

    def __init__(self, orchestrator):
        """
        Initialize with reference to main orchestrator

        Args:
            orchestrator: Main AdaptiveWorkflowOrchestrator instance
        """
        self.orchestrator = orchestrator
        self.logger = logging.getLogger(__name__)

    def run_morning_briefing(self, time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Execute the morning briefing protocol

        Args:
            time: Optional time for the briefing (defaults to now)

        Returns:
            Dict containing the morning briefing
        """
        if time is None:
            time = datetime.now()

        self.logger.info(f"Running morning briefing for {time.strftime('%Y-%m-%d')}")

        briefing = {
            "date": time.strftime("%Y-%m-%d"),
            "generated_at": datetime.now().isoformat(),
            "greeting": self._generate_greeting(time),
            "summary": {},
            "critical_tasks": [],
            "blockers": [],
            "meetings": [],
            "available_time": {},
            "recommendations": []
        }

        # Run an OODA cycle to gather current state
        cycle_result = self.orchestrator.ooda_loop.run_cycle({
            "mode": "morning_briefing",
            "time": time.isoformat()
        })

        # Extract relevant information from cycle
        filtered_data = cycle_result["phases"]["observe"]["filtered_data"]
        orientation = cycle_result["phases"]["orient"]

        # Generate summary
        briefing["summary"] = self._generate_summary(filtered_data, orientation)

        # Extract critical tasks
        briefing["critical_tasks"] = self._extract_critical_tasks(
            filtered_data.get("priority_items", []),
            filtered_data.get("actionable_items", [])
        )

        # Identify blockers
        briefing["blockers"] = self._identify_blockers(filtered_data)

        # Extract today's meetings
        briefing["meetings"] = self._extract_todays_meetings(filtered_data)

        # Calculate available time
        briefing["available_time"] = self._calculate_available_time(
            briefing["meetings"],
            time
        )

        # Generate recommendations
        briefing["recommendations"] = self._generate_recommendations(
            briefing["critical_tasks"],
            briefing["available_time"],
            orientation
        )

        return briefing

    def format_briefing(self, briefing: Dict[str, Any]) -> str:
        """
        Format briefing for display

        Args:
            briefing: Briefing data

        Returns:
            Formatted string for display
        """
        output = []

        # Header
        output.append("=" * 60)
        output.append(f"  {briefing['greeting']}")
        output.append("=" * 60)
        output.append("")

        # Summary
        summary = briefing["summary"]
        output.append("📊 TODAY'S OVERVIEW")
        output.append("-" * 60)
        output.append(f"Critical Tasks: {summary.get('critical_count', 0)}")
        output.append(f"Meetings: {summary.get('meeting_count', 0)}")
        output.append(f"Available Deep Work Time: {summary.get('deep_work_hours', 0):.1f} hours")
        output.append(f"Urgency Level: {summary.get('urgency_level', 'normal').upper()}")
        output.append("")

        # Critical Tasks
        if briefing["critical_tasks"]:
            output.append("🎯 CRITICAL TASKS")
            output.append("-" * 60)
            for i, task in enumerate(briefing["critical_tasks"][:5], 1):
                output.append(f"{i}. {task['title']}")
                output.append(f"   Priority: {task['priority']} | Est: {task['estimated_duration']}min")
                if task.get('deadline'):
                    output.append(f"   Deadline: {task['deadline']}")
                output.append("")

        # Blockers
        if briefing["blockers"]:
            output.append("🚧 BLOCKERS")
            output.append("-" * 60)
            for blocker in briefing["blockers"]:
                output.append(f"• {blocker['description']}")
                output.append(f"  Awaiting: {blocker.get('awaiting', 'resolution')}")
                output.append("")

        # Meetings
        if briefing["meetings"]:
            output.append("📅 TODAY'S MEETINGS")
            output.append("-" * 60)
            for meeting in briefing["meetings"]:
                output.append(f"• {meeting['time']} - {meeting['title']} ({meeting['duration']}min)")
                if meeting.get('prep_needed'):
                    output.append(f"  ⚠️  Requires preparation")
                output.append("")

        # Recommendations
        if briefing["recommendations"]:
            output.append("💡 RECOMMENDATIONS")
            output.append("-" * 60)
            for rec in briefing["recommendations"]:
                output.append(f"• {rec}")
            output.append("")

        output.append("=" * 60)

        return "\n".join(output)

    # Helper methods

    def _generate_greeting(self, time: datetime) -> str:
        """Generate time-appropriate greeting"""
        hour = time.hour

        if hour < 12:
            return f"Good Morning! Here's your briefing for {time.strftime('%A, %B %d')}"
        elif hour < 17:
            return f"Good Afternoon! Here's your briefing for {time.strftime('%A, %B %d')}"
        else:
            return f"Good Evening! Here's your briefing for {time.strftime('%A, %B %d')}"

    def _generate_summary(
        self,
        filtered_data: Dict[str, Any],
        orientation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate high-level summary"""

        priority_count = len(filtered_data.get("priority_items", []))
        actionable_count = len(filtered_data.get("actionable_items", []))

        return {
            "critical_count": priority_count,
            "actionable_count": actionable_count,
            "meeting_count": 0,  # Will be updated
            "deep_work_hours": 0,  # Will be updated
            "urgency_level": orientation.get("context", {}).get("urgency_level", "normal")
        }

    def _extract_critical_tasks(
        self,
        priority_items: List[Dict[str, Any]],
        actionable_items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract and format critical tasks"""

        tasks = []

        for item in priority_items[:5]:  # Top 5 critical
            tasks.append({
                "title": item.get("title", item.get("subject", "Untitled task")),
                "priority": "critical",
                "estimated_duration": item.get("estimated_duration", 30),
                "deadline": item.get("deadline"),
                "source": item.get("source", "unknown")
            })

        return tasks

    def _identify_blockers(self, filtered_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify blocking items"""

        blockers = []

        # Look for items explicitly marked as blockers
        for item in filtered_data.get("priority_items", []):
            if item.get("blocked", False) or "blocker" in item.get("tags", []):
                blockers.append({
                    "description": item.get("title", "Unknown blocker"),
                    "awaiting": item.get("awaiting", "response"),
                    "since": item.get("created_at", "")
                })

        return blockers

    def _extract_todays_meetings(self, filtered_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract today's meetings"""

        meetings = []
        today = datetime.now().date()

        # This would come from calendar data in filtered_data
        # For now, return empty list (would be populated from actual calendar)

        return meetings

    def _calculate_available_time(
        self,
        meetings: List[Dict[str, Any]],
        time: datetime
    ) -> Dict[str, Any]:
        """Calculate available time blocks for deep work"""

        # Assume 8-hour workday (9am-5pm)
        work_start = time.replace(hour=9, minute=0, second=0)
        work_end = time.replace(hour=17, minute=0, second=0)

        total_work_minutes = 8 * 60  # 480 minutes

        # Subtract meeting time
        meeting_minutes = sum(m.get("duration", 0) for m in meetings)

        # Subtract buffer time (15 min per meeting for context switching)
        buffer_minutes = len(meetings) * 15

        available_minutes = total_work_minutes - meeting_minutes - buffer_minutes

        return {
            "total_hours": available_minutes / 60,
            "total_minutes": available_minutes,
            "meeting_time_minutes": meeting_minutes,
            "buffer_time_minutes": buffer_minutes,
            "blocks": self._identify_time_blocks(meetings, work_start, work_end)
        }

    def _identify_time_blocks(
        self,
        meetings: List[Dict[str, Any]],
        work_start: datetime,
        work_end: datetime
    ) -> List[Dict[str, Any]]:
        """Identify continuous time blocks"""

        # In production, would calculate blocks between meetings
        # For now, return example blocks

        return [
            {"start": "09:00", "end": "12:00", "duration_minutes": 180, "type": "deep_work"},
            {"start": "14:00", "end": "17:00", "duration_minutes": 180, "type": "deep_work"}
        ]

    def _generate_recommendations(
        self,
        critical_tasks: List[Dict[str, Any]],
        available_time: Dict[str, Any],
        orientation: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations"""

        recommendations = []

        # Time management recommendations
        deep_work_hours = available_time.get("total_hours", 0)

        if deep_work_hours >= 4:
            recommendations.append(
                f"You have {deep_work_hours:.1f} hours of deep work time available. "
                "Consider tackling your most complex tasks during these blocks."
            )
        elif deep_work_hours >= 2:
            recommendations.append(
                f"You have {deep_work_hours:.1f} hours of focused time. "
                "Prioritize your top 2-3 critical tasks."
            )
        else:
            recommendations.append(
                "Your day is heavily scheduled. Consider rescheduling non-critical meetings "
                "to create focused work time."
            )

        # Task prioritization
        if len(critical_tasks) > 5:
            recommendations.append(
                f"You have {len(critical_tasks)} critical tasks. "
                "Consider delegating or deferring lower-priority items."
            )

        # Energy optimization
        energy_level = orientation.get("user_state", {}).get("energy_level", "medium")

        if energy_level == "high":
            recommendations.append(
                "Your energy is high this morning. Tackle complex, creative work first."
            )

        return recommendations
