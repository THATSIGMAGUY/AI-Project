"""
Perception Module - Main class for environmental sensing
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from .data_filter import DataFilter
from .source_manager import SourceManager


class PerceptionModule:
    """
    The agent's sensory system - watches inputs from various sources.

    Capabilities:
    - Email monitoring (IMAP)
    - Calendar tracking (CalDAV/Google Calendar API)
    - Project management tools (Jira, Trello, Notion)
    - Screen context (OCR for non-API apps)
    - File system monitoring
    - Code repository tracking
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.source_manager = SourceManager(config.get("sources", {}))
        self.data_filter = DataFilter(config.get("filters", {}))

        # Track last observation timestamps
        self.last_observation: Dict[str, datetime] = {}

        # Statistics
        self.stats = {
            "total_observations": 0,
            "filtered_items": 0,
            "sources_active": 0
        }

    def gather_all_sources(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Gather data from all configured sources

        Args:
            context: Optional context to guide data gathering

        Returns:
            Dict with data from all sources
        """
        self.logger.info("Gathering data from all sources")
        self.stats["total_observations"] += 1

        sources_data = {
            "timestamp": datetime.now().isoformat(),
            "email": {},
            "calendar": {},
            "project_management": {},
            "code": {},
            "filesystem": {},
            "screen": {}
        }

        # Gather from each source type
        try:
            sources_data["email"] = self.source_manager.gather_email(context)
        except Exception as e:
            self.logger.error(f"Error gathering email data: {e}")
            sources_data["email"] = {"error": str(e)}

        try:
            sources_data["calendar"] = self.source_manager.gather_calendar(context)
        except Exception as e:
            self.logger.error(f"Error gathering calendar data: {e}")
            sources_data["calendar"] = {"error": str(e)}

        try:
            sources_data["project_management"] = self.source_manager.gather_project_management(context)
        except Exception as e:
            self.logger.error(f"Error gathering project management data: {e}")
            sources_data["project_management"] = {"error": str(e)}

        try:
            sources_data["code"] = self.source_manager.gather_code_activity(context)
        except Exception as e:
            self.logger.error(f"Error gathering code data: {e}")
            sources_data["code"] = {"error": str(e)}

        try:
            sources_data["filesystem"] = self.source_manager.gather_filesystem_changes(context)
        except Exception as e:
            self.logger.error(f"Error gathering filesystem data: {e}")
            sources_data["filesystem"] = {"error": str(e)}

        # Update statistics
        active_sources = sum(1 for data in sources_data.values()
                           if isinstance(data, dict) and "error" not in data)
        self.stats["sources_active"] = active_sources

        return sources_data

    def filter_and_structure(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply intelligent filters to reduce noise and structure data

        Args:
            raw_data: Raw data from all sources

        Returns:
            Filtered and structured data
        """
        self.logger.info("Filtering and structuring raw data")

        structured_data = {
            "timestamp": datetime.now().isoformat(),
            "priority_items": [],
            "background_items": [],
            "actionable_items": [],
            "informational_items": [],
            "metadata": {}
        }

        # Filter email data
        if raw_data.get("email") and "error" not in raw_data["email"]:
            email_filtered = self.data_filter.filter_email(raw_data["email"])
            structured_data["priority_items"].extend(email_filtered.get("urgent", []))
            structured_data["actionable_items"].extend(email_filtered.get("actionable", []))
            structured_data["informational_items"].extend(email_filtered.get("informational", []))

        # Filter calendar data
        if raw_data.get("calendar") and "error" not in raw_data["calendar"]:
            calendar_filtered = self.data_filter.filter_calendar(raw_data["calendar"])
            structured_data["priority_items"].extend(calendar_filtered.get("upcoming_critical", []))
            structured_data["actionable_items"].extend(calendar_filtered.get("needs_prep", []))

        # Filter project management data
        if raw_data.get("project_management") and "error" not in raw_data["project_management"]:
            pm_filtered = self.data_filter.filter_project_management(raw_data["project_management"])
            structured_data["priority_items"].extend(pm_filtered.get("blocked", []))
            structured_data["actionable_items"].extend(pm_filtered.get("in_progress", []))
            structured_data["background_items"].extend(pm_filtered.get("backlog", []))

        # Filter code activity
        if raw_data.get("code") and "error" not in raw_data["code"]:
            code_filtered = self.data_filter.filter_code_activity(raw_data["code"])
            structured_data["actionable_items"].extend(code_filtered.get("reviews_needed", []))
            structured_data["informational_items"].extend(code_filtered.get("recent_changes", []))

        # Add metadata about filtering
        structured_data["metadata"] = {
            "total_items": (len(structured_data["priority_items"]) +
                          len(structured_data["actionable_items"]) +
                          len(structured_data["informational_items"]) +
                          len(structured_data["background_items"])),
            "filtered_count": self.data_filter.get_filtered_count(),
            "noise_reduction_ratio": self.data_filter.get_noise_reduction_ratio()
        }

        self.stats["filtered_items"] += structured_data["metadata"]["filtered_count"]

        return structured_data

    def get_statistics(self) -> Dict[str, Any]:
        """Get perception module statistics"""
        return {
            **self.stats,
            "last_observation": self.last_observation
        }

    def reset_statistics(self):
        """Reset statistics counters"""
        self.stats = {
            "total_observations": 0,
            "filtered_items": 0,
            "sources_active": 0
        }
