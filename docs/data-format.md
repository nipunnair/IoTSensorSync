# Sensor Data Format Specification

This document provides complete specifications for sensor data formats supported by the IoT Sensor Data Collection & Processing Pipeline. Data engineers can use this guide to understand how to format and upload sensor readings.

## 📋 Overview

The system accepts sensor data in multiple formats and provides comprehensive validation to ensure data quality and consistency. All data must conform to the specifications below to be processed correctly.

## 🔧 Core Data Schema

### Required Fields

| Field Name | Data Type | Unit | Valid Range | Required | Description |
|------------|-----------|------|-------------|----------|-------------|
| `timestamp` | datetime/string | ISO 8601 | Any valid datetime | ✅ | When the reading was recorded |
| `temperature` | float/number | °C | -50.0 to 100.0 | ✅ | Temperature sensor reading |
| `weight` | float/number | kg | 0.0 to 1000.0 | ✅ | Weight/load sensor reading |
| `moisture` | float/number | % | 0.0 to 100.0 | ✅ | Humidity/moisture percentage |
| `pressure` | float/number | Pa | 80000.0 to 120000.0 | ✅ | Atmospheric pressure reading |
| `sensor_id` | string | - | Any string | ✅ | Unique identifier for the sensor |

### Optional Fields

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| `location` | string | Physical location of the sensor |
| `device_type` | string | Type/model of the sensor device |
| `battery_level` | float | Battery percentage (0-100) |
| `signal_strength` | float | Signal strength indicator |
| `error_code` | string | Error code if sensor malfunction |

## 📊 Supported Data Formats

### 1. JSON Format

#### Single Reading
```json
{
  "timestamp": "2025-05-25T14:30:15.123456Z",
  "temperature": 23.45,
  "weight": 52.30,
  "moisture": 42.8,
  "pressure": 101325.50,
  "sensor_id": "SENSOR_001"
}
```

#### Multiple Readings (Array)
```json
[
  {
    "timestamp": "2025-05-25T14:30:15.123456Z",
    "temperature": 23.45,
    "weight": 52.30,
    "moisture": 42.8,
    "pressure": 101325.50,
    "sensor_id": "SENSOR_001"
  },
  {
    "timestamp": "2025-05-25T14:30:17.123456Z",
    "temperature": 23.52,
    "weight": 52.28,
    "moisture": 42.6,
    "pressure": 101320.25,
    "sensor_id": "SENSOR_001"
  }
]
```

#### Nested JSON (Multi-sensor)
```json
{
  "readings": [
    {
      "timestamp": "2025-05-25T14:30:15.123456Z",
      "sensors": {
        "temperature": 23.45,
        "weight": 52.30,
        "moisture": 42.8,
        "pressure": 101325.50
      },
      "sensor_id": "SENSOR_001"
    }
  ],
  "metadata": {
    "device_type": "Environmental_Monitor_v2",
    "location": "Warehouse_A"
  }
}
```

### 2. CSV Format

#### Standard CSV
```csv
timestamp,temperature,weight,moisture,pressure,sensor_id
2025-05-25T14:30:15.123456Z,23.45,52.30,42.8,101325.50,SENSOR_001
2025-05-25T14:30:17.123456Z,23.52,52.28,42.6,101320.25,SENSOR_001
2025-05-25T14:30:19.123456Z,23.48,52.32,42.9,101330.15,SENSOR_001
```

#### CSV with Headers and Metadata
```csv
# Device: Environmental Monitor v2.1
# Location: Production Floor A
# Calibration Date: 2025-05-01
# Data Collection Period: 2025-05-25 14:30:00 to 2025-05-25 15:30:00
timestamp,temperature,weight,moisture,pressure,sensor_id,location
2025-05-25T14:30:15.123456Z,23.45,52.30,42.8,101325.50,SENSOR_001,Floor_A
2025-05-25T14:30:17.123456Z,23.52,52.28,42.6,101320.25,SENSOR_001,Floor_A
```

### 3. XML Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sensor_data>
  <reading>
    <timestamp>2025-05-25T14:30:15.123456Z</timestamp>
    <temperature unit="celsius">23.45</temperature>
    <weight unit="kg">52.30</weight>
    <moisture unit="percent">42.8</moisture>
    <pressure unit="pascal">101325.50</pressure>
    <sensor_id>SENSOR_001</sensor_id>
  </reading>
  <reading>
    <timestamp>2025-05-25T14:30:17.123456Z</timestamp>
    <temperature unit="celsius">23.52</temperature>
    <weight unit="kg">52.28</weight>
    <moisture unit="percent">42.6</moisture>
    <pressure unit="pascal">101320.25</pressure>
    <sensor_id>SENSOR_001</sensor_id>
  </reading>
