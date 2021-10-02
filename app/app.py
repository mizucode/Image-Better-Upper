import cv2
from flask import Flask, request, redirect, url_for, render_template, send_file, Response
from waitress import serve
from werkzeug.utils import secure_filename
import imageio
from numpy import asarray
from PIL import Image
import os
import io
from zipfile import ZipFile
from pathlib import Path
from cv2 import dnn_superres


app = Flask(__name__, static_url_path="/static")

UPLOAD_FOLDER = Path(__file__).resolve().parent / 'uploads'

DOWNLOAD_FOLDER = Path(__file__).resolve().parent / 'downloads'

model = Path(__file__).resolve().parent / 'ESPCN_x3.pb'

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
    clean_files()
    return render_template("index.html")


# |upload page, initialize new session, upload button, upload function
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        files = request.files.getlist('file')
        if len(files) == 1 and files[0].filename == '':
            print('No file selected')
            return redirect(request.url)
        for file in files:
            filename = secure_filename(file.filename)
            if file and allowed_file(file.filename):
                file.save(app.config['UPLOAD_FOLDER'] / filename)
                convert_image(app.config['UPLOAD_FOLDER'], filename)
        prepare_images(app.config['DOWNLOAD_FOLDER'], 'updated_images.zip')
        return redirect(url_for('download_file', filename='updated_images.zip'))
    return render_template('upload.html')


# convert image function
def convert_image(path, filename):
    print(path / filename)
    img = imageio.imread(open(path / filename, 'rb'))
    sr = dnn_superres.DnnSuperResImpl_create()
    cv_path = str(model)
    sr.readModel(cv_path)
    sr.setModel("espcn", 3)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    result = sr.upsample(img)
    array = asarray(result)
    image = Image.fromarray(array, 'RGB')
    # When saving the file, we need to remove the original format with split() and replace it with png
    image.save(app.config['DOWNLOAD_FOLDER'] / f'{filename.split(".")[0]}.png')


def prepare_images(path, filename):
    with ZipFile(path / filename, 'w') as zeep:
        for file in path.iterdir():
            if file.suffix != '.png':
                continue
            zeep.write(file, file.name)


@app.route('/download/<filename>')
def download_file(filename):
    if "update more images" in request.form:
        return redirect(url_for('index'))
    return render_template('download.html', value=filename)


# final page displays goodbye message along with prompt to do more images, while files are downloading
@app.route('/return-files/<filename>')
def return_files(filename):
    return_data = io.BytesIO()
    with open((app.config['DOWNLOAD_FOLDER'] / 'updated_images.zip'), 'rb') as fo:
        return_data.write(fo.read())
        return_data.seek(0)
    clean_files()
    return send_file(return_data, mimetype='application/zip',
                     attachment_filename='updated_images.zip', as_attachment=True)


def clean_files():
    for file in app.config['DOWNLOAD_FOLDER'].iterdir():
        if file.suffix != '.keep':
            file.unlink()
    for file in app.config['UPLOAD_FOLDER'].iterdir():
        if file.suffix != '.keep':
            file.unlink()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    serve(app, host='0.0.0.0', port=port, url_scheme='https')
