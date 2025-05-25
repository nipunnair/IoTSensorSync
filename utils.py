from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Union

def format_timestamp(timestamp: Union[datetime, pd.Timestamp, str]) -> str:
    """
    Format timestamp for display.
    
    Args:
        timestamp: Timestamp to format
    
    Returns:
        str: Formatted timestamp string
    """
    if timestamp is None:
        return "N/A"
    
    if isinstance(timestamp, str):
        timestamp = pd.to_datetime(timestamp)
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def validate_sensor_data(data: Dict) -> Dict[str, Any]:
    """
    Validate sensor reading data.
    
    Args:
        data (dict): Sensor reading data
    
    Returns:
        dict: Validation result with 'valid' flag and 'errors' list
    """
    errors = []
    
    # Required fields
    required_fields = ['timestamp', 'temperature', 'weight', 'moisture', 'pressure']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate sensor ranges
    sensor_ranges = {
        'temperature': (-50, 100),
        'weight': (0, 1000),
        'moisture': (0, 100),
        'pressure': (80000, 120000)
    }
    
    for sensor, (min_val, max_val) in sensor_ranges.items():
        if sensor in data:
            value = data[sensor]
            if value is None:
                errors.append(f"{sensor} value is None")
            elif not isinstance(value, (int, float)):
                errors.append(f"{sensor} value must be numeric")
            elif not (min_val <= value <= max_val):
                errors.append(f"{sensor} value {value} is outside valid range [{min_val}, {max_val}]")
    
    # Validate timestamp
    if 'timestamp' in data:
        try:
            if isinstance(data['timestamp'], str):
                pd.to_datetime(data['timestamp'])
            elif not isinstance(data['timestamp'], (datetime, pd.Timestamp)):
                errors.append("timestamp must be a valid datetime")
        except:
            errors.append("Invalid timestamp format")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def calculate_statistics_summary(values: List[float]) -> Dict[str, float]:
    """
    Calculate summary statistics for a list of values.
    
    Args:
        values (list): List of numeric values
    
    Returns:
        dict: Summary statistics
    """
    if not values:
        return {}
    
    values_array = np.array(values)
    
    return {
        'count': len(values),
        'mean': np.mean(values_array),
        'median': np.median(values_array),
        'std': np.std(values_array),
        'min': np.min(values_array),
        'max': np.max(values_array),
        'q25': np.percentile(values_array, 25),
        'q75': np.percentile(values_array, 75)
    }

def detect_data_gaps(timestamps: List[datetime], expected_interval_seconds: int = 60) -> List[Dict]:
    """
    Detect gaps in data collection timestamps.
    
    Args:
        timestamps (list): List of timestamps
        expected_interval_seconds (int): Expected interval between readings
    
    Returns:
        list: List of detected gaps
    """
    if len(timestamps) < 2:
        return []
    
    gaps = []
    sorted_timestamps = sorted(timestamps)
    
    for i in range(1, len(sorted_timestamps)):
        time_diff = (sorted_timestamps[i] - sorted_timestamps[i-1]).total_seconds()
        
        if time_diff > expected_interval_seconds * 2:  # Gap is more than 2x expected interval
            gaps.append({
                'start_time': sorted_timestamps[i-1],
                'end_time': sorted_timestamps[i],
                'duration_seconds': time_diff,
                'duration_formatted': format_duration(time_diff)
            })
    
    return gaps

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds (float): Duration in seconds
    
    Returns:
        str: Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} hours"
    else:
        days = seconds / 86400
        return f"{days:.1f} days"

def export_data_to_csv(data: pd.DataFrame, filename: str = None) -> str:
    """
    Export DataFrame to CSV format.
    
    Args:
        data (pd.DataFrame): Data to export
        filename (str): Optional filename
    
    Returns:
        str: CSV formatted string
    """
    if filename:
        data.to_csv(filename, index=False)
        return f"Data exported to {filename}"
    else:
        return data.to_csv(index=False)

def export_data_to_json(data: pd.DataFrame, filename: str = None) -> str:
    """
    Export DataFrame to JSON format.
    
    Args:
        data (pd.DataFrame): Data to export
        filename (str): Optional filename
    
    Returns:
        str: JSON formatted string
    """
    json_str = data.to_json(orient='records', date_format='iso', indent=2)
    
    if filename:
        with open(filename, 'w') as f:
            f.write(json_str)
        return f"Data exported to {filename}"
    else:
        return json_str

