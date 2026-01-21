from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    """Represents a parsed Apache log entry."""
    ip_address: str
    timestamp: datetime
    request: str
    status_code: int
    response_size: int
    user_agent: str


@dataclass
class DimensionStat:
    """Represents a statistical result for a dimension value."""
    value: str
    count: int
    metric_value: float