</sensor_data>
```

## 🕒 Timestamp Specifications

### Supported Timestamp Formats

#### ISO 8601 (Recommended)
```
2025-05-25T14:30:15.123456Z        # UTC with microseconds
2025-05-25T14:30:15Z               # UTC without microseconds
2025-05-25T14:30:15+00:00          # UTC with timezone offset
2025-05-25T14:30:15-05:00          # EST timezone
2025-05-25T14:30:15.123+02:00      # CET with milliseconds
```

#### Alternative Formats (Accepted)
```
2025-05-25 14:30:15.123456         # Space separator
2025/05/25 14:30:15                # Slash separator
05/25/2025 2:30:15 PM              # US format with AM/PM
1716645015.123                     # Unix timestamp with decimals
1716645015                         # Unix timestamp (seconds)
```

### Timezone Handling
- **Default**: Timestamps without timezone are treated as UTC
- **Recommended**: Always include timezone information
- **Conversion**: System automatically converts to UTC for processing

## 🔍 Data Validation Rules

### Temperature Validation
```python
# Valid range: -50°C to 100°C
valid_temperature = -50.0 <= temperature <= 100.0

# Common invalid values that will be rejected:
temperature = None          # Missing value
temperature = "N/A"         # String instead of number
temperature = -60.0         # Below minimum
temperature = 120.0         # Above maximum
temperature = float('inf')  # Infinite value
```

### Weight Validation
```python
# Valid range: 0kg to 1000kg
valid_weight = 0.0 <= weight <= 1000.0

# Invalid examples:
weight = -5.0              # Negative weight
weight = 1500.0            # Above maximum
weight = ""                # Empty string
```

### Moisture Validation
```python
# Valid range: 0% to 100%
valid_moisture = 0.0 <= moisture <= 100.0

# Invalid examples:
moisture = -10.0           # Negative percentage
moisture = 150.0           # Above 100%
moisture = "45%"           # String with unit
```

### Pressure Validation
```python
# Valid range: 80000Pa to 120000Pa (atmospheric pressure)
valid_pressure = 80000.0 <= pressure <= 120000.0

# Invalid examples:
pressure = 0.0             # Zero pressure
pressure = 50000.0         # Too low
pressure = 150000.0        # Too high
```

## 📤 Data Upload Methods

### 1. Real-time MQTT Publishing
```python
import paho.mqtt.client as mqtt
import json

# Connect to MQTT broker
client = mqtt.Client()
client.connect("your-mqtt-broker.com", 1883, 60)

# Publish sensor data
sensor_data = {
    "timestamp": "2025-05-25T14:30:15.123456Z",
    "temperature": 23.45,
    "weight": 52.30,
    "moisture": 42.8,
    "pressure": 101325.50,
    "sensor_id": "SENSOR_001"
}

client.publish("sensors/readings", json.dumps(sensor_data))
```

### 2. REST API Upload
```python
import requests
import json

# API endpoint
url = "https://your-api-endpoint.com/api/sensor-data"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}

# Single reading
response = requests.post(url, headers=headers, data=json.dumps(sensor_data))

# Batch upload
batch_data = {
    "readings": [sensor_data_1, sensor_data_2, sensor_data_3],
    "metadata": {
        "batch_id": "BATCH_001",
        "upload_time": "2025-05-25T15:00:00Z"
    }
}
response = requests.post(url + "/batch", headers=headers, data=json.dumps(batch_data))
```

### 3. File Upload
```python
# CSV file upload
import pandas as pd

# Prepare CSV data
df = pd.DataFrame(sensor_readings)
df.to_csv('sensor_data.csv', index=False)

# Upload via web interface or API
files = {'file': open('sensor_data.csv', 'rb')}
response = requests.post('https://your-api-endpoint.com/upload', files=files)
```

### 4. Database Direct Insert
```sql
-- PostgreSQL example
INSERT INTO sensor_readings (timestamp, temperature, weight, moisture, pressure, sensor_id)
VALUES 
  ('2025-05-25T14:30:15.123456Z', 23.45, 52.30, 42.8, 101325.50, 'SENSOR_001'),
  ('2025-05-25T14:30:17.123456Z', 23.52, 52.28, 42.6, 101320.25, 'SENSOR_001');
