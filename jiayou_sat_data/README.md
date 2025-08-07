# Satellite Data Processing

This directory contains satellite altimetry data processing scripts and data files.

## Files

- `sa_data.py` - Main script for processing satellite sea level anomaly (SLA) data
- `monthly_raw/` - Directory containing satellite data files (excluded from git due to size)

## Large Data Files

The `monthly_raw/` directory contains 365+ NetCDF (.nc) files of satellite sea level data from 2010-2023. These files are **too large for GitHub** (total size > 10GB).

### Data Details
- **Source**: Satellite altimetry missions (Jason-1, Jason-2, Jason-3)
- **Format**: NetCDF (.nc) files
- **Coverage**: Global monthly sea level anomaly data
- **Time Period**: 2010-2023
- **File Size**: ~2.7-2.9MB per file

### Accessing the Data
If you need access to the satellite data files, please contact the project maintainer for details on how to obtain them.

## Usage

The `sa_data.py` script can process satellite data for specific locations:

```bash
# Process data for a specific station
python sa_data.py station_id

# Process multiple stations
python sa_data.py station_id1 station_id2

# Force update (reprocess existing data)
python sa_data.py station_id -u
```

## Dependencies

- xarray
- pandas
- numpy
- tqdm
- ar6 (custom module for station data)
