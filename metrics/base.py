from abc import ABC, abstractmethod


class MetricCalculator(ABC):
    """Abstract base class for metric calculators."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the metric name (e.g., 'percentage')."""
        pass
    
    @abstractmethod
    def calculate(self, count: int, total: int) -> float:
        """Calculate the metric value from count and total."""
        pass