def calculate_data_quality_score(data: pd.DataFrame) -> float:
    """
    Calculate overall data quality score.
    
    Args:
        data (pd.DataFrame): Sensor data
    
    Returns:
        float: Quality score between 0 and 100
    """
    if data.empty:
        return 0.0
    
    scores = []
    
    # Completeness score
    total_cells = data.size
    non_null_cells = data.notna().sum().sum()
    completeness_score = (non_null_cells / total_cells) * 100
    scores.append(completeness_score)
    
    # Consistency score (based on value ranges)
    sensor_ranges = {
        'temperature': (-50, 100),
        'weight': (0, 1000),
        'moisture': (0, 100),
        'pressure': (80000, 120000)
    }
    
    consistency_scores = []
    for column, (min_val, max_val) in sensor_ranges.items():
        if column in data.columns:
            valid_values = data[column].between(min_val, max_val).sum()
            total_values = data[column].notna().sum()
            if total_values > 0:
                consistency_scores.append((valid_values / total_values) * 100)
    
    if consistency_scores:
        scores.append(np.mean(consistency_scores))
    
    # Temporal consistency score
    if 'timestamp' in data.columns and len(data) > 1:
        is_sorted = data['timestamp'].is_monotonic_increasing
        scores.append(100.0 if is_sorted else 50.0)
    
    return np.mean(scores) if scores else 0.0

def generate_sample_config() -> Dict:
    """
    Generate sample configuration for the IoT system.
    
    Returns:
        dict: Sample configuration
    """
    return {
        'sensors': {
            'temperature': {
                'enabled': True,
                'min_value': -50,
                'max_value': 100,
                'unit': '°C',
                'precision': 2
            },
            'weight': {
                'enabled': True,
                'min_value': 0,
                'max_value': 1000,
                'unit': 'kg',
                'precision': 2
            },
            'moisture': {
                'enabled': True,
                'min_value': 0,
                'max_value': 100,
                'unit': '%',
                'precision': 1
            },
            'pressure': {
                'enabled': True,
                'min_value': 80000,
                'max_value': 120000,
                'unit': 'Pa',
                'precision': 0
            }
        },
        'data_collection': {
            'interval_seconds': 2,
            'max_records': 10000,
            'auto_cleanup': True
        },
        'data_processing': {
            'outlier_detection': True,
            'missing_value_handling': True,
            'smoothing': False,
            'anomaly_threshold': 3.0
        },
        'alerts': {
            'enabled': True,
            'sensor_failure_threshold': 30,  # seconds
            'anomaly_alert': True,
            'data_quality_threshold': 80  # percentage
        }
    }

def format_sensor_value(value: float, sensor_type: str) -> str:
    """
    Format sensor value with appropriate unit and precision.
    
    Args:
        value (float): Sensor value
        sensor_type (str): Type of sensor
    
    Returns:
        str: Formatted value with unit
    """
    if value is None:
        return "N/A"
    
    format_config = {
        'temperature': {'precision': 1, 'unit': '°C'},
        'weight': {'precision': 2, 'unit': 'kg'},
        'moisture': {'precision': 1, 'unit': '%'},
        'pressure': {'precision': 0, 'unit': 'Pa'}
    }
    
    config = format_config.get(sensor_type, {'precision': 2, 'unit': ''})
    
    return f"{value:.{config['precision']}f}{config['unit']}"

def create_alert_message(alert_type: str, sensor: str, value: float, threshold: float) -> str:
    """
    Create formatted alert message.
    
    Args:
        alert_type (str): Type of alert
        sensor (str): Sensor name
        value (float): Current value
        threshold (float): Threshold value
    
    Returns:
        str: Formatted alert message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    alert_messages = {
        'high_value': f"🔴 HIGH VALUE ALERT [{timestamp}]: {sensor.title()} reading {value:.2f} exceeds threshold {threshold:.2f}",
        'low_value': f"🔵 LOW VALUE ALERT [{timestamp}]: {sensor.title()} reading {value:.2f} below threshold {threshold:.2f}",
        'sensor_failure': f"❌ SENSOR FAILURE [{timestamp}]: {sensor.title()} sensor not responding",
        'data_quality': f"⚠️ DATA QUALITY ALERT [{timestamp}]: {sensor.title()} data quality below threshold",
        'anomaly': f"🟡 ANOMALY DETECTED [{timestamp}]: Unusual {sensor.title()} reading {value:.2f}"
    }
    
    return alert_messages.get(alert_type, f"ALERT [{timestamp}]: {sensor.title()} - {alert_type}")
