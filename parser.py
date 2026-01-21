import re
from datetime import datetime
from typing import Iterator, Optional, List

from models import LogEntry


class LogParser:
    """Parses Apache Combined Log Format into LogEntry objects."""
    
    # Apache Combined Log Format regex
    # Example: 83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /path HTTP/1.1" 200 3478 "referer" "user-agent"
    LOG_PATTERN = re.compile(
        r'^(?P<ip>[\d.]+)\s+'           # IP address
        r'(?P<identity>\S+)\s+'          # Identity (usually -)
        r'(?P<user>\S+)\s+'              # User (usually -)
        r'\[(?P<timestamp>[^\]]+)\]\s+'  # Timestamp
        r'"(?P<request>[^"]*)"\s+'       # Request
        r'(?P<status>\d+)\s+'            # Status code
        r'(?P<size>\d+|-)\s*'            # Response size
        r'(?:"(?P<referer>[^"]*)"\s*)?'  # Referer (optional)
        r'(?:"(?P<user_agent>[^"]*)")?'  # User-Agent (optional)
    )
    
    TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"
    
    def __init__(self, processing_mode: str = "streaming"):
        self._mode = processing_mode
    
    def parse(self, file_path: str) -> Iterator[LogEntry]:
        """Parse log file and return iterator of LogEntry objects."""
        if self._mode == "memory":
            return self._parse_memory(file_path)
        else:
            return self._parse_streaming(file_path)
    
    def _parse_memory(self, file_path: str) -> List[LogEntry]:
        """Load entire file into memory, then parse."""
        entries = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = self._parse_line(line)
                if entry:
                    entries.append(entry)
        return entries
    
    def _parse_streaming(self, file_path: str) -> Iterator[LogEntry]:
        """Parse file line by line using generator."""
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = self._parse_line(line)
                if entry:
                    yield entry
    
    def _parse_line(self, line: str) -> Optional[LogEntry]:
        """Parse a single log line into a LogEntry object."""
        line = line.strip()
        if not line:
            return None
        
        match = self.LOG_PATTERN.match(line)
        if not match:
            return None
        
        try:
            timestamp = datetime.strptime(
                match.group('timestamp'),
                self.TIMESTAMP_FORMAT
            )
        except ValueError:
            timestamp = datetime.now()
        
        size_str = match.group('size')
        size = int(size_str) if size_str != '-' else 0
        
        return LogEntry(
            ip_address=match.group('ip'),
            timestamp=timestamp,
            request=match.group('request') or '',
            status_code=int(match.group('status')),
            response_size=size,
            user_agent=match.group('user_agent') or ''
        )
