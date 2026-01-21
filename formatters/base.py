from abc import ABC, abstractmethod
from typing import Dict, List

from models import DimensionStat


class ReportFormatter(ABC):
    """Abstract base class for report formatters."""
    
    @abstractmethod
    def format(self, stats: Dict[str, List[DimensionStat]]) -> str:
        """Format statistics into a report string."""
        pass
