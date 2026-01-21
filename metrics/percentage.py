from metrics.base import MetricCalculator


class PercentageMetric(MetricCalculator):
    """Calculates percentage of total."""
    
    @property
    def name(self) -> str:
        return "percentage"
    
    def calculate(self, count: int, total: int) -> float:
        if total == 0:
            return 0.0
        return round((count / total) * 100, 2)
