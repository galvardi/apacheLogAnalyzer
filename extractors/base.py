from abc import ABC, abstractmethod

from models import LogEntry


class DimensionExtractor(ABC):
    """Abstract base class for dimension extractors."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the dimension name for reporting (e.g., 'Country')."""
        pass
    
    @abstractmethod
    def extract(self, entry: LogEntry) -> str:
        """Extract dimension value from a log entry."""
        pass
