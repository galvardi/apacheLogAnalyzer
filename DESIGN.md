# Statistical Reporting Module - Design Document

## Overview

An extensible Apache log analyzer that produces statistical reports by Country, OS, and Browser.

## Architecture

```
┌─────────────┐     ┌───────────┐     ┌─────────────┐     ┌───────────┐
│  Log File   │────▶│ LogParser │────▶│  Analyzer   │────▶│ Formatter │────▶ Report
└─────────────┘     └───────────┘     │  (cached)   │     └───────────┘
                                      └──────┬──────┘
                                             │
                                      ┌──────▼──────┐
                                      │  Extractors │
                                      │ ┌─────────┐ │
                                      │ │ Country │ │
                                      │ │   OS    │ │
                                      │ │ Browser │ │
                                      │ └─────────┘ │
                                      └─────────────┘
```



### Component Breakdown

| Component | Responsibility |
|-----------|----------------|
| `LogParser` | Parses Apache log lines into `LogEntry` objects (streaming or memory mode) |
| `LogAnalyzer` | Orchestrates parsing, extraction, caching, and aggregation |
| `DimensionExtractor` | Extracts a specific dimension value from a log entry |
| `StatisticsAggregator` | Counts occurrences and calculates percentages |
| `MetricCalculator` | Defines how to calculate statistics (percentage, count, etc.) |
| `ReportFormatter` | Formats aggregated statistics for output |


### Efficenty Descisions
- choose to enable both in memory parsing for the the log file aswell as streaming for when log file has miliions of lines
- implemented a caching mechanism that can be switched on or off through the config that matches current needs of extractors since since if we see a request with the same ip and user agent there is no need to extract it again saving time (added execution time in config file)
- added new mode for geo2 database can be stored in memory or paginated by os (mmap) not currently needed since size is less than 10mb
-


### Extensibilty 

in this regard i have created a number of abstractions so that in the future when more dimmensions(HTTP Method), metrics(total count instead of percentages), and even a json formater instead of console output. these will just require the imlementation of the new class based off of the (base class) examples below

## Key Abstractions and Interfaces

```python
class DimensionExtractor(ABC):
    @property
    def name(self) -> str: ...
    def extract(self, entry: LogEntry) -> str: ...

class MetricCalculator(ABC):
    def calculate(self, count: int, total: int) -> float: ...

class ReportFormatter(ABC):
    def format(self, stats: Dict[str, List[DimensionStat]]) -> str: ...
```

| Abstraction | Purpose | Extensibility |
|-------------|---------|---------------|
| `DimensionExtractor` | Extract a value from log entry | Add new dimensions (HTTP Method, Status Code) |
| `MetricCalculator` | Calculate statistics | Add new metrics (absolute count, ratio) |
| `ReportFormatter` | Format output | Add new formats (JSON, CSV, HTML) |


### Adding a New Dimension (e.g., HTTP Method)

```python
@ExtractorRegistry.register("http_method")
class HTTPMethodExtractor(DimensionExtractor):
    @property
    def name(self) -> str:
        return "HTTP Method"
    
    def extract(self, entry: LogEntry) -> str:
        return entry.request.split()[0]  # GET, POST, etc.
```

Then enable in config:
```yaml
dimensions:
  - name: http_method
    enabled: true
```

### Adding a New Output Format (e.g., JSON)

```python
class JSONFormatter(ReportFormatter):
    def format(self, stats: Dict[str, List[DimensionStat]]) -> str:
        return json.dumps({
            dim: [{"value": s.value, "percentage": s.metric_value} for s in stat_list]
            for dim, stat_list in stats.items()
        }, indent=2)
```

### Adding a New Metric (e.g., Absolute Count)

```python
class AbsoluteCountMetric(MetricCalculator):
    def calculate(self, count: int, total: int) -> float:
        return count
```

## Technology Choices

| Component | Library | Rationale |
|-----------|---------|-----------|
| GeoIP Lookup | `geoip2` | Official MaxMind library, supports memory/mmap/disk modes |
| User-Agent Parsing | `user-agents` | Simple API, accurate browser/OS detection |
| Configuration | `pyyaml` | Human-readable, easy to edit |

## Configuration

```yaml
input:
  log_file: "./apache_log.txt"
  processing_mode: memory  # memory or streaming

cache:
  enabled: true  # cache by (IP + User-Agent)

geoip:
  database_path: "./GeoLite2-Country.mmdb"
  mode: memory  # memory, mmap, or disk

dimensions:
  - name: country
    enabled: true
  - name: os
    enabled: true
  - name: browser
    enabled: true

output:
  sort_by: percentage
  sort_order: descending
  cutoff_percentage: 0  # group values below this into "Other"
  show_execution_time: false
```

## Caching Strategy

Caching is handled centrally in `LogAnalyzer` by `(IP + User-Agent)` tuple:

```python
cache_key = (entry.ip_address, entry.user_agent)
if cache_key in self._cache:
    # Reuse cached extraction results
else:
    # Extract, cache, then aggregate
```

This ensures accuracy (different User-Agents from same IP are handled correctly) while still providing performance benefits for repeated identical requests.

## Trade-offs and Assumptions

| Decision | Trade-off |
|----------|-----------|
| **Streaming vs Memory** | Streaming uses constant memory for large files when files gets massive this allows for proper parsing; memory mode is faster for small files |
| **Cache by (IP + User-Agent)** | More accurate than IP-only caching, slightly larger cache size |
| **Unknown values** | Return "Unknown" rather than failing on unparseable data |

| **Cutoff percentage** | Reduces output clutter but loses granularity for rare values |
