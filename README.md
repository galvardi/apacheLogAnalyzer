# Apache Log Analyzer

A statistical reporting module that analyzes Apache web server logs and produces percentage breakdowns by Country, OS, and Browser.

you can find the desgin doc for this project in the DESIGN,md file


## Requirements

- Python 3.9+
- MaxMind GeoLite2 Country database (.mmdb file)

# Getting started:

## Installation

```bash
pip install -r requirements.txt
```

i have created a configuration file to run the program with different states and extendabilty
## Configuration

Edit `config.yaml` to customize:

```yaml
input:
  log_file: "../apache_log.txt"    # path to log file
  processing_mode: streaming        # memory or streaming

cache:
  enabled: true                     # cache by (IP + User-Agent)

geoip:
  database_path: "./GeoLite2-Country.mmdb"
  mode: memory                      # memory, mmap, or disk

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
  cutoff_percentage: 0.5            # group values below this into "Other"
```

## Usage

```bash
python main.py
```

## Sample Output

```
Country:
  United States 39.38%
  France 8.65%
  Germany 5.72%
  Other 2.30%

OS:
  Windows 33.15%
  Mac OS X 14.44%
  Linux 14.57%
  Other 1.11%

Browser:
  Chrome 28.92%
  Firefox 26.07%
  Safari 2.62%
  Other 4.88%
```
