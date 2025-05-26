# Docker Deployment Guide

This guide provides complete instructions for deploying the IoT Sensor Data Pipeline using Docker containers.

## 🐳 Docker Overview

The application is fully containerized and can be deployed using Docker with minimal setup. This approach ensures:

- **Consistent Environment** - Same behavior across different systems
- **Easy Deployment** - One-command deployment process
- **Scalability** - Ready for production scaling
- **Isolation** - No conflicts with host system dependencies

## 📋 Prerequisites

### System Requirements
- **Docker** - Version 20.0+ 
- **Docker Compose** - Version 2.0+ (optional)
- **Operating System** - Linux, macOS, or Windows with WSL2
- **Memory** - Minimum 2GB RAM available for container
- **Storage** - 1GB free disk space

### Installation
```bash
# Install Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

## 🚀 Quick Start

### Option 1: Using Docker Run Script (Recommended)
```bash
# Make script executable and run
chmod +x docker-run.sh
./docker-run.sh
```

### Option 2: Docker Compose
```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 3: Manual Docker Commands
```bash
# Build the image
docker build -t iot-sensor-pipeline .

# Run the container
docker run -d \
  --name iot-sensor-pipeline \
  -p 5000:5000 \
  -v $(pwd)/exports:/app/exports \
  --restart unless-stopped \
  iot-sensor-pipeline
```

## 🔧 Configuration Options

### Environment Variables
```bash
# Basic configuration
docker run -d \
  --name iot-sensor-pipeline \
  -p 5000:5000 \
  -e STREAMLIT_SERVER_PORT=5000 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  -e STREAMLIT_SERVER_HEADLESS=true \
  iot-sensor-pipeline
```

### Port Mapping
```bash
# Default port (5000)
-p 5000:5000

# Custom port (8080)
-p 8080:5000

# Multiple instances
-p 5001:5000  # Instance 1
-p 5002:5000  # Instance 2
```

### Volume Mounting
```bash
# Data exports
-v $(pwd)/exports:/app/exports

# Configuration files
-v $(pwd)/config:/app/config

# Logs
-v $(pwd)/logs:/app/logs
```

## 📊 Production Deployment

### Docker Compose with Nginx
```yaml
version: '3.8'

services:
  iot-sensor-dashboard:
    build: .
    container_name: iot-sensor-pipeline
    environment:
      - STREAMLIT_SERVER_PORT=5000
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - ./exports:/app/exports
      - ./config:/app/config
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    container_name: iot-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - iot-sensor-dashboard
    restart: unless-stopped
```

### Load Balancing (Multiple Instances)
```yaml
version: '3.8'

services:
  iot-dashboard-1:
    build: .
    container_name: iot-sensor-1
    environment:
      - STREAMLIT_SERVER_PORT=5000
    restart: unless-stopped
    
  iot-dashboard-2:
    build: .
    container_name: iot-sensor-2
    environment:
      - STREAMLIT_SERVER_PORT=5000
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - iot-dashboard-1
      - iot-dashboard-2
    restart: unless-stopped
```

## 🔍 Container Management

### Basic Commands
```bash
# View running containers
docker ps

# View all containers
docker ps -a

# Check container logs
docker logs iot-sensor-pipeline

# Follow logs in real-time
docker logs -f iot-sensor-pipeline

# Execute commands inside container
docker exec -it iot-sensor-pipeline bash

# Restart container
docker restart iot-sensor-pipeline

# Stop container
docker stop iot-sensor-pipeline

# Remove container
docker rm iot-sensor-pipeline

# Remove image
docker rmi iot-sensor-pipeline
```

### Health Monitoring
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' iot-sensor-pipeline

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' iot-sensor-pipeline
```

### Resource Monitoring
```bash
# Monitor resource usage
docker stats iot-sensor-pipeline

# Container resource limits
docker run -d \
  --name iot-sensor-pipeline \
  --memory=1g \
  --cpus=1.0 \
  -p 5000:5000 \
  iot-sensor-pipeline
