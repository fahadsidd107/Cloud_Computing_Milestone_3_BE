# Use Python base image

FROM python:3.9

# Set working directory

WORKDIR /app

# Copy requirements

COPY requirements.txt .

# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .


# Expose port

EXPOSE 5000

# Run application

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
