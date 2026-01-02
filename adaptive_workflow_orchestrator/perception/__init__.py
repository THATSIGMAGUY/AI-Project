"""
Perception Module - The Sensors
Ingests data from various sources and filters noise to extract signals
"""

from .perception_module import PerceptionModule
from .data_filter import DataFilter
from .source_manager import SourceManager

__all__ = ["PerceptionModule", "DataFilter", "SourceManager"]
