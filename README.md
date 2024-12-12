# Flask App with PDF Parsing - Dockerized

This repository contains a Flask app with two endpoints and a background task to parse PDFs using Celery. The app is dockerized and can be run locally with Docker Compose.

## Prerequisites

Before running the application, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)


### Files Overview:

- **`Dockerfile`**: Defines the Docker image for both Flask and Celery services.
- **`docker-compose.yml`**: Configures all the services (Flask, Celery, Redis, and PostgreSQL).
- **`requirements.txt`**: Python dependencies for the app.
- **`app.py`**: Main Flask application entry point.
- **`celery_config.py`**: Celery configuration.
- **`config.py`**: General configurations settings.
- **`helpers.py`**: Helper functions or utility methods
- **`models.py`**: For database models.
- **`create_db.py`**: Script for creating the database schema
- **`tasks.py`**: The Celery task for parsing the PDFs.

---

## Setup Instructions

### Step 1: Clone the Repository
### Step 2: Build the Docker Images
```bash
docker-compose build
```
### Step 3: Start the Services
```bash
docker-compose up
```
### Step 4: Run Database Migrations
```bash
docker exec -it parse-pdf_web_1 bash -c "flask db upgrade"
```
### Step 5: Access the Application
```bash
http://localhost:5000
```
### Step 6:  Test the Endpoints
#### Endpoint 1: /upload_pdf
This endpoint will accept a PDF file, generate a unique identifier for the file, and send it for background processing. The PDF will be processed asynchronously by Celery.

#### Request: POST /upload_pdf
- Form data: A PDF file (the file must be sent using the file field in the form).

#### Request
```bash
curl --location --request POST 'http://127.0.0.1:5000/upload_pdf' \
--form 'file=@"/C:/Users/ACER/Downloads/test_abc.pdf"'
```
#### Response
```json
{
    "file_id": "25d0a41a-90ed-47fb-9155-9ec04114dc13",
    "file_path": "uploads\\25d0a41a-90ed-47fb-9155-9ec04114dc13\\test_abc.pdf",
    "message": "File uploaded successfully"
}
```

#### Endpoint 2: /status/<file_id>
This endpoint will check the status of the PDF file parsing. If completed, returns CSV file else text file.
#### Request
```bash
curl --location --request GET 'http://127.0.0.1:5000/status/25d0a41a-90ed-47fb-9155-9ec04114dc13'
```
#### Response
A response with either the error or result file, or a status message.
```json
{
    "message": "The file is currently being processed.",
    "status": "processing"
}
```

