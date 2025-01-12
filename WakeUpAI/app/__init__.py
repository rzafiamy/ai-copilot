from flask import Flask
import os
import json

app = Flask(__name__)

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

app.config['UPLOAD_FOLDER'] = config['upload_folder']
app.config['ALLOWED_EXTENSIONS'] = set(config['allowed_extensions'])