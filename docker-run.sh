#!/bin/bash

# IoT Sensor Pipeline - Docker Deployment Script

echo "🚀 Starting IoT Sensor Data Pipeline with Docker..."

# Create exports directory for data output
mkdir -p exports

# Build and run the application
echo "📦 Building Docker image..."
docker build -t iot-sensor-pipeline .

echo "🏃 Starting container..."
docker run -d \
  --name iot-sensor-pipeline \
  -p 7001:7001 \
  -v $(pwd)/exports:/app/exports \
  --restart unless-stopped \
  iot-sensor-pipeline

echo "✅ IoT Sensor Pipeline is now running!"
echo "🌐 Access the dashboard at: http://localhost:7001"
echo ""
echo "📋 Container management commands:"
echo "  View logs:    docker logs iot-sensor-pipeline"
echo "  Stop:         docker stop iot-sensor-pipeline"
echo "  Remove:       docker rm iot-sensor-pipeline"
echo "  Restart:      docker restart iot-sensor-pipeline"