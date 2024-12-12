import os
from flask import jsonify, send_file


def successs_response(message="Request completed successfully", data=None, status_code=200):
    """
    A helper function to create standardized success responses.

    Arguments:
    - message (str): Custom success message.
    - data (dict): Additional data to include in the response.
    - status_code (int): HTTP status code for the response (default is 200).
    
    Returns:
    - tuple: JSON response and the corresponding HTTP status code.
    """
    response = {"message": message}
    
    if data:
        response.update(data)
    
    return jsonify(response), status_code


def error_response(error="An unexpected error occurred", data=None, status_code=400):
    """
    A helper function to create standardized error responses.

    Arguments:
    - error (str): Custom error message.
    - data (dict): Additional data to include in the response.
    - status_code (int): HTTP status code for the error (default is 400).
    
    Returns:
    - tuple: JSON response and the corresponding HTTP status code.
    """
    response = {"error": error}
    
    if data:
        response.update(data)
    
    return jsonify(response), status_code


def send_file_if_exists(filepath, file_type):
    """
    Check if the file exists and send it, otherwise return an error.
    """
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True), 200
    return jsonify({"error": f"{file_type} file not found: {filepath}"}), 404


def create_media_folders(app, unique_id):
    """
    Create an upload and result folder.

    Args:
    - base_folder (str): The base directory where folders will be created.
    - unique_id (str): A unique identifier for the folders.

    Returns:
    - dict: A dictionary with paths for the upload and result folders.
    """
    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], unique_id)
    result_folder = os.path.join(app.config['RESULT_FOLDER'], unique_id)

    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(result_folder, exist_ok=True)

    return {"upload_folder": upload_folder, "result_folder": result_folder}


def get_file_size(file):
    """
    Get the size of a file-like object in megabytes.
    """
    file.seek(0, os.SEEK_END)
    file_size_bytes = file.tell()
    file.seek(0)
    return file_size_bytes / (1024 * 1024)  # Convert to MB