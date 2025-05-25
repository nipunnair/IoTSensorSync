# Architecture Overview

This document provides a comprehensive overview of the IoT Sensor Data Collection & Processing Pipeline architecture, detailing system components, data flow, and design principles.

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Data Pipeline  │───▶│  Presentation   │
│                 │    │                 │    │     Layer       │
│ • IoT Sensors   │    │ • Validation    │    │ • Dashboard     │
│ • Simulators    │    │ • Processing    │    │ • Analytics     │
│ • APIs          │    │ • Storage       │    │ • Export        │
│ • Files         │    │ • Analytics     │    │ • Controls      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow Pipeline

```
Raw Sensor Data → Validation → Storage → Processing → Analytics → Visualization
       ↓              ↓           ↓          ↓           ↓           ↓
   JSON/CSV      Error Check   DataFrame   Cleaning   Statistics  Dashboard
   MQTT/API      Range Valid   Thread-Safe  Outliers   Trends      Real-time
   Real-time     Type Check    In-Memory    Missing    Correlations Export
```

## 🧩 Component Architecture

### 1. Data Layer

#### **SensorSimulator** (`sensor_simulator.py`)
- **Purpose**: Generates realistic sensor data for testing and demonstration
- **Capabilities**:
  - Multi-sensor simulation (temperature, weight, moisture, pressure)
  - Natural variation patterns with daily cycles
  - Configurable anomaly injection
  - Sensor failure simulation
- **Integration Points**: Replaceable with real IoT data sources

#### **DataStorage** (`data_storage.py`)
- **Purpose**: Thread-safe in-memory data management
- **Features**:
  - Thread-safe operations with locks
  - Automatic data type enforcement
  - Memory usage optimization (configurable limits)
  - Time-based data retrieval
  - Export functionality
- **Storage Model**: Pandas DataFrame with optimized indexing

#### **Utils** (`utils.py`)
- **Purpose**: Common utilities and validation functions
- **Functions**:
  - Data validation and type checking
  - Timestamp formatting and parsing
  - Export format handlers
  - Data quality scoring
  - Alert message generation

### 2. Processing Layer

#### **DataProcessor** (`data_processor.py`)
- **Purpose**: Data cleaning, validation, and preprocessing
- **Processing Pipeline**:
  1. **Missing Value Handling**: Forward fill, backward fill, interpolation
  2. **Invalid Value Removal**: Range-based validation
  3. **Outlier Detection**: Z-score and IQR methods
  4. **Data Smoothing**: Savitzky-Golay filtering
  5. **Temporal Consistency**: Timestamp validation
- **Quality Metrics**: Completeness, consistency, temporal alignment

#### **Analytics** (`analytics.py`)
- **Purpose**: Advanced statistical analysis and insights
- **Capabilities**:
  - **Descriptive Statistics**: Mean, median, variance, skewness, kurtosis
  - **Trend Analysis**: Linear regression with confidence intervals
  - **Correlation Analysis**: Pearson correlation with significance testing
  - **Anomaly Detection**: Multiple algorithm support
  - **Health Scoring**: Sensor performance evaluation
  - **Insight Generation**: Automated recommendations

### 3. Presentation Layer

#### **Streamlit Application** (`app.py`)
- **Purpose**: Interactive web interface and real-time dashboard
- **Architecture Pattern**: Session-based state management
- **Components**:
  - **Control Panel**: Simulation controls and settings
  - **Real-time Dashboard**: Live metrics and visualizations
  - **Data Processing Interface**: Quality analysis and cleaning tools
  - **Analytics Dashboard**: Statistical insights and trends
  - **Data Explorer**: Interactive data filtering and visualization

## 🔄 Data Flow Architecture

### 1. Data Ingestion
```python
# Current: Simulation
sensor_data = sensor_simulator.generate_reading()

# Future: Real IoT Integration
sensor_data = mqtt_client.get_latest_reading()
sensor_data = api_client.fetch_sensor_data()
sensor_data = file_parser.parse_csv_upload()
```

### 2. Data Validation
```python
validation_result = validate_sensor_data(sensor_data)
if validation_result['valid']:
    proceed_to_storage()
else:
    log_errors(validation_result['errors'])
```

### 3. Data Storage
```python
# Thread-safe storage with automatic cleanup
data_storage.add_reading(sensor_data)
# Automatic memory management and indexing
```

### 4. Data Processing
```python
# Configurable processing pipeline
cleaned_data = data_processor.clean_data(
    raw_data,
    remove_outliers=True,
    fill_missing=True,
    smooth_data=False
)
```

### 5. Analytics Processing
```python
# Multi-dimensional analysis
statistics = analytics.calculate_statistics(data)
trends = analytics.analyze_trends(data)
correlations = analytics.analyze_correlations(data)
insights = analytics.generate_insights(data)
```