```

## 🚫 Common Data Issues and Solutions

### Issue 1: Invalid Timestamp Format
```json
// ❌ Invalid
{"timestamp": "05/25/2025 2:30 PM", ...}

// ✅ Correct
{"timestamp": "2025-05-25T14:30:00Z", ...}
```

### Issue 2: String Numbers
```json
// ❌ Invalid
{"temperature": "23.45", ...}

// ✅ Correct
{"temperature": 23.45, ...}
```

### Issue 3: Missing Required Fields
```json
// ❌ Invalid (missing pressure)
{
  "timestamp": "2025-05-25T14:30:15Z",
  "temperature": 23.45,
  "weight": 52.30,
  "moisture": 42.8,
  "sensor_id": "SENSOR_001"
}

// ✅ Correct
{
  "timestamp": "2025-05-25T14:30:15Z",
  "temperature": 23.45,
  "weight": 52.30,
  "moisture": 42.8,
  "pressure": 101325.50,
  "sensor_id": "SENSOR_001"
}
```

### Issue 4: Out-of-Range Values
```json
// ❌ Invalid (temperature too high)
{"temperature": 150.0, ...}

// ✅ Correct
{"temperature": 23.45, ...}
```

## 🔧 Data Processing Pipeline

### Input Validation
1. **Schema Validation**: Check required fields
2. **Type Validation**: Ensure correct data types
3. **Range Validation**: Verify values within acceptable ranges
4. **Timestamp Validation**: Parse and validate timestamp format

### Data Cleaning
1. **Missing Value Handling**: Forward fill, interpolation
2. **Outlier Detection**: Z-score and IQR methods
3. **Duplicate Removal**: Timestamp-based deduplication
4. **Data Smoothing**: Optional Savitzky-Golay filtering

### Quality Scoring
```python
# Data quality metrics calculated automatically
quality_score = {
    "completeness": 98.5,      # Percentage of non-missing values
    "consistency": 95.2,       # Percentage within valid ranges
    "temporal": 99.1,          # Timestamp consistency
    "overall": 97.6            # Combined quality score
}
```

## 📋 Integration Examples

### Python Integration
```python
import requests
import json
from datetime import datetime

class SensorDataUploader:
    def __init__(self, api_endpoint, api_key):
        self.endpoint = api_endpoint
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def upload_reading(self, temperature, weight, moisture, pressure, sensor_id):
        data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature": temperature,
            "weight": weight,
            "moisture": moisture,
            "pressure": pressure,
            "sensor_id": sensor_id
        }
        
        response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(data))
        return response.status_code == 200

# Usage
uploader = SensorDataUploader("https://api.example.com/sensors", "your_api_key")
success = uploader.upload_reading(23.5, 52.3, 42.8, 101325, "SENSOR_001")
```

### Arduino/ESP32 Integration
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

void uploadSensorData(float temp, float weight, float moisture, float pressure) {
    HTTPClient http;
    http.begin("https://api.example.com/sensors");
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer YOUR_API_KEY");
    
    DynamicJsonDocument doc(1024);
    doc["timestamp"] = getISOTimestamp();
    doc["temperature"] = temp;
    doc["weight"] = weight;
    doc["moisture"] = moisture;
    doc["pressure"] = pressure;
    doc["sensor_id"] = "ESP32_001";
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    http.end();
}
```

## 📞 Support and Validation

### Data Validation Endpoint
```bash
# Test your data format
curl -X POST https://api.example.com/validate \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2025-05-25T14:30:15Z",
    "temperature": 23.45,
    "weight": 52.30,
    "moisture": 42.8,
    "pressure": 101325.50,
    "sensor_id": "SENSOR_001"
  }'
```

### Error Response Format
```json
{
  "valid": false,
  "errors": [
    "temperature value 150.0 is outside valid range [-50.0, 100.0]",
    "moisture field is missing",
    "timestamp format is invalid"
  ],
  "suggestions": [
    "Ensure temperature is between -50°C and 100°C",
    "Include all required fields: timestamp, temperature, weight, moisture, pressure, sensor_id",
    "Use ISO 8601 timestamp format: YYYY-MM-DDTHH:MM:SSZ"
  ]
}
```

For additional support or questions about data formats, please refer to the API documentation or contact the development team.