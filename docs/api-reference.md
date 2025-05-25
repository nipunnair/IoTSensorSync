# API Reference

This document provides comprehensive API reference for integrating with the IoT Sensor Data Collection & Processing Pipeline.

## 🌐 API Overview

The system provides multiple integration endpoints for real-time data ingestion, batch uploads, and data retrieval. All APIs follow RESTful conventions and support JSON payloads.

### Base URL
```
https://your-deployment-url.com/api/v1
```

### Authentication
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## 📡 Real-time Data Ingestion

### POST /sensors/readings
Submit individual sensor readings in real-time.

#### Request
```http
POST /api/v1/sensors/readings
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "timestamp": "2025-05-25T14:30:15.123456Z",
  "temperature": 23.45,
  "weight": 52.30,
  "moisture": 42.8,
  "pressure": 101325.50,
  "sensor_id": "SENSOR_001"
}
```

#### Response
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "status": "success",
  "message": "Sensor reading recorded successfully",
  "reading_id": "read_123456789",
  "timestamp": "2025-05-25T14:30:15.123456Z",
  "processed": true
}
```

#### Error Response
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "message": "Validation failed",
  "errors": [
    "temperature value 150.0 is outside valid range [-50.0, 100.0]",
    "moisture field is missing"
  ]
}
```

### POST /sensors/readings/batch
Submit multiple sensor readings in a single request.

#### Request
```http
POST /api/v1/sensors/readings/batch
Content-Type: application/json

{
  "readings": [
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
  ],
  "metadata": {
    "batch_id": "BATCH_001",
    "source": "Production_Floor_A"
  }
}
```

#### Response
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "status": "success",
  "message": "Batch processed successfully",
  "batch_id": "BATCH_001",
  "total_readings": 2,
  "successful": 2,
  "failed": 0,
  "errors": []
}
```

## 📊 Data Retrieval

### GET /sensors/readings
Retrieve sensor readings with optional filtering.

#### Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `sensor_id` | string | Filter by sensor ID | all |
| `start_time` | datetime | Start of time range | 24h ago |
| `end_time` | datetime | End of time range | now |
| `limit` | integer | Maximum results | 1000 |
| `format` | string | Response format (json/csv) | json |

#### Request
```http
GET /api/v1/sensors/readings?sensor_id=SENSOR_001&start_time=2025-05-25T10:00:00Z&limit=100
```

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": [
    {
      "timestamp": "2025-05-25T14:30:15.123456Z",
      "temperature": 23.45,
      "weight": 52.30,
      "moisture": 42.8,
      "pressure": 101325.50,
      "sensor_id": "SENSOR_001"
    }
  ],
  "metadata": {
    "total_count": 1,
    "page": 1,
    "has_more": false
  }
}
```

### GET /sensors/readings/latest
Get the most recent reading for each sensor.

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": {
    "SENSOR_001": {
      "timestamp": "2025-05-25T14:30:15.123456Z",
      "temperature": 23.45,
      "weight": 52.30,
      "moisture": 42.8,
      "pressure": 101325.50,
      "sensor_id": "SENSOR_001"
    }
  },
  "last_updated": "2025-05-25T14:30:15.123456Z"
}
```

## 🔍 Analytics Endpoints

### GET /analytics/statistics
Get statistical summary for sensor data.

#### Request
```http
GET /api/v1/analytics/statistics?sensor_id=SENSOR_001&time_range=24h
```

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": {
    "temperature": {
      "count": 1440,
      "mean": 23.45,
      "std": 2.15,
      "min": 18.2,
      "max": 28.9,
      "q25": 21.8,
      "q75": 25.1
    },
    "weight": {
      "count": 1440,
      "mean": 52.30,
      "std": 3.21,
      "min": 45.1,
      "max": 58.7,
      "q25": 50.2,
      "q75": 54.8
    }
  },
  "time_range": {
    "start": "2025-05-24T14:30:15Z",
    "end": "2025-05-25T14:30:15Z"
  }
}
```

### GET /analytics/trends
Get trend analysis for sensor data.

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": {
    "temperature": {
      "direction": "Increasing",
      "slope": 0.0012,
      "r_squared": 0.85,
      "confidence": "High",
      "p_value": 0.001
    },
    "moisture": {
      "direction": "Decreasing",
      "slope": -0.0008,
      "r_squared": 0.72,
      "confidence": "High",
      "p_value": 0.003
    }
  }
}
```

### GET /analytics/correlations
Get correlation analysis between sensors.

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": {
    "temperature_vs_moisture": {
      "coefficient": -0.78,
      "strength": "Strong",
      "direction": "Negative",
      "significant": true
    },
    "weight_vs_pressure": {
      "coefficient": 0.23,
      "strength": "Weak",
      "direction": "Positive",
      "significant": false
    }
  }
}
```

## 🏥 Health and Status

### GET /health
System health check endpoint.

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "healthy",
  "timestamp": "2025-05-25T14:30:15.123456Z",
  "services": {
    "database": "operational",
    "processing": "operational",
    "analytics": "operational"
  },
  "metrics": {
    "total_sensors": 5,
    "active_sensors": 4,
    "data_quality_score": 97.5,
    "uptime_hours": 168.5
  }
}
```

### GET /sensors/health
Individual sensor health metrics.

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": {
    "SENSOR_001": {
      "status": "Excellent",
      "health_score": 98.5,
      "availability_percent": 99.2,
      "last_reading": "2025-05-25T14:30:15Z",
      "issues": []
    },
    "SENSOR_002": {
      "status": "Fair",
      "health_score": 65.8,
      "availability_percent": 78.5,
      "last_reading": "2025-05-25T14:25:10Z",
      "issues": [
        "High variability in readings",
        "Intermittent connectivity"
      ]
    }
  }
}
```

