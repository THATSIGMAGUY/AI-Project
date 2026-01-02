"""
Data Filter - Reduces noise and extracts signals from raw data
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import re
import logging


class DataFilter:
    """
    Intelligent filtering system to reduce noise and highlight important signals.

    Filters work on multiple levels:
    - Priority-based (urgent vs. informational)
    - Pattern-based (recurring emails, common notifications)
    - User preference-based (learned from past interactions)
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Load filtering rules
        self.spam_patterns = config.get("spam_patterns", [])
        self.priority_keywords = config.get("priority_keywords", [
            "urgent", "critical", "asap", "deadline", "blocker", "emergency"
        ])
        self.noise_senders = config.get("noise_senders", [])

        # Statistics
        self.filtered_count = 0
        self.total_processed = 0

    def filter_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter email data into categories

        Returns:
            Dict with categorized emails: urgent, actionable, informational, spam
        """
        categorized = {
            "urgent": [],
            "actionable": [],
            "informational": [],
            "spam": []
        }

        emails = email_data.get("messages", [])
        self.total_processed += len(emails)

        for email in emails:
            # Check if spam
            if self._is_spam(email):
                categorized["spam"].append(email)
                self.filtered_count += 1
                continue

            # Check if from noise sender
            if self._is_noise_sender(email.get("from", "")):
                categorized["spam"].append(email)
                self.filtered_count += 1
                continue

            # Categorize by priority
            if self._is_urgent(email):
                categorized["urgent"].append(email)
            elif self._is_actionable(email):
                categorized["actionable"].append(email)
            else:
                categorized["informational"].append(email)

        return categorized

    def filter_calendar(self, calendar_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter calendar events by urgency and preparation needs

        Returns:
            Dict with categorized events
        """
        categorized = {
            "upcoming_critical": [],
            "needs_prep": [],
            "routine": []
        }

        events = calendar_data.get("events", [])
        now = datetime.now()

        for event in events:
            event_time = datetime.fromisoformat(event.get("start", now.isoformat()))
            time_until = event_time - now

            # Events in the next 2 hours are critical
            if time_until < timedelta(hours=2):
                categorized["upcoming_critical"].append(event)
            # Events in the next 24 hours that need prep
            elif time_until < timedelta(hours=24) and event.get("requires_prep", False):
                categorized["needs_prep"].append(event)
            else:
                categorized["routine"].append(event)

        return categorized

    def filter_project_management(self, pm_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter project management tasks by status and priority

        Returns:
            Dict with categorized tasks
        """
        categorized = {
            "blocked": [],
            "in_progress": [],
            "backlog": [],
            "completed": []
        }

        tasks = pm_data.get("tasks", [])

        for task in tasks:
            status = task.get("status", "").lower()
            priority = task.get("priority", "medium").lower()

            if "blocked" in status or task.get("blockers", []):
                categorized["blocked"].append(task)
            elif "in progress" in status or "doing" in status:
                categorized["in_progress"].append(task)
            elif status == "done" or status == "completed":
                categorized["completed"].append(task)
            else:
                categorized["backlog"].append(task)

        # Sort each category by priority
        for category in categorized:
            categorized[category].sort(
                key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(
                    x.get("priority", "medium").lower(), 1
                )
            )

        return categorized

    def filter_code_activity(self, code_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter code activity by actionability

        Returns:
            Dict with categorized code items
        """
        categorized = {
            "reviews_needed": [],
            "recent_changes": [],
            "ci_failures": []
        }

        # Pull requests needing review
        prs = code_data.get("pull_requests", [])
        for pr in prs:
            if pr.get("needs_review", False):
                categorized["reviews_needed"].append(pr)

        # Recent commits
        commits = code_data.get("commits", [])
        categorized["recent_changes"] = commits[:10]  # Latest 10

        # CI/CD failures
        ci_results = code_data.get("ci_results", [])
        for result in ci_results:
            if result.get("status") == "failed":
                categorized["ci_failures"].append(result)

        return categorized

    def _is_spam(self, email: Dict[str, Any]) -> bool:
        """Check if email matches spam patterns"""
        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()

        for pattern in self.spam_patterns:
            if re.search(pattern, subject) or re.search(pattern, body):
                return True
        return False

    def _is_noise_sender(self, sender: str) -> bool:
        """Check if sender is in noise list"""
        sender_lower = sender.lower()
        return any(noise in sender_lower for noise in self.noise_senders)

    def _is_urgent(self, email: Dict[str, Any]) -> bool:
        """Check if email is urgent"""
        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()
        priority = email.get("priority", "normal").lower()

        # Check priority header
        if priority == "high" or priority == "urgent":
            return True

        # Check for urgent keywords
        urgent_indicators = subject + " " + body
        return any(keyword in urgent_indicators for keyword in self.priority_keywords)

    def _is_actionable(self, email: Dict[str, Any]) -> bool:
        """Check if email requires action"""
        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()

        action_keywords = [
            "please", "can you", "could you", "need", "request",
            "action required", "review", "approve", "respond"
        ]

        content = subject + " " + body
        return any(keyword in content for keyword in action_keywords)

    def get_filtered_count(self) -> int:
        """Get count of filtered items"""
        return self.filtered_count

    def get_noise_reduction_ratio(self) -> float:
        """Calculate noise reduction ratio"""
        if self.total_processed == 0:
            return 0.0
        return self.filtered_count / self.total_processed
