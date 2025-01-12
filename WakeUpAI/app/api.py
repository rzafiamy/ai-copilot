from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
from . import app
from .utils import (
    allowed_file,
    calculate_file_hash,
    extract_pdf_pages,
    save_pages_to_storage,
    ensure_storage_folder,
)
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
        # Save file temporarily to calculate hash
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Calculate hash of the file
        file_hash = calculate_file_hash(upload_path)

        # Ensure storage folder for the file
        storage_path = ensure_storage_folder(app.config['STORAGE_FOLDER'], file_hash)

        # Check if the file already exists
        if os.listdir(storage_path):
            os.remove(upload_path)  # Clean up temporary file
            return jsonify({"error": "File already uploaded"}), 400

        # Extract PDF pages and save to storage
        pages = extract_pdf_pages(upload_path)
        save_pages_to_storage(pages, storage_path)

        
        return jsonify({
            "message": "File uploaded and processed successfully",
            "hash": file_hash,
            "pages": len(pages),
        }), 200

    return jsonify({"error": "Invalid file format"}), 400