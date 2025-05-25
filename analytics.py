import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

class Analytics:
    """
    Advanced analytics and statistical analysis for IoT sensor data.
    Provides trend analysis, correlation analysis, and statistical summaries.
    """
    
    def __init__(self):
        self.sensor_columns = ['temperature', 'weight', 'moisture', 'pressure']
    
    def calculate_statistics(self, data: pd.DataFrame) -> dict:
        """
        Calculate comprehensive statistics for sensor data.
        
        Args:
            data (pd.DataFrame): Sensor data
        
        Returns:
            dict: Statistical analysis results
        """
        if data.empty:
            return {}
        
        results = {}
        
        # Descriptive statistics
        numeric_columns = [col for col in self.sensor_columns if col in data.columns]
        if numeric_columns:
            results['descriptive'] = data[numeric_columns].describe()
            
            # Additional statistics
            results['skewness'] = data[numeric_columns].skew()
            results['kurtosis'] = data[numeric_columns].kurtosis()
            
            # Correlation matrix
            results['correlation'] = data[numeric_columns].corr()
            
            # Variance analysis
            results['variance'] = data[numeric_columns].var()
            results['coefficient_of_variation'] = (data[numeric_columns].std() / data[numeric_columns].mean()) * 100
        
        return results
    
    def analyze_trends(self, data: pd.DataFrame) -> dict:
        """
        Analyze trends in sensor data over time.
        
        Args:
            data (pd.DataFrame): Sensor data with timestamps
        
        Returns:
            dict: Trend analysis results for each sensor
        """
        if data.empty or len(data) < 3:
            return {}
        
        trends = {}
        
        # Convert timestamps to numeric for regression
        data_sorted = data.sort_values('timestamp')
        time_numeric = pd.to_numeric(data_sorted['timestamp']) / 10**9  # Convert to seconds
        
        for column in self.sensor_columns:
            if column in data.columns:
                values = data_sorted[column].dropna()
                time_vals = time_numeric[values.index]
                
                if len(values) < 3:
                    continue
                
                # Linear regression for trend
                slope, intercept, r_value, p_value, std_err = stats.linregress(time_vals, values)
                
                # Determine trend direction
                if abs(slope) < std_err:
                    direction = "Stable"
                elif slope > 0:
                    direction = "Increasing"
                else:
                    direction = "Decreasing"
                
                trends[column] = {
                    'slope': slope,
                    'intercept': intercept,
                    'r_squared': r_value**2,
                    'p_value': p_value,
                    'std_error': std_err,
                    'direction': direction,
                    'confidence': 'High' if r_value**2 > 0.7 else 'Medium' if r_value**2 > 0.3 else 'Low'
                }
        
        return trends
    
    def detect_anomalies(self, data: pd.DataFrame, method: str = 'zscore') -> dict:
        """
        Detect anomalies in sensor data using various methods.
        
        Args:
            data (pd.DataFrame): Sensor data
            method (str): Anomaly detection method ('zscore', 'iqr', 'isolation')
        
        Returns:
            dict: Anomaly detection results
        """
        if data.empty:
            return {}
        
        anomalies = {}
        
        for column in self.sensor_columns:
            if column in data.columns:
                values = data[column].dropna()
                
                if len(values) < 3:
                    continue
                
                if method == 'zscore':
                    z_scores = np.abs(stats.zscore(values))
                    anomaly_indices = values.index[z_scores > 3]
                    
                elif method == 'iqr':
                    Q1 = values.quantile(0.25)
                    Q3 = values.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    anomaly_indices = values.index[(values < lower_bound) | (values > upper_bound)]
                
                else:
                    anomaly_indices = []
                
                anomalies[column] = {
                    'count': len(anomaly_indices),
                    'percentage': (len(anomaly_indices) / len(values)) * 100,
                    'indices': anomaly_indices.tolist(),
                    'values': values.loc[anomaly_indices].tolist() if len(anomaly_indices) > 0 else []
                }
        
        return anomalies
    
    def calculate_sensor_health(self, data: pd.DataFrame) -> dict:
        """
        Calculate health metrics for each sensor.
        
        Args:
            data (pd.DataFrame): Sensor data
        
        Returns:
            dict: Sensor health metrics
        """
        if data.empty:
            return {}
        
        health_metrics = {}
        
        for column in self.sensor_columns:
            if column in data.columns:
                values = data[column]
                
                # Data availability
                availability = (values.notna().sum() / len(values)) * 100
                
                # Data stability (coefficient of variation)
                cv = (values.std() / values.mean()) * 100 if values.mean() != 0 else 100
                
                # Recent data quality (last 10% of readings)
                recent_count = max(1, int(len(values) * 0.1))
                recent_values = values.tail(recent_count)
                recent_stability = (recent_values.std() / recent_values.mean()) * 100 if recent_values.mean() != 0 else 100
                
                # Overall health score
                health_score = min(100, (availability * 0.4) + ((100 - min(cv, 100)) * 0.3) + ((100 - min(recent_stability, 100)) * 0.3))
                
                # Health status
                if health_score >= 90:
                    status = "Excellent"
                elif health_score >= 70:
                    status = "Good"
                elif health_score >= 50:
                    status = "Fair"
                else:
                    status = "Poor"
                
                health_metrics[column] = {
                    'availability_percent': round(availability, 2),
                    'stability_cv': round(cv, 2),
                    'recent_stability_cv': round(recent_stability, 2),
                    'health_score': round(health_score, 2),
                    'status': status
                }
        
        return health_metrics
    
    def analyze_correlations(self, data: pd.DataFrame) -> dict:
        """
        Analyze correlations between different sensors.
        
        Args:
            data (pd.DataFrame): Sensor data
        
        Returns:
            dict: Correlation analysis results
        """
        if data.empty:
            return {}
        
        numeric_columns = [col for col in self.sensor_columns if col in data.columns]
        
        if len(numeric_columns) < 2:
            return {}
        
        correlations = {}
        correlation_matrix = data[numeric_columns].corr()
        
        # Extract significant correlations
        for i, col1 in enumerate(numeric_columns):
            for j, col2 in enumerate(numeric_columns):
                if i < j:  # Avoid duplicates and self-correlation
                    corr_value = correlation_matrix.loc[col1, col2]
                    
                    # Determine correlation strength
                    abs_corr = abs(corr_value)
                    if abs_corr >= 0.7:
                        strength = "Strong"
                    elif abs_corr >= 0.4:
                        strength = "Moderate"
                    elif abs_corr >= 0.2:
                        strength = "Weak"
                    else:
                        strength = "Very Weak"
                    
                    # Determine direction
                    direction = "Positive" if corr_value > 0 else "Negative"
                    
                    correlations[f"{col1}_vs_{col2}"] = {
                        'coefficient': round(corr_value, 3),
                        'strength': strength,
                        'direction': direction,
                        'significant': abs_corr >= 0.2
                    }
        
        return {
            'pairwise_correlations': correlations,
            'correlation_matrix': correlation_matrix.round(3)
        }
    
    def generate_insights(self, data: pd.DataFrame) -> list:
        """
        Generate actionable insights from sensor data analysis.
        
        Args:
            data (pd.DataFrame): Sensor data
        
        Returns:
            list: List of insights and recommendations
        """
        if data.empty:
            return ["No data available for analysis"]
        
        insights = []
        
        # Analyze trends
        trends = self.analyze_trends(data)
        for sensor, trend_data in trends.items():
            if trend_data['confidence'] == 'High':
                insights.append(
                    f"📈 {sensor.title()} shows a {trend_data['direction'].lower()} trend with high confidence (R² = {trend_data['r_squared']:.3f})"
                )
        
        # Analyze correlations
        correlations = self.analyze_correlations(data)
        if 'pairwise_correlations' in correlations:
            for pair, corr_data in correlations['pairwise_correlations'].items():
                if corr_data['significant'] and corr_data['strength'] in ['Strong', 'Moderate']:
                    sensors = pair.replace('_vs_', ' and ')
                    insights.append(
                        f"🔗 {corr_data['strength']} {corr_data['direction'].lower()} correlation detected between {sensors} (r = {corr_data['coefficient']})"
                    )
        
        # Analyze sensor health
        health = self.calculate_sensor_health(data)
        for sensor, health_data in health.items():
            if health_data['status'] in ['Poor', 'Fair']:
                insights.append(
                    f"⚠️ {sensor.title()} sensor health is {health_data['status'].lower()} (score: {health_data['health_score']}/100)"
                )
            elif health_data['status'] == 'Excellent':
                insights.append(
                    f"✅ {sensor.title()} sensor is performing excellently (score: {health_data['health_score']}/100)"
                )
        
        # Analyze data quality
        stats_info = self.calculate_statistics(data)
        if 'coefficient_of_variation' in stats_info:
            for sensor, cv in stats_info['coefficient_of_variation'].items():
                if cv > 50:  # High variability
                    insights.append(
                        f"📊 {sensor.title()} shows high variability (CV = {cv:.1f}%) - consider checking sensor calibration"
                    )
        
        # Add general recommendations
        if len(data) > 100:
            insights.append("📈 Sufficient data collected for reliable trend analysis and model building")
        else:
            insights.append("⏱️ More data collection recommended for robust statistical analysis")
        
        return insights if insights else ["📋 Data analysis completed - no significant patterns detected yet"]
    
    def get_performance_metrics(self, data: pd.DataFrame) -> dict:
        """
        Calculate performance metrics for the entire sensor system.
        
        Args:
            data (pd.DataFrame): Sensor data
        
        Returns:
            dict: System performance metrics
        """
        if data.empty:
            return {}
        
        metrics = {}
        
        # Data collection metrics
        if 'timestamp' in data.columns:
            time_span = data['timestamp'].max() - data['timestamp'].min()
            metrics['data_collection_period'] = str(time_span)
            metrics['average_collection_rate'] = f"{len(data) / max(1, time_span.total_seconds() / 3600):.2f} readings/hour"
        
        # Data quality metrics
        numeric_columns = [col for col in self.sensor_columns if col in data.columns]
        if numeric_columns:
            total_possible_readings = len(data) * len(numeric_columns)
            actual_readings = data[numeric_columns].notna().sum().sum()
            metrics['data_completeness'] = f"{(actual_readings / total_possible_readings) * 100:.2f}%"
            
            # System reliability
            anomalies = self.detect_anomalies(data)
            total_anomalies = sum([anomaly['count'] for anomaly in anomalies.values()])
            metrics['anomaly_rate'] = f"{(total_anomalies / actual_readings) * 100:.2f}%"
            
            # Overall system health
            health_scores = [self.calculate_sensor_health(data)[sensor]['health_score'] for sensor in numeric_columns]
            metrics['overall_system_health'] = f"{np.mean(health_scores):.2f}/100"
        
        return metrics
