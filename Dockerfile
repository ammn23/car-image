FROM python:3.9-slim

# Start with the official Python 3.9 image
FROM python:3.9-slim

# Install a comprehensive set of system libraries for headless OpenCV
# This prevents errors like "libGL.so.1" and "libgthread-2.0.so.0"
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file first to leverage Docker's layer caching
COPY ./requirements.txt /code/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application files
COPY . .

# Command to run the Uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./best.pt /code/best.pt
COPY ./app.py /code/app.py


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]