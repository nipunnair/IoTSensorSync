import pandas as pd
import numpy as np
from scipy import stats
from scipy.signal import savgol_filter
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """
    Handles data cleaning, validation, and preprocessing for IoT sensor data.
    Provides outlier detection, missing value handling, and data smoothing.
    """
    
    def __init__(self):
        # Define sensor value ranges for validation
        self.sensor_ranges = {
            'temperature': (-50, 100),
            'weight': (0, 1000),
            'moisture': (0, 100),
            'pressure': (80000, 120000)
        }
        
        # Outlier detection parameters
        self.outlier_threshold = 3  # Z-score threshold
        self.iqr_multiplier = 1.5  # IQR multiplier for outlier detection
    
    def clean_data(self, data, remove_outliers=True, fill_missing=True, smooth_data=False):
        """
        Comprehensive data cleaning pipeline.
        
        Args:
            data (pd.DataFrame): Raw sensor data
            remove_outliers (bool): Whether to remove outliers
            fill_missing (bool): Whether to fill missing values
            smooth_data (bool): Whether to apply smoothing
        
        Returns:
            pd.DataFrame: Cleaned data
        """
        if data.empty:
            return data
        
        cleaned_data = data.copy()
        
        # Step 1: Handle missing values
        if fill_missing:
            cleaned_data = self._fill_missing_values(cleaned_data)
        
        # Step 2: Remove invalid values
        cleaned_data = self._remove_invalid_values(cleaned_data)
        
        # Step 3: Remove outliers
        if remove_outliers:
            cleaned_data = self._remove_outliers(cleaned_data)
        
        # Step 4: Apply smoothing
        if smooth_data and len(cleaned_data) > 5:
            cleaned_data = self._apply_smoothing(cleaned_data)
        
        # Step 5: Sort by timestamp
        cleaned_data = cleaned_data.sort_values('timestamp').reset_index(drop=True)
        
        return cleaned_data
    
    def detect_outliers(self, data):
        """
        Detect outliers in sensor data using multiple methods.
        
        Args:
            data (pd.DataFrame): Sensor data
        
        Returns:
            pd.DataFrame: Rows containing outliers
        """
        if data.empty:
            return pd.DataFrame()
        
        outlier_indices = set()
        sensor_columns = ['temperature', 'weight', 'moisture', 'pressure']
        
        for column in sensor_columns:
            if column in data.columns:
                # Z-score method
                z_scores = np.abs(stats.zscore(data[column].dropna()))
                z_outliers = data.index[z_scores > self.outlier_threshold]
                outlier_indices.update(z_outliers)
                
                # IQR method
                Q1 = data[column].quantile(0.25)
                Q3 = data[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - self.iqr_multiplier * IQR
                upper_bound = Q3 + self.iqr_multiplier * IQR
                
                iqr_outliers = data.index[
                    (data[column] < lower_bound) | (data[column] > upper_bound)
                ]
                outlier_indices.update(iqr_outliers)
        
        return data.loc[list(outlier_indices)]
    
    def analyze_data_quality(self, data):
        """
        Analyze the quality of sensor data.
        
        Args:
            data (pd.DataFrame): Sensor data
        
        Returns:
            dict: Data quality metrics
        """
        if data.empty:
            return {}
        
        sensor_columns = ['temperature', 'weight', 'moisture', 'pressure']
        
        quality_metrics = {
            'total_records': len(data),
            'missing_values': data.isnull().sum().sum(),
            'missing_percentage': (data.isnull().sum().sum() / (len(data) * len(sensor_columns))) * 100,
            'duplicate_records': data.duplicated().sum(),
            'invalid_values': 0,
            'outliers_detected': len(self.detect_outliers(data)),
            'data_completeness': 0,
            'temporal_consistency': self._check_temporal_consistency(data)
        }
        
        # Count invalid values
        for column in sensor_columns:
            if column in data.columns:
                min_val, max_val = self.sensor_ranges[column]
                invalid_count = len(data[
                    (data[column] < min_val) | (data[column] > max_val)
                ])
                quality_metrics['invalid_values'] += invalid_count
        
        # Calculate data completeness
        total_possible_values = len(data) * len(sensor_columns)
        valid_values = total_possible_values - quality_metrics['missing_values']
        quality_metrics['data_completeness'] = (valid_values / total_possible_values) * 100
        
        return quality_metrics
    
    def get_cleaned_data(self, data):
        """
        Get cleaned version of the data with default settings.
        
        Args:
            data (pd.DataFrame): Raw sensor data
        
        Returns:
            pd.DataFrame: Cleaned data
        """
        return self.clean_data(data, remove_outliers=True, fill_missing=True, smooth_data=False)
    
    def _fill_missing_values(self, data):
        """Fill missing values using forward fill and interpolation."""
        sensor_columns = ['temperature', 'weight', 'moisture', 'pressure']
        
        for column in sensor_columns:
            if column in data.columns:
                # Forward fill first
                data[column] = data[column].fillna(method='ffill')
                
                # Then backward fill for remaining NaN values
                data[column] = data[column].fillna(method='bfill')
                
                # Linear interpolation for any remaining gaps
                data[column] = data[column].interpolate(method='linear')
                
                # If still NaN (e.g., all values were NaN), fill with sensor range midpoint
                if data[column].isnull().any():
                    min_val, max_val = self.sensor_ranges[column]
                    midpoint = (min_val + max_val) / 2
                    data[column] = data[column].fillna(midpoint)
        
        return data
    
    def _remove_invalid_values(self, data):
        """Remove values outside valid sensor ranges."""
        sensor_columns = ['temperature', 'weight', 'moisture', 'pressure']
        
        for column in sensor_columns:
            if column in data.columns:
                min_val, max_val = self.sensor_ranges[column]
                # Replace invalid values with NaN
                data.loc[
                    (data[column] < min_val) | (data[column] > max_val), 
                    column
                ] = np.nan
        
        # Fill the NaN values created
        data = self._fill_missing_values(data)
        
        return data
    
    def _remove_outliers(self, data):
        """Remove outliers using IQR method."""
        sensor_columns = ['temperature', 'weight', 'moisture', 'pressure']
        
        for column in sensor_columns:
            if column in data.columns and len(data[column].dropna()) > 4:
                Q1 = data[column].quantile(0.25)
                Q3 = data[column].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - self.iqr_multiplier * IQR
                upper_bound = Q3 + self.iqr_multiplier * IQR
                
                # Replace outliers with NaN
                data.loc[
                    (data[column] < lower_bound) | (data[column] > upper_bound),
                    column
                ] = np.nan
        
        # Fill the NaN values created
        data = self._fill_missing_values(data)
        
        return data
    
    def _apply_smoothing(self, data):
        """Apply Savitzky-Golay smoothing filter."""
        sensor_columns = ['temperature', 'weight', 'moisture', 'pressure']
        
        # Need at least 5 points for smoothing
        if len(data) < 5:
            return data
        
        window_length = min(5, len(data))
        if window_length % 2 == 0:
            window_length -= 1  # Must be odd
        
        for column in sensor_columns:
            if column in data.columns:
                try:
                    data[column] = savgol_filter(
                        data[column], 
                        window_length=window_length, 
                        polyorder=2
                    )
                except:
                    # If smoothing fails, keep original data
                    pass
        
        return data
    
    def _check_temporal_consistency(self, data):
        """Check if timestamps are properly ordered and consistent."""
        if len(data) < 2:
            return True
        
        # Check if timestamps are monotonically increasing
        timestamps_sorted = data['timestamp'].is_monotonic_increasing
        
        # Check for reasonable time intervals (not too frequent or too sparse)
        time_diffs = data['timestamp'].diff().dt.total_seconds().dropna()
        reasonable_intervals = (time_diffs >= 0.5) & (time_diffs <= 3600)  # 0.5s to 1 hour
        
        return timestamps_sorted and reasonable_intervals.all()
