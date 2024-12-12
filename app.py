import uuid
import os

from flask import (
    Flask,
    request
)
from flask_migrate import Migrate

from config import Config
from models import (
    db,
    FileUpload,
    TaskStatusEnum
)
from helpers import (
    successs_response,
    error_response,
    send_file_if_exists,
    create_media_folders,
    get_file_size,
)


# Initialize the Flask application
app = Flask(__name__)

# Load configuration from Config class
app.config.from_object(Config)

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)  # Set up migration

from celery_config import make_celery
celery = make_celery(app)  # Initialize Celery


@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    """
    This API endpoint handles the file upload, generates unique identifier for the file, creates necessary directories,
    saves the file, and triggers the background task to parse the PDF.
    """
    pdf_file = request.files.get("file")
    
    if not pdf_file:
        return error_response("Please upload a pdf file.")
    
    if pdf_file.filename == "":
        return error_response("No file selected.")
    
    if pdf_file.content_type != "application/pdf":
        return error_response("Invalid file type. Only PDF files are allowed.")
    
    file_size_mb = get_file_size(pdf_file)

    if file_size_mb > 16:
        return error_response(f"File size exceeds the limit of 16 MB. The uploaded file is {file_size_mb:.2f} MB.")
    
    filename = pdf_file.filename
    unique_id = str(uuid.uuid4())

    # Create folder to store uploaded files and the resulted files in their respective directory
    folders = create_media_folders(app, unique_id)

    upload_path = folders["upload_folder"]
    result_path = folders["result_folder"]

    # Save the PDF file inside the created folder
    pdf_path = os.path.join(upload_path, filename)
    pdf_file.save(pdf_path)

    # Create a new record in the database for the uploaded file with the unique identifier
    new_pdf_file = FileUpload(id=unique_id, filename=filename, filepath=pdf_path)
    db.session.add(new_pdf_file)
    db.session.commit()

    from tasks import parse_pdf
    # Start the background task to parse the PDF
    parse_pdf.apply_async(args=[unique_id, result_path])

    return successs_response(
        "File uploaded successfully",
        data={"file_id": unique_id, "file_path": pdf_path}
    )


@app.route("/status/<file_id>", methods=["GET"])
def check_status(file_id):
    """
    Endpoint to check the status of a PDF processing task using the unique identifier (file_id).

    This endpoint will return:
    - The resulting CSV file if pdf processing is complete.
    - The error messages in a TXT file if pdf processing has failed.
    - A message indicating that the file is still processing.

    Args:
        file_id (str): The unique identifier of the PDF file whose status is being queried.

    Returns:
        Response: A response with either the error or result file, or a status message.
    """
    pdf_file = FileUpload.query.filter_by(id=file_id).first()
    if not pdf_file:
        return error_response("Pdf file not found", status_code=404)
    
    filename = pdf_file.filename.split('.')[0]
    status = pdf_file.status
    folder_path = os.path.join(app.config["RESULT_FOLDER"], file_id)

    if status == TaskStatusEnum.FAILED:
        txt_file = os.path.join(folder_path, f"{filename}.txt")
        return send_file_if_exists(txt_file, "Error text")
    elif status == TaskStatusEnum.COMPLETED:
        csv_file = os.path.join(folder_path, f"{filename}.csv")
        return send_file_if_exists(csv_file, "Result csv")

    return successs_response(
        message="The file is currently being processed.",
        data={"status": status.value}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)