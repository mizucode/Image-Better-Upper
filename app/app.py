from flask import Flask, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
import imageio
from numpy import asarray
from PIL import Image
import os
from pathlib import Path
import asyncio
import cv2
from cv2 import dnn_superres
import numpy


# could be using static to declare/implement static folder path instead of app/uploads
app = Flask(__name__, static_url_path="/static")
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"

# replace with actual secret key?
app.secret_key = '34745h3u7657hdfjhfddfy'


UPLOAD_FOLDER = Path(__file__).resolve().parent / 'uploads'

# why print(x2)?
print(UPLOAD_FOLDER)

DOWNLOAD_FOLDER = Path(__file__).resolve().parent / 'downloads'
print(DOWNLOAD_FOLDER)

# use these or upload.js?
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


# global function?
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# |index page, starting point
@app.route('/')
def index():
    return render_template("index.html")


# |upload page, initialize new session, upload button, upload function
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        # session['file'] = str(app.config['UPLOAD_FOLDER'] / filename)
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(app.config['UPLOAD_FOLDER'] / filename)
            convert_image(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('download_file', filename=filename))
    return render_template('upload.html')


# convert image function
def convert_image(path, filename):
    print(path / filename)
    img = imageio.imread(open(path / filename, 'rb'))
    sr = dnn_superres.DnnSuperResImpl_create()
    cv_path = "ESPCN_x3.pb"
    sr.readModel(cv_path)
    sr.setModel("espcn", 3)
    result = sr.upsample(img)
    array = asarray(result)
    image = Image.fromarray(array, 'RGB')
    # When saving the file, we need to remove the original format with split() and replace it with png
    image.save(app.config['DOWNLOAD_FOLDER'] / f'{filename.split(".")[0]}.png')


@app.route('/download/<filename>')
def download_file(filename):
    # session.modified = True
    if "update more images" in request.form:
        app.logger.warning('update more images is in da request form')
        return redirect(url_for('index'))
    app.logger.warning('update more images was not in da request form')
    return render_template('download.html', value=filename)


# final page displays goodbye message along with prompt to do more images, while files are downloading
@app.route('/return-files/<filename>')
def return_files(filename):
    with open(app.config['DOWNLOAD_FOLDER'] / f'{filename.split(".")[0]}.png', 'rb') as imgdata:
        img = imageio.imread(imgdata)
    clean_files()
    return send_file(img, attachment_filename=f'{filename.split(".")[0]}.png', as_attachment=True)


def clean_files():
    for file in app.config['DOWNLOAD_FOLDER'].iterdir():
        file.unlink()
    for file in app.config['UPLOAD_FOLDER'].iterdir():
        file.unlink()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
