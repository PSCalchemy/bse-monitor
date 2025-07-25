#!/usr/bin/env python3
"""
Docker Setup for BSE Monitor
Run in a container that restarts automatically
"""

import os

def create_simple_dockerfile():
    """Create a simple Dockerfile"""
    content = """FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install requests beautifulsoup4 lxml schedule python-dotenv email-validator textblob

# Copy files
COPY *.py ./
COPY .env ./

# Run the monitor
CMD ["python", "bse_monitor.py"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(content)
    print("✅ Created simple Dockerfile")

def create_docker_compose():
    """Create docker-compose.yml"""
    content = """version: '3.8'

services:
  bse-monitor:
    build: .
    container_name: bse-monitor
    restart: unless-stopped
    environment:
      - TZ=Asia/Kolkata
    volumes:
      - ./logs:/app/logs
    networks:
      - bse-network

networks:
  bse-network:
    driver: bridge
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(content)
    print("✅ Created docker-compose.yml")

def create_run_script():
    """Create run script"""
    content = """#!/bin/bash
# BSE Monitor Docker Runner

echo "🚀 Starting BSE Monitor in Docker..."

# Build and run with Docker Compose
docker-compose up -d

echo "✅ BSE Monitor is running in Docker!"
echo "📊 Check logs: docker-compose logs -f"
echo "⏹️  Stop: docker-compose down"
echo "🔄 Restart: docker-compose restart"
"""
    
    with open('run_docker.sh', 'w') as f:
        f.write(content)
    os.chmod('run_docker.sh', 0o755)
    print("✅ Created run_docker.sh")

def main():
    """Create Docker setup files"""
    print("🐳 Creating Docker Setup")
    print("=" * 30)
    
    create_simple_dockerfile()
    create_docker_compose()
    create_run_script()
    
    print("\n📋 Docker Commands:")
    print("1. Build and start: ./run_docker.sh")
    print("2. View logs: docker-compose logs -f")
    print("3. Stop: docker-compose down")
    print("4. Restart: docker-compose restart")
    
    print("\n💡 Benefits:")
    print("- Runs in background")
    print("- Auto-restarts if it crashes")
    print("- Easy to manage")
    print("- Can run on any server")

if __name__ == "__main__":
    main() 