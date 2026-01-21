from user_agents import parse

from models import LogEntry
from extractors.base import DimensionExtractor
from extractors.registry import ExtractorRegistry


@ExtractorRegistry.register("os")
class OSExtractor(DimensionExtractor):
    """Extracts operating system from User-Agent string."""
    
    @property
    def name(self) -> str:
        return "OS"
    
    def extract(self, entry: LogEntry) -> str:
        if not entry.user_agent:
            return "Unknown"
        try:
            ua = parse(entry.user_agent)
            os_family = ua.os.family
            return os_family if os_family and os_family != "Other" else "Unknown"
        except Exception:
            return "Unknown"
