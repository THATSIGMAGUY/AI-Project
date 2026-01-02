"""
Memory System - Short-term and Long-term Memory
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import deque
import logging
import json


class ShortTermMemory:
    """
    Short-term memory for current conversation context.
    Stores recent interactions and current state.
    """

    def __init__(self, max_items: int = 100):
        self.max_items = max_items
        self.storage: Dict[str, Any] = {}
        self.access_log: deque = deque(maxlen=max_items)
        self.logger = logging.getLogger(__name__)

    def store(self, key: str, value: Any) -> None:
        """Store an item in short-term memory"""
        self.storage[key] = {
            "value": value,
            "stored_at": datetime.now().isoformat(),
            "access_count": 0
        }
        self.access_log.append({
            "key": key,
            "action": "store",
            "timestamp": datetime.now().isoformat()
        })

        # Evict old items if we're over capacity
        if len(self.storage) > self.max_items:
            self._evict_oldest()

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve an item from short-term memory"""
        if key in self.storage:
            item = self.storage[key]
            item["access_count"] += 1
            item["last_accessed"] = datetime.now().isoformat()

            self.access_log.append({
                "key": key,
                "action": "retrieve",
                "timestamp": datetime.now().isoformat()
            })

            return item["value"]
        return None

    def clear(self) -> None:
        """Clear short-term memory"""
        self.storage.clear()
        self.access_log.clear()
        self.logger.info("Short-term memory cleared")

    def _evict_oldest(self) -> None:
        """Evict the least recently used item"""
        if not self.storage:
            return

        # Find item with oldest last_accessed time
        oldest_key = min(
            self.storage.keys(),
            key=lambda k: self.storage[k].get("last_accessed", self.storage[k]["stored_at"])
        )
        del self.storage[oldest_key]
        self.logger.debug(f"Evicted {oldest_key} from short-term memory")

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_items": len(self.storage),
            "capacity": self.max_items,
            "utilization": len(self.storage) / self.max_items,
            "total_accesses": len(self.access_log)
        }


class LongTermMemory:
    """
    Long-term memory using a vector database for semantic search.
    Stores past projects, templates, and learned patterns.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # In production, this would use an actual vector database (Pinecone, Weaviate, etc.)
        # For now, using simple in-memory storage
        self.storage: List[Dict[str, Any]] = []
        self.patterns: Dict[str, List[Dict[str, Any]]] = {}

    def store(self, content: Any, metadata: Dict[str, Any]) -> str:
        """
        Store an item in long-term memory

        Args:
            content: The content to store
            metadata: Metadata about the content (type, tags, timestamp, etc.)

        Returns:
            ID of the stored item
        """
        item_id = f"ltm_{len(self.storage)}_{datetime.now().timestamp()}"

        item = {
            "id": item_id,
            "content": content,
            "metadata": metadata,
            "stored_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": None
        }

        self.storage.append(item)
        self.logger.debug(f"Stored item {item_id} in long-term memory")

        return item_id

    def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar items using semantic search

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of similar items
        """
        # In production, this would use vector similarity search
        # For now, simple keyword matching
        results = []

        for item in self.storage:
            # Simple relevance score based on keyword overlap
            score = self._calculate_relevance(query, item)
            if score > 0:
                results.append({
                    **item,
                    "relevance_score": score
                })

        # Sort by relevance and return top results
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]

    def get_patterns(self, pattern_type: str) -> List[Dict[str, Any]]:
        """
        Retrieve learned patterns of a specific type

        Args:
            pattern_type: Type of pattern (e.g., "user_activity", "email_templates")

        Returns:
            List of patterns
        """
        return self.patterns.get(pattern_type, [])

    def store_pattern(self, pattern_type: str, pattern: Dict[str, Any]) -> None:
        """
        Store a learned pattern

        Args:
            pattern_type: Type of pattern
            pattern: Pattern data
        """
        if pattern_type not in self.patterns:
            self.patterns[pattern_type] = []

        pattern["stored_at"] = datetime.now().isoformat()
        self.patterns[pattern_type].append(pattern)
        self.logger.info(f"Stored new {pattern_type} pattern")

    def recall(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Recall a specific item by ID

        Args:
            item_id: ID of the item to recall

        Returns:
            The item if found, None otherwise
        """
        for item in self.storage:
            if item["id"] == item_id:
                item["access_count"] += 1
                item["last_accessed"] = datetime.now().isoformat()
                return item
        return None

    def _calculate_relevance(self, query: str, item: Dict[str, Any]) -> float:
        """Calculate relevance score between query and item"""
        # Simple keyword-based relevance (in production, use embeddings)
        query_words = set(query.lower().split())
        content_str = str(item["content"]).lower()

        matches = sum(1 for word in query_words if word in content_str)
        return matches / max(len(query_words), 1)

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_items": len(self.storage),
            "total_patterns": sum(len(patterns) for patterns in self.patterns.values()),
            "pattern_types": list(self.patterns.keys()),
            "storage_size_estimate": len(str(self.storage))  # Rough estimate
        }


class MemorySystem:
    """
    Unified memory system combining short-term and long-term memory
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize both memory types
        self.short_term = ShortTermMemory(
            max_items=config.get("short_term_capacity", 100)
        )
        self.long_term = LongTermMemory(
            config.get("long_term", {})
        )

    def consolidate(self) -> None:
        """
        Consolidate important items from short-term to long-term memory.
        This mimics how human memory works - important items get consolidated.
        """
        self.logger.info("Consolidating memories")

        # Identify important items (high access count)
        threshold_access_count = 3

        for key, item in self.short_term.storage.items():
            if item["access_count"] >= threshold_access_count:
                # Move to long-term memory
                self.long_term.store(
                    content=item["value"],
                    metadata={
                        "type": "consolidated_memory",
                        "original_key": key,
                        "access_count": item["access_count"],
                        "short_term_stored_at": item["stored_at"]
                    }
                )
                self.logger.debug(f"Consolidated {key} to long-term memory")

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about both memory systems"""
        return {
            "short_term": self.short_term.get_stats(),
            "long_term": self.long_term.get_stats()
        }
