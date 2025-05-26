# Developer Setup Guide

This guide provides complete instructions for setting up and running the IoT Sensor Data Collection & Processing Pipeline.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 1GB free space

### Required Software (Choose One)

#### Option A: Docker (Recommended)
- **Docker**: Version 20.0+
- **Docker Compose**: Version 2.0+ (optional)
- Web browser (Chrome, Firefox, Safari, or Edge)

#### Option B: Local Python Development
- **Python**: Version 3.11 or higher
- **pip**: Package manager
- Git (for cloning the repository)
- Web browser (Chrome, Firefox, Safari, or Edge)

## 🚀 Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd iot-sensor-pipeline
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv iot-env

# Activate virtual environment
# On Windows:
iot-env\Scripts\activate
# On macOS/Linux:
source iot-env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python -c "import streamlit, pandas, plotly, scipy, numpy; print('All dependencies installed successfully!')"
```

## 🏃‍♂️ Running the Application

### Option 1: Local Development (Python)
```bash
streamlit run app.py --server.port 5000
```

### Option 2: Docker (Recommended)

#### Quick Start with Docker
```bash
# Make script executable and run
chmod +x docker-run.sh
./docker-run.sh
```

#### Using Docker Compose
```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f iot-sensor-dashboard

# Stop the application
docker-compose down
```

#### Manual Docker Commands
```bash
# Build the Docker image
docker build -t iot-sensor-pipeline .

# Run the container
docker run -d \
  --name iot-sensor-pipeline \
  -p 5000:5000 \
  -v $(pwd)/exports:/app/exports \
  --restart unless-stopped \
  iot-sensor-pipeline

# View logs
docker logs -f iot-sensor-pipeline

# Stop the container
docker stop iot-sensor-pipeline
```

### Option 3: Production Deployment
```bash
streamlit run app.py --server.port 5000 --server.headless true
```

### Custom Configuration
Create a `.streamlit/config.toml` file:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "light"
```

### Docker vs Local Development

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Local Python** | Fast development cycle, easy debugging | Requires Python setup, environment conflicts | Development |
| **Docker** | Consistent environment, easy deployment | Slower rebuild, requires Docker | Production, Sharing |
| **Docker Compose** | Multi-service setup, production-like | More complex configuration | Integration testing |

### Accessing the Application
Once running, open your browser and navigate to:
- **Local/Docker**: `http://localhost:5000`
- **Production**: `http://your-server-ip:5000`

## 🔧 Development Environment

### Project Structure
```
iot-sensor-pipeline/
├── app.py                 # Main Streamlit application
├── sensor_simulator.py    # Sensor data simulation
├── data_processor.py      # Data cleaning and processing
├── data_storage.py        # In-memory data storage
├── analytics.py           # Statistical analysis
├── utils.py              # Utility functions
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
└── README.md            # Project overview
```

### Key Files Description

#### `app.py`
- Main application entry point
- Streamlit interface and dashboard
- Session state management
- Real-time updates and controls

#### `sensor_simulator.py`
- Generates realistic sensor data
- Configurable sensor ranges and variations
- Anomaly simulation capabilities

#### `data_processor.py`
- Data validation and cleaning
- Outlier detection algorithms
- Missing value handling
- Data quality metrics

#### `data_storage.py`
- Thread-safe data storage
- In-memory DataFrame management
- Data retrieval and filtering
- Memory usage optimization

#### `analytics.py`
- Statistical analysis functions
- Trend detection and correlation
- Anomaly detection algorithms
- Performance metrics calculation

#### `utils.py`
- Common utility functions
- Data validation helpers
- Formatting and export functions

## 🔄 Development Workflow

### Making Changes
1. **Code Modifications**: Edit any of the Python files
2. **Auto-reload**: Streamlit automatically reloads on file changes
3. **Testing**: Use the built-in simulation for immediate feedback
4. **Debugging**: Check browser console and terminal for errors

### Adding New Features
1. **Sensor Types**: Modify `sensor_simulator.py` and update validation ranges
2. **Processing Methods**: Add functions to `data_processor.py`
3. **Analytics**: Extend `analytics.py` with new statistical methods
4. **UI Components**: Update `app.py` with new dashboard elements

### Configuration Options

#### Sensor Configuration
```python
# In sensor_simulator.py
self.sensor_ranges = {
    'temperature': (-50, 100),
    'weight': (0, 1000),
    'moisture': (0, 100),
    'pressure': (80000, 120000)
}
```

#### Data Processing Settings
```python
# In data_processor.py
self.outlier_threshold = 3  # Z-score threshold
self.iqr_multiplier = 1.5   # IQR multiplier
```

#### Storage Limits
```python
# In data_storage.py
self._max_records = 10000  # Maximum stored records
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
streamlit run app.py --server.port 8501
```

#### Module Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### Memory Issues
- Reduce `_max_records` in `data_storage.py`
- Clear data regularly using the dashboard
- Monitor memory usage in the system metrics

#### Performance Issues
- Increase data collection interval
- Disable smoothing for large datasets
- Optimize processing parameters

### Debug Mode
Enable debug logging by adding to your script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🧪 Testing

### Manual Testing
1. Start the application
2. Click "Start" to begin simulation
3. Verify real-time data updates
4. Test data processing features
5. Export data and verify format

### Data Validation
```python
# Test sensor data validation
from utils import validate_sensor_data

test_data = {
    'timestamp': '2025-05-25T14:30:15',
    'temperature': 25.5,
    'weight': 50.0,
    'moisture': 45.0,
    'pressure': 101325.0,
    'sensor_id': 'TEST_001'
}

result = validate_sensor_data(test_data)
print(f"Valid: {result['valid']}, Errors: {result['errors']}")
```

## 📦 Building for Production

### Environment Variables
Set these for production deployment:
```bash
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_PORT=5000
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.headless=true"]
```

## 🤝 Contributing

### Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where appropriate

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Update documentation
6. Submit pull request

### Issue Reporting
When reporting issues, include:
- Python version
- Operating system
- Steps to reproduce
- Error messages
- Expected vs actual behavior

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [SciPy Documentation](https://docs.scipy.org/)

For questions or support, please check the project issues or contact the development team.