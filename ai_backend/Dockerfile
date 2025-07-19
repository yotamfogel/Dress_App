FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy your backend code
COPY . /app

# Install numpy first and pin it
RUN pip install --no-cache-dir numpy==1.26.4

# Install PyTorch with specific versions that match mmcv-full requirements
RUN pip install --no-cache-dir torch==1.13.1+cpu torchvision==0.14.1+cpu torchaudio==0.13.1+cpu --index-url https://download.pytorch.org/whl/cpu

# Install mmcv-full prebuilt wheel (CPU version) - must match PyTorch version
RUN pip install --no-cache-dir mmcv-full==1.7.1 -f https://download.openmmlab.com/mmcv/dist/cpu/torch1.13.1/index.html

# Install mmdet and detectron2 (CPU)
RUN pip install --no-cache-dir mmdet==2.28.2
RUN pip install --no-cache-dir 'git+https://github.com/facebookresearch/detectron2.git'

# Install other dependencies
RUN pip install --no-cache-dir flask flask-cors opencv-python pillow scikit-learn webcolors ultralytics

# Reinstall numpy to ensure it's still 1.26.4 (in case anything upgraded it)
RUN pip install --no-cache-dir numpy==1.26.4

# Verify numpy version
RUN python -c "import numpy; print('Numpy version:', numpy.__version__)"

# Expose the backend port (change if needed)
EXPOSE 5000

# Start the backend server
CMD ["python", "start_enhanced_server.py"]