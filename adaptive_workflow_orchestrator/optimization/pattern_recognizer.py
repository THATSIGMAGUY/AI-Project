"""
Pattern Recognizer - Detects repetitive patterns in user behavior
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging


class PatternRecognizer:
    """
    Analyzes action logs to detect repetitive patterns.

    Pattern types detected:
    - Temporal: "Every Friday at 3pm, user does X"
    - Sequential: "User always does A, then B, then C"
    - Trigger-based: "When X happens, user does Y"
    - Bulk: "User processes many similar items in a batch"
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.min_occurrences = config.get("min_occurrences", 3)
        self.lookback_days = config.get("lookback_days", 30)

        # Store detected patterns
        self.detected_patterns: List[Dict[str, Any]] = []

    def detect_patterns(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect patterns in a list of actions

        Args:
            actions: List of action log entries

        Returns:
            List of detected patterns
        """
        patterns = []

        # Detect different pattern types
        patterns.extend(self._detect_temporal_patterns(actions))
        patterns.extend(self._detect_sequential_patterns(actions))
        patterns.extend(self._detect_trigger_patterns(actions))
        patterns.extend(self._detect_bulk_patterns(actions))

        # Store newly detected patterns
        for pattern in patterns:
            if pattern not in self.detected_patterns:
                pattern["detected_at"] = datetime.now().isoformat()
                self.detected_patterns.append(pattern)

        return patterns

    def _detect_temporal_patterns(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect time-based patterns (e.g., every Monday at 9am)

        Returns:
            List of temporal patterns
        """
        patterns = []

        # Group actions by hour of day and day of week
        time_buckets = defaultdict(list)

        for action in actions:
            timestamp_str = action.get("timestamp", "")
            if not timestamp_str:
                continue

            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                hour = timestamp.hour
                day_of_week = timestamp.strftime("%A")  # Monday, Tuesday, etc.

                action_type = action.get("action", {}).get("type", action.get("type", ""))

                key = (day_of_week, hour, action_type)
                time_buckets[key].append(action)

            except Exception as e:
                continue

        # Find recurring temporal patterns
        for (day, hour, action_type), action_list in time_buckets.items():
            if len(action_list) >= self.min_occurrences:
                patterns.append({
                    "type": "temporal",
                    "pattern": f"{action_type}_every_{day}_at_{hour}h",
                    "frequency": len(action_list),
                    "details": {
                        "day_of_week": day,
                        "hour": hour,
                        "action_type": action_type
                    },
                    "description": f"You perform '{action_type}' every {day} around {hour}:00",
                    "automation_potential": "high"
                })

        return patterns

    def _detect_sequential_patterns(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect sequential patterns (e.g., always A->B->C)

        Returns:
            List of sequential patterns
        """
        patterns = []

        # Extract action sequences
        sequences = []
        current_sequence = []

        for i, action in enumerate(actions):
            action_type = action.get("action", {}).get("type", action.get("type", ""))

            if not action_type:
                continue

            current_sequence.append(action_type)

            # Consider sequences of 2-4 actions
            if len(current_sequence) >= 4:
                current_sequence.pop(0)

            # Look for this sequence in the rest of the data
            if len(current_sequence) >= 2:
                sequence_tuple = tuple(current_sequence)
                sequences.append(sequence_tuple)

        # Find frequently occurring sequences
        sequence_counts = Counter(sequences)

        for sequence, count in sequence_counts.items():
            if count >= self.min_occurrences:
                patterns.append({
                    "type": "sequential",
                    "pattern": "->".join(sequence),
                    "frequency": count,
                    "details": {
                        "sequence": list(sequence),
                        "length": len(sequence)
                    },
                    "description": f"You often perform this sequence: {' → '.join(sequence)}",
                    "automation_potential": "high"
                })

        return patterns

    def _detect_trigger_patterns(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect trigger-based patterns (e.g., when email arrives, do X)

        Returns:
            List of trigger patterns
        """
        patterns = []

        # Look for action pairs within short time windows (5 minutes)
        time_window = timedelta(minutes=5)

        trigger_pairs = defaultdict(int)

        for i in range(len(actions) - 1):
            try:
                action1 = actions[i]
                action2 = actions[i + 1]

                time1 = datetime.fromisoformat(action1.get("timestamp", ""))
                time2 = datetime.fromisoformat(action2.get("timestamp", ""))

                if time2 - time1 <= time_window:
                    type1 = action1.get("action", {}).get("type", action1.get("type", ""))
                    type2 = action2.get("action", {}).get("type", action2.get("type", ""))

                    if type1 and type2 and type1 != type2:
                        trigger_pairs[(type1, type2)] += 1

            except Exception:
                continue

        # Find frequently occurring triggers
        for (trigger, response), count in trigger_pairs.items():
            if count >= self.min_occurrences:
                patterns.append({
                    "type": "trigger",
                    "pattern": f"{trigger}_triggers_{response}",
                    "frequency": count,
                    "details": {
                        "trigger": trigger,
                        "response": response
                    },
                    "description": f"When '{trigger}' happens, you usually do '{response}'",
                    "automation_potential": "medium"
                })

        return patterns

    def _detect_bulk_patterns(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect bulk processing patterns (e.g., user processes 20 emails at once)

        Returns:
            List of bulk patterns
        """
        patterns = []

        # Group actions by timestamp proximity (within 10 minutes = likely a batch)
        batch_window = timedelta(minutes=10)
        batches = []
        current_batch = []
        last_time = None

        for action in actions:
            try:
                timestamp = datetime.fromisoformat(action.get("timestamp", ""))
                action_type = action.get("action", {}).get("type", action.get("type", ""))

                if last_time is None or timestamp - last_time <= batch_window:
                    current_batch.append((timestamp, action_type, action))
                else:
                    if len(current_batch) >= 5:  # At least 5 actions in batch
                        batches.append(current_batch)
                    current_batch = [(timestamp, action_type, action)]

                last_time = timestamp

            except Exception:
                continue

        # Analyze batches
        for batch in batches:
            # Check if batch is homogeneous (same action type)
            action_types = [action_type for _, action_type, _ in batch]
            type_counts = Counter(action_types)

            dominant_type, dominant_count = type_counts.most_common(1)[0]

            if dominant_count >= len(batch) * 0.7:  # 70% same type
                patterns.append({
                    "type": "bulk",
                    "pattern": f"bulk_{dominant_type}",
                    "frequency": len(batches),
                    "details": {
                        "action_type": dominant_type,
                        "typical_batch_size": dominant_count,
                        "total_items": len(batch)
                    },
                    "description": f"You often process multiple '{dominant_type}' actions in batches",
                    "automation_potential": "very_high"
                })

        return patterns

    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get summary of detected patterns"""
        pattern_types = Counter(p.get("type") for p in self.detected_patterns)

        return {
            "total_patterns": len(self.detected_patterns),
            "by_type": dict(pattern_types),
            "high_potential": len([
                p for p in self.detected_patterns
                if p.get("automation_potential") in ["high", "very_high"]
            ]),
            "recent_patterns": self.detected_patterns[-10:]
        }
