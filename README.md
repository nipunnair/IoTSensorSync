# IoT Sensor Data Collection & Processing Pipeline

A comprehensive Streamlit-based application for collecting, processing, and analyzing IoT sensor data from temperature, weight, moisture, and pressure sensors.

## 🌟 Features

- **Real-time Data Collection**: Live sensor data simulation and monitoring
- **Advanced Data Processing**: Outlier detection, missing value handling, and data smoothing
- **Comprehensive Analytics**: Trend analysis, correlation studies, and anomaly detection
- **Interactive Dashboard**: Real-time visualizations and data exploration tools
- **Data Export**: CSV and JSON export capabilities for processed data
- **Sensor Health Monitoring**: Performance metrics and health scoring for each sensor

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd iot-sensor-pipeline
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py --server.port 5000
```

4. Open your browser and navigate to `http://localhost:5000`

## 📖 Documentation

- [Developer Setup Guide](docs/developer-guide.md) - Complete setup and development instructions
- [Architecture Overview](docs/architecture.md) - System design and component details
- [Data Format Specification](docs/data-format.md) - Sensor data format for integration
- [API Reference](docs/api-reference.md) - Integration endpoints and methods

## 🏗️ Architecture

The application follows a modular pipeline architecture:

```
Sensor Data → Validation → Storage → Processing → Analytics → Visualization
```

### Core Components:
- **Sensor Simulator**: Generates realistic sensor readings
- **Data Storage**: Thread-safe in-memory data management
- **Data Processor**: Cleaning, validation, and preprocessing
- **Analytics Engine**: Statistical analysis and trend detection
- **Streamlit Interface**: Interactive dashboard and controls

## 📊 Dashboard Features

### Real-time Dashboard
- Live sensor readings with trend indicators
- Time series visualizations for all sensors
- Current status and health metrics

### Data Processing
- Data quality analysis and metrics
- Outlier detection and visualization
- Configurable cleaning options

### Analytics
- Statistical summaries and correlation analysis
- Trend analysis with confidence intervals
- Distribution analysis and insights

### Data Explorer
- Filterable data views by date and sensor
- Custom visualization builder
- Export functionality

## 🔧 Integration

The system supports multiple integration methods:

- **MQTT**: Real-time sensor data streaming
- **REST API**: HTTP-based data ingestion
- **File Upload**: Batch data processing
- **Database**: Direct database connections

## 📈 Use Cases

- Industrial IoT monitoring systems
- Environmental data collection
- Research and development projects
- Educational demonstrations
- Prototype testing and validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions and support:
- Check the [documentation](docs/)
- Open an [issue](issues/)
- Contact the development team