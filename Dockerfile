FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the source code
COPY open_pages open_pages

# Run the application
EXPOSE 80
CMD ["fastapi", "run", "open_pages/main.py", "--proxy-headers", "--port", "80"]