## 📤 Data Export

### GET /export/data
Export sensor data in various formats.

#### Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `format` | string | Export format (csv/json/excel) | csv |
| `sensor_id` | string | Filter by sensor ID | all |
| `start_time` | datetime | Start of time range | 24h ago |
| `end_time` | datetime | End of time range | now |
| `processed` | boolean | Include processed data | true |

#### Request
```http
GET /api/v1/export/data?format=csv&sensor_id=SENSOR_001&start_time=2025-05-25T00:00:00Z
```

#### Response
```http
HTTP/1.1 200 OK
Content-Type: text/csv
Content-Disposition: attachment; filename="sensor_data_20250525.csv"

timestamp,temperature,weight,moisture,pressure,sensor_id
2025-05-25T14:30:15.123456Z,23.45,52.30,42.8,101325.50,SENSOR_001
2025-05-25T14:30:17.123456Z,23.52,52.28,42.6,101320.25,SENSOR_001
```

## 🛠️ Configuration Management

### GET /config
Get current system configuration.

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "config": {
    "sensors": {
      "temperature": {
        "enabled": true,
        "min_value": -50,
        "max_value": 100,
        "unit": "°C"
      }
    },
    "data_collection": {
      "interval_seconds": 2,
      "max_records": 10000
    },
    "processing": {
      "outlier_detection": true,
      "missing_value_handling": true
    }
  }
}
```

### PUT /config
Update system configuration.

#### Request
```http
PUT /api/v1/config
Content-Type: application/json

{
  "data_collection": {
    "interval_seconds": 5,
    "max_records": 15000
  },
  "processing": {
    "outlier_detection": true,
    "smoothing": true
  }
}
```

## 📝 Validation

### POST /validate
Validate sensor data format without storing.

#### Request
```http
POST /api/v1/validate
Content-Type: application/json

{
  "timestamp": "2025-05-25T14:30:15Z",
  "temperature": 23.45,
  "weight": 52.30,
  "moisture": 42.8,
  "pressure": 101325.50,
  "sensor_id": "SENSOR_001"
}
```

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "valid": true,
  "message": "Data format is valid",
  "suggestions": []
}
```

## 🔐 Authentication

### POST /auth/token
Get API access token.

#### Request
```http
POST /api/v1/auth/token
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "scope": "read write"
}
```

## 📋 Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Invalid or missing authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Data validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## 🧪 Testing and Examples

### cURL Examples

#### Submit Single Reading
```bash
curl -X POST https://api.example.com/api/v1/sensors/readings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "timestamp": "2025-05-25T14:30:15Z",
    "temperature": 23.45,
    "weight": 52.30,
    "moisture": 42.8,
    "pressure": 101325.50,
    "sensor_id": "SENSOR_001"
  }'
```

#### Get Recent Data
```bash
curl -X GET "https://api.example.com/api/v1/sensors/readings?limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Export Data as CSV
```bash
curl -X GET "https://api.example.com/api/v1/export/data?format=csv" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -o sensor_data.csv
```

### Python SDK Example
```python
import requests
import json

class SensorAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def submit_reading(self, reading_data):
        response = requests.post(
            f"{self.base_url}/sensors/readings",
            headers=self.headers,
            data=json.dumps(reading_data)
        )
        return response.json()
    
    def get_readings(self, **filters):
        response = requests.get(
            f"{self.base_url}/sensors/readings",
            headers=self.headers,
            params=filters
        )
        return response.json()

# Usage
api = SensorAPI("https://api.example.com/api/v1", "your_api_key")
result = api.submit_reading({
    "timestamp": "2025-05-25T14:30:15Z",
    "temperature": 23.45,
    "weight": 52.30,
    "moisture": 42.8,
    "pressure": 101325.50,
    "sensor_id": "SENSOR_001"
})
```

## 📊 Rate Limits

| Endpoint | Rate Limit | Burst Limit |
|----------|------------|-------------|
| POST /sensors/readings | 100/minute | 200 |
| POST /sensors/readings/batch | 10/minute | 20 |
| GET /sensors/readings | 1000/hour | 100 |
| GET /analytics/* | 500/hour | 50 |
| GET /export/data | 10/hour | 5 |

## 🔄 Webhooks

### Webhook Events
- `sensor.reading.created` - New sensor reading received
- `sensor.health.changed` - Sensor health status changed
- `data.quality.alert` - Data quality threshold breached
- `system.maintenance` - System maintenance notifications

### Webhook Payload Example
```json
{
  "event": "sensor.reading.created",
  "timestamp": "2025-05-25T14:30:15Z",
  "data": {
    "sensor_id": "SENSOR_001",
    "reading": {
      "timestamp": "2025-05-25T14:30:15Z",
      "temperature": 23.45,
      "weight": 52.30,
      "moisture": 42.8,
      "pressure": 101325.50
    }
  }
}
```

For additional API support or integration assistance, please contact the development team or refer to the main documentation.