import pandas as pd
from datetime import datetime, timedelta
import threading
from typing import Dict, List, Optional

class DataStorage:
    """
    Thread-safe in-memory storage for IoT sensor data.
    Provides methods for storing, retrieving, and managing sensor readings.
    """
    
    def __init__(self):
        self._data = pd.DataFrame()
        self._lock = threading.Lock()
        self._max_records = 10000  # Limit memory usage
        
        # Initialize empty DataFrame with correct columns
        self._initialize_dataframe()
    
    def _initialize_dataframe(self):
        """Initialize empty DataFrame with proper column structure."""
        columns = ['timestamp', 'temperature', 'weight', 'moisture', 'pressure', 'sensor_id']
        self._data = pd.DataFrame(columns=columns)
        
        # Set proper data types
        self._data['timestamp'] = pd.to_datetime(self._data['timestamp'])
        self._data['temperature'] = pd.to_numeric(self._data['temperature'])
        self._data['weight'] = pd.to_numeric(self._data['weight'])
        self._data['moisture'] = pd.to_numeric(self._data['moisture'])
        self._data['pressure'] = pd.to_numeric(self._data['pressure'])
    
    def add_reading(self, reading: Dict) -> bool:
        """
        Add a new sensor reading to storage.
        
        Args:
            reading (dict): Sensor reading data
        
        Returns:
            bool: True if successfully added, False otherwise
        """
        try:
            with self._lock:
                # Convert reading to DataFrame row
                new_row = pd.DataFrame([reading])
                
                # Ensure timestamp is datetime
                new_row['timestamp'] = pd.to_datetime(new_row['timestamp'])
                
                # Add to main dataframe
                self._data = pd.concat([self._data, new_row], ignore_index=True)
                
                # Sort by timestamp to maintain order
                self._data = self._data.sort_values('timestamp').reset_index(drop=True)
                
                # Limit memory usage by keeping only recent records
                if len(self._data) > self._max_records:
                    self._data = self._data.tail(self._max_records).reset_index(drop=True)
                
                return True
                
        except Exception as e:
            print(f"Error adding reading: {e}")
            return False
    
    def get_all_data(self) -> pd.DataFrame:
        """
        Get all stored sensor data.
        
        Returns:
            pd.DataFrame: All sensor readings
        """
        with self._lock:
            return self._data.copy()
    
    def get_recent_data(self, hours: int = 1) -> pd.DataFrame:
        """
        Get sensor data from the last N hours.
        
        Args:
            hours (int): Number of hours to look back
        
        Returns:
            pd.DataFrame: Recent sensor readings
        """
        with self._lock:
            if self._data.empty:
                return pd.DataFrame()
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_data = self._data[self._data['timestamp'] >= cutoff_time]
            return recent_data.copy()
    
    def get_data_by_sensor(self, sensor_id: str) -> pd.DataFrame:
        """
        Get data for a specific sensor.
        
        Args:
            sensor_id (str): Sensor identifier
        
        Returns:
            pd.DataFrame: Data for the specified sensor
        """
        with self._lock:
            if 'sensor_id' in self._data.columns:
                sensor_data = self._data[self._data['sensor_id'] == sensor_id]
                return sensor_data.copy()
            return pd.DataFrame()
    
    def get_data_by_timerange(self, start_time: datetime, end_time: datetime) -> pd.DataFrame:
        """
        Get data within a specific time range.
        
        Args:
            start_time (datetime): Start of time range
            end_time (datetime): End of time range
        
        Returns:
            pd.DataFrame: Data within the specified time range
        """
        with self._lock:
            if self._data.empty:
                return pd.DataFrame()
            
            time_filtered = self._data[
                (self._data['timestamp'] >= start_time) & 
                (self._data['timestamp'] <= end_time)
            ]
            return time_filtered.copy()
    
    def get_latest_reading(self) -> Optional[Dict]:
        """
        Get the most recent sensor reading.
        
        Returns:
            dict or None: Latest sensor reading
        """
        with self._lock:
            if self._data.empty:
                return None
            
            latest_row = self._data.iloc[-1]
            return latest_row.to_dict()
    
    def get_latest_timestamp(self) -> Optional[datetime]:
        """
        Get the timestamp of the most recent reading.
        
        Returns:
            datetime or None: Latest timestamp
        """
        with self._lock:
            if self._data.empty:
                return None
            
            return self._data['timestamp'].iloc[-1]
    
    def get_total_readings(self) -> int:
        """
        Get the total number of stored readings.
        
        Returns:
            int: Total number of readings
        """
        with self._lock:
            return len(self._data)
    
    def has_data(self) -> bool:
        """
        Check if any data is stored.
        
        Returns:
            bool: True if data exists, False otherwise
        """
        with self._lock:
            return not self._data.empty
    
    def clear_data(self) -> bool:
        """
        Clear all stored data.
        
        Returns:
            bool: True if successfully cleared
        """
        try:
            with self._lock:
                self._initialize_dataframe()
                return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
    
    def get_sensor_summary(self) -> Dict:
        """
        Get summary statistics for all sensors.
        
        Returns:
            dict: Summary statistics
        """
        with self._lock:
            if self._data.empty:
                return {}
            
            sensor_columns = ['temperature', 'weight', 'moisture', 'pressure']
            summary = {}
            
            for column in sensor_columns:
                if column in self._data.columns:
                    summary[column] = {
                        'count': len(self._data[column].dropna()),
                        'mean': self._data[column].mean(),
                        'min': self._data[column].min(),
                        'max': self._data[column].max(),
                        'std': self._data[column].std(),
                        'latest': self._data[column].iloc[-1] if not self._data.empty else None
                    }
            
            summary['metadata'] = {
                'total_records': len(self._data),
                'time_span': {
                    'start': self._data['timestamp'].min(),
                    'end': self._data['timestamp'].max()
                } if not self._data.empty else None,
                'sensors': self._data['sensor_id'].unique().tolist() if 'sensor_id' in self._data.columns else []
            }
            
            return summary
    
    def get_data_for_export(self, format_type: str = 'csv') -> str:
        """
        Get data formatted for export.
        
        Args:
            format_type (str): Export format ('csv' or 'json')
        
        Returns:
            str: Formatted data
        """
        with self._lock:
            if self._data.empty:
                return ""
            
            if format_type.lower() == 'csv':
                return self._data.to_csv(index=False)
            elif format_type.lower() == 'json':
                return self._data.to_json(orient='records', date_format='iso')
            else:
                raise ValueError(f"Unsupported format: {format_type}")
    
    def get_memory_usage(self) -> Dict:
        """
        Get memory usage information.
        
        Returns:
            dict: Memory usage statistics
        """
        with self._lock:
            memory_info = {
                'records_count': len(self._data),
                'max_records': self._max_records,
                'memory_usage_mb': self._data.memory_usage(deep=True).sum() / 1024 / 1024,
                'usage_percentage': (len(self._data) / self._max_records) * 100
            }
            
            return memory_info
