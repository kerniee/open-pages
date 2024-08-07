FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the source code
COPY open_pages open_pages
COPY templates templates

# Run the application
EXPOSE 80
CMD ["uvicorn", "open_pages.main:app", "--proxy-headers", "--port", "80", "--host", "0.0.0.0"]
