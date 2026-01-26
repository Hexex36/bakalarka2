#!/bin/bash

echo "🐳 OpenBB Docker Setup for European Options"
echo "==============================================="

# Check if Docker is running
if ! docker --version > /dev/null 2>&1; then
    echo "❌ Docker is not installed or not running"
    echo "Please install Docker first:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install docker.io"
    echo "  CentOS/RHEL: sudo yum install docker"
    echo "  macOS: Download Docker Desktop from docker.com"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose is not installed"
    echo "Installing docker-compose..."
    
    # Install docker-compose
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    else
        echo "Please install docker-compose manually:"
        echo "  Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
fi

echo "✅ Docker prerequisites verified"
echo ""

# Start OpenBB container
echo "🚀 Starting OpenBB Platform with Docker..."
echo ""

# Create environment file for API key
if [ ! -f .env ]; then
    echo "Creating .env file for API key..."
    cat > .env << EOF
# OpenBB API Configuration
# Get your free API key from https://my.openbb.co/
OPENBB_API_KEY=your_api_key_here
EOF
    echo "✅ .env file created"
    echo ""
    echo "📝 IMPORTANT: Add your OpenBB API key to .env file"
    echo "   Get free key from: https://my.openbb.co/"
    echo "   Then edit .env file with your key"
    echo ""
fi

# Start the container
echo "🔄 Launching OpenBB container..."
docker-compose up -d

# Wait a moment for container to start
sleep 5

# Show container status
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "🌐 Access OpenBB Web Interface:"
echo "   Open your browser and go to: http://localhost:8080"
echo ""
echo "📋 Instructions:"
echo "   1. Set up your OpenBB account at https://my.openbb.co/"
echo "   2. Get your free API key"
echo "   3. Edit .env file with: OPENBB_API_KEY=your_actual_key"
echo "   4. Restart container: docker-compose restart"
echo ""
echo "🎯 European Options Data Workflow:"
echo "   • Go to Derivatives → Options Chains"
echo "   • Enter symbol: SPX (S&P 500)"
echo "   • Choose provider: Cboe (recommended)"
echo "   • Select expirations and export as CSV"
echo "   • Data will be saved to ./data directory"
echo ""
echo "✅ Docker OpenBB is now running with professional European options data!"