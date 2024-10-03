from flask import Flask, request, render_template, jsonify, send_file
import pydicom
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np

app = Flask(__name__)

# Create a directory to store converted images
OUTPUT_DIR = "converted_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'dicom_file' not in request.files:
        return 'No file part', 400

    file = request.files['dicom_file']
    if file.filename == '':
        return 'No selected file', 400

    try:
        # Load DICOM file
        dicom_file = pydicom.dcmread(file)

        # Convert DICOM to PNG or JPEG
        pixel_array = dicom_file.pixel_array
        plt.imsave(os.path.join(OUTPUT_DIR, 'converted_image.png'), pixel_array, cmap='gray')

        # Load the converted image
        img = Image.fromarray(pixel_array)
        img_path = os.path.join(OUTPUT_DIR, 'converted_image.png')
        img.save(img_path)

        # Prepare metadata
        metadata = {elem.name: elem.value for elem in dicom_file.iterall() if not elem.tag.is_private}

        return render_template('result.html', img_path=img_path, metadata=metadata)

    except Exception as e:
        return f'Error occurred: {str(e)}', 500

@app.route('/converted_image.png')
def get_image():
    return send_file(os.path.join(OUTPUT_DIR, 'converted_image.png'))

if __name__ == '__main__':
    app.run(debug=True)
