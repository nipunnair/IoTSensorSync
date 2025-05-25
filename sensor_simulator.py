import random
import numpy as np
from datetime import datetime
import math

class SensorSimulator:
    """
    Simulates IoT sensor readings for temperature, weight, moisture, and pressure.
    Generates realistic sensor data with natural variations and occasional anomalies.
    """
    
    def __init__(self):
        # Base values for sensors
        self.base_temperature = 22.0  # Celsius
        self.base_weight = 50.0  # kg
        self.base_moisture = 45.0  # percentage
        self.base_pressure = 101325.0  # Pascal
        
        # Variation parameters
        self.temperature_range = 5.0
        self.weight_range = 10.0
        self.moisture_range = 15.0
        self.pressure_range = 1000.0
        
        # Noise parameters
        self.noise_level = 0.1
        
        # Anomaly simulation
        self.anomaly_probability = 0.05  # 5% chance of anomaly
        
        # Seasonal trends (simulate daily temperature cycles)
        self.time_offset = 0
        
    def generate_reading(self):
        """
        Generate a single sensor reading with realistic variations.
        
        Returns:
            dict: Sensor reading with timestamp and sensor values
        """
        timestamp = datetime.now()
        
        # Time-based variations (simulate daily cycles)
        hour_of_day = timestamp.hour
        time_factor = math.sin(2 * math.pi * hour_of_day / 24)
        
        # Generate base readings with natural variations
        temperature = self._generate_temperature(time_factor)
        weight = self._generate_weight()
        moisture = self._generate_moisture(time_factor)
        pressure = self._generate_pressure()
        
        # Apply sensor-specific constraints
        temperature = max(-50, min(100, temperature))  # Realistic temperature range
        weight = max(0, weight)  # Weight cannot be negative
        moisture = max(0, min(100, moisture))  # Moisture percentage bounds
        pressure = max(80000, min(120000, pressure))  # Realistic pressure range
        
        reading = {
            'timestamp': timestamp,
            'temperature': round(temperature, 2),
            'weight': round(weight, 2),
            'moisture': round(moisture, 2),
            'pressure': round(pressure, 2),
            'sensor_id': 'SIM_001'
        }
        
        return reading
    
    def _generate_temperature(self, time_factor):
        """Generate temperature reading with daily cycle and noise."""
        # Base temperature with daily variation
        temp = self.base_temperature + (time_factor * 3)  # 3°C daily swing
        
        # Add random variation
        temp += random.uniform(-self.temperature_range/2, self.temperature_range/2)
        
        # Add noise
        temp += random.gauss(0, self.noise_level)
        
        # Simulate anomalies
        if random.random() < self.anomaly_probability:
            temp += random.uniform(-10, 15)  # Temperature spike/drop
        
        return temp
    
    def _generate_weight(self):
        """Generate weight reading with gradual changes."""
        # Weight changes more slowly and predictably
        weight = self.base_weight + random.uniform(-self.weight_range/2, self.weight_range/2)
        
        # Add small noise
        weight += random.gauss(0, self.noise_level * 0.5)
        
        # Simulate anomalies (sudden weight changes)
        if random.random() < self.anomaly_probability * 0.5:  # Less frequent anomalies
            weight += random.uniform(-20, 20)
        
        return weight
    
    def _generate_moisture(self, time_factor):
        """Generate moisture reading inversely correlated with temperature."""
        # Moisture tends to be inversely related to temperature
        moisture = self.base_moisture - (time_factor * 5)  # Inverse relationship
        
        # Add random variation
        moisture += random.uniform(-self.moisture_range/2, self.moisture_range/2)
        
        # Add noise
        moisture += random.gauss(0, self.noise_level)
        
        # Simulate anomalies
        if random.random() < self.anomaly_probability:
            moisture += random.uniform(-20, 25)
        
        return moisture
    
    def _generate_pressure(self):
        """Generate atmospheric pressure reading."""
        # Pressure changes more slowly
        pressure = self.base_pressure + random.uniform(-self.pressure_range/2, self.pressure_range/2)
        
        # Add small noise
        pressure += random.gauss(0, self.noise_level * 10)
        
        # Simulate weather-related pressure changes
        if random.random() < 0.1:  # 10% chance of weather change
            pressure += random.uniform(-2000, 2000)
        
        return pressure
    
    def simulate_sensor_failure(self):
        """
        Simulate sensor failure by returning invalid readings.
        
        Returns:
            dict: Invalid sensor reading for testing error handling
        """
        return {
            'timestamp': datetime.now(),
            'temperature': None,
            'weight': -999,  # Invalid weight
            'moisture': 150,  # Invalid moisture (>100%)
            'pressure': 0,  # Invalid pressure
            'sensor_id': 'SIM_001',
            'error': 'SENSOR_FAILURE'
        }
    
    def get_sensor_info(self):
        """
        Get information about the simulated sensors.
        
        Returns:
            dict: Sensor specifications and ranges
        """
        return {
            'sensors': {
                'temperature': {
                    'unit': '°C',
                    'range': (-50, 100),
                    'accuracy': '±0.1°C',
                    'base_value': self.base_temperature
                },
                'weight': {
                    'unit': 'kg',
                    'range': (0, 1000),
                    'accuracy': '±0.05kg',
                    'base_value': self.base_weight
                },
                'moisture': {
                    'unit': '%',
                    'range': (0, 100),
                    'accuracy': '±1%',
                    'base_value': self.base_moisture
                },
                'pressure': {
                    'unit': 'Pa',
                    'range': (80000, 120000),
                    'accuracy': '±10Pa',
                    'base_value': self.base_pressure
                }
            },
            'simulation_parameters': {
                'anomaly_probability': self.anomaly_probability,
                'noise_level': self.noise_level,
                'update_interval': '1-10 seconds'
            }
        }
