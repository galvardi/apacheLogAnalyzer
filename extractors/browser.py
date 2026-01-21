from user_agents import parse

from models import LogEntry
from extractors.base import DimensionExtractor
from extractors.registry import ExtractorRegistry


@ExtractorRegistry.register("browser")
class BrowserExtractor(DimensionExtractor):
    """Extracts browser from User-Agent string."""
    
    @property
    def name(self) -> str:
        return "Browser"
    
    def extract(self, entry: LogEntry) -> str:
        if not entry.user_agent:
            return "Unknown"
        try:
            ua = parse(entry.user_agent)
            browser_family = ua.browser.family
            return browser_family if browser_family and browser_family != "Other" else "Unknown"
        except Exception:
            return "Unknown"
