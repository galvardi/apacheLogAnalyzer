from collections import Counter
from typing import Dict, List, Optional

from models import DimensionStat
from metrics.base import MetricCalculator


class StatisticsAggregator:
    """Aggregates dimension values and computes statistics."""
    
    def __init__(self, metric: MetricCalculator):
        self._data: Dict[str, Counter] = {}
        self._total_entries: int = 0
        self._metric = metric
    
    def add(self, dimension: str, value: str) -> None:
        """Add a value for a dimension."""
        if dimension not in self._data:
            self._data[dimension] = Counter()
        self._data[dimension][value] += 1
    
    def increment_total(self) -> None:
        """Increment total entry count."""
        self._total_entries += 1
    
    @property
    def total_entries(self) -> int:
        """Return total number of entries processed."""
        return self._total_entries
    
    @property
    def dimensions(self) -> List[str]:
        """Return list of dimension names."""
        return list(self._data.keys())
    
    def get_statistics(self, dimension: str, sort_by: str = "percentage",
                       sort_order: str = "descending",
                       cutoff_percentage: Optional[float] = None) -> List[DimensionStat]:
        """Get statistics for a dimension, sorted as specified."""
        counter = self._data.get(dimension, Counter())
        
        stats = []
        other_count = 0
        
        for value, count in counter.items():
            percentage = self._metric.calculate(count, self._total_entries)
            
            if cutoff_percentage is not None and percentage < cutoff_percentage:
                other_count += count
            else:
                stats.append(DimensionStat(
                    value=value,
                    count=count,
                    metric_value=percentage
                ))
        
        # Add "Other" if there are values below cutoff
        if other_count > 0:
            stats.append(DimensionStat(
                value="Other",
                count=other_count,
                metric_value=self._metric.calculate(other_count, self._total_entries)
            ))
        
        # Sort by specified field
        if sort_by == "percentage" or sort_by == "metric_value":
            key_func = lambda s: s.metric_value
        elif sort_by == "count":
            key_func = lambda s: s.count
        else:
            key_func = lambda s: s.value
        
        reverse = sort_order == "descending"
        return sorted(stats, key=key_func, reverse=reverse)
