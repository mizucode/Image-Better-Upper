from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import imageio
from numpy import asarray
from PIL import Image
import os
from pathlib import Path

UPLOAD_FOLDER = Path(__file__).resolve().parent / 'uploads'
print(UPLOAD_FOLDER)
DOWNLOAD_FOLDER = Path(__file__).resolve().parent / 'downloads'
print(DOWNLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_url_path="/static")
# DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] / filename)
            process_file(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template("index.html")


def process_file(path, filename):
    convert_image(path, filename)


def convert_image(path, filename):
    print(path / filename)
    im = imageio.imread(open(path / filename, 'rb'))
    array = asarray(im)
    image = Image.fromarray(array, 'RGB')
    # When saving the file, we need to remove the original format with split() and replace it with png
    image.save(app.config['DOWNLOAD_FOLDER'] / f'{filename.split(".")[0]}.png')


@app.route('/app/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], f'{filename.split(".")[0]}.png', as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
