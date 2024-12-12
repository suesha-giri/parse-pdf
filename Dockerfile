FROM python:3.8.1-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py", "--host=0.0.0.0", "--port=5000"]
