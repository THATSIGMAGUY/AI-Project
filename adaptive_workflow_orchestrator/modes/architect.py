"""
Architect Mode - Weekly meta-review and optimization

Analyzes patterns and proposes systemic improvements
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging


class Architect:
    """
    Mode C: The Architect (Upgrading)

    Provides weekly meta-review and systemic optimization.

    Features:
    - Analyzes time allocation and patterns
    - Presents metrics and insights
    - Proposes automations and workflow improvements
    - Strategic planning assistance
    - System upgrade proposals
    """

    def __init__(self, orchestrator):
        """
        Initialize with reference to main orchestrator

        Args:
            orchestrator: Main AdaptiveWorkflowOrchestrator instance
        """
        self.orchestrator = orchestrator
        self.logger = logging.getLogger(__name__)

    def run_meta_review(
        self,
        period: str = "week",
        time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Run a meta-review of work patterns and productivity

        Args:
            period: Review period ("week", "month", "quarter")
            time: Optional end time for review (defaults to now)

        Returns:
            Meta-review report
        """
        if time is None:
            time = datetime.now()

        self.logger.info(f"Running meta-review for past {period}")

        # Calculate period boundaries
        period_start, period_end = self._get_period_boundaries(period, time)

        review = {
            "period": period,
            "start_date": period_start.strftime("%Y-%m-%d"),
            "end_date": period_end.strftime("%Y-%m-%d"),
            "generated_at": datetime.now().isoformat(),

            "time_analysis": {},
            "productivity_metrics": {},
            "pattern_insights": {},
            "optimization_proposals": [],
            "recommendations": [],
            "goals_progress": {}
        }

        # Analyze time allocation
        review["time_analysis"] = self._analyze_time_allocation(period_start, period_end)

        # Calculate productivity metrics
        review["productivity_metrics"] = self._calculate_productivity_metrics(
            period_start, period_end
        )

        # Get pattern insights from optimization loop
        review["pattern_insights"] = self._get_pattern_insights(period_start, period_end)

        # Get optimization proposals
        review["optimization_proposals"] = self._get_optimization_proposals()

        # Generate strategic recommendations
        review["recommendations"] = self._generate_strategic_recommendations(review)

        # Review goals progress
        review["goals_progress"] = self._review_goals_progress()

        return review

    def format_review(self, review: Dict[str, Any]) -> str:
        """
        Format meta-review for presentation

        Args:
            review: Review data

        Returns:
            Formatted string
        """
        output = []

        # Header
        output.append("=" * 70)
        output.append(f"  META-REVIEW: {review['period'].upper()}")
        output.append(f"  {review['start_date']} to {review['end_date']}")
        output.append("=" * 70)
        output.append("")

        # Time Analysis
        time_analysis = review["time_analysis"]
        output.append("⏱️  TIME ALLOCATION")
        output.append("-" * 70)
        output.append(f"Total Work Time: {time_analysis.get('total_hours', 0):.1f} hours")
        output.append("")
        output.append("Breakdown:")
        for category, hours in time_analysis.get("by_category", {}).items():
            percentage = (hours / max(time_analysis.get('total_hours', 1), 1)) * 100
            output.append(f"  {category.title()}: {hours:.1f}h ({percentage:.1f}%)")
        output.append("")

        # Productivity Metrics
        metrics = review["productivity_metrics"]
        output.append("📊 PRODUCTIVITY METRICS")
        output.append("-" * 70)
        output.append(f"Tasks Completed: {metrics.get('tasks_completed', 0)}")
        output.append(f"Automation Rate: {metrics.get('automation_rate', 0):.1%}")
        output.append(f"Time Saved by Automations: {metrics.get('time_saved_minutes', 0)} minutes")
        output.append(f"Average Response Time: {metrics.get('avg_response_time_hours', 0):.1f} hours")
        output.append("")

        # Pattern Insights
        insights = review["pattern_insights"]
        if insights.get("detected_patterns"):
            output.append("🔍 PATTERN INSIGHTS")
            output.append("-" * 70)
            for pattern in insights["detected_patterns"][:5]:
                output.append(f"• {pattern.get('description', 'Pattern detected')}")
                output.append(f"  Frequency: {pattern.get('frequency', 0)} times")
                output.append("")

        # Optimization Proposals
        proposals = review["optimization_proposals"]
        if proposals:
            output.append("💡 OPTIMIZATION PROPOSALS")
            output.append("-" * 70)
            for i, proposal in enumerate(proposals[:5], 1):
                output.append(f"{i}. {proposal.get('title', 'Optimization')}")
                output.append(f"   {proposal.get('description', '')}")
                output.append(f"   Estimated savings: {proposal.get('estimated_time_savings_minutes', 0)} min/week")
                output.append("")

        # Recommendations
        if review["recommendations"]:
            output.append("🎯 STRATEGIC RECOMMENDATIONS")
            output.append("-" * 70)
            for rec in review["recommendations"]:
                output.append(f"• {rec}")
            output.append("")

        # Goals Progress
        goals = review["goals_progress"]
        if goals.get("goals"):
            output.append("🎯 GOALS PROGRESS")
            output.append("-" * 70)
            for goal in goals["goals"]:
                progress = goal.get("progress", 0)
                bar = self._create_progress_bar(progress)
                output.append(f"{goal.get('title', 'Goal')}: {bar} {progress}%")
            output.append("")

        output.append("=" * 70)

        return "\n".join(output)

    def propose_upgrade(
        self,
        proposal_type: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Propose a system upgrade

        Args:
            proposal_type: Type of upgrade (automation, integration, workflow)
            details: Upgrade details

        Returns:
            Upgrade proposal
        """
        self.logger.info(f"Proposing upgrade: {proposal_type}")

        proposal = {
            "id": f"upgrade_{datetime.now().timestamp()}",
            "type": proposal_type,
            "created_at": datetime.now().isoformat(),
            "status": "proposed",
            "details": details,
            "impact_assessment": self._assess_upgrade_impact(proposal_type, details),
            "implementation_plan": self._create_implementation_plan(proposal_type, details)
        }

        return proposal

    # Helper methods

    def _get_period_boundaries(
        self,
        period: str,
        end_time: datetime
    ) -> tuple[datetime, datetime]:
        """Calculate period start and end times"""

        if period == "week":
            period_start = end_time - timedelta(days=7)
        elif period == "month":
            period_start = end_time - timedelta(days=30)
        elif period == "quarter":
            period_start = end_time - timedelta(days=90)
        else:
            period_start = end_time - timedelta(days=7)  # Default to week

        return period_start, end_time

    def _analyze_time_allocation(
        self,
        start: datetime,
        end: datetime
    ) -> Dict[str, Any]:
        """Analyze how time was spent during period"""

        # In production, would analyze actual logged activities
        return {
            "total_hours": 40.0,
            "by_category": {
                "meetings": 12.0,
                "coding": 15.0,
                "email": 5.0,
                "planning": 3.0,
                "admin": 2.0,
                "learning": 3.0
            },
            "by_day": {
                "Monday": 8.0,
                "Tuesday": 9.0,
                "Wednesday": 7.5,
                "Thursday": 8.5,
                "Friday": 7.0
            }
        }

    def _calculate_productivity_metrics(
        self,
        start: datetime,
        end: datetime
    ) -> Dict[str, Any]:
        """Calculate productivity metrics"""

        # Get optimization stats
        opt_stats = self.orchestrator.optimization.get_optimization_stats()

        return {
            "tasks_completed": 45,
            "automation_rate": 0.35,  # 35% of tasks automated
            "time_saved_minutes": opt_stats.get("time_saved_minutes", 0),
            "avg_response_time_hours": 4.2,
            "focus_time_percentage": 0.60,  # 60% time in focused work
            "context_switches_per_day": 12
        }

    def _get_pattern_insights(
        self,
        start: datetime,
        end: datetime
    ) -> Dict[str, Any]:
        """Get pattern insights from optimization loop"""

        pattern_summary = self.orchestrator.optimization.pattern_recognizer.get_pattern_summary()

        return {
            "total_patterns_detected": pattern_summary.get("total_patterns", 0),
            "detected_patterns": self.orchestrator.optimization.pattern_recognizer.detected_patterns,
            "high_automation_potential": pattern_summary.get("high_potential", 0)
        }

    def _get_optimization_proposals(self) -> List[Dict[str, Any]]:
        """Get active optimization proposals"""

        return self.orchestrator.optimization.get_active_proposals()

    def _generate_strategic_recommendations(self, review: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations based on review"""

        recommendations = []

        # Meeting time recommendations
        time_analysis = review.get("time_analysis", {})
        meeting_hours = time_analysis.get("by_category", {}).get("meetings", 0)
        total_hours = time_analysis.get("total_hours", 1)

        meeting_percentage = (meeting_hours / total_hours) * 100

        if meeting_percentage > 40:
            recommendations.append(
                f"You spent {meeting_percentage:.0f}% of your time in meetings. "
                "Consider declining non-essential meetings or delegating attendance."
            )

        # Automation recommendations
        metrics = review.get("productivity_metrics", {})
        automation_rate = metrics.get("automation_rate", 0)

        if automation_rate < 0.3:
            recommendations.append(
                f"Your automation rate is {automation_rate:.0%}. "
                f"You have {len(review.get('optimization_proposals', []))} pending automation proposals. "
                "Enabling these could save significant time."
            )

        # Focus time recommendations
        focus_percentage = metrics.get("focus_time_percentage", 0)

        if focus_percentage < 0.5:
            recommendations.append(
                f"Only {focus_percentage:.0%} of your time was spent in focused work. "
                "Consider blocking dedicated focus time on your calendar."
            )

        # Context switching
        context_switches = metrics.get("context_switches_per_day", 0)

        if context_switches > 15:
            recommendations.append(
                f"You averaged {context_switches} context switches per day. "
                "Try batching similar tasks together to maintain flow state."
            )

        return recommendations

    def _review_goals_progress(self) -> Dict[str, Any]:
        """Review progress on user's goals"""

        # Get goals from user manual
        user_goals = self.orchestrator.cognitive.user_manual.get_preference(
            "goals",
            "short_term",
            []
        )

        # Calculate progress (in production, would track actual progress)
        goals_with_progress = []

        for goal in user_goals:
            goals_with_progress.append({
                "title": goal.get("title", "Goal"),
                "progress": goal.get("progress", 50),  # Placeholder
                "target_date": goal.get("target_date"),
                "status": "on_track"
            })

        return {
            "total_goals": len(goals_with_progress),
            "goals": goals_with_progress,
            "on_track": len([g for g in goals_with_progress if g["status"] == "on_track"]),
            "at_risk": 0
        }

    def _assess_upgrade_impact(
        self,
        upgrade_type: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess impact of proposed upgrade"""

        return {
            "effort": "medium",  # low, medium, high
            "risk": "low",
            "estimated_time_savings": "2 hours/week",
            "user_value": "high",
            "dependencies": []
        }

    def _create_implementation_plan(
        self,
        upgrade_type: str,
        details: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create step-by-step implementation plan"""

        return [
            {"step": 1, "action": "Setup automation", "estimated_time": "15 min"},
            {"step": 2, "action": "Test automation", "estimated_time": "10 min"},
            {"step": 3, "action": "Enable and monitor", "estimated_time": "5 min"}
        ]

    def _create_progress_bar(self, progress: int, width: int = 20) -> str:
        """Create ASCII progress bar"""

        filled = int((progress / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"
