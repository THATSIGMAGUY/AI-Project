"""
Permission Manager - Implements tiered permission system
"""

from typing import Dict, Any
from enum import Enum
import logging


class PermissionTier(Enum):
    """Permission tiers as defined in the system design"""
    TIER_1_READ_ONLY = "tier_1"  # No approval needed
    TIER_2_DRAFT = "tier_2"       # User must approve
    TIER_3_AUTONOMOUS = "tier_3"   # Runs in background (shadow mode)


class PermissionManager:
    """
    Manages permission tiers and approval requirements.

    Tier 1 (Read-Only):
    - Summarize emails
    - Search files
    - Analyze calendar
    - No approval needed

    Tier 2 (Draft):
    - Write email drafts
    - Write code
    - Create calendar invites
    - User must click "Approve" to send/run

    Tier 3 (Autonomous):
    - Sorting files
    - Scheduling confirmed meetings
    - Data entry
    - Runs in background (Shadow Mode)
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Load permission rules
        self.permission_rules = self._load_permission_rules(config)

        # Track shadow mode completions for Tier 3
        self.shadow_mode_log: Dict[str, int] = {}

        # User-configured overrides
        self.user_overrides = config.get("user_overrides", {})

    def _load_permission_rules(self, config: Dict[str, Any]) -> Dict[str, PermissionTier]:
        """Load default permission rules"""
        return {
            # Tier 1: Read-only actions
            "search": PermissionTier.TIER_1_READ_ONLY,
            "read": PermissionTier.TIER_1_READ_ONLY,
            "analyze": PermissionTier.TIER_1_READ_ONLY,
            "summarize": PermissionTier.TIER_1_READ_ONLY,
            "list": PermissionTier.TIER_1_READ_ONLY,

            # Tier 2: Draft/approval required
            "send_email": PermissionTier.TIER_2_DRAFT,
            "create_event": PermissionTier.TIER_2_DRAFT,
            "execute_code": PermissionTier.TIER_2_DRAFT,
            "write_file": PermissionTier.TIER_2_DRAFT,
            "delete": PermissionTier.TIER_2_DRAFT,
            "modify": PermissionTier.TIER_2_DRAFT,

            # Tier 3: Autonomous
            "sort": PermissionTier.TIER_3_AUTONOMOUS,
            "organize": PermissionTier.TIER_3_AUTONOMOUS,
            "tag": PermissionTier.TIER_3_AUTONOMOUS,
            "archive": PermissionTier.TIER_3_AUTONOMOUS,
        }

    def check_permission(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if an action is permitted and what approval is needed

        Args:
            action: Action to check

        Returns:
            Dict with permission decision
        """
        action_type = action.get("type", "")
        action_subtype = action.get("subtype", "")

        # Determine tier
        tier = self._determine_tier(action_type, action_subtype)

        # Check user overrides
        override = self._check_user_override(action_type)
        if override:
            tier = override

        # Build permission result
        result = {
            "allowed": True,
            "tier": tier.value,
            "requires_approval": False,
            "reason": ""
        }

        if tier == PermissionTier.TIER_1_READ_ONLY:
            # Always allowed, no approval needed
            result["requires_approval"] = False
            result["reason"] = "Read-only action, no approval needed"

        elif tier == PermissionTier.TIER_2_DRAFT:
            # Requires user approval
            result["requires_approval"] = True
            result["reason"] = "This action modifies data and requires approval"

        elif tier == PermissionTier.TIER_3_AUTONOMOUS:
            # Check if we've run this before successfully
            if self._is_first_run(action):
                result["requires_approval"] = True
                result["reason"] = "First time running this automation - requires approval"
            else:
                result["requires_approval"] = False
                result["reason"] = "Autonomous action, running in shadow mode"

        return result

    def _determine_tier(self, action_type: str, action_subtype: str) -> PermissionTier:
        """Determine the permission tier for an action"""
        # Check subtype first (more specific)
        if action_subtype and action_subtype in self.permission_rules:
            return self.permission_rules[action_subtype]

        # Check main action type
        for keyword, tier in self.permission_rules.items():
            if keyword in action_type.lower() or keyword in action_subtype.lower():
                return tier

        # Default to requiring approval for safety
        return PermissionTier.TIER_2_DRAFT

    def _check_user_override(self, action_type: str) -> PermissionTier:
        """Check if user has overridden permission for this action type"""
        return self.user_overrides.get(action_type)

    def _is_first_run(self, action: Dict[str, Any]) -> bool:
        """Check if this is the first time running this action type"""
        action_signature = f"{action.get('type')}:{action.get('subtype')}"

        if action_signature not in self.shadow_mode_log:
            return True

        # If we've run it successfully before, it's not first run
        return self.shadow_mode_log[action_signature] < 1

    def record_successful_execution(self, action: Dict[str, Any]) -> None:
        """
        Record successful execution of a Tier 3 action

        Args:
            action: The action that was executed
        """
        action_signature = f"{action.get('type')}:{action.get('subtype')}"

        if action_signature not in self.shadow_mode_log:
            self.shadow_mode_log[action_signature] = 0

        self.shadow_mode_log[action_signature] += 1
        self.logger.info(f"Recorded successful execution of {action_signature}")

    def update_user_override(self, action_type: str, tier: PermissionTier) -> None:
        """
        Allow user to override permission tier for an action type

        Args:
            action_type: Type of action
            tier: New permission tier
        """
        self.user_overrides[action_type] = tier
        self.logger.info(f"User override set: {action_type} -> {tier.value}")

    def get_permission_summary(self) -> Dict[str, Any]:
        """Get summary of permission configuration"""
        return {
            "total_rules": len(self.permission_rules),
            "user_overrides": len(self.user_overrides),
            "tier_1_actions": sum(1 for t in self.permission_rules.values()
                                 if t == PermissionTier.TIER_1_READ_ONLY),
            "tier_2_actions": sum(1 for t in self.permission_rules.values()
                                 if t == PermissionTier.TIER_2_DRAFT),
            "tier_3_actions": sum(1 for t in self.permission_rules.values()
                                 if t == PermissionTier.TIER_3_AUTONOMOUS),
            "shadow_mode_completions": len(self.shadow_mode_log)
        }
