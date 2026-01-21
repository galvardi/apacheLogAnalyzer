import geoip2.database

from models import LogEntry
from extractors.base import DimensionExtractor
from extractors.registry import ExtractorRegistry


@ExtractorRegistry.register("country")
class CountryExtractor(DimensionExtractor):
    """Extracts country from IP address using GeoIP database."""
    
    def __init__(self, db_path: str, db_mode: str = "memory"):
        mode_map = {
            "memory": geoip2.database.MODE_MEMORY,
            "mmap": geoip2.database.MODE_MMAP,
            "disk": geoip2.database.MODE_FILE,
        }
        mode = mode_map.get(db_mode, geoip2.database.MODE_MEMORY)
        self._reader = geoip2.database.Reader(db_path, mode=mode)
    
    @property
    def name(self) -> str:
        return "Country"
    
    def extract(self, entry: LogEntry) -> str:
        try:
            response = self._reader.country(entry.ip_address)
            return response.country.name or "Unknown"
        except Exception:
            return "Unknown"
    
    def close(self):
        self._reader.close()
