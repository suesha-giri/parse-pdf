import os
import csv
import traceback
import pdfplumber

from app import celery
from models import (
    TaskStatusEnum,
    FileUpload,
    db
)

        
@celery.task()
def parse_pdf(pdf_id, result_path):
    """
    Background task to parse a PDF file, extract the first table, and save it as a CSV file.
    
    Args:
    - pdf_id (int): The ID of the PDF record in the database.
    - result_path (str): The path where result files should be saved.
    
    Returns:
    - str: A message indicating success or failure.
    """
    pdf_file = FileUpload.query.filter_by(id=pdf_id).first()
    filename = pdf_file.filename.split('.')[0]

    try:
        # Open the PDF file using pdfplumber
        with pdfplumber.open(pdf_file.filepath) as pdf:
            first_table = None
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    first_table = tables[0]  # Extract the first table found
                    break
    
        if not first_table:
            raise ValueError("No tables found in the PDF.")

        # Write the first table to a CSV file
        csv_file_path = os.path.join(result_path, f"{filename}.csv")
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(first_table)
        
        pdf_file.status = TaskStatusEnum.COMPLETED

    except Exception as e:
        # Write the error details to a text file
        error_file_path = os.path.join(result_path, f"{filename}.txt")
        with open(error_file_path, 'w') as error_file:
            error_file.write(f"Error occurred: {e}\n")
            error_file.write(traceback.format_exc())
        
        pdf_file.status = TaskStatusEnum.FAILED

    finally:
        db.session.commit()

    return True