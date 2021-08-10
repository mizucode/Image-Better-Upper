import imageio
from numpy import asarray
from PIL import Image

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def filename():
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


pic = imageio.imread(filename)

array = asarray(pic)
arraycopy = array.copy()

img = Image.fromarray(arraycopy, 'RGB')

img.save(filename)
img.show()
