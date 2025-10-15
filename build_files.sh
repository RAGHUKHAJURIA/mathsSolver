#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static

# Copy static files if they exist
if [ -d "static_files" ]; then
    cp -r static_files/* static/
fi

echo "Build completed successfully!"