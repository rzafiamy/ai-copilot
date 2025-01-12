from flask import request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from . import app
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Here we would process the file (e.g., parse PDF, schedule tasks, etc.)
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    
    return jsonify({"error": "Invalid file format"}), 400