### 6. Visualization
```python
# Real-time dashboard updates
plotly_charts = generate_time_series(data)
metrics = calculate_current_readings(data)
health_scores = evaluate_sensor_health(data)
```

## 🔧 Technical Architecture

### Threading Model
- **Main Thread**: Streamlit application and UI
- **Background Threads**: Data collection and processing
- **Thread Safety**: Locks on shared data structures
- **Auto-refresh**: Streamlit's built-in rerun mechanism

### Memory Management
```python
# Configurable limits
MAX_RECORDS = 10000  # Prevents memory overflow
CLEANUP_THRESHOLD = 0.9  # Automatic cleanup trigger
TIME_WINDOW = 24  # Hours of data retention
```

### State Management
```python
# Streamlit session state
st.session_state.data_storage = DataStorage()
st.session_state.simulation_active = False
st.session_state.processing_config = {...}
```

### Error Handling
- **Graceful Degradation**: Continue operation despite individual sensor failures
- **Validation Layers**: Multiple validation points in the pipeline
- **User Feedback**: Clear error messages and status indicators
- **Recovery Mechanisms**: Automatic retry and fallback options

## 🔌 Integration Architecture

### Current Integration Points

#### 1. Sensor Data Input
```python
# Extensible sensor interface
class SensorInterface:
    def generate_reading(self) -> Dict
    def get_sensor_info(self) -> Dict
    def simulate_failure(self) -> Dict
```

#### 2. Storage Backend
```python
# Replaceable storage interface
class StorageInterface:
    def add_reading(self, data: Dict) -> bool
    def get_data(self, filters: Dict) -> pd.DataFrame
    def export_data(self, format: str) -> str
```

#### 3. Processing Pipeline
```python
# Configurable processing steps
class ProcessorInterface:
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame
    def analyze_quality(self, data: pd.DataFrame) -> Dict
    def detect_outliers(self, data: pd.DataFrame) -> pd.DataFrame
```

### Future Integration Options

#### 1. **MQTT Integration**
```python
# Real-time IoT data streaming
import paho.mqtt.client as mqtt

class MQTTSensorClient:
    def __init__(self, broker_host, topics):
        self.client = mqtt.Client()
        self.topics = topics
        
    def on_message(self, client, userdata, message):
        sensor_data = json.loads(message.payload)
        self.data_storage.add_reading(sensor_data)
```

#### 2. **REST API Integration**
```python
# Cloud IoT platform integration
import requests

class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {api_key}'}
        
    def fetch_sensor_data(self, sensor_id, time_range):
        response = requests.get(f'{self.base_url}/sensors/{sensor_id}')
        return response.json()
```

#### 3. **Database Integration**
```python
# Time-series database integration
import psycopg2
from sqlalchemy import create_engine

class DatabaseClient:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        
    def fetch_recent_data(self, hours=1):
        query = """
        SELECT timestamp, temperature, weight, moisture, pressure, sensor_id
        FROM sensor_readings 
        WHERE timestamp >= NOW() - INTERVAL '%s hours'
        ORDER BY timestamp DESC
        """
        return pd.read_sql(query, self.engine, params=[hours])
```

## 📊 Performance Architecture

### Scalability Considerations
- **Memory Usage**: Configurable data retention limits
- **Processing Speed**: Vectorized operations with Pandas/NumPy
- **Real-time Updates**: Efficient delta updates instead of full refreshes
- **Visualization**: Optimized Plotly charts with data sampling

### Performance Optimizations
```python
# Efficient data operations
data = data.copy()  # Avoid in-place modifications
data.set_index('timestamp', inplace=True)  # Fast time-based queries
data = data.astype({'sensor_id': 'category'})  # Memory optimization
```

### Monitoring and Metrics
- **Data Quality Scores**: Real-time quality assessment
- **System Health**: Memory usage and performance tracking
- **Sensor Health**: Individual sensor performance metrics
- **Processing Metrics**: Pipeline performance indicators

## 🛡️ Security Architecture

### Data Validation
- **Input Sanitization**: Type checking and range validation
- **Schema Validation**: Structured data requirements
- **Error Containment**: Isolated error handling

### Access Control
- **Local Deployment**: Single-user access model
- **Future Enhancements**: Authentication and authorization layers
- **Data Privacy**: In-memory storage with no persistent logging

## 🔮 Extensibility Architecture

### Plugin Architecture
The system is designed for easy extension:

```python
# Custom sensor plugin
class CustomSensor(SensorInterface):
    def generate_reading(self):
        # Custom sensor logic
        return sensor_data

# Custom analytics plugin
class CustomAnalytics(AnalyticsInterface):
    def custom_analysis(self, data):
        # Custom analysis logic
        return results
```

### Configuration Management
```python
# Extensible configuration
CONFIG = {
    'sensors': {...},
    'processing': {...},
    'analytics': {...},
    'visualization': {...}
}
```

This architecture provides a solid foundation for IoT data collection and processing while maintaining flexibility for future enhancements and integrations.