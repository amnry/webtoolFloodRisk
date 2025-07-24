import re
from datetime import datetime, timedelta
import json

def parse_tide_data(station):
    """Parse tide data from NOAA text file for specified station"""
    tide_data = []
    
    # Map station names to file names
    station_files = {
        'portjefferson': 'HighTide/portJeff.txt',
        'miami': 'HighTide/miami.txt'
    }
    
    if station not in station_files:
        return []
    
    file_path = station_files[station]
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    
    # Determine units from header
    units = 'Metric'  # Default
    for line in lines:
        if 'Units:' in line:
            units = line.split('Units:')[1].strip()
            break
    
    # Skip header lines and find data section
    data_started = False
    for line in lines:
        line = line.strip()
        
        # Skip header lines
        if line.startswith('Date') or line.startswith('NOAA') or line.startswith('Disclaimer'):
            continue
            
        # Skip empty lines
        if not line:
            continue
            
        # Check if this is a data line (contains date and time)
        if re.match(r'\d{4}/\d{2}/\d{2}', line):
            data_started = True
            parts = line.split('\t')
            if len(parts) >= 4:
                date_str = parts[0].strip()
                day = parts[1].strip()
                time_str = parts[2].strip()
                pred_str = parts[3].strip()
                high_low = parts[4].strip() if len(parts) > 4 else 'H'
                
                try:
                    # Parse date and time
                    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                    time_obj = datetime.strptime(time_str, '%I:%M %p')
                    
                    # Combine date and time
                    full_datetime = datetime.combine(date_obj.date(), time_obj.time())
                    
                    # Convert prediction to float
                    prediction = float(pred_str)
                    
                    # Convert feet to meters if needed
                    if units == 'Feet':
                        prediction = prediction * 0.3048  # Convert feet to meters
                    
                    tide_data.append({
                        'datetime': full_datetime.isoformat(),
                        'date': date_str,
                        'time': time_str,
                        'day': day,
                        'prediction': prediction,
                        'type': high_low,  # H for high, L for low
                        'units': 'meters'  # Always convert to meters for consistency
                    })
                except ValueError as e:
                    print(f"Error parsing line: {line} - {e}")
                    continue
    
    return tide_data

def parse_port_jefferson_data():
    """Parse Port Jefferson tide data from the NOAA text file (legacy function)"""
    return parse_tide_data('portjefferson')

def get_tide_predictions_for_date(target_date_str, station='portjefferson'):
    """Get tide predictions for a specific date and station"""
    tide_data = parse_tide_data(station)
    
    # Convert target date string to datetime object
    try:
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    except ValueError:
        return []
    
    # Filter data for the target date
    daily_predictions = []
    for entry in tide_data:
        entry_date = datetime.fromisoformat(entry['datetime']).date()
        if entry_date == target_date:
            daily_predictions.append(entry)
    
    # Sort by time
    daily_predictions.sort(key=lambda x: x['time'])
    
    return daily_predictions

def generate_24_hour_tide_data(target_date_str, station='portjefferson'):
    """Generate 24-hour tide data with interpolated values for smooth charting"""
    daily_predictions = get_tide_predictions_for_date(target_date_str, station)
    
    if not daily_predictions:
        return None
    
    # Create 24-hour data points
    hours = []
    heights = []
    times = []
    
    # Get the target date
    target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    
    # Create 24-hour timeline
    for hour in range(24):
        current_time = datetime.combine(target_date, datetime.min.time().replace(hour=hour))
        hours.append(hour)
        times.append(current_time.strftime('%I:%M %p'))
        
        # Find the closest tide prediction for this hour
        closest_prediction = None
        min_time_diff = float('inf')
        
        for pred in daily_predictions:
            pred_time = datetime.strptime(pred['time'], '%I:%M %p').time()
            pred_datetime = datetime.combine(target_date, pred_time)
            
            time_diff = abs((current_time - pred_datetime).total_seconds() / 3600)
            
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_prediction = pred['prediction']
        
        # Use the closest prediction or interpolate
        if closest_prediction is not None:
            heights.append(closest_prediction)
        else:
            # Fallback to a base tide height
            heights.append(1.5)
    
    return {
        'hours': hours,
        'heights': heights,
        'times': times,
        'predictions': daily_predictions
    }

