# Use a slim version of Python
FROM python:3.11-slim


# Set the working directory in the Docker image
WORKDIR /app


# Install system dependencies
RUN apt-get update && apt-get install -y \    
    #dependencies for detectron2
    git \
    g++ \
    # dependencies for cv2
    libgl1-mesa-glx \
    libglib2.0-0 \
    # dependencies for torchvision
    libjpeg-dev \
    libpng-dev \
    # good pracice to remove redundancy    
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install the CPU-only version of PyTorch
RUN pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu


# Clone the Detectron2 repository and install
RUN git clone https://github.com/facebookresearch/detectron2.git && \
    python -m pip install -e detectron2


COPY requirements.txt .
# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of your application's source code
COPY . .


# The command to run your application
CMD ["python", "app.py"]

