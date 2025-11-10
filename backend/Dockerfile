FROM python:3.10-slim

# Cài đặt system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy và cài đặt requirements trước
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Port cho Render
ENV PORT=5000
EXPOSE 5000

# Start command
CMD ["python", "app.py"]
