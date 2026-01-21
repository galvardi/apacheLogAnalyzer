from typing import Iterator, List, Dict, Optional

from models import LogEntry, DimensionStat
from parser import LogParser
from extractors.base import DimensionExtractor
from aggregator import StatisticsAggregator
from formatters.base import ReportFormatter


class LogAnalyzer:
    """Orchestrates log parsing, dimension extraction, and report generation."""
    
    def __init__(
        self,
        parser: LogParser,
        extractors: List[DimensionExtractor],
        aggregator: StatisticsAggregator,
        formatter: ReportFormatter,
        sort_by: str = "percentage",
        sort_order: str = "descending",
        cache_enabled: bool = True,
        cutoff_percentage: Optional[float] = None
    ):
        self._parser = parser
        self._extractors = extractors
        self._aggregator = aggregator
        self._formatter = formatter
        self._sort_by = sort_by
        self._sort_order = sort_order
        self._cache_enabled = cache_enabled
        self._cutoff_percentage = cutoff_percentage
        self._cache: Dict[tuple, Dict[str, str]] = {}
    
    def analyze(self, log_file_path: str) -> str:
        """Analyze log file and return formatted report."""
        entries = self._parser.parse(log_file_path)
        self._process_entries(entries)
        stats = self._generate_statistics()
        return self._formatter.format(stats)
    
    def _process_entries(self, entries: Iterator[LogEntry]) -> None:
        """Process all log entries through extractors."""
        for entry in entries:
            self._aggregator.increment_total()
            
            if self._cache_enabled:
                self._process_with_cache(entry)
            else:
                self._process_without_cache(entry)
    
    def _process_with_cache(self, entry: LogEntry) -> None:
        """Process entry with (IP + User-Agent) caching."""
        cache_key = (entry.ip_address, entry.user_agent)
        if cache_key in self._cache:
            for dimension, value in self._cache[cache_key].items():
                self._aggregator.add(dimension, value)
        else:
            cached_values = {}
            for extractor in self._extractors:
                value = extractor.extract(entry)
                cached_values[extractor.name] = value
                self._aggregator.add(extractor.name, value)
            self._cache[cache_key] = cached_values
    
    def _process_without_cache(self, entry: LogEntry) -> None:
        """Process entry without caching."""
        for extractor in self._extractors:
            value = extractor.extract(entry)
            self._aggregator.add(extractor.name, value)
    
    def _generate_statistics(self) -> Dict[str, List[DimensionStat]]:
        """Generate sorted statistics for all dimensions."""
        stats = {}
        for extractor in self._extractors:
            dimension = extractor.name
            stats[dimension] = self._aggregator.get_statistics(
                dimension,
                sort_by=self._sort_by,
                sort_order=self._sort_order,
                cutoff_percentage=self._cutoff_percentage
            )
        return stats