def get_tide_statistics(target_date_str, station='portjefferson'):
    """Get tide statistics for a specific date"""
    daily_predictions = get_tide_predictions_for_date(target_date_str, station)
    
    if not daily_predictions:
        return None
    
    # Separate high and low tides
    high_tides = [p for p in daily_predictions if p['type'] == 'H']
    low_tides = [p for p in daily_predictions if p['type'] == 'L']
    
    if not high_tides or not low_tides:
        return None
    
    # Find highest and lowest tides
    highest_tide = max(high_tides, key=lambda x: x['prediction'])
    lowest_tide = min(low_tides, key=lambda x: x['prediction'])
    
    # Calculate tidal range
    tidal_range = highest_tide['prediction'] - lowest_tide['prediction']
    
    return {
        'high_tide': {
            'time': highest_tide['time'],
            'height': highest_tide['prediction']
        },
        'low_tide': {
            'time': lowest_tide['time'],
            'height': lowest_tide['prediction']
        },
        'tidal_range': tidal_range,
        'all_highs': high_tides,
        'all_lows': low_tides
    }

def generate_date_range_tide_data(from_date_str, to_date_str, station='portjefferson'):
    """Generate tide data for a date range"""
    tide_data = parse_tide_data(station)
    
    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except ValueError:
        return None
    
    # Filter data for the date range
    range_predictions = []
    for entry in tide_data:
        entry_date = datetime.fromisoformat(entry['datetime']).date()
        if from_date <= entry_date <= to_date:
            range_predictions.append(entry)
    
    if not range_predictions:
        return None
    
    # Sort by datetime
    range_predictions.sort(key=lambda x: x['datetime'])
    
    # Extract data for charting
    dates = []
    heights = []
    times = []
    
    for pred in range_predictions:
        date_obj = datetime.fromisoformat(pred['datetime'])
        dates.append(date_obj.strftime('%m/%d'))
        times.append(pred['time'])
        heights.append(pred['prediction'])
    
    return {
        'dates': dates,
        'heights': heights,
        'times': times,
        'predictions': range_predictions
    }

def get_date_range_statistics(from_date_str, to_date_str, station='portjefferson'):
    """Get tide statistics for a date range"""
    daily_predictions = []
    tide_data = parse_tide_data(station)
    
    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
    except ValueError:
        return None
    
    # Filter data for the date range
    for entry in tide_data:
        entry_date = datetime.fromisoformat(entry['datetime']).date()
        if from_date <= entry_date <= to_date:
            daily_predictions.append(entry)
    
    if not daily_predictions:
        return None
    
    # Separate high and low tides
    high_tides = [p for p in daily_predictions if p['type'] == 'H']
    low_tides = [p for p in daily_predictions if p['type'] == 'L']
    
    if not high_tides or not low_tides:
        return None
    
    # Find highest and lowest tides in the range
    highest_tide = max(high_tides, key=lambda x: x['prediction'])
    lowest_tide = min(low_tides, key=lambda x: x['prediction'])
    
    # Calculate average tidal range
    avg_high = sum(p['prediction'] for p in high_tides) / len(high_tides)
    avg_low = sum(p['prediction'] for p in low_tides) / len(low_tides)
    avg_tidal_range = avg_high - avg_low
    
    return {
        'highest_tide': {
            'date': highest_tide['date'],
            'time': highest_tide['time'],
            'height': highest_tide['prediction']
        },
        'lowest_tide': {
            'date': lowest_tide['date'],
            'time': lowest_tide['time'],
            'height': lowest_tide['prediction']
        },
        'avg_tidal_range': avg_tidal_range,
        'total_highs': len(high_tides),
        'total_lows': len(low_tides),
        'date_range': f"{from_date_str} to {to_date_str}"
    }

if __name__ == "__main__":
    # Test the parser
    test_date = "2025-06-01"
    data = generate_24_hour_tide_data(test_date)
    stats = get_tide_statistics(test_date)
    
    print(f"Port Jefferson Tide Data for {test_date}:")
    print(f"24-hour data points: {len(data['heights']) if data else 0}")
    print(f"Statistics: {stats}") 