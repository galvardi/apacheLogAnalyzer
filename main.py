#!/usr/bin/env python3
"""
Statistical Reporting Module - Apache Log Analyzer
"""

import time
from pathlib import Path

import yaml

from parser import LogParser
from extractors import CountryExtractor, OSExtractor, BrowserExtractor
from metrics import PercentageMetric
from aggregator import StatisticsAggregator
from formatters import ConsoleFormatter
from analyzer import LogAnalyzer


def main():
    start_time = time.perf_counter()
    
    # Load configuration
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Resolve paths relative to config location
    base_path = config_path.parent
    log_path = base_path / config['input']['log_file']
    geoip_path = base_path / config['geoip']['database_path']
    
    # Create components
    parser = LogParser(config['input'].get('processing_mode', 'streaming'))
    
    # Build extractors based on enabled dimensions
    extractor_map = {
        'country': lambda: CountryExtractor(str(geoip_path), config['geoip'].get('mode', 'memory')),
        'os': lambda: OSExtractor(),
        'browser': lambda: BrowserExtractor(),
    }
    
    extractors = [
        extractor_map[dim['name']]()
        for dim in config.get('dimensions', [])
        if dim.get('enabled')
    ]
    
    aggregator = StatisticsAggregator(metric=PercentageMetric())
    formatter = ConsoleFormatter()
    
    output = config.get('output', {})
    cache_enabled = config.get('cache', {}).get('enabled', True)
    cutoff_percentage = output.get('cutoff_percentage')
    
    analyzer = LogAnalyzer(
        parser=parser,
        extractors=extractors,
        aggregator=aggregator,
        formatter=formatter,
        sort_by=output.get('sort_by', 'percentage'),
        sort_order=output.get('sort_order', 'descending'),
        cache_enabled=cache_enabled,
        cutoff_percentage=cutoff_percentage
    )
    
    print(analyzer.analyze(str(log_path)))
    
    if output.get('show_execution_time'):
        elapsed_time = time.perf_counter() - start_time
        print(f"\nExecution time: {elapsed_time:.3f} seconds")


if __name__ == '__main__':
    main()