```

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000
# or
sudo netstat -tulpn | grep :5000

# Kill process
sudo kill -9 <PID>

# Use different port
docker run -p 8080:5000 iot-sensor-pipeline
```

#### Container Won't Start
```bash
# Check logs for errors
docker logs iot-sensor-pipeline

# Run interactively for debugging
docker run -it --rm iot-sensor-pipeline bash

# Check image build
docker build --no-cache -t iot-sensor-pipeline .
```

#### Memory Issues
```bash
# Check Docker memory usage
docker system df

# Clean up unused resources
docker system prune -a

# Increase container memory
docker run --memory=2g iot-sensor-pipeline
```

#### Network Connectivity
```bash
# Test container network
docker exec iot-sensor-pipeline curl -f http://localhost:5000/_stcore/health

# Check port binding
docker port iot-sensor-pipeline

# Test from host
curl http://localhost:5000
```

### Performance Optimization

#### Resource Limits
```yaml
services:
  iot-sensor-dashboard:
    build: .
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
```

#### Multi-stage Build (Optimized Dockerfile)
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --user streamlit pandas plotly numpy scipy

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["streamlit", "run", "app.py", "--server.port=5000"]
```

## 🔐 Security Considerations

### Container Security
```bash
# Run as non-root user
docker run --user 1000:1000 iot-sensor-pipeline

# Read-only filesystem
docker run --read-only iot-sensor-pipeline

# Drop capabilities
docker run --cap-drop=ALL iot-sensor-pipeline

# Limit resources
docker run --memory=1g --cpus=1.0 iot-sensor-pipeline
```

### Network Security
```bash
# Custom network
docker network create iot-network
docker run --network=iot-network iot-sensor-pipeline

# No external access
docker run --network=none iot-sensor-pipeline
```

## 📈 Scaling and High Availability

### Horizontal Scaling
```yaml
version: '3.8'

services:
  iot-dashboard:
    build: .
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    ports:
      - "5000-5002:5000"
```

### Docker Swarm Deployment
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml iot-stack

# Scale service
docker service scale iot-stack_iot-dashboard=5

# View services
docker service ls
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iot-sensor-dashboard
spec:
  replicas: 3
  selector:
    matchLabels:
      app: iot-sensor-dashboard
  template:
    metadata:
      labels:
        app: iot-sensor-dashboard
    spec:
      containers:
      - name: dashboard
        image: iot-sensor-pipeline:latest
        ports:
        - containerPort: 5000
        resources:
          limits:
            memory: "1Gi"
            cpu: "1000m"
          requests:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: iot-dashboard-service
spec:
  selector:
    app: iot-sensor-dashboard
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

## 🧪 Testing Docker Deployment

### Automated Testing Script
```bash
#!/bin/bash

echo "🧪 Testing Docker deployment..."

# Build image
docker build -t iot-sensor-pipeline-test .

# Run container
docker run -d --name test-container -p 5001:5000 iot-sensor-pipeline-test

# Wait for startup
sleep 30

# Test health endpoint
if curl -f http://localhost:5001/_stcore/health; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Test main application
if curl -f http://localhost:5001; then
    echo "✅ Application accessible"
else
    echo "❌ Application not accessible"
    exit 1
fi

# Cleanup
docker stop test-container
docker rm test-container
docker rmi iot-sensor-pipeline-test

echo "🎉 All tests passed!"
```

## 📝 Best Practices

### Development
- Use `.dockerignore` to exclude unnecessary files
- Multi-stage builds for smaller images
- Pin dependency versions for reproducibility
- Use health checks for container monitoring

### Production
- Set resource limits and reservations
- Use secrets for sensitive configuration
- Implement proper logging and monitoring
- Regular security updates and patches

### Monitoring
- Container resource usage monitoring
- Application performance metrics
- Log aggregation and analysis
- Automated alerting for failures

This Docker deployment setup provides a robust, scalable foundation for running the IoT Sensor Data Pipeline in any containerized environment.