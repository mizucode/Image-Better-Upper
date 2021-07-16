from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session
from werkzeug.utils import secure_filename
import imageio
from numpy import asarray
from PIL import Image
import os
from pathlib import Path

UPLOAD_FOLDER = Path(__file__).resolve().parent / 'uploads'

# why print(x2)?
print(UPLOAD_FOLDER)

DOWNLOAD_FOLDER = Path(__file__).resolve().parent / 'downloads'
print(DOWNLOAD_FOLDER)

# use these or upload.js?
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# could be using static to declare/implement static folder path instead of app/uploads
app = Flask(__name__, static_url_path="/static")

# replace with actual secret key?
app.secret_key = 'SECRET KEY'

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
            convert_image(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('download_file', filename=filename))
        return redirect(url_for('download'))
    return render_template('upload.html')


# convert image function
def convert_image(path, filename):
    print(path / filename)
    im = imageio.imread(open(path / filename, 'rb'))
    array = asarray(im)
    image = Image.fromarray(array, 'RGB')
    # When saving the file, we need to remove the original format with split() and replace it with png
    image.save(app.config['DOWNLOAD_FOLDER'] / f'{filename.split(".")[0]}.png')


# converted images page, displays list of updated images, and button prompt to download them
#@app.route('/updated', methods=['GET'])
#def updated():
    #path = DOWNLOAD_FOLDER
    #dirs = os.listdir(path)
    #for filename in dirs:
        #filename = secure_filename(filename)
        #return redirect(url_for('download', filename=filename))
    #return render_template("updated.html")


@app.route('/app/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], f'{filename.split(".")[0]}.png', as_attachment=True)


# final page displays goodbye message along with prompt to do more images, while files are downloading
@app.route('/download')
def download():
    if "update more images" in request.form:
        # Clear current Flask session and redirects to home page.
        session.pop('UPLOAD_FOLDER', None)
        session.pop('DOWNLOAD_FOLDER', None)
        return redirect(url_for('/'))
    return render_template("download.html")


#app.add_url_rule(
    #"/app/uploads/<filename>", endpoint="download_file", build_only=True
#)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
