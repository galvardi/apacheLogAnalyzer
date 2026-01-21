from typing import Dict, List

from models import DimensionStat
from formatters.base import ReportFormatter


class ConsoleFormatter(ReportFormatter):
    """Formats statistics for console output."""
    
    def format(self, stats: Dict[str, List[DimensionStat]]) -> str:
        """Format statistics into console-friendly text."""
        lines = []
        
        for dimension, dimension_stats in stats.items():
            lines.append(f"{dimension}:")
            
            for stat in dimension_stats:
                # Format: "  Value Name    XX.XX%"
                lines.append(f"{stat.value} {stat.metric_value:.2f}%")
            
            lines.append("")  # Empty line between dimensions
        
        return "\n".join(lines).rstrip()
